from django.db import models

class JobOffer(models.Model):
    match_score = models.FloatField(default=0.0)
    reason = models.TextField(blank=True)
    technologies_matched = models.TextField(blank=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    apply_link = models.CharField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
    