from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db import models


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=180, default='Untitled')
    description = models.TextField(blank=True, null=True)

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __repr__(self):
        return '<Budget: {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)


class Transaction(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=180, default='Untitled')
    description = models.TextField(blank=True, null=True)

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_completed = models.DateField(blank=True, null=True)

    STATES = (
        ('COMPLETE', 'Complete'),
        ('INCOMPLETE', 'Incomplete'),
    )
    status = models.CharField(
        max_length=16,
        choices=STATES,
        default='Incomplete'
    )

    def __repr__(self):
        return '<Transaction: {} | {}>'.format(self.title, self.status)

    def __str__(self):
        return '{} | {}'.format(self.title, self.status)


@receiver(models.signals.post_save, sender=Transaction)
def set_transaction_completed_date(sender, instance, **kwargs):
    """Update the date completed if completed."""
    if instance.date_completed == 'Complete' and not instance.date_completed:
        instance.date_completed = timezone.now()
        instance.save()
