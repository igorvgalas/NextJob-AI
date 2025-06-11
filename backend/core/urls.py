from rest_framework.routers import DefaultRouter
from .views import JobOfferViewSet

router = DefaultRouter()
router.register(r'jobs', JobOfferViewSet, basename='joboffer')


urlpatterns = router.urls
