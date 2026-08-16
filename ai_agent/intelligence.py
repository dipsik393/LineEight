from .tools import (
    get_clients,
    get_projects,
    get_inquiries,
    get_messages,
    get_dashboard_stats,
)


def get_business_insights():
    """
    Analyze Line Eight's current business data
    and return actionable insights.
    """

    clients = get_clients()
    projects = get_projects()
    inquiries = get_inquiries()
    messages = get_messages()
    stats = get_dashboard_stats()

    insights = []


    # ======================================================
    # CLIENT INSIGHTS
    # ======================================================

    inactive_clients = [
        client
        for client in clients
        if client.get("status") == "inactive"
    ]

    if inactive_clients:

        insights.append(
            {
                "type": "client",
                "priority": "medium",
                "title": "Inactive clients",
                "message": (
                    f"There are {len(inactive_clients)} "
                    "inactive clients that may need follow-up."
                ),
                "count": len(inactive_clients),
            }
        )


    # ======================================================
    # PROJECT INSIGHTS
    # ======================================================

    draft_projects = [
        project
        for project in projects
        if project.get("status") == "draft"
    ]

    if draft_projects:

        insights.append(
            {
                "type": "project",
                "priority": "medium",
                "title": "Draft projects",
                "message": (
                    f"There are {len(draft_projects)} "
                    "projects currently in draft status."
                ),
                "count": len(draft_projects),
            }
        )


    # ======================================================
    # MESSAGE INSIGHTS
    # ======================================================

    unread_messages = [
        message
        for message in messages
        if not message.get("is_read")
    ]

    if unread_messages:

        insights.append(
            {
                "type": "message",
                "priority": "high",
                "title": "Unread client messages",
                "message": (
                    f"You have {len(unread_messages)} "
                    "unread client messages."
                ),
                "count": len(unread_messages),
            }
        )


    # ======================================================
    # INQUIRY INSIGHTS
    # ======================================================

    new_inquiries = [
        inquiry
        for inquiry in inquiries
        if str(
            inquiry.get("status", "")
        ).lower() == "new"
    ]

    if new_inquiries:

        insights.append(
            {
                "type": "inquiry",
                "priority": "high",
                "title": "New inquiries",
                "message": (
                    f"There are {len(new_inquiries)} "
                    "new inquiries waiting for attention."
                ),
                "count": len(new_inquiries),
            }
        )


    # ======================================================
    # NO PROBLEMS
    # ======================================================

    if not insights:

        insights.append(
            {
                "type": "system",
                "priority": "low",
                "title": "Everything looks good",
                "message": (
                    "There are currently no major "
                    "items requiring attention."
                ),
                "count": 0,
            }
        )


    return {
        "stats": stats,
        "insights": insights,
    }