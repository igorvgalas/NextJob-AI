from django.contrib import admin

# Register your models here.

from .models import JobOffer

@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'company', 'location', 'created_at')
    search_fields = ('title', 'company__name', 'location')
    list_filter = ('location', 'created_at')
    ordering = ('-created_at',)

    def company(self, obj):
        return obj.company.name if obj.company else "No Company"
    
    company.short_description = 'Company Name'
