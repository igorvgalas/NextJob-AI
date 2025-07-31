'''This file contains the serializers for the core application.
It includes serializers for job offers, skills, and user skills.'''

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import JobOffer, UserSkill, Skill

User = get_user_model()  # Import the user model dynamically


class UserCreateSerializer(BaseUserCreateSerializer):
    """Serializer for creating a user.
    It extends the BaseUserCreateSerializer from Djoser.
    It includes fields for id, username, password, email, first_name, and last_name.
    """

    class Meta(BaseUserCreateSerializer.Meta):
        """
        Meta class to define the fields and model to be used in the serializer.
        """
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    """Serializer for user details.
    It extends the BaseUserSerializer from Djoser.
    It includes fields for id, username, email, first_name, last_name, is_staff, and is_active.
    """

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'is_staff', 'is_active']


class JobOfferSerializer(serializers.ModelSerializer):
    """Serializer for job offers.
    It includes fields for id, match_score, reason, technologies_matched,
    title, company, location, description, apply_link, created_at, user, and email
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    technologies_matched = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    technologies_matched_display = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = JobOffer
        fields = [
            "id",
            "match_score",
            "reason",
            "technologies_matched",
            "technologies_matched_display",
            "title",
            "company",
            "location",
            "description",
            "apply_link",
            "created_at",
            "user",
            "email",
        ]

    def create(self, validated_data):
        # Convert list to comma-separated string before saving
        technologies = validated_data.pop("technologies_matched", [])
        validated_data["technologies_matched"] = ", ".join(technologies)
        return super().create(validated_data)

    def get_technologies_matched_display(self, obj):
        """Returns a list of technologies matched."""
        if not obj.technologies_matched:
            return []
        return obj.technologies_matched.split(", ")

class JobOfferTestSerializer(serializers.ModelSerializer):
    """Serializer for job offers used in tests.
    It includes fields for id, title, company, location, description, apply_link, and created_at.
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    # email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = JobOffer
        fields = ['id', 'title', 'company', 'location', 'description', 'apply_link', 'created_at', 'user_name', 'email']

class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skills.
    It includes fields for id and name.
    """
    class Meta:
        model = Skill
        fields = ['id', 'name']


class UserSkillSerializer(serializers.ModelSerializer):
    """Serializer for user skills.
    It includes fields for id, user, skills, and skill_ids.
    The skill_ids field is used for creating or updating user skills.
    """
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skills', 'skill_ids']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        skill_ids = validated_data.pop("skill_ids", [])
        user = self.context["request"].user
        instance, _ = UserSkill.objects.get_or_create(user=user)
        if skill_ids:
            instance.skills.set(skill_ids)
        return instance

    def update(self, instance, validated_data):
        skill_ids = validated_data.get("skill_ids")
        if skill_ids is not None:
            instance.skills.set(skill_ids)
        return instance

class UserSkillStatSerializer(serializers.Serializer):
    """Serializer for user skill statistics.
    It includes fields for username and num_skills.
    """
    username = serializers.CharField()
    num_skills = serializers.IntegerField()

