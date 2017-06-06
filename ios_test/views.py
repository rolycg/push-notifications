# Create your views here.
from push_notifications.models import APNSDevice
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


@api_view(['GET', 'POST'])
def send_message(request):
    device = APNSDevice.objects.get(registration_id="b40618f6ab61c2a9d1cba54afd0b45d01b4c630c986b85a068c3334273af0775")
    device.send_message("You've got mail")
    return Response({'results': 'Ok'}, status=HTTP_200_OK)
