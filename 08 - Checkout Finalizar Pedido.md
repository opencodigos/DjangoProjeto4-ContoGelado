##Checkout Finalizar Pedido

Agora vamos implementar um checkout simples para finalizar o pedido.

Primeiro precisamos fazer uma modificação no modelo Pedido.

```python
...
entrega = models.BooleanField(default=False)
endereco = models.TextField(null=True)

class Pagamento(models.TextChoices):
    CARTAO = 'CARTAO', 'Cartão'
    PIX = 'PIX', 'Pix'
    DINHEIRO = 'DINHEIRO', 'Dinheiro'
pagamento = models.CharField(max_length=100, choices=Pagamento.choices, null=True)
```

`python manage.py makemigrations && python manage.py migrate`

Depois disso no Pedido temos alguns campos auxiliares.

forms.py

```python
from django import forms
from .models import Pedido

class PedidoUpdateForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['endereco', 'pagamento']
        widgets = {
            'endereco': forms.Textarea(attrs={'cols': 30, 'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs): 
        super(PedidoUpdateForm, self).__init__(*args, **kwargs) 

        # Adiciona as class Bootstrap
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input form-control-sm'
            else:
                field.widget.attrs['class'] = 'form-control form-control-sm'
```

views.py

```python
@login_required(login_url="/admin/login/")
def checkout_pedido(request):
    pedido = Pedido.objects.filter(user=request.user, status=True).first()
    
    if request.method == 'POST':
        form = PedidoUpdateForm(request.POST, instance=pedido)
        if form.is_valid():
                        pedido = form.save(commit=False) 
            pedido.status = False
            pedido.save()
            messages.success(request, 'Pedido atualizado com sucesso!')
            return redirect('cardapio')
    else:
        form = PedidoUpdateForm(instance=pedido)

    return render(request, 'pedido.html', {'form': form, 'pedido': pedido})
```

`path('checkout-pedido/', views.checkout_pedido, name='checkout_pedido'),`

pedido.html

```python
{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %} 

<h2 class="pb-2 border-bottom">Meu Pedido: <span class="text-success fs-bold">N° {{pedido.id}}</span></h2>

<p>Revise seu pedido para finaliza-lo. Ao finalizar vamos abrir o whatsapp para confirmação de pagamento.</p>

<div class="d-flex">  
    
    <form class="p-2 flex-fill" method="post" action="{% if total_itens > 0 %}{% url 'checkout_pedido' %}{% endif %}">
        {% csrf_token %}
        <h4 class="mb-3 text-primary">Endereço de Entrega</h4> 
        <div class="d-flex gap-2">
            <input type="text" class="form-control form-control-sm" id="cep" name="cep" maxlength="8" placeholder="CEP: 00000-000">
            <input type="text" class="form-control form-control-sm" id="numero_casa" name="numero_casa" maxlength="8" placeholder="Número Casa">
        </div>
        {{form}}
        <button type="submit" class="btn btn-success mt-3">Finalizar Pedido</button>
    </form>

    <div class="p-2 flex-fill">
            
            <!-- Lista de Itens -->
            
    </div> 
</div>
{% endblock %}
```

Lista de Item que podemos utilizar é a mesma da sacola.

```python
    <ul class="list-group mb-3">
        <!-- Lista de Itens do Carrinho --> 
        {% for item in sacola_itens.potes.all %}
        <li class="list-group-item d-flex align-items-center 
            justify-content-between lh-sm pote-item" data-poteid="{{item.id}}">
            <div class="text-start list-item">
                <h6 class="my-0 text-dark fw-bold">Pote {{item.embalagem.tipo}} - R$ {{item.preco_total}} </h6>
                <p class="my-0">Sabores: {{item.obter_descricao_sabores}}</p>
                <p class="my-0">Coberturas: {{item.obter_descricao_coberturas|default:"Não"}}</p>				</div>  
            <div class="qty">
                <span class="minus sacola_minus bg-dark">-</span>
                <input type="number" class="dsb countCartItem_{{item.id}}" id="countCartItem_{{item.id}}" 
                    name="countCartItem" value="{{item.quantidade}}"> 
                <span class="plus sacola_plus bg-dark">+</span>
            </div> 
            <div class="div">
                <a href="#" class="link-danger remove-item"> <i class="fas fa-trash"></i></a>
            </div>
        </li>
        {% endfor %} 
        <li class="list-group-item d-flex align-items-center 
            justify-content-between p-3 text-success">
            <span>Total (R$)</span>
            <h2><strong id="atualizaValor">R$ {{sacola_itens.preco}}</strong></h2>
        </li>
</ul>
```

