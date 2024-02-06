from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta


def set_period():
    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    next_try = now + timedelta(minutes=1)
    return next_try
