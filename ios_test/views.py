# Create your views here.
from push_notifications.models import APNSDevice
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ios_notifications.settings import JAZWINGS_KEY


@api_view(['GET'])
def send_message(request):
    print(str(request.query_params.keys()))
    try:
        key = request.query_params['key']
        msg = request.query_params['msg']
        title = request.query_params['title']
    except KeyError:
        return Response({'Error': 'Wrong params'}, status=HTTP_400_BAD_REQUEST)
    if key != JAZWINGS_KEY:
        return Response({'Error': 'Wrong authentication'}, status=HTTP_400_BAD_REQUEST)
    for device in APNSDevice.objects.all():
        device.send_message(message={'title': title, 'body': msg})
    return Response({'results': 'Ok'}, status=HTTP_200_OK)
