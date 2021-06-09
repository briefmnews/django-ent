import pytest

from django_ent.apps import DjangoEntConfig

pytestmark = pytest.mark.django_db


class TestDjangoEsidocConfig(object):
    @staticmethod
    def test_apps():
        assert "django_ent" in DjangoEntConfig.name
