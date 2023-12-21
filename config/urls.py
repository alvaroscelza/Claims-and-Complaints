from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


# region Admin configuration
urlpatterns = i18n_patterns(path('admin/', admin.site.urls), prefix_default_language=False)
admin.site.site_header = settings.APP_NAME
admin.site.index_title = settings.APP_DESCRIPTION
admin.site.site_title = settings.APP_NAME
# endregion

# region Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title=settings.APP_NAME + 'API',
        default_version='v1',
        description=settings.APP_DESCRIPTION,
        contact=openapi.Contact(email='skollars.software.development@gmail.com')
    ),
    public=True
)
swagger_path = path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger')
urlpatterns += i18n_patterns(swagger_path, prefix_default_language=False)
# endregion

# region Core configuration
core_path = path('api/v1/core/', include('applications.core.urls'))
urlpatterns += i18n_patterns(core_path, prefix_default_language=False)
# endregion

# region Tenant configuration
tenants_path = path('api/v1/tenants/', include('applications.tenants.urls'))
urlpatterns += i18n_patterns(tenants_path, prefix_default_language=False)
# endregion

# region Media configuration
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# endregion

# region Templates configuration
urlpatterns += i18n_patterns(path('', TemplateView.as_view(template_name="index.html")), prefix_default_language=False)
# endregion
