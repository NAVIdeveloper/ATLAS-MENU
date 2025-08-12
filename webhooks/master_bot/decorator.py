from core.models import User
from partners.models import Branch

def is_staff(user_id):
    return Branch.objects.filter(telegram_id=user_id)

#decorator
def auth_staff(func):
    def wrapper(message,*args, **kwargs):
        branch = is_staff(message.from_user.id).select_related('language').first()
        if branch:
            return func(message,branch)
        return None
    return wrapper
