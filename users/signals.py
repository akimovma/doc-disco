from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.signals import user_logged_in

from users.helpers import get_user_ip
from users.models import User, CustomerProfile, ClerkProfile, UserSession


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if instance.is_customer:
        try:
            instance.customer_profile.save()
        except ObjectDoesNotExist:
            CustomerProfile.objects.create(user=instance)
    elif instance.is_clerk:
        try:
            instance.clerk_profile.save()
        except ObjectDoesNotExist:
            ClerkProfile.objects.create(user=instance)


def proceed_clerks_sessions(sender, request=None, user=None, **kwargs):
    if user.is_clerk:
        user_session, _ = UserSession.objects.get_or_create(
            user=user,
            session_id=request.session.session_key,
            ip=get_user_ip(request)
        )
        sessions_to_delete = UserSession.objects.filter(user=user).exclude(session_id=user_session.session_id)
        Session.objects.filter(session_key__in=sessions_to_delete.values_list('session_id')).delete()


user_logged_in.connect(proceed_clerks_sessions)
