from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import JobOffer, UserSkill, Skill

User = get_user_model()  # Import the user model dynamically


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        """
        Meta class to define the fields and model to be used in the serializer.
        """
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'is_staff', 'is_active']


class JobOfferSerializer(serializers.ModelSerializer):
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
        return obj.technologies_matched.split(", ")


class UserSkillSerializer(serializers.ModelSerializer):
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all())
    skill_name = serializers.CharField(source='skill.name', read_only=True)

    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skill', 'skill_name', 'proficiency']
