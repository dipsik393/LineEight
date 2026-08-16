from .client_tools import (
    get_client_projects,
    get_client_updates,
    get_client_files,
    get_client_messages,
    get_client_overview,
)


def client_assistant(client, message, conversation=None):
    """
    Local AI assistant for clients.

    The assistant can only access information
    belonging to the currently logged-in client.
    """

    message = message.lower().strip()

    # ==========================================
    # HELP
    # ==========================================

    if (
        "help" in message
        or "what can you do" in message
        or "commands" in message
    ):
        return (
            "I can help you with:\n\n"
            "• Your projects\n"
            "• Project updates\n"
            "• Your files\n"
            "• Your messages\n"
            "• Your project overview\n\n"
            "You can also ask follow-up questions such as:\n\n"
            "\"Which project is active?\"\n"
            "\"When was it updated?\"\n"
            "\"Show me its files\"\n"
            "\"Who sent the latest message?\""
        )

    # ==========================================
    # GET DATA
    # ==========================================

    projects = get_client_projects(client)
    updates = get_client_updates(client)
    files = get_client_files(client)
    messages = get_client_messages(client)

    # ==========================================
    # OVERVIEW
    # ==========================================

    if (
        "overview" in message
        or "summary" in message
        or "status" in message
    ):

        overview = get_client_overview(client)

        return (
            f"Here is your Line Eight project overview:\n\n"
            f"Client: {overview['client']}\n"
            f"Company: {overview['company'] or 'N/A'}\n"
            f"Account status: {overview['status']}\n\n"
            f"Projects: {overview['projects']}\n"
            f"Updates: {overview['updates']}\n"
            f"Files: {overview['files']}\n"
            f"Messages: {overview['messages']}"
        )

    # ==========================================
    # ACTIVE PROJECT
    # ==========================================

    if (
        "active project" in message
        or "which project is active" in message
        or "what project is active" in message
        or "current project" in message
    ):

        active_projects = [
            project
            for project in projects
            if str(project.get("status", "")).lower()
            in ["active", "in progress", "ongoing"]
        ]

        if not active_projects:
            return "You currently have no active projects."

        response = "Your active project(s):\n\n"

        for project in active_projects:
            response += (
                f"• {project['title']}\n"
                f"  Service: {project['service']}\n"
                f"  Industry: {project['industry']}\n"
                f"  Status: {project['status']}\n"
                f"  Duration: {project['duration']}\n\n"
            )

        return response

    # ==========================================
    # PROJECTS
    # ==========================================

    if (
        "projects" in message
        or "my projects" in message
        or "show me my project" in message
        or "list my project" in message
    ):

        if not projects:
            return "You currently have no projects."

        response = "Here are your projects:\n\n"

        for project in projects:
            response += (
                f"• {project['title']}\n"
                f"  Service: {project['service']}\n"
                f"  Industry: {project['industry']}\n"
                f"  Status: {project['status']}\n"
                f"  Duration: {project['duration']}\n\n"
            )

        return response

    # ==========================================
    # LATEST UPDATE
    # ==========================================

    if (
        "when was it updated" in message
        or "when was it last updated" in message
        or "latest update" in message
        or "latest project update" in message
    ):

        if not updates:
            return "There are currently no project updates."

        latest = updates[0]

        return (
            "Your latest project update:\n\n"
            f"Project: {latest['project']}\n"
            f"Update: {latest['title']}\n"
            f"{latest['description']}\n"
            f"Status: {latest['status']}\n"
            f"Date: {latest['created_at']}"
        )

    # ==========================================
    # UPDATES
    # ==========================================

    if (
        "update" in message
        or "progress" in message
    ):

        if not updates:
            return "There are currently no project updates."

        response = "Your latest project updates:\n\n"

        for update in updates[:10]:
            response += (
                f"• {update['project']}\n"
                f"  {update['title']}\n"
                f"  {update['description']}\n"
                f"  Status: {update['status']}\n"
                f"  Date: {update['created_at']}\n\n"
            )

        return response

    # ==========================================
    # PROJECT FILES
    # ==========================================

    if (
        "show me its files" in message
        or "show its files" in message
        or "project files" in message
        or "my files" in message
        or "show me my files" in message
        or "file" in message
        or "download" in message
        or "document" in message
    ):

        if not files:
            return "You currently have no project files."

        response = "Your project files:\n\n"

        for file in files:
            response += (
                f"• {file['name']}\n"
                f"  Project: {file['project']}\n"
                f"  {file['description'] or 'No description'}\n"
                f"  Download: {file['url']}\n\n"
            )

        return response

    # ==========================================
    # LATEST MESSAGE
    # ==========================================

    if (
        "latest message" in message
        or "who sent the latest message" in message
        or "most recent message" in message
    ):

        if not messages:
            return "You currently have no messages."

        latest = messages[-1]

        return (
            "Your latest message:\n\n"
            f"Project: {latest['project']}\n"
            f"From: {latest['sender']}\n"
            f"Message: {latest['message']}\n"
            f"Date: {latest['created_at']}"
        )

    # ==========================================
    # MESSAGES
    # ==========================================

    if (
        "message" in message
        or "messages" in message
        or "conversation" in message
    ):

        if not messages:
            return "You currently have no messages."

        response = "Your recent messages:\n\n"

        for item in messages[-10:]:
            response += (
                f"• {item['project']}\n"
                f"  From: {item['sender']}\n"
                f"  {item['message']}\n"
                f"  Date: {item['created_at']}\n\n"
            )

        return response

    # ==========================================
    # UNKNOWN
    # ==========================================

    return (
        "I don't understand that request yet.\n\n"
        "You can ask me about:\n\n"
        "• Your projects\n"
        "• Active projects\n"
        "• Project updates\n"
        "• Your files\n"
        "• Your messages\n"
        "• Your project overview\n\n"
        "Try:\n"
        "\"Which project is active?\"\n"
        "\"When was it updated?\"\n"
        "\"Show me its files\"\n"
        "\"Who sent the latest message?\""
    )