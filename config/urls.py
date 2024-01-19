from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# region Admin configuration
urlpatterns = i18n_patterns(path('admin/', admin.site.urls), prefix_default_language=False)
admin.site.site_header = settings.APP_NAME
admin.site.index_title = settings.APP_DESCRIPTION
admin.site.site_title = settings.APP_NAME
# endregion

# region Core configuration
core_path = path('', include('applications.core.urls'))
urlpatterns += i18n_patterns(core_path, prefix_default_language=False)
# endregion

# region Users configuration
users_path = path('users/', include('applications.users.urls'))
urlpatterns += i18n_patterns(users_path, prefix_default_language=False)
# endregion

# region Media configuration
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# endregion

# region Generic Templates configuration
# contact_template = TemplateView.as_view(template_name='contact.html')
# urlpatterns += i18n_patterns(path(r'contact/', contact_template), prefix_default_language=False)
# terms_and_conditions_template = TemplateView.as_view(template_name='terms_and_conditions.html')
# urlpatterns += i18n_patterns(path(r'terms/', terms_and_conditions_template), prefix_default_language=False)
# endregion
