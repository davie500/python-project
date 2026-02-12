from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ConversationCreateForm, MessageCreateForm
from .models import Conversation, Message


@login_required
def conversation_list(request: HttpRequest) -> HttpResponse:
    conversations = Conversation.objects.filter(user=request.user).only(
        "id", "title", "updated_at", "created_at"
    )
    return render(
        request,
        "chat/conversation_list.html",
        {"conversations": conversations, "create_form": ConversationCreateForm()},
    )


@login_required
@require_POST
def conversation_create(request: HttpRequest) -> HttpResponse:
    form = ConversationCreateForm(request.POST)
    if form.is_valid():
        conversation = form.save(commit=False)
        conversation.user = request.user
        if not conversation.title.strip():
            conversation.title = "Nova conversa"
        conversation.save()
        return redirect("chat:conversation_detail", conversation_id=conversation.id)
    conversations = Conversation.objects.filter(user=request.user).only(
        "id", "title", "updated_at", "created_at"
    )
    return render(
        request,
        "chat/conversation_list.html",
        {"conversations": conversations, "create_form": form},
        status=400,
    )


@login_required
def conversation_detail(request: HttpRequest, conversation_id: int) -> HttpResponse:
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    messages = conversation.messages.all().only("id", "role", "content", "created_at")
    return render(
        request,
        "chat/conversation_detail.html",
        {
            "conversation": conversation,
            "messages": messages,
            "message_form": MessageCreateForm(),
        },
    )


@login_required
@require_POST
def message_create(request: HttpRequest, conversation_id: int) -> HttpResponse:
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    form = MessageCreateForm(request.POST)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.conversation = conversation
        msg.role = Message.Role.USER
        msg.save()
        return redirect("chat:conversation_detail", conversation_id=conversation.id)

    messages = conversation.messages.all().only("id", "role", "content", "created_at")
    return render(
        request,
        "chat/conversation_detail.html",
        {"conversation": conversation, "messages": messages, "message_form": form},
        status=400,
    )

