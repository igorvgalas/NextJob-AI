'''This file contains the Django models for the job offer and user skills system.
It includes the JobOffer, Skill, and UserSkill models, which are used to manage job offers,
skills, and user skills in the application.'''
from django.db import models
from django.conf import settings


class JobOffer(models.Model):
    """Model representing a job offer.
    Attributes:
        user (ForeignKey): The user who created the job offer.
        email (EmailField): The email associated with the job offer.
        match_score (FloatField): The score indicating how well the job offer matches user skills.
        reason (TextField): The reason for the match score.
        technologies_matched (TextField): Comma-separated list of technologies matched.
        title (CharField): The title of the job offer.
        company (CharField): The company offering the job.
        location (CharField): The location of the job.
        description (TextField): A description of the job offer.
        apply_link (CharField): The link to apply for the job.
        created_at (DateTimeField): The date and time when the job offer was created.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_offers', null=True, blank=True
    )
    email = models.EmailField(default='', blank=True, null=True)
    match_score = models.FloatField(default=0.0)
    reason = models.TextField(blank=True, null=True)
    technologies_matched = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    apply_link = models.CharField(max_length=1020, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        
    def __str__(self):
        return f"{self.title} at {self.company}"

    def save(self, *args, **kwargs):
        if self.email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user_obj = User.objects.filter(email=self.email).first()
            self.user = user_obj if user_obj else None
        super().save(*args, **kwargs)


class Skill(models.Model):
    """Model representing a skill.
    Attributes:
        name (CharField): The name of the skill.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class UserSkill(models.Model):
    """Model representing a user's skills.
    Attributes:
        user (ForeignKey): The user who has the skills.
        skills (ManyToManyField): The skills associated with the user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_skills')
    skills = models.ManyToManyField(Skill, related_name='user_skills', blank=True)

    def get_skill_ids(self):
        """Returns a list of skill IDs associated with the user."""
        if self.pk:
            return list(self.skills.all().values_list('id', flat=True))  # pylint:disable=no-member
        return []
