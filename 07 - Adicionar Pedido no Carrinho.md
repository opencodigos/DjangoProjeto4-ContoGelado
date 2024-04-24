##Adicionar Pedido no Carrinho

Agora vamos adicionar pedido no carrinho quantos o usuário selecionar.

Como vocês podem perceber o catálogo é open para qualquer usuário ver. Até os que não estão autenticados. Mas para adicionar no carrinho vamos obrigar o usuário está logado, fazendo a validação e redirecionamento.

No template, sabores.html podemos adicionar uma validação assim ou depois podemos fazer o tratamento na view adicionando **`@login_required(login_url="/admin/login/")`**

```html
{% if request.user.is_authenticated %}
<button type="button" class="btn btn-primary btn-lg">Adicionar</button> 
{% else %} 
<a class="btn btn-dark btn-lg" href="/admin/login">Faça o Login</a>
{% endif %}
```

Quanto usuário está autenticado ele pode adicionar os itens no carrinho. No modelo **SacolaItens** podemos ver o tipos de informações que precisamos enviar. Então pensei numa lista de objetos. 

***embalagem_id** = Identificador do tipo de embalagem.
**sabores_selecionados** = Lista de todos os sabores que usuário selecionou.
**cobertura_selecionadas** = Lista de Adicionais/Coberturas que usuário selecionou.
**quantidade_pote** = Quantidade do pote montado que usuário selecionou.*

Tendo essas informações passamos para views e fica mais facil de fazer o tratamento e salvar na tabela **SacolaItens**, certo ? 

```html
var dados = {
    'embalagem_id': modalId,
    'sabores_selecionados': saboresSelecionados,
    'cobertura_selecionadas': coberturaSelecionadas,
    'quantidade_pote': quantidade_pote
};
```

**Vou criar a view que vai receber esses dados.**

```html
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url="/admin/login/")
def adicionar_sacola(request):
    if request.method == "POST": 
        try: 
            dados_str = request.POST.get('dados', None)
            dados = json.loads(dados_str) 
            print(dados) 
            return JsonResponse({'status': 'success', 
                                    'message': 'Item adicionado na sacola com sucesso.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Requisição inválida.'})
```

No template sabores.html vamos ter um evento de click para enviar itens para sacola.

Para evento de click criei uma class auxiliar no template sabores.html

```html
<button type="button" class="btn btn-primary btn-lg btnEnviarSacola">
    Adicionar</button>
```

cardapio.html

```html
// Coleta itens para sacola.
$('.btnEnviarSacola').click(function () {
    // Obter o modalId do atributo data-modalid
    var modalId = $(this).closest('.modal').data('modalid');
        
    var saboresSelecionados = atualizarTotalSelecionado(modalId);

    var coberturaSelecionadas = selCobertura(modalId);

    var quantidade_pote = parseInt($('.qtdPote_' + modalId).val()) || 1;

    var dados = {
        'embalagem_id': modalId,
        'sabores_selecionados': saboresSelecionados,
        'cobertura_selecionadas': coberturaSelecionadas,
        'quantidade_pote': quantidade_pote
    };
    console.log(dados);
        
});
```

**atualizarTotalSelecionado**

```html
function atualizarTotalSelecionado(modalId) {
    var totalSelecionado = 0;
    var saboresSelecionados = [];

    $('.count_'+modalId).each(function() {
        totalSelecionado += parseInt($(this).val());
        
        var saborId = $(this).data('saborid');
        var quantidade = parseInt($(this).val());
        
        if (quantidade > 0) {
            saboresSelecionados.push({
                'sabor_id': saborId,
                'quantidade': quantidade
            });
        } 

    });
    $('#resultselsabor_' + modalId).text(totalSelecionado);
    
    console.log(saboresSelecionados);
    return saboresSelecionados;
}
```

**selCobertura**

```html
function selCobertura(modalId) {
    var selCobertura= [];
    $('.selcobertura_' + modalId).each(function () {
        var coberturaid = $(this).data('coberturaid');
        var quantidade = parseInt($(this).val());
        if (quantidade > 0) {
            selCobertura.push({
                'cobertura_id': coberturaid,
                'quantidade': quantidade
            });
        }
    });
    console.log(selCobertura);
    return selCobertura;
}
```

Atualiza no evento de click para selecionar coberturas.

```html
// Coberturas/Adicionais 
$(document).on('click', '.plus', function(){ 
    ...
    selCobertura(modalId)
});
$(document).on('click', '.minus', function(){
    ...
    selCobertura(modalId)
});
```

