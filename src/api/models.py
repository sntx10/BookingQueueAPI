from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    name = models.CharField(max_length=191)
    max_duration = models.IntegerField()
    max_users = models.IntegerField()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('queue', 'Queue'),
                                                      ('completed', 'Completed')])

    def save(self, *args, **kwargs):
        if Booking.objects.filter(resource=self.resource,
                                  start_time__lt=self.end_time,
                                  end_time__gt=self.start_time).exists():
            raise ValueError("Slot is already booked.")
        super().save(*args, **kwargs)


class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
