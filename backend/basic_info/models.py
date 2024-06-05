from django.db import models
from utils.models import TimeStamp
from django.utils.translation import ugettext_lazy as _

class Country(TimeStamp):
<<<<<<< HEAD
    title = models.CharField(_('Field Name') , max_length=200)
    is_show = models.BooleanField(_('Field Name') ,default=True)

=======
    title = models.CharField(max_length=200)
    flag = models.CharField(max_length=200, null=True)
    is_show = models.BooleanField(default=True)
>>>>>>> 7fda1b6a7f916a228f515ffd9d2c05175b81e36a

    def __str__(self):
        return f"{self.title} - {self.is_show}"

class City(TimeStamp):
    title = models.CharField(_('Field Name') ,max_length=200)
    is_show = models.BooleanField(_('Field Name') ,default=True)
    country = models.ForeignKey(_('Field Name') ,Country, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
<<<<<<< HEAD
        return f"{self.title} - {self.is_show}"


class State(TimeStamp):
    title = models.CharField(_('Field Name') ,max_length=200 , default = 'nothing')
    is_show = models.BooleanField(_('Field Name') , default=True)
    city = models.ForeignKey(_('Field Name') , City, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return f"{self.title} - {self.is_show}"
=======
        return f"{self.title} - {self.is_show}"
>>>>>>> 7fda1b6a7f916a228f515ffd9d2c05175b81e36a
