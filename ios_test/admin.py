from django.contrib import admin
from push_notifications.admin import DeviceAdmin
from ios_test.models import APNSDevicesExtended

# Register your models here.


class APNSDeviceExtendedAdmin(DeviceAdmin):
    pass


admin.site.register(APNSDevicesExtended, APNSDeviceExtendedAdmin)