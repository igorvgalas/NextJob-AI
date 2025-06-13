from rest_framework.routers import DefaultRouter
from .views import JobOfferViewSet, UserSkillViewSet

router = DefaultRouter()
router.register(r'jobs', JobOfferViewSet, basename='joboffer')
router.register(r'userskills', UserSkillViewSet, basename='userskill')


urlpatterns = router.urls
