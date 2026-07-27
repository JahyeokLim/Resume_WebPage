from .models import ContactMessage


def unread_inbox_count(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return {}
    return {'unread_inbox_count': ContactMessage.objects.filter(is_read=False).count()}
