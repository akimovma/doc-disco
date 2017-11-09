from celery.task import task
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.models import Site

from post_office import mail

from doc_disco.utils import get_or_none
from users.models import User
from users.tokens import account_activation_token


@task
def verification_email_send(user_pk):
    user = get_or_none(User, pk=user_pk)
    if not user:
        return
    url_params = {
        'uid': urlsafe_base64_encode(force_bytes(user_pk)),
        'token': account_activation_token.make_token(user)
    }
    url = "%s%s" % (Site.objects.get_current().domain,
                    reverse_lazy('users:verify_email', kwargs=url_params))

    ctx = {
        'verify_url': url,
    }
    mail.send(user.email, 'noreply@doc_disco.com',
              template='Signup verification email',
              context=ctx)