Certo, Agora vamos passar esses dados para view utilizando Ajax. 

```python
// Faça uma solicitação AJAX para a view Django
    $.ajax({
        type: 'POST',
        url: "{% url 'adicionar_sacola' %}",  // Substitua pela URL correta
        data: {
            'dados': JSON.stringify(dados),
            'csrfmiddlewaretoken': '{{ csrf_token }}'  // Token CSRF
        },
        dataType: 'json', 
        success: function (response) {
            console.log(response);
        },
        error: function (xhr, status, error) {
            console.error('Erro na solicitação AJAX:', error);
        }
    }); 
```

Com os dados da requisição em nossa views vamos começar o tratamento. Primeiro vamos obter o carrinho existente do usuário, se carrinho não existir vamos precisar criar. O carrinho só não vai exitir quando é a primeira vez que usuário adiciona o item. Depois vamos criar Pote, adicionar sabores e cobertura conforme codigo abaixo.

```python
embalagem_id = dados.get('embalagem_id', None)
quantidade_pote = int(dados.get('quantidade_pote', None))

# Tente obter a sacola existente do usuário
pedido = Pedido.objects.filter(user=request.user, status=True).first()

# Se não existir uma sacola, crie uma nova
if not pedido: 
    # Crie um novo pedido e associe a sacola criada
    pedido = Pedido.objects.create(user=request.user, 
                                    itens_da_sacola=SacolaItens.objects.create())

monta_pote = MontaPote.objects.create(
    embalagem_id=embalagem_id, quantidade=quantidade_pote)

for sabor in dados['sabores_selecionados']:
    SelSabor.objects.create(pote=monta_pote, 
                            sabor_id=sabor['sabor_id'], 
                            quantidade_bolas=sabor['quantidade'])  

pedido.itens_da_sacola.potes.add(monta_pote)
pedido.itens_da_sacola.preco_total()
```

Legal, como vocês podem ver conseguimos criar um carrinho com as informaçõe passadas para views. Mas não está salvando os adicionais/coberturas. No começo do video comentei que não ia mais modificar os modelos. Realmente estava com uma ideia que no desenvolvimento achei que fica melhor o usuario ter a liberdade de selecionar quantas coberturas ele quiser comprar.

**Por exemplo**, podemos expecificar quantas colcha, colher a quantidade de adicionais/coberturas podemos colocar. Isso seria interessante. 

**Então vamos fazer essa modificação:**

models.py

```python
class SelCobertura(models.Model):
    pote = models.ForeignKey(MontaPote, 
                                related_name='pote_cobertura', 
                                on_delete=models.CASCADE, null=True) 
    cobertura = models.ForeignKey(Cobertura,
                                    related_name='cobertura', 
                                    on_delete=models.CASCADE, null=True)
    quantidade_cobertura = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Cobertura: {self.cobertura.nome}, Quantidade: {self.quantidade_cobertura}"
    
    class Meta:
        verbose_name = 'A - SelCobertura'
        verbose_name_plural = 'A - SelCobertura'
```

Atualiza o contador do preço do pote para contar todas as coberturas

```python
class MontaPote(models.Model):
    embalagem = models.ForeignKey(Embalagem, 
                                    related_name='embalagem', 
                                    on_delete=models.CASCADE, null=True)
    # coberturas = models.ManyToManyField(Cobertura)
    quantidade = models.PositiveIntegerField(null=True) 

    def preco_total(self):
        preco_embalagem = self.embalagem.preco if self.embalagem else 0 
        preco_sabores = 0
        preco_coberturas = 0
        for selsabor in self.pote.all(): 
            preco_sabor = selsabor.sabor.tipo.preco
            quantidade_bolas = selsabor.quantidade_bolas
            preco_sabores += preco_sabor * quantidade_bolas 
            
        for selcobertura in self.pote_cobertura.all():
            preco_cobertura = selcobertura.cobertura.preco
            quantidade_cobertura = selcobertura.quantidade_cobertura
            preco_coberturas += preco_cobertura * quantidade_cobertura
                        ...
```

Rodamos: `python manage.py makemigrations && python manage.py migrate`

Para visualizar no admin

```html
class SelCoberturaInline(admin.TabularInline):
    model = SelCobertura
    extra = 0

class SelSaborInline(admin.TabularInline):
    model = SelSabor
    extra = 0

@admin.register(MontaPote)
class MontaPoteAdmin(admin.ModelAdmin):
    inlines = [
        SelSaborInline,
        SelCoberturaInline
    ] 
```

quando adicionamos uma cobertura/adicionais nos dados do objeto vem assim: 

