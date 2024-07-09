from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from utils.models import TimeStamp, UUID
User = get_user_model()


class Image(TimeStamp, UUID):
    image = models.ImageField(upload_to='media_hub/images/',
                              verbose_name=_('Image'), help_text='Upload image with specific pixels')
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name, verbose_name_plural = _('Image'), _('Images')
