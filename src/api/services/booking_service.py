from django.utils import timezone
from ..models import Booking, Queue


def create_booking(user, resource, start_time, end_time):
    if Booking.objects.filter(
        resource=resource,
        start_time__lt=end_time,
        end_time__gt=start_time
    ).exists():
        queue_entry = Queue.objects.create(user=user, resource=resource)
        return {"status": "queued", "queue_entry": queue_entry}

    booking = Booking.objects.create(
        user=user,
        resource=resource,
        start_time=start_time,
        end_time=end_time,
        status='active'
    )

    return {"status": "created", "booking": booking}


def cancel_booking(booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()

    if Queue.objects.filter(booking=booking).exists():
        next_in_queue = Queue.objects.filter(booking=booking).first()
        if next_in_queue:
            next_in_queue.delete()
            notify_user(next_in_queue.user)
    return {"status": "cancelled"}


def notify_user(user):
    print(f"User {user.username} has been notified!")