{cobertura_id: 2, quantidade: 2} vamos na views fazer o tratamento.

```python
for cobertura in dados['cobertura_selecionadas']:
    # Adicione a cobertura ao pote durante a criação
    SelCobertura.objects.create(pote=monta_pote, 
                            cobertura_id=cobertura['cobertura_id'], 
                            quantidade_cobertura=cobertura['quantidade'])
```

Agora vamos fazer tratamento no template para visualizar essas informações. 
Como o icone do carrinho está na navbar eu estou fazendo com que esse icone seja exibido em todas as paginas, vamos fazer tratamento de maneira global. Portando vamos criar nossa função no arquivo **context_processors.py**

```python
def context_sacola(request):
    if request.user.is_authenticated:
        # Recupere o pedido do usuário com status True (Ativo)
        pedidos = Pedido.objects.filter(user=request.user, status=True)

        # Inicialize a variável total_itens
        total_itens = 0

        # Itere sobre para contar o número total de itens em todas as sacolas
        for pedido in pedidos:
            total_itens += pedido.itens_da_sacola.potes.count()

        # Recupere o ID da primeira sacola se existir
        sacola = pedidos.first().itens_da_sacola if pedidos else None
    
        # Retorne os resultados
        return {
            'sacola_itens': sacola,
            'total_itens': total_itens
        }
    else:
        return {}
```

```html
'core.context_processors.context_sacola', 
```

No template sacola.html

```html
<ul class="list-group mb-3">
    <!-- Lista de Itens do Carrinho -->
    {% for item in sacola_itens.potes.all %} 
    {{item}}
    {% endfor %}
    
    <li class="list-group-item d-flex align-items-center 
        justify-content-between p-3 text-success">
        <span>Total (R$)</span>
        <h2><strong id="atualizaValor">R$ {{sacola_itens.preco}}</strong></h2>
    </li>
</ul>  

```

Aplicando as class do bootstrap.

```python
<!-- Lista de Itens do Carrinho -->
{% for item in sacola_itens.potes.all %}
<li class="list-group-item d-flex align-items-center justify-content-between lh-sm">
    <div class="text-start list-item">
        <h6 class="my-0 text-dark fw-bold">Pote {{item.embalagem.tipo}} - R$ {{item.preco_total}} </h6>
        <p class="my-0">Sabores: </p>
        <p class="my-0">Coberturas: </p>
    </div>  
    <div class="qty">
        <span class="minus bg-dark">-</span>
        <input type="number" class="dsb countCartItem" id="countCartItem" 
            name="countCartItem" value="{{item.quantidade}}"> 
        <span class="plus bg-dark">+</span>
    </div> 
    <div class="div">
        <a href="#" class="link-danger"> <i class="fas fa-trash"></i></a>
    </div>
</li>
{% endfor %}
```

Agora vamos fazer a descrição dos sabores e coberturas.

**Sabores**

```python
def obter_descricao_sabores(self):
    descricao_sabores = []
    for sel_sabor in self.pote.all():
        quantidade_sabor = sel_sabor.quantidade_bolas
        descricao_sabor = f"{quantidade_sabor}x {sel_sabor.sabor.nome}"
        descricao_sabores.append(descricao_sabor)
    return ";".join(descricao_sabores)
```

**Coberturas**

```python
def obter_descricao_coberturas(self):
    descricao_coberturas = []
    for sel_cobertura in self.pote_cobertura.all():
        quantidade_cobertura = sel_cobertura.quantidade_cobertura
        descricao_cobertura = f"{quantidade_cobertura}x {sel_cobertura.cobertura.nome}"
        descricao_coberturas.append(descricao_cobertura)
    return ";".join(descricao_coberturas)
```

```python
<p class="my-0">Sabores: {{item.obter_descricao_sabores}}</p>
<p class="my-0">Coberturas: {{item.obter_descricao_coberturas|default:"Não"}}</p>
```

Adiciona um CSS para melhorar visualização.

```python
/* Menu */
.offcanvas.offcanvas-end {
    width: 550px;
}

.list-group-item {
    height: 110px;
    border: none;
    border-bottom: 2px solid;
    margin-bottom: 20px; 
}

.list-group-item .list-item {
    font-size: 12px;
    font-style: italic;
    color: gray;
    width: 290px; 
}
```

Antes de continuar vamos arrumar 2 coisas. Quando adicionar um item no carrinho atualizar a pagina, assim conseguimos ver o resultado no carrinho. Depois pensando em fazer isso de maneira dinâmica. 

cardapio.html  

