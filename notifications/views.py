from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user)
    # Mark all as read
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications/notifications_list.html', {
        'notifications': notifications,
    })