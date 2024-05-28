from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .utils_otp import SendOtp, get_user_otp
from .utils_jwt import get_tokens_for_user
from .models import Profile
User = get_user_model()

class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class CheckPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

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
                phone_number=self.validated_data.get('phone_number'), 
                password=self.validated_data.get('password'))
            
        else:
            user = User.objects.create_user(
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
    
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20)
    new_password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError("The password is wrong.")
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
            raise serializers.ValidationError("Invalid token")

        return attrs

    def save(self, **kwargs):
        token = RefreshToken(self.validated_data['refresh_token'])
        token.blacklist()
        return self.validated_data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'date_of_birth', 'address', 'city', 'state', 'country', 'postal_code', 'national_id']
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
