from django.db import models

class Genoma(models.Model):
    id = models.AutoField(primary_key=True)
    sequencia = models.CharField(max_length=255)

    def __str__(self):
        return f"Genoma {self.id}: {self.sequencia}"


class Simulacao(models.Model):
    id = models.AutoField(primary_key=True)
    genes_pais = models.TextField(default="")
    numero_geracoes = models.PositiveIntegerField()
    resultado = models.TextField(blank=True, null=True)
    estatisticas = models.JSONField(blank=True, null=True)  # Salva estatísticas em JSON
    grafico_dados = models.JSONField(blank=True, null=True)  # Dados do gráfico
    heredograma_dados = models.JSONField(blank=True, null=True)  # Dados do heredograma
    data_criacao = models.DateTimeField(auto_now_add=True)


    genomas = models.ManyToManyField(Genoma)

    def __str__(self):
        return f"Simulação {self.id} - Gerações: {self.numero_geracoes}"
