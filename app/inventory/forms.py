from django import forms
from django.utils import timezone

from .models import EstoqueItem, Fruta, Fruteira


class FrutaForm(forms.ModelForm):
    class Meta:
        model = Fruta
        fields = ["nome", "descricao", "preco_unitario", "unidade", "ativa"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3, "placeholder": "Descricao opcional"}),
            "preco_unitario": forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
        }

    def clean_preco_unitario(self):
        preco_unitario = self.cleaned_data["preco_unitario"]
        if preco_unitario <= 0:
            raise forms.ValidationError("O preco unitario deve ser maior que zero.")
        return preco_unitario


class EstoqueItemForm(forms.ModelForm):
    class Meta:
        model = EstoqueItem
        fields = ["fruteira", "fruta", "quantidade", "data_vencimento", "observacoes"]
        widgets = {
            "data_vencimento": forms.DateInput(attrs={"type": "date"}),
            "quantidade": forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
            "observacoes": forms.Textarea(attrs={"rows": 3, "placeholder": "Observacoes opcionais"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fruteira"].queryset = Fruteira.objects.filter(ativa=True).order_by("nome")
        self.fields["fruta"].queryset = Fruta.objects.filter(ativa=True).order_by("nome")

    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        if quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantidade

    def clean_data_vencimento(self):
        data_vencimento = self.cleaned_data["data_vencimento"]
        if data_vencimento < timezone.localdate():
            raise forms.ValidationError("A data de vencimento nao pode estar no passado.")
        return data_vencimento
