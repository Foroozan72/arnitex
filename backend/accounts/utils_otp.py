import pyotp
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail

def get_user_otp(phone_number=None, email=None):
	if phone_number != None:
		stored_otp = cache.get(phone_number)
	else:
		stored_otp = cache.get(email)
	if stored_otp:
		return int(stored_otp)

class SendOtp:
	@staticmethod
	def generate_otp():
		totp = pyotp.TOTP(s=pyotp.random_base32(), digits=5)
		code = totp.now()
		print('code: ', code)
		return code

	@staticmethod
	def send_otp_SMS(phone_number):
		otp = SendOtp.generate_otp()
		cache.set(phone_number, otp, 180)

	@staticmethod
	def send_otp_email(email):
		otp = SendOtp.generate_otp()
		cache.set(email, otp, 180)
		send_mail('Send OTP', f'OTP: {otp}', settings.EMAIL_HOST_USER, [email])
