from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import EstoqueItemForm
from .models import EstoqueItem


@require_http_methods(["GET", "POST"])
def inventory_home(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = EstoqueItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item de estoque cadastrado com sucesso.")
            return redirect("inventory:home")
        messages.error(request, "Nao foi possivel salvar. Revise os campos do formulario.")
    else:
        form = EstoqueItemForm()

    itens_estoque = EstoqueItem.objects.select_related("fruteira", "fruta").all()
    sem_cadastros_base = not form.fields["fruteira"].queryset.exists() or not form.fields["fruta"].queryset.exists()

    return render(
        request,
        "inventory/home.html",
        {
            "form": form,
            "itens_estoque": itens_estoque,
            "sem_cadastros_base": sem_cadastros_base,
        },
    )
