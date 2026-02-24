from django.conf import settings
from django.db import models


class Fruteira(models.Model):
    """Modelo para representar uma fruteira/loja."""
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, default="")
    endereco = models.CharField(max_length=500, blank=True, default="")
    telefone = models.CharField(max_length=20, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]
        verbose_name = "Fruteira"
        verbose_name_plural = "Fruteiras"


class Fruta(models.Model):
    """Modelo para representar tipos de frutas."""
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, default="")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(
        max_length=20,
        choices=[
            ("kg", "Quilograma"),
            ("un", "Unidade"),
            ("dz", "Dúzia"),
            ("cx", "Caixa"),
        ],
        default="kg"
    )
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.get_unidade_display()})"

    class Meta:
        ordering = ["nome"]
        verbose_name = "Fruta"
        verbose_name_plural = "Frutas"


class EstoqueItem(models.Model):
    """Modelo para representar itens de estoque com vencimento."""
    fruteira = models.ForeignKey(
        Fruteira,
        on_delete=models.CASCADE,
        related_name="estoques"
    )
    fruta = models.ForeignKey(
        Fruta,
        on_delete=models.CASCADE,
        related_name="estoques"
    )
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    data_entrada = models.DateField(auto_now_add=True)
    data_vencimento = models.DateField()
    lote = models.CharField(max_length=100, blank=True, default="")
    observacoes = models.TextField(blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def dias_para_vencer(self):
        """Retorna quantos dias faltam para vencer."""
        from datetime import date
        delta = self.data_vencimento - date.today()
        return delta.days

    def esta_vencido(self):
        """Verifica se o produto já venceu."""
        from datetime import date
        return self.data_vencimento < date.today()

    def __str__(self):
        return f"{self.fruta.nome} - {self.fruteira.nome} ({self.quantidade}{self.fruta.unidade})"

    class Meta:
        ordering = ["data_vencimento", "fruteira", "fruta"]
        verbose_name = "Item de Estoque"
        verbose_name_plural = "Itens de Estoque"
        indexes = [
            models.Index(fields=["fruteira", "data_vencimento"]),
            models.Index(fields=["fruta", "data_vencimento"]),
        ]
