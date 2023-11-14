from django.contrib.auth import get_user_model

User = get_user_model()


class CASBackend:
    """
    CAS authentication with UAI (Unité Administrative Immatriculée) number
    """

    @staticmethod
    def authenticate(request, ent_uai_numbers):
        return User.objects.filter(entinstitution__uai__in=ent_uai_numbers).last()

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