```python
success: function (response) {
    // Handle a resposta da view aqui
    if (response.status === 'success') {
        console.log('Itens adicionados à sacola com sucesso!');
        location.reload();
    } else {
        console.error('Erro ao adicionar itens à sacola:', response.message);
    }
},
```

Depois como vcs podem ver o contador do item fica open para usuario digitar. Vamos bloquear isso. Quando faço isso no inicio do document significa que todo elemento que tem essa classe dsb vai iniciar como disabled (desabilitado). Vou fazer isso com input tipo number que tem count.

```python
$(document).ready(function(){
            $('.dsb').prop('disabled', true);
```

```python
<input type="number" class="dsb ... " ... 
```

**Continuando…**

**Atualizar quantidade do pedido no carrinho**

primeiro vamos dar nomes aos boi. Coloquei uma class pote-item para ter acesso ao data-poteid para obter o identificador de cada pote da lista.

```python
<!-- Lista de Itens do Carrinho -->
            {% for item in sacola_itens.potes.all %}
            <li class="list-group-item d-flex align-items-center 
                justify-content-between lh-sm pote-item" data-poteid="{{item.id}}">
```

Depois, Vamos precisar fazer algumas modificações nessa parte do template para ter acesso a cada valor individualmente. 

```python
<div class="qty">
    <span class="minus sacola_minus bg-dark">-</span>
    <input type="number" class="dsb countCartItem_{{item.id}}" 
        id="countCartItem_{{item.id}}" 
        name="countCartItem_{{item.id}}" value="{{item.quantidade}}" disabled> 
    <span class="plus sacola_plus bg-dark">+</span> 
</div> 
```

Estou colocando o script em js/scripts por que o template sacola está “global” no template base então para colocar um script lá a gente pode usar o js/scripts.js. Vamos lá

js/scripts.js

```python
console.log("loading js/scripts");

$(document).ready(function() {

    // Altera a quantidade de Potes no carrinho.
    $(document).on('click', '.sacola_plus, .sacola_minus', function(){
        // Obtem o Identificador do Pote
        // closest procra o ancestral mais próximo subindo na hierarquia do DOM a partir do elemento atual
        var poteId = $(this).closest('.pote-item').data('poteid');
    
        // Use .siblings() para encontrar o elemento irmão do botão clicado
        var inputCountPote = $(this).siblings('input.countCartItem_'+poteId); 
    
        // Atualiza a quantidade no frontend
        if ($(this).hasClass('sacola_plus')) {
            // Incrementa a quantidade quando o botão de adição é clicado
            inputCountPote.val(parseInt(inputCountPote.val()) + 1); 
        } else if ($(this).hasClass('sacola_minus')) {
            // Decrementa a quantidade, com um valor mínimo de 0, quando o botão de subtração é clicado
            inputCountPote.val(Math.max(parseInt(inputCountPote.val()) - 1, 1));
        }

        var currentValue = parseInt(inputCountPote.val());

        // Exibe a quantidade atual no console
        console.log("Quantidade Atual:", currentValue);
    
    });
    
})
```

Vamos criar nossa função que vai receber os parametros para fazer a atualização

views.py

```python
@login_required(login_url="/admin/login/")
def atualiza_quantidade_sacola(request):
    if request.method == 'POST':
                pedido = Pedido.objects.filter(user=request.user, status=True).first()        
        
        pote_id = request.POST.get('poteId', None)
        novaQuantidade = request.POST.get('novaQuantidade', None)
        
        print(pote_id)
        print(novaQuantidade)

        response = {
            'status': 'success',
            'message': 'Atualizado', 
        }
        return JsonResponse(response)
    else:
        # Se a requisição não for do tipo POST, você pode retornar um erro ou outra resposta apropriada
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
```

urls.py

```python
path('atualiza_quantidade_sacola/', views.atualiza_quantidade_sacola, name='atualiza_quantidade_sacola'),
```

No scripts adicionamos a requisição 

```python
$.ajax({
    url: "/atualiza_quantidade_sacola/",
    type: "POST",
    data: { 
        "poteId" : poteId,
        "novaQuantidade": currentValue,
    }, 
    success: function (response) {
        console.log(response); 
    },
    error: function (error) {
        console.error("Erro:", error);
        // Adicione aqui qualquer manipulação adicional em caso de erro.
    }
});
```

Error: 

```python
Forbidden (CSRF token missing.): /atualiza_quantidade_sacola/
[07/Apr/2024 21:27:10] "POST /atualiza_quantidade_sacola/ HTTP/1.1" 403 2507
```

