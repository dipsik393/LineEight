from inquiries.models import Inquiry


def dashboard_notifications(request):

    return {

        "new_messages": Inquiry.objects.filter(
            status="new"
        ).count()

    }