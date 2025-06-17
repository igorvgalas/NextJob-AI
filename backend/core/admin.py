from django.contrib import admin

# Register your models here.

from .models import JobOffer, UserSkill, Skill


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'location',
                    'created_at', 'user', 'email')
    search_fields = ('title', 'company__name', 'location')
    list_filter = ('location', 'created_at')
    ordering = ('-created_at',)

    def company(self, obj):
        return obj.company.name if obj.company else "No Company"

    company.short_description = 'Company Name'


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_skill_names')
    search_fields = ('user__username',)
    ordering = ('user',)

    def get_skill_names(self, obj):
        return ", ".join(str(skill.name) for skill in obj.skills.all())


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name',)
    ordering = ('name',)
