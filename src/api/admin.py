from django.contrib import admin

from api.models import Resource, Booking, Queue

admin.site.register(Resource)
admin.site.register(Booking)
admin.site.register(Queue)
