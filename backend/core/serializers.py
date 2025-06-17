from collections import defaultdict
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


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


# class UserSkillListSerializer(serializers.Serializer):
#     id = serializers.IntegerField()  # Add id field
#     user = serializers.IntegerField()
#     skills = SkillSerializer(many=True)

# # Custom list serializer to group skills by user


# class UserSkillGroupByUserSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         grouped = defaultdict(list)
#         for item in data:
#             grouped[item.user_id].append(item)
#         result = []
#         for user_id, items in grouped.items():
#             skills = []
#             ids = []
#             for item in items:
#                 skills.extend(item.skills.all())
#                 ids.append(item.id)
#             # Remove duplicates
#             unique_skills = {s.id: s for s in skills}.values()
#             result.append({
#                 "id": ids[0] if ids else None,  # Use the first UserSkill id
#                 "user": user_id,
#                 "skills": SkillSerializer(unique_skills, many=True).data
#             })
#         return result


# class UserSkillSerializer(serializers.ModelSerializer):
#     skills = SkillSerializer(many=True)

#     class Meta:
#         model = UserSkill
#         fields = ['id', 'user', 'skills']
#         list_serializer_class = UserSkillGroupByUserSerializer


# class UserSkillCreateSerializer(serializers.ModelSerializer):
#     skills = serializers.ListField(
#         child=serializers.IntegerField(), write_only=True)

#     class Meta:
#         model = UserSkill
#         fields = ['id', 'user', 'skills']

#     def create(self, validated_data):
#         user = validated_data['user']
#         skills_data = validated_data.get('skills', [])
#         # Always use the first UserSkill for this user, or create if none exists
#         obj, _ = UserSkill.objects.get_or_create(user=user)
#         obj.skills.set(skills_data)
#         # Delete any duplicate UserSkill objects for this user
#         UserSkill.objects.filter(user=user).exclude(pk=obj.pk).delete()
#         return obj


# class UserSkillUpdateSerializer(serializers.ModelSerializer):
#     skills = serializers.ListField(
#         child=serializers.IntegerField(), write_only=True)

#     class Meta:
#         model = UserSkill
#         fields = ['skills']

#     def update(self, instance, validated_data):
#         skills_data = validated_data.get('skills', [])
#         instance.skills.set(skills_data)
#         return instance

class UserSkillSerializer(serializers.ModelSerializer):
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

