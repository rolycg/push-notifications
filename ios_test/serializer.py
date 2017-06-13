from push_notifications.api.rest_framework import APNSDeviceSerializer
from rest_framework import serializers
from ios_test.models import APNSDevicesExtended


class APNSDeviceSerializerExtended(APNSDeviceSerializer):
    badge = serializers.IntegerField()

    class Meta:
        model = APNSDevicesExtended
        fields = '__all__'
