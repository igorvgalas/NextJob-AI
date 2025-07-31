import json
import os

from django.db.models import Count, F
from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .filter import JobOfferFilter
from .models import JobOffer, Skill, UserSkill
from .serializers import (JobOfferSerializer,
                          JobOfferTestSerializer,
                          SkillSerializer,
                          UserSkillSerializer,
                          UserSkillStatSerializer)
from .paginations import StandardPagination


class JobOfferViewSet(viewsets.ModelViewSet):
    """ViewSet for managing job offers.
    It provides CRUD operations for job offers.
    It supports filtering, searching, and ordering.
    """
    queryset = JobOffer.objects.select_related('user').order_by('-created_at')
    serializer_class = JobOfferSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
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


class JobOfferTestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobOfferTestSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = JobOffer.objects.select_related(
            'user').order_by('-created_at')
        print(queryset.explain())
        return queryset


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('name')


class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.select_related(
        "user").prefetch_related("skills")
    # queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['user__username']
    ordering_fields = ['user__username']
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserSkillStatViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSkillStatSerializer
    http_method_names = ['get', 'head', 'options']
    pagination_class = None

    def get_queryset(self):
        queryset = (UserSkill.objects.select_related("user")
                    .annotate(num_skills=Count("skills"))
                    .values(username=F("user__username"), num_skills=F("num_skills")))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
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
        except Exception as e:  # pylint: disable=broad-except
            return Response({"error": f"Invalid token: {e}"}, status=HTTP_400_BAD_REQUEST)

        email = idinfo.get("email")
        # first_name = idinfo.get("given_name", "")
        # last_name = idinfo.get("family_name", "")

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
