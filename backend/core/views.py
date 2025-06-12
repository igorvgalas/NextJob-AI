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

from .models import JobOffer
from .serializers import JobOfferSerializer
from .filter import JobOfferFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class JobOfferPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class JobOfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobOffer.objects.all().order_by('-created_at')
    serializer_class = JobOfferSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobOfferFilter
    pagination_class = JobOfferPagination

    @action(detail=False, methods=['post'], url_path='bulk_create')
    def bulk_create(self, request):
        if not isinstance(request.data, list):
            return Response({"detail": "Expected a list of items."}, status=400)

        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": f"{len(serializer.validated_data)} job offers created."}, status=201)
        return Response(serializer.errors, status=400)


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
            "first_name": first_name,
            "last_name": last_name,
        })

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "pk": user.pk,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "created": created,
        })
