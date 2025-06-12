from django.db import models
from django.conf import settings


class JobOffer(models.Model):
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

    def __str__(self):
        return f"{self.title} at {self.company}"

    def save(self, *args, **kwargs):
        if self.email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user_obj = User.objects.filter(email=self.email).first()
            self.user = user_obj if user_obj else None
        super().save(*args, **kwargs)
