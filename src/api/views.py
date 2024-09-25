from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Resource, Booking
from .serializers import ResourceSerializer, BookingSerializer
from .services.booking_service import create_booking, cancel_booking


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        resource_id = request.data.get("resource")
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")

        try:
            resource = Resource.objects.get(id=resource_id)
        except Resource.DoesNotExist:
            return Response({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)

        result = create_booking(user, resource, start_time, end_time)

        if result["status"] == "queued":
            return Response({"message": "Added to queue", "queue_entry": result["queue_entry"].id},
                            status=status.HTTP_202_ACCEPTED)
        elif result["status"] == "created":
            return Response(BookingSerializer(result["booking"]).data, status=status.HTTP_201_CREATED)

        return Response({"error": "Could not create booking."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        booking_id = self.kwargs.get("pk")
        result = cancel_booking(booking_id)
        return Response({"status": result["status"]}, status=status.HTTP_204_NO_CONTENT)