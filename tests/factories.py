import datetime
import factory

from django.contrib.auth import get_user_model

from django_ent.models import ENTInstitution


class InstitutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ENTInstitution

    institution_name = factory.Sequence(lambda n: "Lycée {0}".format(n))
    uai = factory.Sequence(lambda n: "{0}".format(n))
    ends_at = datetime.datetime.today()
    ent = "HDF"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: "noel{0}@flantier.com".format(n))
    is_active = True
    institution = factory.RelatedFactory(InstitutionFactory, "user")
