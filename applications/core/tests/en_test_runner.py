from django.conf import settings
from django.test.runner import DiscoverRunner


class EnTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        settings.LANGUAGE_CODE = 'en'
        super().setup_test_environment(**kwargs)
