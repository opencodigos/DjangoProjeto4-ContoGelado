##Modelagem

Diagrama para entender mais ou menos a ideia do projeto. 

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/a063a051-4fb5-4b47-ad10-54cee14f4f39/27310de1-e17a-44db-83b5-072b0cdf1ef4/Untitled.png)

Podemos começar pelo backend. Vamos montrar os modelos… Depois nos preocupamos com layout e demais configurações. Acredito que pelo modelo podemos usar o django admin para simulação mais evidente. Certo, vamos lá…

**Modelo Embalagem.** 

Pensando no processo de comprar um sorvete. Podemos escolher o tamanho da embalagem que queremos. E o tamanho da embalagem tem que ter o valor correspondente. Não pode acontecer por exemplo: Cliente comprar 1L e pagar 10 reais e comprar 2L e pagar 10 reais.

Então temos que ter o controle de do valor da embalagem com base na capacdade maxima de bolas de sorvete.

**Ex: 1L com total de 6 Bolas**

**Ex: 2L com total de 12 Bolas**

**Ex: 400mL total de 4 bolas** 

E assim vai, varia de acordo com cada empresa de vcs.

```python
from django.db import models
from django.contrib.auth.models import User

# Tipo de Pote (1L - 1/5L - 2L - 400mL - 800mL )
class Embalagem(models.Model):
    tipo = models.CharField(max_length=50)
    capacidade_maxima_bolas = models.PositiveIntegerField()
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f'R$ {self.preco:.2f}' # Formata por ex R$ 23,30
    
    def __str__(self):
        return f'{self.tipo} | PREÇO: R$ {self.preco:.2f}'

    class Meta:
        verbose_name = '1 - Embalagem'
        verbose_name_plural = '1 - Embalagem'
```

**Tipo de Sabor** 

Defino o tipo se é tradicional, premium, sorbet (fruta) ou Açai. Lembrando que esse é tipo e não lista de Sabores. A ideia é diferenciar o valor. Tradicional e Premium são valores diferentes e podemos usar essa tabela para fazer essa diferença.

```jsx
# Tradicional / Premium / Sorbet / Açai
class TipoSabor(models.Model):
    tipo = models.CharField(max_length=100)
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'
    
    def __str__(self):
        return f'{self.tipo} | PREÇO: R$ {self.preco:.2f}'

    class Meta:
        verbose_name = '2 - TipoSabor'
        verbose_name_plural = '2 - TipoSabor'
```

**Sabor**

Lista de Sabores tem um relacionamento foreignkey com Tipo de Sabor. Isso significa que; O tipo Tradicional pode ter N* sabores. E esses sabores são definidos nessa tabela. Ai não tem controle de preço expecificamente, pois o valor é definido na tabela tipo de sabor, onde Tradicional é valor X que corresponde a todos os sabores relacionados. Assim fica mais facil.

```jsx
# Lista de Sabores
class Sabor(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.ForeignKey(TipoSabor, related_name='tipo_sabor', on_delete=models.CASCADE)
    ativo = models.BooleanField() 
    
    def __str__(self):
        return f'{self.nome} | PREÇO: R$ {self.tipo.preco:.2f}'

    class Meta:
        verbose_name = '3 - Sabor'
        verbose_name_plural = '3 - Sabor'
```

**Coberturas e Recheios**

Mesmo conceito dos anteriores. A cobertura/recheios são a parte e tem valor para ser cobrado.

Depois vamos usar essa tabela para relacionar com outras tabelas.

```jsx
# Coberturas Disponiveis
class Cobertura(models.Model):
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'
    
    def __str__(self):
        return f'{self.nome} | PREÇO: R$ {self.preco:.2f}'
    
    class Meta:
        verbose_name = '4 - Cobertura'
        verbose_name_plural = '4 - Cobertura' 
```

**Monta o Pote**

Esse modelo é onde montamos o pote. Imagina o processo como seria: Pegamos a embalagem, adicionamos os sorvetes e coberturas. Por fim a quantidade um, dois potes iguais. Lembrando que 1 pote pode conter varias bolas de sorvete, por isso temos um relacionamento na tabela SelSabor onde usamos uma foreingkey. Por fim a quantidade de bolas por exemplo, sabemos que 1L é 6 bolas então posso adicionar 3 bolas de morango e 3 de chocolate, por isso em SelSabor temos campo quantidade_bolas para sabermos a quantidade que será adicionada no pote.

```jsx
# Monta o Pote  
class MontaPote(models.Model):
    embalagem = models.ForeignKey(Embalagem, related_name='embalagem', on_delete=models.CASCADE, null=True)
    coberturas = models.ManyToManyField(Cobertura)
    quantidade = models.PositiveIntegerField(null=True) 

    def __str__(self):
        return f"ID: {self.id} / POTE: {self.embalagem.tipo} / Qtd: {self.quantidade}"

    class Meta:
        verbose_name = 'B - MontaPote'
        verbose_name_plural = 'B - MontaPote'
        
# Seleciona Sabores 
class SelSabor(models.Model):
    pote = models.ForeignKey(MontaPote, related_name='pote', on_delete=models.CASCADE, null=True)
    sabor = models.ForeignKey(Sabor, related_name='sabor', on_delete=models.CASCADE, null=True)
    quantidade_bolas = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Sabor: {self.sabor.nome}, Quantidade de Bolas: {self.quantidade_bolas}"
    
    class Meta:
        verbose_name = 'A - SelSabor'
        verbose_name_plural = 'A - SelSabor'
```

**Sacolas de Itens**

Sacola de itens podemos chamar de carinho. Por que é onde fica todos os potes que cliente montou e vai comprar. Por isso um campo ManyToManyField muitos para muitos. E campo preco para ver o valor total do carinho. Pensei em deixar esse campo preco como tratamento no frontend. Mas achei interessante deixar registrado na tabela.

```jsx
# Sacolas de Itens
class SacolaItens(models.Model):
    potes = models.ManyToManyField(MontaPote)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Armazena o valor como um número decimal
    
    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'  # Formata o valor com 2 casas decimais
    
    def __str__(self):
        return f"CARINHO: {self.id}"

    class Meta:
        verbose_name = 'C - SacolaItens'
        verbose_name_plural = 'C - SacolaItens'
```

**Pedido**

Montei algo simples de inicio mas no decorrer do curso será modificada. Essa tabela seria o status de tudo, temos ali uma relação com cliente que seria o User. Temos a lista de itens, data do pedido que está sendo efetuado, status e se está pago ou não. A ideia é partindo desse modelo fazemos o envio para finalizar no whatsapp talvez ? ou no sistema mesmo ai precisamos pensar num controle de demanda. Vamos ver no desenrolar o que acontece, o que for mais facil pra não complicar muito.

```jsx
# Registro do Pedido
class Pedido(models.Model):
    data_pedido = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, related_name='pedido_user', on_delete=models.PROTECT)
    itens_da_sacola = models.OneToOneField(SacolaItens, on_delete=models.CASCADE, null=True)    
    status = models.BooleanField()
    pago = models.BooleanField()
    # Endereço
    # Pagamento com Card / Dinheiro / Pix
    
    def __str__(self):
        return f"Pedido: {self.id} / {self.user} / (PAGO: {self.pago})"

    class Meta:
        verbose_name = 'D - Pedido'
        verbose_name_plural = 'D - Pedido'
```