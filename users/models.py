from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.sessions.models import Session

from .validators import validate_phone


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, group_pk=None, *args, **kwargs):
        created = self.id is None
        super().save(*args, **kwargs)
        if created and group_pk:
            group = Group.objects.get(pk=group_pk)
            self.groups.add(group)
            self.save()

    def get_short_name(self):
        return '{} {:.1}.'.format(self.last_name, self.first_name)

    def remove_sessions(self):
        UserSession.objects.filter(user=self).delete()

    @property
    def is_customer(self):
        return self.groups.filter(name='Customers').exists()

    @property
    def is_clerk(self):
        return self.groups.filter(name='Clerks').exists()

    @property
    def is_head_clerk(self):
        return self.groups.filter(name='Head-clerks').exists()


class UserSession(models.Model):
    user = models.ForeignKey(User, related_name='sessions')
    session = models.ForeignKey(Session)
    ip = models.GenericIPAddressField()


class CustomerProfile(models.Model):
    ATTORNEY = 0
    TITLE_SEARCHER = 1
    APPRAISER = 2
    REAL_ESTATE_AGENT = 3
    MEMBER_OF_THE_PUBLIC = 4
    ATTORNEY_ASSISTANT_SECRETARY = 5

    CUSTOMER_TYPE = (
        (ATTORNEY, 'Attorney'),
        (TITLE_SEARCHER, 'Title Searcher'),
        (APPRAISER, 'Appraiser'),
        (REAL_ESTATE_AGENT, 'Real Estate Agent'),
        (MEMBER_OF_THE_PUBLIC, 'Member of the Public'),
        (ATTORNEY_ASSISTANT_SECRETARY, 'Attorney Assistant / Secretary')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')

    phone_number = models.CharField(validators=[validate_phone], max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    accepted_agreement = models.BooleanField(default=False)
    hear_us_from = models.CharField(max_length=200, blank=True, null=True)
    customer_type = models.IntegerField(choices=CUSTOMER_TYPE, default=ATTORNEY)

    def __str__(self):
        return self.user.get_full_name()


class ClerkProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clerk_profile')
    phone_number = models.CharField(validators=[validate_phone], max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
