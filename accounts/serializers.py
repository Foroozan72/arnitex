from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils_otp import SendOtp, get_user_otp
from .utils_jwt import get_tokens_for_user
User = get_user_model()

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=11, required=False)

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise serializers.ValidationError("Sending one of the email and phone number fields is required.")
    
        elif attrs.get('email') and attrs.get('phone_number'):
            raise serializers.ValidationError("Please send only one between the email and phone number fields.")
        
        return attrs

    def save(self, **kwargs):
        if self.validated_data.get('phone_number'):
            SendOtp.send_otp_SMS(self.validated_data.get('phone_number'))

        else:
            SendOtp.send_otp_email(self.validated_data.get('email'))
        return self.validated_data

class RegisterVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=11, required=False)
    password = serializers.CharField(max_length=20)
    otp = serializers.IntegerField(
        min_value=10000, max_value=999999, write_only=True, required=True
    )
    refresh = serializers.CharField(max_length=128, read_only=True)
    access = serializers.CharField(max_length=128, read_only=True)

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise serializers.ValidationError("Sending one of the email and phone number fields is required.")
    
        elif attrs.get('email') and attrs.get('phone_number'):
            raise serializers.ValidationError("Please send only one between the email and phone number fields.")
        
        elif attrs.get('email'):
            if User.objects.filter(email=attrs.get('email')):
                raise serializers.ValidationError("The email aleady exists.")
            
            elif get_user_otp(email=attrs["email"]) == None:
                raise serializers.ValidationError("Your OTP has been expired")

            elif get_user_otp(email=attrs["email"]) != attrs["otp"]:
                raise serializers.ValidationError("Invalid OTP token")
        else:
            if User.objects.filter(phone_number=attrs.get('phone_number')):
                raise serializers.ValidationError("The email aleady exists.")
            
            elif get_user_otp(phone_number=attrs["phone_number"]) == None:
                raise serializers.ValidationError("Your OTP has been expired")

            elif get_user_otp(phone_number=attrs["phone_number"]) != attrs["otp"]:
                raise serializers.ValidationError("Invalid OTP token")
        return attrs

    def save(self, **kwargs):
        if self.validated_data.get('phone_number'):
            user = User.objects.create_user(
                phone_number=self.validated_data.get('phone_number'))
            
        else:
            user = User.objects.create_superuser(
                email=self.validated_data.get('email'), 
                password=self.validated_data.get('password'))

        self.validated_data["access"] = get_tokens_for_user(user)['access']
        self.validated_data["refresh"] = get_tokens_for_user(user)['refresh']
        return self.validated_data

class LoginVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=11, required=False)
    password = serializers.CharField(max_length=20)
    otp = serializers.IntegerField(
        min_value=10000, max_value=999999, write_only=True, required=True
    )
    refresh = serializers.CharField(max_length=128, read_only=True)
    access = serializers.CharField(max_length=128, read_only=True)

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise serializers.ValidationError("Sending one of the email and phone number fields is required.")
    
        elif attrs.get('email') and attrs.get('phone_number'):
            raise serializers.ValidationError("Please send only one between the email and phone number fields.")
        
        elif attrs.get('email'):
            if not User.objects.filter(email=attrs.get('email')):
                raise serializers.ValidationError("The email is not exists.")
            
            elif get_user_otp(email=attrs["email"]) == None:
                raise serializers.ValidationError("Your OTP has been expired")

            elif get_user_otp(email=attrs["email"]) != attrs["otp"]:
                raise serializers.ValidationError("Invalid OTP token")

            user = User.objects.get(email=attrs["email"])
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError("The password or email is incorrect")
        else:
            if not User.objects.filter(phone_number=attrs.get('phone_number')):
                raise serializers.ValidationError("The phone number is not exists.")
            
            elif get_user_otp(phone_number=attrs["phone_number"]) == None:
                raise serializers.ValidationError("Your OTP has been expired")

            elif get_user_otp(phone_number=attrs["phone_number"]) != attrs["otp"]:
                raise serializers.ValidationError("Invalid OTP token")

            user = User.objects.get(phone_number=attrs["phone_number"])
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError("The password or phone number is incorrect")
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
    otp = serializers.IntegerField(
        min_value=10000, max_value=999999, write_only=True, required=True
    )

    def validate(self, attrs):
        if attrs.get('email') is None and attrs.get('phone_number') is None:
            raise serializers.ValidationError("Sending one of the email and phone number fields is required.")
    
        elif attrs.get('email') and attrs.get('phone_number'):
            raise serializers.ValidationError("Please send only one between the email and phone number fields.")
        
        elif attrs.get('email'):
            if not User.objects.filter(email=attrs.get('email')):
                raise serializers.ValidationError("The email is not exists.")
            
            elif get_user_otp(email=attrs["email"]) == None:
                raise serializers.ValidationError("Your OTP has been expired")

            elif get_user_otp(email=attrs["email"]) != attrs["otp"]:
                raise serializers.ValidationError("Invalid OTP token")
            
        else:
            if not User.objects.filter(phone_number=attrs.get('phone_number')):
                raise serializers.ValidationError("The phone number is not exists.")
            
            elif get_user_otp(phone_number=attrs["phone_number"]) == None:
                raise serializers.ValidationError("Your OTP has been expired")

            elif get_user_otp(phone_number=attrs["phone_number"]) != attrs["otp"]:
                raise serializers.ValidationError("Invalid OTP token")
            
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