sacola podemos adicionar chamada

```python
<button type="button" class="btn btn-success btn-lg">
    <a href="{% if total_itens > 0 %}{% url 'checkout_pedido' %}{% endif %}" class="link-light text-decoration-none">
        Ir para checkout</a>
</button> 
```

navbar.html

```python
{% if request.path|slice:":18" == '/checkout-pedido/' %}
<div class="d-flex justify-content-between align-items-center">
    <a class="link-dark text-decoration-none" href="{% url 'inicio' %}"><i class="fas fa-arrow-left fa-2x"></i></a>
    <div>
        <img src="https://via.placeholder.com/200" alt="" width="150">
        <h2 class="link-dark text-decoration-none">Checkout</h2>
    </div>
</div>
{% else %}
{% include 'components/navbar.html' %}
{% endif %}
```

Agora vamos configurar uma api para buscar o CEP.

utilizar essa api: [`https://viacep.com.br/ws/](https://viacep.com.br/ws/)' + cep + '/json/`

```python
// Pagina Finalizar Pedido
    $("#cep").on('keyup', function () {
        var cep = $(this).val().replace(/\D/g, '');
        console.log(cep);
        
        if (cep.length === 8) {

            // Fazer a chamada AJAX para buscar o endereço com base no CEP
            $.ajax({
                url: 'https://viacep.com.br/ws/' + cep + '/json/',
                method: 'GET',
                success: function (data) { 
                    
                    var numero_casa = $("#numero_casa").val(); 

                    // Criar o endereço formatado
                    var enderecoFormatado = 'Rua: ' + data.logradouro + ', ' + 
                    'Bairro: ' + data.bairro + ', ' + 
                    'Cidade: ' + data.localidade + ', ' + 
                    'Estado: ' + data.uf + ', ' + 
                    'Número: ' + numero_casa;

                    // Preencher o campo de endereço
                    $("#id_endereco").val(enderecoFormatado);
                },
                error: function (error) {
                    console.log("Erro ao buscar CEP:", error);
                    alert("Erro ao buscar CEP. Verifique se o CEP é válido.");
                }
            });
        }
    });
```

Como podem perceber o numero nao vem, então precisamos adicionar 

```python
$("#numero_casa").on('blur', function () {
    var numero_casa = $(this).val().replace(/\D/g, '');
    var cep = $("#id_endereco").val();
    var enderecoFormatado = cep + ', ' +
    'Número: ' + numero_casa;
    $("#id_endereco").val(enderecoFormatado);
});
```

Melhora. 

Como vcs podem ver estamos utilizando a mesma lista de itens que tem na sacola certo ? 

Podemos simplificar isso compartilhando template unico.

**lista-itens.html**

```python
{% load static %}
<ul class="list-group mb-3">  
    <!-- Lista de Itens do Carrinho --> 
    {% for item in sacola_itens.potes.all %}
    <li class="list-group-item d-flex align-items-center 
        justify-content-between lh-sm pote-item" data-poteid="{{item.id}}">
        <div class="text-start list-item">
            <h6 class="my-0 text-dark fw-bold">Pote {{item.embalagem.tipo}} - R$ {{item.preco_total}} </h6>
            <p class="my-0">Sabores: {{item.obter_descricao_sabores}}</p>
            <p class="my-0">Coberturas: {{item.obter_descricao_coberturas|default:"Não"}}</p>				</div>  
        <div class="qty">
            <span class="minus sacola_minus bg-dark">-</span>
            <input type="number" class="dsb countCartItem_{{item.id}}" id="countCartItem_{{item.id}}" 
                name="countCartItem" value="{{item.quantidade}}"> 
            <span class="plus sacola_plus bg-dark">+</span>
        </div> 
        <div class="div">
            <a href="#" class="link-danger remove-item"> <i class="fas fa-trash"></i></a>
        </div>
    </li>
    {% endfor %} 
    <li class="list-group-item d-flex align-items-center 
        justify-content-between p-3 text-success">
        <span>Total (R$)</span>
        <h2><strong id="atualizaValor">R$ {{sacola_itens.preco}}</strong></h2>
    </li>
</ul>   
```

Faz include dele em sacola.html e pedido.html

```python
{% include 'components/lista-itens.html' %}
```

Fica bem melhor e mais organizado.