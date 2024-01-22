from rest_framework.routers import SimpleRouter

from .views import AccountsController

router = SimpleRouter()
router.register(r'accounts', AccountsController, basename='accounts')
urlpatterns = router.urls
