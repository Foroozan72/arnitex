from django.db import models
from utils.models import TimeStamp, UUID


class Country(TimeStamp):
    title = models.CharField(max_length=200  )
    is_show = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.title} - {self.is_show}"

class City(TimeStamp):
    title = models.CharField(max_length=200)
    tssssitle = models.CharField(max_length=200)
    is_show = models.BooleanField(default = True)
    country = models.ForeignKey(Country , on_delete = models.CASCADE , related_name='city')

    def __str__(self):
        return f"{self.title} - {self.is_show}"

class State(TimeStamp):
    title = models.CharField(max_length=200),
    titless = models.CharField(max_length=200),
    is_show = models.BooleanField(default = True)
    city = models.ForeignKey(City , on_delete=models.CASCADE , related_name='state')

    def __str__(self):
        return f"{self.title} - {self.is_show}"

# Create your models here.


