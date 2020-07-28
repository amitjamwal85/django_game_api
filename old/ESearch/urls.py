from rest_framework.routers import SimpleRouter
from ESearch.views import PublisherViewSet

app_name = 'publisher'

router = SimpleRouter()
router.register(r'', PublisherViewSet, basename='publisher')
urlpatterns = router.urls