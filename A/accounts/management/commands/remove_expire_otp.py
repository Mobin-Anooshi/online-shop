from typing import Any
from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime,timedelta
import pytz


class Command(BaseCommand):
    help = 'remove all expire otp codes '
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        expire_time = datetime.now(pytz.timezone('Asia/Tehran'))-timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expire_time).delete()
        self.stdout.write(self.style.SUCCESS('success'))