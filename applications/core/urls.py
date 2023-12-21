from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# TODO: complete
urlpatterns = router.urls

urlpatterns += [
    path('sessions/', TokenObtainPairView.as_view(), name='sessions'),
]
