from ..models import Queue


def add_to_queue(user):
    queue_entry = Queue.objects.create(user=user)
    print(f"User {user.username} added to queue")
    return queue_entry

