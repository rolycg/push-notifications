from django.db import models
from django.utils.translation import ugettext_lazy as _
from push_notifications.models import APNSDevice


# Create your models here.


class APNSDevicesExtended(APNSDevice):
    class Meta:
        verbose_name = _('APNS Devices Extended')
        verbose_name_plural = _('APNS Devices Extended')

    badge = models.PositiveIntegerField(verbose_name=_('Badge'), default=0, help_text=_('Number of badges'))
