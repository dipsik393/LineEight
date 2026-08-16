from .tools import (
    get_clients,
    get_projects,
    get_inquiries,
    get_messages,
    get_dashboard_stats,
    get_my_projects,
    get_my_updates,
    get_my_files,
    get_my_messages,
)

from .intelligence import get_business_insights


def local_assistant(message, conversation=None):
    """
    Line Eight local assistant.

    This version does not require the OpenAI API.

    It can handle:
        - Dashboard statistics
        - Business summary
        - Business intelligence
        - Clients
        - Active clients
        - Inactive clients
        - Projects
        - Published projects
        - Draft projects
        - Inquiries
        - New inquiries
        - Messages
        - Unread messages
        - Basic conversation context
        - Help
    """

    # ==========================================================
    # CLEAN INPUT
    # ==========================================================

    message = (message or "").strip()

    if not message:
        return "Please enter a message."

    text = message.lower()


    # ==========================================================
    # LOAD CONVERSATION HISTORY
    # ==========================================================

    history = []

    if conversation:

        previous_messages = (
            conversation.messages
            .all()
            .order_by("created_at")
        )

        for item in previous_messages:

            history.append({
                "role": item.role,
                "content": item.content,
            })


    # ==========================================================
    # GREETINGS
    # ==========================================================

    greetings = [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ]

    if any(text.startswith(greeting) for greeting in greetings):

        return (
            "Hello! 👋\n\n"
            "I'm the Line Eight assistant. "
            "I can help you check clients, projects, "
            "inquiries, messages, dashboard statistics "
            "and business insights."
        )


    # ==========================================================
    # HELP
    # ==========================================================

    if (
        "help" in text
        or "what can you do" in text
        or "what do you do" in text
        or "commands" in text
        or "features" in text
    ):

        return (
            "I can currently help you with:\n\n"

            "• Clients\n"
            "• Active clients\n"
            "• Inactive clients\n"
            "• Projects\n"
            "• Published projects\n"
            "• Draft projects\n"
            "• Inquiries\n"
            "• New inquiries\n"
            "• Messages\n"
            "• Unread messages\n"
            "• Dashboard statistics\n"
            "• Business insights\n"
            "• Business summary\n\n"

            "Try asking:\n\n"

            "\"Show me my clients\"\n"
            "\"Show me active clients\"\n"
            "\"Show me my projects\"\n"
            "\"Show me published projects\"\n"
            "\"Show me new inquiries\"\n"
            "\"Show me unread messages\"\n"
            "\"What needs my attention?\"\n"
            "\"Analyze my business\"\n"
            "\"Give me a business summary\""
        )


    # ==========================================================
    # BUSINESS INTELLIGENCE
    # IMPORTANT: BEFORE GENERAL PROJECT/CLIENT/MESSAGE CHECKS
    # ==========================================================

    if (
        "what needs my attention" in text
        or "what needs attention" in text
        or "what should i do" in text
        or "what do i need to do" in text
        or "anything important" in text
        or "anything i should know" in text
        or "business insights" in text
        or "business insight" in text
        or "analyze the business" in text
        or "analyze my business" in text
        or "what is happening" in text
    ):

        intelligence = get_business_insights()

        insights = intelligence.get("insights", [])

        if not insights:

            return (
                "I couldn't find any business insights "
                "at the moment."
            )

        response = (
            "Here is what needs your attention:\n\n"
        )

        for insight in insights:

            title = insight.get(
                "title",
                "Attention item"
            )

            message_text = insight.get(
                "message",
                ""
            )

            priority = insight.get(
                "priority",
                "low"
            )

            response += (
                f"• {title}\n"
                f"  {message_text}\n"
                f"  Priority: "
                f"{str(priority).capitalize()}\n\n"
            )

        return response


    # ==========================================================
    # BUSINESS SUMMARY
    # ==========================================================

    if (
        "business summary" in text
        or "business report" in text
        or "give me a report" in text
        or "summarize the business" in text
        or "summarize my business" in text
        or "business overview" in text
    ):

        intelligence = get_business_insights()

        stats = intelligence.get(
            "stats",
            {}
        )

        insights = intelligence.get(
            "insights",
            []
        )

        response = (
            "Line Eight Business Summary\n\n"

            "CLIENTS\n"
            f"Total clients: "
            f"{stats.get('total_clients', 0)}\n"

            f"Active clients: "
            f"{stats.get('active_clients', 0)}\n"

            f"Inactive clients: "
            f"{stats.get('inactive_clients', 0)}\n\n"

            "PROJECTS\n"
            f"Total projects: "
            f"{stats.get('total_projects', 0)}\n"

            f"Published projects: "
            f"{stats.get('published_projects', 0)}\n"

            f"Draft projects: "
            f"{stats.get('draft_projects', 0)}\n\n"

            "INQUIRIES\n"
            f"Total inquiries: "
            f"{stats.get('total_inquiries', 0)}\n"

            f"New inquiries: "
            f"{stats.get('new_inquiries', 0)}\n\n"

            "COMMUNICATION\n"
            f"Unread messages: "
            f"{stats.get('unread_messages', 0)}\n\n"

            "FILES & UPDATES\n"
            f"Files: "
            f"{stats.get('total_files', 0)}\n"

            f"Project updates: "
            f"{stats.get('total_updates', 0)}\n\n"

            "ATTENTION ITEMS\n\n"
        )

        if insights:

            for insight in insights:

                title = insight.get(
                    "title",
                    "Attention item"
                )

                message_text = insight.get(
                    "message",
                    ""
                )

                priority = insight.get(
                    "priority",
                    "low"
                )

                response += (
                    f"• {title}\n"
                    f"  {message_text}\n"
                    f"  Priority: "
                    f"{str(priority).capitalize()}\n\n"
                )

        else:

            response += (
                "No major attention items were found."
            )

        return response


    # ==========================================================
    # DASHBOARD STATISTICS
    # ==========================================================

    if (
        "dashboard" in text
        or "statistics" in text
        or "stats" in text
        or "dashboard overview" in text
        or "dashboard statistics" in text
    ):

        stats = get_dashboard_stats()

        return (
            "Here is your Line Eight dashboard overview:\n\n"

            f"Clients: "
            f"{stats['total_clients']}\n"

            f"Active clients: "
            f"{stats['active_clients']}\n\n"

            f"Projects: "
            f"{stats['total_projects']}\n"

            f"Published projects: "
            f"{stats['published_projects']}\n"

            f"Draft projects: "
            f"{stats['draft_projects']}\n\n"

            f"Inquiries: "
            f"{stats['total_inquiries']}\n"

            f"New inquiries: "
            f"{stats['new_inquiries']}\n\n"

            f"Unread messages: "
            f"{stats['unread_messages']}\n"

            f"Files: "
            f"{stats['total_files']}\n"

            f"Project updates: "
            f"{stats['total_updates']}"
        )


    # ==========================================================
    # ACTIVE CLIENTS
    # ==========================================================

    if (
        "active client" in text
        or "active clients" in text
    ):

        clients = get_clients()

        active_clients = [
            client
            for client in clients
            if str(
                client.get("status", "")
            ).lower() == "active"
        ]

        if not active_clients:

            return (
                "There are currently no active clients."
            )

        response = "Active clients:\n\n"

        for client in active_clients:

            name = (
                client.get("name")
                or client.get("username")
                or "Unnamed client"
            )

            response += (
                f"• {name}\n"
                f"  Company: "
                f"{client.get('company') or 'N/A'}\n"
                f"  Email: "
                f"{client.get('email') or 'N/A'}\n"
                f"  Status: "
                f"{client.get('status') or 'Unknown'}\n\n"
            )

        return response


    # ==========================================================
    # INACTIVE CLIENTS
    # ==========================================================

    if (
        "inactive client" in text
        or "inactive clients" in text
    ):

        clients = get_clients()

        inactive_clients = [
            client
            for client in clients
            if str(
                client.get("status", "")
            ).lower() == "inactive"
        ]

        if not inactive_clients:

            return (
                "There are currently no inactive clients."
            )

        response = "Inactive clients:\n\n"

        for client in inactive_clients:

            name = (
                client.get("name")
                or client.get("username")
                or "Unnamed client"
            )

            response += (
                f"• {name}\n"
                f"  Company: "
                f"{client.get('company') or 'N/A'}\n"
                f"  Email: "
                f"{client.get('email') or 'N/A'}\n\n"
            )

        return response


    # ==========================================================
    # CLIENTS
    # ==========================================================

    if (
        "client" in text
        or "clients" in text
        or "customer" in text
        or "customers" in text
    ):

        clients = get_clients()

        if not clients:

            return (
                "There are currently no clients "
                "in the system."
            )

        response = "Here are your clients:\n\n"

        for client in clients:

            name = (
                client.get("name")
                or client.get("username")
                or "Unnamed client"
            )

            response += (
                f"• {name}\n"
                f"  Company: "
                f"{client.get('company') or 'N/A'}\n"
                f"  Email: "
                f"{client.get('email') or 'N/A'}\n"
                f"  Status: "
                f"{client.get('status') or 'Unknown'}\n\n"
            )

        return response


    # ==========================================================
    # PUBLISHED PROJECTS
    # ==========================================================

    if (
        "published project" in text
        or "published projects" in text
    ):

        projects = get_projects()

        published_projects = [
            project
            for project in projects
            if str(
                project.get("status", "")
            ).lower() == "published"
        ]

        if not published_projects:

            return (
                "There are currently no published projects."
            )

        response = "Published projects:\n\n"

        for project in published_projects:

            response += (
                f"• "
                f"{project.get('title', 'Untitled project')}\n"
                f"  Client: "
                f"{project.get('client') or 'N/A'}\n"
                f"  Service: "
                f"{project.get('service') or 'N/A'}\n"
                f"  Category: "
                f"{project.get('category') or 'N/A'}\n\n"
            )

        return response


    # ==========================================================
    # DRAFT PROJECTS
    # ==========================================================

    if (
        "draft project" in text
        or "draft projects" in text
    ):

        projects = get_projects()

        draft_projects = [
            project
            for project in projects
            if str(
                project.get("status", "")
            ).lower() == "draft"
        ]

        if not draft_projects:

            return (
                "There are currently no draft projects."
            )

        response = "Draft projects:\n\n"

        for project in draft_projects:

            response += (
                f"• "
                f"{project.get('title', 'Untitled project')}\n"
                f"  Client: "
                f"{project.get('client') or 'N/A'}\n"
                f"  Service: "
                f"{project.get('service') or 'N/A'}\n"
                f"  Category: "
                f"{project.get('category') or 'N/A'}\n\n"
            )

        return response


    # ==========================================================
    # PROJECTS
    # ==========================================================

    if (
        "project" in text
        or "projects" in text
    ):

        projects = get_projects()

        if not projects:

            return (
                "There are currently no projects "
                "in the system."
            )

        response = "Here are your projects:\n\n"

        for project in projects:

            title = (
                project.get("title")
                or "Untitled project"
            )

            client = (
                project.get("client")
                or "No client"
            )

            service = (
                project.get("service")
                or "N/A"
            )

            category = (
                project.get("category")
                or "N/A"
            )

            status = (
                project.get("status")
                or "Unknown"
            )

            response += (
                f"• {title}\n"
                f"  Client: {client}\n"
                f"  Service: {service}\n"
                f"  Category: {category}\n"
                f"  Status: {status}\n\n"
            )

        return response


    # ==========================================================
    # NEW INQUIRIES
    # ==========================================================

    if (
        "new inquiry" in text
        or "new inquiries" in text
        or "new lead" in text
        or "new leads" in text
    ):

        inquiries = get_inquiries()

        new_inquiries = [
            inquiry
            for inquiry in inquiries
            if str(
                inquiry.get("status", "")
            ).lower() in ["new", "pending"]
        ]

        if not new_inquiries:

            return (
                "There are currently no new inquiries."
            )

        response = "New inquiries:\n\n"

        for inquiry in new_inquiries:

            response += (
                f"• "
                f"{inquiry.get('name', 'Unknown')}\n"
                f"  Email: "
                f"{inquiry.get('email') or 'N/A'}\n"
                f"  Service: "
                f"{inquiry.get('service') or 'N/A'}\n"
                f"  Status: "
                f"{inquiry.get('status') or 'Unknown'}\n\n"
            )

        return response


    # ==========================================================
    # INQUIRIES
    # ==========================================================

    if (
        "inquiry" in text
        or "inquiries" in text
        or "contact request" in text
        or "contact requests" in text
        or "lead" in text
        or "leads" in text
    ):

        inquiries = get_inquiries()

        if not inquiries:

            return "There are currently no inquiries."

        response = "Here are your inquiries:\n\n"

        for inquiry in inquiries:

            response += (
                f"• "
                f"{inquiry.get('name', 'Unknown')}\n"
                f"  Email: "
                f"{inquiry.get('email') or 'N/A'}\n"
                f"  Service: "
                f"{inquiry.get('service') or 'N/A'}\n"
                f"  Status: "
                f"{inquiry.get('status') or 'Unknown'}\n\n"
            )

        return response


    # ==========================================================
    # UNREAD MESSAGES
    # IMPORTANT:
    # BEFORE GENERAL MESSAGE CHECK
    # ==========================================================

    if (
        "unread message" in text
        or "unread messages" in text
    ):

        messages = get_messages()

        unread_messages = [
            item
            for item in messages
            if not item.get("is_read")
        ]

        if not unread_messages:

            return (
                "You currently have no unread messages."
            )

        response = "Unread client messages:\n\n"

        for item in unread_messages[:10]:

            response += (
                f"• "
                f"{item.get('client', 'Unknown client')}\n"
                f"  Project: "
                f"{item.get('project', 'Unknown project')}\n"
                f"  Message: "
                f"{item.get('message', '')}\n"
                f"  Date: "
                f"{item.get('created_at', 'N/A')}\n\n"
            )

        return response


    # ==========================================================
    # GENERAL MESSAGES
    # ==========================================================

    if (
        "message" in text
        or "messages" in text
        or "chat" in text
        or "chats" in text
    ):

        messages = get_messages()

        if not messages:

            return (
                "There are currently no client messages."
            )

        response = "Recent client messages:\n\n"

        for item in messages[:10]:

            response += (
                f"• "
                f"{item.get('client', 'Unknown client')}"
                f" — "
                f"{item.get('project', 'Unknown project')}\n"
                f"  {item.get('message', '')}\n"
                f"  Read: "
                f"{'Yes' if item.get('is_read') else 'No'}\n"
                f"  Date: "
                f"{item.get('created_at', 'N/A')}\n\n"
            )

        return response


    # ==========================================================
    # PREVIOUS QUESTION
    # ==========================================================

    if (
        "what did i ask" in text
        or "previous question" in text
        or "previous message" in text
        or "what was i asking" in text
        or "what were we discussing" in text
    ):

        previous_user_messages = [
            item["content"]
            for item in history
            if item["role"] == "user"
        ]

        if not previous_user_messages:

            return (
                "This is the beginning of our conversation."
            )

        previous = previous_user_messages[-1]

        return (
            "Your previous message was:\n\n"
            f"\"{previous}\""
        )


    # ==========================================================
    # FOLLOW-UP QUESTIONS
    # ==========================================================

    if (
        text.startswith("what about")
        or text.startswith("which ones")
        or text.startswith("how about")
        or text in [
            "tell me more",
            "more",
            "and them",
            "and those",
        ]
    ):

        if history:

            previous_user_messages = [
                item["content"]
                for item in history
                if item["role"] == "user"
            ]

            if previous_user_messages:

                previous = previous_user_messages[-1]

                return (
                    "I understand this as a follow-up "
                    "to your previous request:\n\n"
                    f"\"{previous}\"\n\n"
                    "The local assistant can use this "
                    "conversation context, but deeper "
                    "reasoning will be added in the next "
                    "AI layer."
                )

        return (
            "I need a little more context. "
            "Tell me what you'd like me to look at."
        )


    # ==========================================================
    # UNKNOWN REQUEST
    # ==========================================================

    return (
        "I don't understand that request yet.\n\n"

        "You can ask me about:\n\n"

        "• Clients\n"
        "• Active clients\n"
        "• Inactive clients\n"
        "• Projects\n"
        "• Published projects\n"
        "• Draft projects\n"
        "• Inquiries\n"
        "• New inquiries\n"
        "• Messages\n"
        "• Unread messages\n"
        "• Dashboard statistics\n"
        "• Business insights\n"
        "• Business summary\n\n"

        "For example:\n\n"

        "\"Show me my clients\"\n"
        "\"Show me active clients\"\n"
        "\"Show me published projects\"\n"
        "\"Show me new inquiries\"\n"
        "\"Show me unread messages\"\n"
        "\"What needs my attention?\"\n"
        "\"Analyze my business\"\n"
        "\"Give me a business summary\""
    )



