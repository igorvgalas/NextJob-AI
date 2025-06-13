from django.contrib import admin

# Register your models here.

from .models import JobOffer, UserSkill, Skill

@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'company', 'location', 'created_at', 'user', 'email')
    search_fields = ('title', 'company__name', 'location')
    list_filter = ('location', 'created_at')
    ordering = ('-created_at',)

    def company(self, obj):
        return obj.company.name if obj.company else "No Company"
    
    company.short_description = 'Company Name'

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    def skills_list(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    skills_list.short_description = 'Skills'

    list_display = ('user', 'skills_list')
    search_fields = ('user__username', 'skills__name')
    list_filter = ('proficiency',)
    ordering = ('user',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)