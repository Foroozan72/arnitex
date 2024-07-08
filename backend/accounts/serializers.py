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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'date_of_birth', 'address', 'city', 'state', 'country', 'postal_code', 'national_id']
        read_only_fields = ['user']

    def retrieve(self, instance):
        return self.data

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.national_id = validated_data.get('national_id', instance.national_id)
        instance.save()
        return instance
