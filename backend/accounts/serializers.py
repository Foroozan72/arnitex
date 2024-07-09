from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from .utils_otp import SendOtp, get_user_otp
from .utils_jwt import get_tokens_for_user
from .models import Profile
from utils.response import CustomValidationError
User = get_user_model()

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=11, required=False)
    position = serializers.CharField(max_length=11, required=False, default='login')

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise CustomValidationError(_('Sending one of the email and phone number fields is required.'))

        elif attrs.get('email') and attrs.get('phone_number'):
            raise CustomValidationError(_('Please submit only one item between the email and phone number fields.'))

        elif attrs.get('position') == 'login' and attrs.get('email') and not User.objects.filter(email=attrs.get('email')).exists():
            raise CustomValidationError(_('The email is not exists.'))

        elif attrs.get('position') == 'login' and attrs.get('phone_number') and not User.objects.filter(phone_number=attrs.get('phone_number')).exists():
            raise CustomValidationError(_('The phone number is not exists.'))

        elif attrs.get('position') == 'register' and attrs.get('email') and User.objects.filter(email=attrs.get('email')).exists():
            raise CustomValidationError(_('This email exists.'))

        elif attrs.get('position') == 'register' and attrs.get('phone_number') and User.objects.filter(phone_number=attrs.get('phone_number')).exists():
            raise CustomValidationError(_('This phone number exists.'))

        return attrs

    def save(self, **kwargs):
        if self.validated_data.get('phone_number'):
            SendOtp.send_otp_SMS(self, self.validated_data.get('phone_number'))

        else:
            SendOtp.send_otp_email(self, self.validated_data.get('email'))
        return self.validated_data

class RegisterVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=11, required=False)
    password1 = serializers.CharField(max_length=20)
    password2 = serializers.CharField(max_length=20)
    otp = serializers.IntegerField(write_only=True, required=True
    )
    refresh = serializers.CharField(max_length=128, read_only=True)
    access = serializers.CharField(max_length=128, read_only=True)

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise CustomValidationError(_('Sending one of the email and phone number fields is required.'))
    
        elif attrs.get('email') and attrs.get('phone_number'):
            raise CustomValidationError(_('Please submit only one item between the email and phone number fields.'))
    
        elif attrs.get('password1') != attrs.get('password2'):
            raise CustomValidationError(_("The password is not the same."))
        
        elif attrs.get('email'):
            if User.objects.filter(email=attrs.get('email')):
                raise CustomValidationError(_("The email aleady exists."))
            
            elif get_user_otp(email=attrs["email"]) == None:
                raise CustomValidationError(_("Your OTP has been expired."))

            elif get_user_otp(email=attrs["email"]) != attrs["otp"]:
                raise CustomValidationError(_("Invalid OTP."))
        else:
            if User.objects.filter(phone_number=attrs.get('phone_number')):
                raise CustomValidationError(_("The phone number aleady exists."))
            
            elif get_user_otp(phone_number=attrs["phone_number"]) == None:
                raise CustomValidationError(_("Your OTP has been expired."))

            elif get_user_otp(phone_number=attrs["phone_number"]) != attrs["otp"]:
                raise CustomValidationError(_("Invalid OTP."))
        return attrs

    def save(self, **kwargs):
        if self.validated_data.get('phone_number'):
            user = User.objects.create_user(
                phone_number=self.validated_data.get('phone_number'), 
                password=self.validated_data.get('password1'))
            
        else:
            user = User.objects.create_user(
                email=self.validated_data.get('email'), 
                password=self.validated_data.get('password1'))

        self.validated_data["access"] = get_tokens_for_user(user)['access']
        self.validated_data["refresh"] = get_tokens_for_user(user)['refresh']
        return self.validated_data

class LoginVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=11, required=False)
    password = serializers.CharField(max_length=20)
    otp = serializers.IntegerField(write_only=True, required=True
    )
    refresh = serializers.CharField(max_length=128, read_only=True)
    access = serializers.CharField(max_length=128, read_only=True)

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise CustomValidationError(_('Sending one of the email and phone number fields is required.'))
    
        elif attrs.get('email') and attrs.get('phone_number'):
            raise CustomValidationError(_('Please submit only one item between the email and phone number fields.'))
        
        elif attrs.get('email'):
            if not User.objects.filter(email=attrs.get('email')):
                raise CustomValidationError(_("The email is not exists."))
            
            elif get_user_otp(email=attrs["email"]) == None:
                raise CustomValidationError(_("Your OTP has been expired."))

            elif get_user_otp(email=attrs["email"]) != attrs["otp"]:
                raise CustomValidationError(_("Invalid OTP."))

            user = User.objects.get(email=attrs["email"])
            if not user.check_password(attrs['password']):
                raise CustomValidationError(_("The password or email is incorrect."))
        else:
            if not User.objects.filter(phone_number=attrs.get('phone_number')):
                raise CustomValidationError(_("The phone number is not exists."))
            
            elif get_user_otp(phone_number=attrs["phone_number"]) == None:
                raise CustomValidationError(_("Your OTP has been expired."))

            elif get_user_otp(phone_number=attrs["phone_number"]) != attrs["otp"]:
                raise CustomValidationError(_("Invalid OTP."))

            user = User.objects.get(phone_number=attrs["phone_number"])
            if not user.check_password(attrs['password']):
                raise CustomValidationError(_("The password or phone number is incorrect."))
        return attrs

    def save(self, **kwargs):
        if self.validated_data.get('phone_number'):
            user = User.objects.get(
                phone_number=self.validated_data.get('phone_number'))
        
        else:
            user = User.objects.get(
                email=self.validated_data.get('email'))
            
        self.validated_data["access"] = get_tokens_for_user(user)['access']
        self.validated_data["refresh"] = get_tokens_for_user(user)['refresh']
        return self.validated_data

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=11, required=False)
    new_password = serializers.CharField(max_length=20)
    otp = serializers.IntegerField(write_only=True, required=True
    )

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise CustomValidationError(_('Sending one of the email and phone number fields is required.'))
    
        elif attrs.get('email') and attrs.get('phone_number'):
            raise CustomValidationError(_('Please submit only one item between the email and phone number fields.'))
        
        elif attrs.get('email'):
            if not User.objects.filter(email=attrs.get('email')):
                raise CustomValidationError(_("The email is not exists."))
            
            elif get_user_otp(email=attrs["email"]) == None:
                raise CustomValidationError(_("Your OTP has been expired."))

            elif get_user_otp(email=attrs["email"]) != attrs["otp"]:
                raise CustomValidationError(_("Invalid OTP."))
            
        else:
            if not User.objects.filter(phone_number=attrs.get('phone_number')):
                raise CustomValidationError(_("The phone number is not exists."))
            
            elif get_user_otp(phone_number=attrs["phone_number"]) == None:
                raise CustomValidationError(_("Your OTP has been expired."))

            elif get_user_otp(phone_number=attrs["phone_number"]) != attrs["otp"]:
                raise CustomValidationError(_("Invalid OTP."))
            
        return attrs

    def save(self, **kwargs):
        if self.validated_data.get('phone_number'):
            user = User.objects.get(
                phone_number=self.validated_data.get('phone_number'))
        
        else:
            user = User.objects.get(
                email=self.validated_data.get('email'))
            
        user.set_password(self.validated_data.get('new_password'))
        user.save()
            
        self.validated_data["access"] = get_tokens_for_user(user)['access']
        self.validated_data["refresh"] = get_tokens_for_user(user)['refresh']
        return self.validated_data
    
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20)
    new_password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['password']):
            raise CustomValidationError(_("The password is incorrect."))
        return attrs 
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

        return self.validated_data

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=300)

    def validate(self, attrs):
        try:
            token = RefreshToken(attrs['refresh_token'])
        except Exception as e:
            raise CustomValidationError(_("Invalid token."))

        return attrs

    def save(self, **kwargs):
        token = RefreshToken(self.validated_data['refresh_token'])
        token.blacklist()
        return self.validated_data





from rest_framework import serializers
from .models import Profile
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
import random
import string
import unicodedata

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'image', 'date_of_birth', 'address', 'city', 'state', 'country', 'postal_code', 'national_id']
        read_only_fields = ['user']

    def retrieve(self, instance):
        return self.data

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.image = validated_data.get('image', instance.image)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.national_id = validated_data.get('national_id', instance.national_id)

        # Generate image with initials if no image is uploaded
        if instance.first_name and instance.last_name and instance.image == 'profile/image/default.jpg' :
            initials = self.get_initials(instance.first_name, instance.last_name)
            image_path = self.generate_initials_image(initials)
            # instance.image.save(image_path, save=False)

        instance.save()
        return instance

    def get_initials(self, first_name, last_name):
        # Determine the initials based on the language of the characters
        if self.is_persian(first_name) and self.is_persian(last_name):
            initials = (last_name[0] + ' ' + first_name[0])
        else:
            initials = (last_name[0].upper() + first_name[0].upper())
        return initials

    def is_persian(self, text):
        # Check if the text is in Persian
        for char in text:
            if 'ARABIC' in unicodedata.name(char):
                return True
        return False

    def generate_initials_image(self, initials):
        # Create an image with initials
        image_size = (250, 250)
        background_color = self.get_random_color()
        text_color = (255, 255, 255)
        font_size = 100

        image = Image.new('RGB', image_size, color=background_color)
        draw = ImageDraw.Draw(image)
        # استفاده از یک فونت که در دسترس است
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)

        # Get the size of the text
        text_bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = (image_size[0] - text_width) / 2
        text_y = (image_size[1] - text_height) / 2
        draw.text((text_x, text_y), initials, fill=text_color, font=font)

        # Generate a random filename
        filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.png'
        image_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image.save(image_path)

        # Return relative path to the image
        return os.path.join('profile_pics', filename)

    def get_random_color(self):
        # Generate a random color
        return tuple(random.randint(0, 255) for _ in range(3))