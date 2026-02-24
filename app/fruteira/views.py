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


@require_http_methods(["GET", "POST"])
def fruteira_home(request: HttpRequest) -> HttpResponse:
    carrinho = request.session.get("fruteira_carrinho", {})

    if request.method == "POST":
        fruta_id = request.POST.get("fruta_id", "")
        acao = request.POST.get("acao", "adicionar")
        fruta_ids_validos = {fruta["id"] for fruta in FRUTAS}

        if fruta_id in fruta_ids_validos:
            qtd_atual = int(carrinho.get(fruta_id, 0))
            if acao == "remover":
                nova_qtd = max(0, qtd_atual - 1)
            else:
                nova_qtd = qtd_atual + 1

            if nova_qtd == 0:
                carrinho.pop(fruta_id, None)
            else:
                carrinho[fruta_id] = nova_qtd

            request.session["fruteira_carrinho"] = carrinho

        return redirect("fruteira:home")

    itens_carrinho = []
    total_itens = 0
    total = 0.0
    for fruta in FRUTAS:
        qtd = int(carrinho.get(fruta["id"], 0))
        total_itens += qtd
        subtotal = qtd * fruta["preco"]
        total += subtotal
        itens_carrinho.append(
            {
                "id": fruta["id"],
                "nome": fruta["nome"],
                "preco": fruta["preco"],
                "quantidade": qtd,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "fruteira/home.html",
        {
            "frutas": FRUTAS,
            "itens_carrinho": itens_carrinho,
            "total": total,
            "carrinho_vazio": total_itens == 0,
        },
    )
