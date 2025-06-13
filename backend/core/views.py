import os
import json
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from django.conf import settings

from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import JobOffer, UserSkill, Skill
from .serializers import JobOfferSerializer, UserSkillSerializer, SkillSerializer
from .filter import JobOfferFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class StandardPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class JobOfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobOffer.objects.all().order_by('-created_at')
    serializer_class = JobOfferSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobOfferFilter
    pagination_class = StandardPagination

    @action(detail=False, methods=['post'], url_path='bulk_create')
    def bulk_create(self, request):
        if not isinstance(request.data, list):
            return Response({"detail": "Expected a list of items."}, status=400)

        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": f"{len(serializer.validated_data)} job offers created."}, status=201)
        return Response(serializer.errors, status=400)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    pagination_class = None 

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('name')

class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'skill']
    search_fields = ['skill__name']
    ordering_fields = ['user', 'skill']
    pagination_class = StandardPagination

    @action(detail=False, methods=['post'], url_path='set_skills')
    def set_skills(self, request):
        """
        Replace all UserSkill entries for a user with the provided skills and proficiencies.
        Expects: {"user": user_id, "skills": {skill_id: proficiency, ...}}
        """
        user_id = request.data.get('user')
        skills_dict = request.data.get('skills', {})
        if not user_id or not isinstance(skills_dict, dict):
            return Response({"detail": "user and skills (dict) are required."}, status=400)
        # Remove existing UserSkill for this user
        UserSkill.objects.filter(user_id=user_id).delete()
        # Create new UserSkill for each skill/proficiency
        new_user_skills = []
        for skill_id, proficiency in skills_dict.items():
            user_skill = UserSkill.objects.create(
                user_id=user_id, skill_id=skill_id, proficiency=proficiency)
            new_user_skills.append(user_skill)
        serializer = self.get_serializer(new_user_skills, many=True)
        return Response(serializer.data)


class GoogleAuthView(APIView):
    def post(self, request):
        token = request.data.get("id_token")
        access_token = request.data.get("accessToken")
        refresh_token = request.data.get("refreshToken")

        credentials_path = "/Users/cheef/Documents/nextjob-ai/services/gmail_reader/credentials.json"
        os.makedirs(os.path.dirname(credentials_path), exist_ok=True)

        if not token:
            return Response({"error": "Missing id_token"}, status=HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(
                token, google_requests.Request(), settings.IOS_GOOGLE_CLIENT_ID)
        except Exception as e:
            return Response({"error": f"Invalid token: {e}"}, status=HTTP_400_BAD_REQUEST)

        email = idinfo.get("email")
        first_name = idinfo.get("given_name", "")
        last_name = idinfo.get("family_name", "")

        # Store credentials per user (by email)
        if email:
            all_credentials = {}
            if os.path.exists(credentials_path) and os.path.getsize(credentials_path) > 0:
                with open(credentials_path, "r", encoding="utf-8") as f:
                    try:
                        all_credentials = json.load(f)
                    except json.JSONDecodeError:
                        print(
                            "⚠️ credentials.json is invalid JSON — starting with empty dict")
                        all_credentials = {}
            all_credentials[email] = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            with open(credentials_path, "w", encoding="utf-8") as f:
                json.dump(all_credentials, f, indent=2)

        User = get_user_model()
        user, created = User.objects.get_or_create(email=email, defaults={
            "username": email,
        })

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "pk": user.pk,
                "username": user.username,  # Added username to response
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "created": created,
        })
