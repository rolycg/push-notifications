# Create your views here.
import base64

from Crypto import Random
from Crypto.Cipher import AES
from push_notifications.api.rest_framework import APNSDeviceSerializer, APNSDeviceAuthorizedViewSet
from push_notifications.models import APNSDevice
from rest_framework.decorators import api_view, list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from ios_notifications.settings import JAZWINGS_KEY

iv = Random.new().read(AES.block_size)

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def decode(cipher):
    enc = base64.urlsafe_b64decode(cipher)
    iv = enc[:16]
    cipher = AES.new(JAZWINGS_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


def parse_data(data):
    try:
        data = data.decode('latin1')
        keys = data.split('&&&')
        title = keys[0].split('===')[1]
        assert keys[0].split('===')[0] == 'title'
        msg = keys[1].split('===')[1]
        assert keys[1].split('===')[0] == 'msg'
        return title, msg
    except Exception as e:
        print(str(e))
        return 0


@api_view(['GET'])
def send_message(request):
    try:
        key = request.query_params['q']
    except KeyError:
        return Response({'Error': 'Wrong params'}, status=HTTP_400_BAD_REQUEST)
    data = decode(key)
    ret = parse_data(data)
    if ret:
        title, msg = ret
        for device in APNSDevice.objects.all():
            device.send_message(message={'title': title, 'body': msg})
        return Response({'results': 'Ok'}, status=HTTP_200_OK)
    else:
        return Response({'Error': 'Wrong request'}, status=HTTP_400_BAD_REQUEST)


class MyDeviceViewSetMixin(APNSDeviceAuthorizedViewSet):
    lookup_field = "registration_id"

    def perform_create(self, serializer):
        return super(APNSDeviceAuthorizedViewSet, self).perform_create(serializer)

    @list_route(methods=['POST'], permission_classes=(AllowAny,))
    def add_device(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            print(str(serializer.data))
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)


class APNSDeviceViewSet(MyDeviceViewSetMixin, ModelViewSet):
    queryset = APNSDevice.objects.all()
    serializer_class = APNSDeviceSerializer
