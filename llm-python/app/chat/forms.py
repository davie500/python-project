from django import forms

from .models import Conversation, Message


class ConversationCreateForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Título (opcional)"}
            )
        }


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Digite sua mensagem...",
                }
            )
        }

