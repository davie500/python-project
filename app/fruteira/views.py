from decimal import Decimal, ROUND_DOWN

from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from inventory.models import EstoqueItem, Fruteira

FRETE_FIXO = 8.0
FRETE_GRATIS_ACIMA_DE = 40.0
CUPONS = {
    "FRUTA10": 0.10,
    "VITAMINA15": 0.15,
}
FRETE_GRATIS_CUPONS = {"FRETEGRATIS", "ENTREGAZERO"}


@require_http_methods(["GET", "POST"])
def fruteira_home(request: HttpRequest) -> HttpResponse:
    carrinho = request.session.get("fruteira_carrinho", {})
    cupom_codigo = request.session.get("fruteira_cupom", "")
    estoque_disponivel = {}
    frutas_disponiveis = []
    fruteiras_ativas = list(Fruteira.objects.filter(ativa=True).order_by("nome"))

    fruteira_ativa = fruteiras_ativas[0] if fruteiras_ativas else None
    fruteira_id_sessao = request.session.get("fruteira_ativa_id")
    if fruteira_id_sessao:
        fruteira_ativa = next((f for f in fruteiras_ativas if f.id == fruteira_id_sessao), fruteira_ativa)

    if fruteira_ativa:
        hoje = timezone.localdate()
        estoque_por_fruta = (
            EstoqueItem.objects
            .filter(
                fruteira=fruteira_ativa,
                fruta__ativa=True,
                data_vencimento__gte=hoje,
                quantidade__gt=0,
            )
            .values("fruta_id", "fruta__nome", "fruta__preco_unitario")
            .annotate(quantidade_disponivel=Sum("quantidade"))
            .order_by("fruta__nome")
        )

        for row in estoque_por_fruta:
            fruta_id = str(row["fruta_id"])
            qtd_decimal = row["quantidade_disponivel"] or Decimal("0")
            qtd_carrinho_max = int(qtd_decimal.quantize(Decimal("1"), rounding=ROUND_DOWN))
            if qtd_carrinho_max <= 0:
                continue
            estoque_disponivel[fruta_id] = qtd_carrinho_max
            frutas_disponiveis.append(
                {
                    "id": fruta_id,
                    "nome": row["fruta__nome"],
                    "preco": float(row["fruta__preco_unitario"]),
                    "estoque": qtd_carrinho_max,
                }
            )

    request.session["fruteira_ativa_id"] = fruteira_ativa.id if fruteira_ativa else None

    if request.method == "POST":
        acao = request.POST.get("acao", "")

        if acao == "limpar":
            request.session["fruteira_carrinho"] = {}
            request.session["fruteira_cupom"] = ""
            request.session["fruteira_feedback"] = "Carrinho limpo."
            return redirect("fruteira:home")

        if acao == "aplicar_cupom":
            codigo = request.POST.get("cupom_codigo", "").strip().upper()
            if codigo in CUPONS:
                request.session["fruteira_cupom"] = codigo
                request.session["fruteira_feedback"] = f"Cupom {codigo} aplicado."
            elif codigo in FRETE_GRATIS_CUPONS:
                request.session["fruteira_cupom"] = codigo
                request.session["fruteira_feedback"] = f"Cupom {codigo} aplicado para frete gratis."
            else:
                request.session["fruteira_cupom"] = ""
                request.session["fruteira_feedback"] = "Cupom invalido."
            return redirect("fruteira:home")

        fruta_id = request.POST.get("fruta_id", "")
        if fruta_id in estoque_disponivel:
            qtd_atual = int(carrinho.get(fruta_id, 0))
            qtd_limite = min(99, estoque_disponivel[fruta_id])

            if acao == "remover":
                nova_qtd = max(0, qtd_atual - 1)
            elif acao == "atualizar_qtd":
                try:
                    nova_qtd = int(request.POST.get("quantidade", "0"))
                except ValueError:
                    nova_qtd = qtd_atual
                nova_qtd = max(0, min(qtd_limite, nova_qtd))
            else:
                nova_qtd = min(qtd_limite, qtd_atual + 1)

            if nova_qtd == 0:
                carrinho.pop(fruta_id, None)
            else:
                carrinho[fruta_id] = nova_qtd
            request.session["fruteira_carrinho"] = carrinho

        return redirect("fruteira:home")

    busca = request.GET.get("q", "").strip().lower()
    frutas_filtradas = [
        fruta for fruta in frutas_disponiveis if busca in fruta["nome"].lower()
    ] if busca else frutas_disponiveis

    itens_carrinho = []
    total_itens = 0
    subtotal = 0.0
    for fruta in frutas_disponiveis:
        qtd = int(carrinho.get(fruta["id"], 0))
        qtd = min(qtd, estoque_disponivel.get(fruta["id"], 0))
        if qtd != int(carrinho.get(fruta["id"], 0)):
            carrinho[fruta["id"]] = qtd
        total_itens += qtd
        subtotal_item = qtd * fruta["preco"]
        subtotal += subtotal_item
        itens_carrinho.append(
            {
                "id": fruta["id"],
                "nome": fruta["nome"],
                "preco": fruta["preco"],
                "quantidade": qtd,
                "subtotal": subtotal_item,
            }
        )

    frutas_ids_validas = {fruta["id"] for fruta in frutas_disponiveis}
    for fruta_id in list(carrinho.keys()):
        if fruta_id not in frutas_ids_validas:
            carrinho.pop(fruta_id, None)
    request.session["fruteira_carrinho"] = carrinho

    desconto_percentual = CUPONS.get(cupom_codigo, 0.0)
    desconto = subtotal * desconto_percentual
    frete_gratis_por_cupom = cupom_codigo in FRETE_GRATIS_CUPONS
    frete = 0.0 if subtotal >= FRETE_GRATIS_ACIMA_DE or total_itens == 0 or frete_gratis_por_cupom else FRETE_FIXO
    total = subtotal - desconto + frete
    feedback = request.session.pop("fruteira_feedback", "")

    return render(
        request,
        "fruteira/home.html",
        {
            "frutas": frutas_filtradas,
            "itens_carrinho": itens_carrinho,
            "subtotal": subtotal,
            "desconto": desconto,
            "desconto_percentual": int(desconto_percentual * 100),
            "cupom_codigo": cupom_codigo,
            "frete": frete,
            "total": total,
            "carrinho_vazio": total_itens == 0,
            "q": request.GET.get("q", ""),
            "feedback": feedback,
            "meta_frete_gratis": FRETE_GRATIS_ACIMA_DE,
            "fruteira_ativa": fruteira_ativa,
            "estoque_por_fruta": frutas_disponiveis,
            "frete_gratis_por_cupom": frete_gratis_por_cupom,
        },
    )