def client_assistant(message, client):
    """
    Local AI assistant for a specific client.

    Only returns information belonging
    to the logged-in client.
    """

    message = message.lower().strip()

    # ==========================================
    # PROJECTS
    # ==========================================

    if (
        "project" in message
        or "projects" in message
        or "work" in message
    ):

        projects = get_my_projects(client)

        if not projects:
            return "You currently don't have any projects."

        response = "Here are your projects:\n\n"

        for project in projects:

            response += (
                f"• {project['title']}\n"
                f"  Service: {project['service']}\n"
                f"  Industry: {project['industry']}\n"
                f"  Status: {project['status']}\n"
                f"  Started: {project['created_at']}\n\n"
            )

        return response


    # ==========================================
    # PROJECT UPDATES
    # ==========================================

    if (
        "update" in message
        or "updates" in message
        or "progress" in message
        or "latest" in message
    ):

        updates = get_my_updates(client)

        if not updates:
            return "There are currently no project updates."

        response = "Here are your latest project updates:\n\n"

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
    # FILES
    # ==========================================

    if (
        "file" in message
        or "files" in message
        or "document" in message
        or "documents" in message
    ):

        files = get_my_files(client)

        if not files:
            return "There are currently no files available for your projects."

        response = "Here are your project files:\n\n"

        for file in files:

            response += (
                f"• {file['name']}\n"
                f"  Project: {file['project']}\n"
                f"  {file['description'] or 'No description'}\n"
                f"  Added: {file['created_at']}\n\n"
            )

        return response


    # ==========================================
    # MESSAGES
    # ==========================================

    if (
        "message" in message
        or "messages" in message
        or "chat" in message
        or "communication" in message
    ):

        messages = get_my_messages(client)

        if not messages:
            return "You currently don't have any messages."

        response = "Your recent messages:\n\n"

        for item in messages[:10]:

            response += (
                f"• {item['project']}\n"
                f"  From: {item['sender']}\n"
                f"  {item['message']}\n"
                f"  {'Unread' if not item['is_read'] else 'Read'}\n"
                f"  {item['created_at']}\n\n"
            )

        return response


    # ==========================================
    # HELP
    # ==========================================

    if (
        "help" in message
        or "what can you do" in message
        or "commands" in message
    ):

        return (
            "I can help you with your Line Eight account.\n\n"

            "You can ask me about:\n\n"

            "• Your projects\n"
            "• Project updates\n"
            "• Project progress\n"
            "• Project files\n"
            "• Your messages\n\n"

            "For example:\n\n"

            "\"Show me my projects\"\n"
            "\"What is the latest update?\"\n"
            "\"Show me my files\"\n"
            "\"Do I have any messages?\""
        )


    # ==========================================
    # UNKNOWN REQUEST
    # ==========================================

    return (
        "I don't understand that request yet.\n\n"

        "Try asking me about:\n\n"

        "• Your projects\n"
        "• Project updates\n"
        "• Project files\n"
        "• Your messages\n\n"

        "For example:\n"
        "\"Show me my projects\""
    )