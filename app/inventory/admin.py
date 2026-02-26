from django.contrib import admin
from .models import Fruteira, Fruta, EstoqueItem


@admin.register(Fruteira)
class FruteiraAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "email", "ativa", "atualizada_em")
    list_filter = ("ativa", "criada_em", "atualizada_em")
    search_fields = ("nome", "descricao", "telefone", "email")
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("nome", "descricao", "ativa")
        }),
        ("Contato", {
            "fields": ("endereco", "telefone", "email")
        }),
        ("Timestamps", {
            "fields": ("criada_em", "atualizada_em"),
            "classes": ("collapse",)
        }),
    )
    readonly_fields = ("criada_em", "atualizada_em")


@admin.register(Fruta)
class FrutaAdmin(admin.ModelAdmin):
    list_display = ("nome", "unidade", "preco_unitario", "ativa", "atualizada_em")
    list_filter = ("ativa", "unidade", "criada_em")
    search_fields = ("nome", "descricao")
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("nome", "descricao", "ativa")
        }),
        ("Preço e Medida", {
            "fields": ("preco_unitario", "unidade")
        }),
        ("Timestamps", {
            "fields": ("criada_em", "atualizada_em"),
            "classes": ("collapse",)
        }),
    )
    readonly_fields = ("criada_em", "atualizada_em")


@admin.register(EstoqueItem)
class EstoqueItemAdmin(admin.ModelAdmin):
    list_display = ("fruta", "fruteira", "quantidade", "data_vencimento", "dias_para_vencer_display", "status_vencimento")
    list_filter = ("fruteira", "fruta", "data_vencimento", "data_entrada")
    search_fields = ("fruta__nome", "fruteira__nome", "lote")
    fieldsets = (
        ("Produto e Fruteira", {
            "fields": ("fruta", "fruteira")
        }),
        ("Estoque", {
            "fields": ("quantidade", "lote", "observacoes")
        }),
        ("Datas", {
            "fields": ("data_entrada", "data_vencimento")
        }),
        ("Timestamps", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",)
        }),
    )
    readonly_fields = ("criado_em", "atualizado_em", "data_entrada")

    def dias_para_vencer_display(self, obj):
        return obj.data_vencimento.strftime("%d/%m/%y")
    dias_para_vencer_display.short_description = "Dias para Vencer"

    def status_vencimento(self, obj):
        if obj.esta_vencido():
            return '❌ Vencido'
        elif obj.dias_para_vencer() <= 7:
            return '⚠️ Vencendo'
        else:
            return '✅ Ok'
    status_vencimento.short_description = "Status"