Tem uma solucão nesse link que vai nos ajudar a implementar um token.

https://stackoverflow.com/questions/5639346/what-is-the-shortest-function-for-reading-a-cookie-by-name-in-javascript

fica assim, atualizando no scripts.

```python
// Função para obter o valor do cookie CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

...

// Obtenha o token CSRF do cookie
var csrftoken = getCookie('csrftoken');

$.ajax({
    url: "/atualiza_quantidade_sacola/",
    type: "POST",
    data: { 
        "poteId" : poteId,
        "novaQuantidade": currentValue,
    },
    beforeSend: function (xhr) {
        // Inclua o token CSRF no cabeçalho da requisição
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (response) {
        console.log(response); 
    },
    error: function (error) {
        console.error("Erro:", error);
        // Adicione aqui qualquer manipulação adicional em caso de erro.
    }
});
```

Agora na views vamos fazer uns tratamento para alterar os valores no banco de dados.

```python
pote = get_object_or_404(MontaPote, id=pote_id)
pote.quantidade = int(novaQuantidade)
pote.save()

response = {
    'status': 'success',
    'message': 'Atualizado',
    'novo_valor': f'R$ {pedido.itens_da_sacola.preco_total()}' 
}
```

Como vcs viram no console a mudança acontece e está sendo atualizada. Agora precisamos passar esse resultado para usuario conseguir saber se item foi atualizado de fato ou nao.  

```python
template da sacola.html
<div id="messageAlert"></div>

scripts.js
// Adicione aqui qualquer manipulação adicional após o sucesso da requisição.
var atualizaValor = $('#atualizaValor'); // Substitua 'spanQuantidade_' pelo identificador real que você está usando

atualizaValor.text(response['novo_valor']);

console.log(response['message'])

$('#messageAlert').text(
    response['message']).fadeIn(400).delay(2000).fadeOut(400);
```

**Remover pedido do Carrinho**

primeiro vamos adicionar uma classe auxiliar para ter acesso ao item. 

sacola.html

```python
<div class="div">
    <a href="#" class="link-danger remove-item"> <i class="fas fa-trash"></i></a>
</div>
```

na views 

```python
@login_required(login_url="/admin/login/")
def remove_item_sacola(request):
    if request.method == 'POST':
        pedido = Pedido.objects.filter(user=request.user, status=True).first()

        pote_id = request.POST.get('poteId', None)

        # Verifique se o pote_id é fornecido
        if not pote_id:
            return JsonResponse(
                {'status': 'error', 'message': 'ID do pote não fornecido'},
                status=400)  
        
        # Encontre o MontaPote específico
        pote = get_object_or_404(MontaPote, id=pote_id)

        # Exclua o pote
        pote.delete()
        
        response = {
            'status': 'success',
            'message': 'Item removido com sucesso',
            'novo_valor': f'R$ {pedido.itens_da_sacola.preco_total()}' 
        }
            
        return JsonResponse(response)
    else:
        # Se a requisição não for do tipo POST, você pode retornar um erro ou outra resposta apropriada
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
```

```python
path('remove_item_sacola/', views.remove_item_sacola, name='remove_item_sacola'),
```

scripts.js

```python
// Remover Item da Sacola
$(document).on('click', '.remove-item', function(){
    // Obtem o Identificador do Pote
    // closest procra o ancestral mais próximo subindo na hierarquia do DOM a partir do elemento atual
    var poteId = $(this).closest('.pote-item').data('poteid');

    console.log("Identificador do Item:", poteId);

    // Obtenha o token CSRF do cookie
    var csrftoken = getCookie('csrftoken');

    // Envio Ajax com o token CSRF para view atualiza quantidade
    $.ajax({
        url: "/remove_item_sacola/",
        type: "POST",
        data: { "poteId" : poteId },
        beforeSend: function (xhr) {
            // Inclua o token CSRF no cabeçalho da requisição
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (response) {
            console.log("Sucesso:", response);  
        },
        error: function (error) {
            console.error("Erro:", error);
            // Adicione aqui qualquer manipulação adicional em caso de erro.
        }
    });
});
```

Transmitir isso para usuario saber que foi excluido. 

```python
// Armazene uma referência ao elemento <li> correspondente
var poteItem = $(this).closest('.pote-item');

No success 
poteItem.fadeOut(400, function() {
    $(this).remove();
});

var atualizaValor = $('#atualizaValor'); 

atualizaValor.text(response['novo_valor']);
console.log(response['message'])
$('#messageAlert').text(
    response['message']).fadeIn(400).delay(2000).fadeOut(400);
```