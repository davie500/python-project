from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

FRUTAS = [
    {"id": "maca", "nome": "Maca", "preco": 4.50},
    {"id": "banana", "nome": "Banana", "preco": 3.20},
    {"id": "laranja", "nome": "Laranja", "preco": 5.00},
    {"id": "uva", "nome": "Uva", "preco": 9.90},
    {"id": "abacaxi", "nome": "Abacaxi", "preco": 7.50},
]
FRETE_FIXO = 8.0
FRETE_GRATIS_ACIMA_DE = 40.0
CUPONS = {
    "FRUTA10": 0.10,
    "VITAMINA15": 0.15,
}


@require_http_methods(["GET", "POST"])
def fruteira_home(request: HttpRequest) -> HttpResponse:
    carrinho = request.session.get("fruteira_carrinho", {})
    cupom_codigo = request.session.get("fruteira_cupom", "")
    feedback = ""

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
            else:
                request.session["fruteira_cupom"] = ""
                request.session["fruteira_feedback"] = "Cupom invalido."
            return redirect("fruteira:home")

        fruta_id = request.POST.get("fruta_id", "")
        fruta_ids_validos = {fruta["id"] for fruta in FRUTAS}
        if fruta_id in fruta_ids_validos:
            qtd_atual = int(carrinho.get(fruta_id, 0))

            if acao == "remover":
                nova_qtd = max(0, qtd_atual - 1)
            elif acao == "atualizar_qtd":
                try:
                    nova_qtd = int(request.POST.get("quantidade", "0"))
                except ValueError:
                    nova_qtd = qtd_atual
                nova_qtd = max(0, min(99, nova_qtd))
            else:
                nova_qtd = qtd_atual + 1

            if nova_qtd == 0:
                carrinho.pop(fruta_id, None)
            else:
                carrinho[fruta_id] = nova_qtd
            request.session["fruteira_carrinho"] = carrinho

        return redirect("fruteira:home")

    busca = request.GET.get("q", "").strip().lower()
    frutas_filtradas = [
        fruta for fruta in FRUTAS if busca in fruta["nome"].lower()
    ] if busca else FRUTAS

    itens_carrinho = []
    total_itens = 0
    subtotal = 0.0
    for fruta in FRUTAS:
        qtd = int(carrinho.get(fruta["id"], 0))
        total_itens += qtd
        subtotal = qtd * fruta["preco"]
        subtotal += subtotal
        itens_carrinho.append(
            {
                "id": fruta["id"],
                "nome": fruta["nome"],
                "preco": fruta["preco"],
                "quantidade": qtd,
                "subtotal": subtotal,
            }
        )

    desconto_percentual = CUPONS.get(cupom_codigo, 0.0)
    desconto = subtotal * desconto_percentual
    frete = 0.0 if subtotal >= FRETE_GRATIS_ACIMA_DE or total_itens == 0 else FRETE_FIXO
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
        },
    )
