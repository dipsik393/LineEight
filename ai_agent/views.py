from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .models import AIConversation, AIMessage
from .services import local_assistant

from clients.models import Client
from .client_services import client_assistant

@staff_member_required
def ai_assistant(request, conversation_id=None):

    # -----------------------------------
    # GET SELECTED CONVERSATION
    # -----------------------------------

    if conversation_id:

        conversation = get_object_or_404(
            AIConversation,
            id=conversation_id,
            user=request.user
        )

    else:

        conversation = (
            AIConversation.objects
            .filter(user=request.user)
            .first()
        )

        if not conversation:

            conversation = AIConversation.objects.create(
                user=request.user,
                title="New Conversation"
            )

    # -----------------------------------
    # HANDLE MESSAGE
    # -----------------------------------

    if request.method == "POST":

        question = request.POST.get("message", "").strip()

        if question:

            # Save user message

            AIMessage.objects.create(
                conversation=conversation,
                role="user",
                content=question
            )

            # Generate response

            response = local_assistant(question, conversation)

            # Save assistant response

            AIMessage.objects.create(
                conversation=conversation,
                role="assistant",
                content=response
            )

            # Set conversation title

            if conversation.title == "New Conversation":

                conversation.title = question[:60]

                conversation.save()

            return redirect(
                "ai_conversation",
                conversation_id=conversation.id
            )

    # -----------------------------------
    # ALL USER CONVERSATIONS
    # -----------------------------------

    conversations = (
        AIConversation.objects
        .filter(user=request.user)
        .order_by("-updated_at")
    )

    messages = conversation.messages.all()

    return render(
        request,
        "dashboard/ai/assistant.html",
        {
            "conversation": conversation,
            "conversations": conversations,
            "messages": messages,
        }
    )


# ==========================================
# NEW CONVERSATION
# ==========================================

@staff_member_required
def new_conversation(request):

    conversation = AIConversation.objects.create(
        user=request.user,
        title="New Conversation"
    )

    return redirect(
        "ai_conversation",
        conversation_id=conversation.id
    )


# ==========================================
# DELETE CONVERSATION
# ==========================================

@staff_member_required
def delete_conversation(request, conversation_id):

    conversation = get_object_or_404(
        AIConversation,
        id=conversation_id,
        user=request.user
    )

    conversation.delete()

    return redirect("ai_assistant")



@login_required
def client_ai(request, conversation_id=None):

    client = get_object_or_404(
        Client,
        user=request.user
    )

    # -----------------------------------------
    # GET CONVERSATION
    # -----------------------------------------

    if conversation_id:

        conversation = get_object_or_404(
            AIConversation,
            id=conversation_id,
            user=request.user
        )

    else:

        conversation = (
            AIConversation.objects
            .filter(user=request.user)
            .order_by("-updated_at")
            .first()
        )

        if not conversation:

            conversation = AIConversation.objects.create(
                user=request.user,
                title="New Conversation"
            )

    # -----------------------------------------
    # HANDLE MESSAGE
    # -----------------------------------------

    if request.method == "POST":

        question = request.POST.get(
            "message",
            ""
        ).strip()

        if question:

            AIMessage.objects.create(
                conversation=conversation,
                role="user",
                content=question
            )

            response = client_assistant(
                client,
                question,
                conversation
            )

            AIMessage.objects.create(
                conversation=conversation,
                role="assistant",
                content=response
            )

            if conversation.title == "New Conversation":

                conversation.title = question[:50]
                conversation.save()

            return redirect(
                "client_ai_conversation",
                conversation_id=conversation.id
            )

    # -----------------------------------------
    # CLIENT CONVERSATIONS
    # -----------------------------------------

    conversations = (
        AIConversation.objects
        .filter(user=request.user)
        .order_by("-updated_at")
    )

    messages = conversation.messages.all()

    return render(
        request,
        "clients/ai/assistant.html",
        {
            "client": client,
            "conversation": conversation,
            "conversations": conversations,
            "messages": messages,
        }
    )


@login_required
def client_new_conversation(request):

    client = get_object_or_404(
        Client,
        user=request.user
    )

    conversation = AIConversation.objects.create(
        user=request.user,
        title="New Conversation"
    )

    return redirect(
        "client_ai_conversation",
        conversation_id=conversation.id
    )