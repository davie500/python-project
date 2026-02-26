from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import EstoqueItemForm, FrutaForm
from .models import EstoqueItem, Fruta


@require_http_methods(["GET", "POST"])
def inventory_home(request: HttpRequest) -> HttpResponse:
    fruta_em_edicao = None
    fruta_id_edicao = request.GET.get("editar_fruta")
    if fruta_id_edicao:
        fruta_em_edicao = Fruta.objects.filter(id=fruta_id_edicao).first()

    fruta_form = FrutaForm(prefix="fruta", instance=fruta_em_edicao)
    estoque_form = EstoqueItemForm(prefix="estoque")

    if request.method == "POST":
        form_tipo = request.POST.get("form_tipo")
        if form_tipo == "fruta_salvar":
            fruta_id = request.POST.get("fruta_id")
            fruta_instance = Fruta.objects.filter(id=fruta_id).first() if fruta_id else None
            fruta_form = FrutaForm(request.POST, prefix="fruta", instance=fruta_instance)
            if fruta_form.is_valid():
                fruta_form.save()
                if fruta_instance:
                    messages.success(request, "Fruta atualizada com sucesso.")
                else:
                    messages.success(request, "Fruta cadastrada com sucesso.")
                return redirect("inventory:home")
            messages.error(request, "Nao foi possivel salvar a fruta. Revise os campos.")
        elif form_tipo == "fruta_remover":
            fruta_id = request.POST.get("fruta_id")
            fruta = get_object_or_404(Fruta, id=fruta_id)
            fruta.delete()
            messages.success(request, "Fruta removida com sucesso.")
            return redirect("inventory:home")
        else:
            estoque_form = EstoqueItemForm(request.POST, prefix="estoque")
            if estoque_form.is_valid():
                estoque_form.save()
                messages.success(request, "Item de estoque cadastrado com sucesso.")
                return redirect("inventory:home")
            messages.error(request, "Nao foi possivel salvar o item de estoque. Revise os campos.")

    itens_estoque = EstoqueItem.objects.select_related("fruteira", "fruta").all()
    frutas = Fruta.objects.order_by("nome")
    sem_fruteiras = not estoque_form.fields["fruteira"].queryset.exists()
    sem_frutas_ativas = not estoque_form.fields["fruta"].queryset.exists()

    return render(
        request,
        "inventory/home.html",
        {
            "fruta_form": fruta_form,
            "estoque_form": estoque_form,
            "fruta_em_edicao": fruta_em_edicao,
            "frutas": frutas,
            "itens_estoque": itens_estoque,
            "sem_fruteiras": sem_fruteiras,
            "sem_frutas_ativas": sem_frutas_ativas,
        },
    )
