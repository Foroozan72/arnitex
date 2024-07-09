from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from utils.models import TimeStamp, UUID
from django.utils.translation import gettext_lazy as _
from wallet.models import Wallet

class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None):
        if not phone_number and not email:
            raise ValueError('User must enter phone number or email')

        user = self.model(email=email, phone_number=phone_number,)

        user.set_password(password)
        user.save(using=self._db)
        Profile.objects.create(user=user)
        Wallet.objects.create(user=user)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None):
        user = self.create_user(email, phone_number, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=20, blank=True, null=True , verbose_name=_('Phone_number'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Date_joined'))
    last_login = models.DateTimeField(auto_now=True, verbose_name=_('Last_login'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Is_verified'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is_staff'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    class Meta():
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    objects = UserManager()

    def __str__(self):
        return f"{self.email} - {self.phone_number}"

class Profile(TimeStamp, UUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    image = models.ImageField(default='profile/images/default.jpg', upload_to='profile/images', null=True, blank=True, verbose_name=_('Image'))
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('First_name'))
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Last_name'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date_of_birth'))
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Address'))
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('City'))
    state = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('State'))
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Country'))
    postal_code = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Postal_code'))
    national_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('National_id'))