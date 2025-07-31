'''This file contains the URL routing for the core application.
It includes the routes for job offers, skills, and user skills.'''
from rest_framework.routers import DefaultRouter
from .views import JobOfferTestViewSet, JobOfferViewSet, UserSkillViewSet, SkillViewSet, UserSkillStatViewSet
from debug_toolbar.toolbar import debug_toolbar_urls

router = DefaultRouter()
router.register(r'jobs', JobOfferViewSet, basename='joboffer')
router.register(r'jobtest', JobOfferTestViewSet, basename='jobtest')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'userskills', UserSkillViewSet, basename='userskill')
router.register(r'userskillstats', UserSkillStatViewSet, basename='userskillstat')



urlpatterns = router.urls + debug_toolbar_urls()
