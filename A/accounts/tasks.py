from celery import shared_task
from accounts.models import OtpCode
from datetime import datetime,timedelta
import pytz


@shared_task
def expire_otp_codes():
        expire_time = datetime.now(pytz.timezone('Asia/Tehran'))-timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expire_time).delete()