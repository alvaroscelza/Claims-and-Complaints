from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# region Admin configuration
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls), prefix_default_language=False
)
admin.site.site_header = admin.site.site_title = settings.APP_NAME
admin.site.index_title = settings.APP_DESCRIPTION
# endregion

# # region Core configuration
# core_path = path('api/v1/core/', include('applications.core.urls'))
# urlpatterns += i18n_patterns(core_path, prefix_default_language=False)
# # endregion

# region Media configuration
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# endregion

# region Templates configuration
urlpatterns += i18n_patterns(
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('accounts/', include('users.urls', namespace='users')),
    prefix_default_language=False,
)
# endregion
