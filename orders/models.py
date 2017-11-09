from django.db import models
from django.urls import reverse

from users.models import CustomerProfile


class Order(models.Model):
    TO_FILL = 0
    IN_PROGRESS = 1
    COMPLETE = 2

    STATUSES = (
        (TO_FILL, 'To Fill'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETE, 'Complete'),
    )
    owner = models.ForeignKey(CustomerProfile, related_name='orders', on_delete=models.CASCADE)

    file_number = models.CharField('File number/Customer Reference (Optional)', max_length=100, blank=True, null=True)
    case = models.CharField('Case #', max_length=150)
    party_name = models.CharField('Party or Entity name', max_length=100)

    name = models.CharField('Exact name', max_length=100)
    needed_date = models.DateField('Date you need')

    status = models.IntegerField('Order status', choices=STATUSES, default=TO_FILL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orders:detail', args=[str(self.id)])
