Vamos fazer alguns ajustes, depois que colocar itens na Sacola gostaria que informação fosse atualziada no campo “preco” automaticamente. 

```python
# Monta o Pote  
class MontaPote(models.Model):
    embalagem = models.ForeignKey(Embalagem, related_name='embalagem', on_delete=models.CASCADE, null=True)
    coberturas = models.ManyToManyField(Cobertura)
    quantidade = models.PositiveIntegerField(null=True)
    
    def preco_total(self):
        preco_embalagem = self.embalagem.preco if self.embalagem else 0
        preco_coberturas = sum(cobertura.preco for cobertura in self.coberturas.all())
        preco_sabores = 0
        for selsabor in self.pote.all():
            preco_sabor = selsabor.sabor.tipo.preco
            quantidade_bolas = selsabor.quantidade_bolas
            preco_sabores += preco_sabor * quantidade_bolas
        total_pote = preco_embalagem + preco_coberturas + preco_sabores
        total = total_pote * self.quantidade
        return total 

    def __str__(self):
        return f"ID: {self.id} / POTE: {self.embalagem.tipo} / Qtd: {self.quantidade} / {self.preco_total()}"

    class Meta:
        verbose_name = 'B - MontaPote'
        verbose_name_plural = 'B - MontaPote'
```

```python
# Sacolas de Itens
class SacolaItens(models.Model):
    potes = models.ManyToManyField(MontaPote)
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Armazena o valor como um número decimal
  
    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'  # Formata o valor com 2 casas decimais

    def preco_total(self):
        # Calcule a soma dos preços de todos os potes na sacola
        sacola_total = 0
        for pote in self.potes.all():
            sacola_total += pote.preco_total()
        self.preco = sacola_total
        self.save()
        return sacola_total
        
    def __str__(self):
        return f"CARINHO: {self.id} / {self.preco_total()}"

    class Meta:
        verbose_name = 'C - SacolaItens'
        verbose_name_plural = 'C - SacolaItens'
```