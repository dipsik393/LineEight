from .models import Message
from inquiries.models import Inquiry


def notifications(request):

    new_messages = 0
    client_unread_messages = 0

    if request.user.is_authenticated:

        # ==========================================
        # STAFF
        # ==========================================

        if request.user.is_staff:

            # Website contact inquiries
            new_messages = Inquiry.objects.filter(
                status="new"
            ).count()

            # Client Portal messages sent by clients
            client_unread_messages = Message.objects.filter(
                is_read=False,
                sender__is_staff=False
            ).count()

        # ==========================================
        # CLIENT
        # ==========================================

        else:

            try:

                client = request.user.client_profile

                # Messages sent by Line Eight staff
                client_unread_messages = Message.objects.filter(
                    client=client,
                    is_read=False,
                    sender__is_staff=True
                ).count()

                new_messages = client_unread_messages

            except Exception:

                new_messages = 0
                client_unread_messages = 0

    return {
        "new_messages": new_messages,
        "client_unread_messages": client_unread_messages,
    }