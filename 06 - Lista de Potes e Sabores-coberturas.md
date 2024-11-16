## Vamos configurar a lista de recepientes na pagina de cardapio.

Para isso na nossa view vamos criar 2 query uma de embalagens e outra de tipo de sabores. O tipo de sabor tem todos os relacionamentos que precisamos para montar o pode completo. Ok.

**`*views.py*`**

```python
from .models import Embalagem, TipoSabor

def cardapio(request):
    embalagens = Embalagem.objects.filter(ativo=True)
    tipo_sabor = TipoSabor.objects.filter(ativo=True)
    context = {
        'embalagens': embalagens,
        'tipo_sabor': tipo_sabor
    }
    return render(request, 'cardapio.html', context)
```

Então no template do cardapio fica assim. primero podemos fazer o for para listar todas as embalagens que cadastramos.

**`*cardapio.html*`**

```html
{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %} 
<h2 class="pb-2 border-bottom">Cardápio</h2>
<p>Selecione o recipiente para montar seu sorvete. A quantidade de bolas de sorvete pode variar, e você pode escolher diferentes sabores.</p>
<div class="row row-cols-1 row-cols-lg-4 align-items-stretch g-4 py-5">
	{% for emb  in embalagens %}
	<div class="col">
		<a href="" class="link-dark text-decoration-none" data-bs-toggle="modal" data-bs-target="#sabores_{{emb.id}}">
		<div class="card border-0" style="height: 250px; background-size: cover; 
			background-image: url('https://http2.mlstatic.com/D_NQ_NP_917685-MLB49794642888_042022-O.webp');">
			<div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
				<ul class="d-flex list-unstyled mt-auto text-dark">
					<li class="d-flex align-items-center me-3"> 
						<h1>{{emb.tipo}}</h1>
					</li>
					<li class="d-flex align-items-center">
						<svg class="bi me-2" width="1em" height="1em">
							<use xlink:href="#calendar3"></use>
						</svg>
						<h6>{{emb.capacidade_maxima_bolas}} Bolas</h6>
					</li>
				</ul>
			</div>
		</div>
		</a>
	*</div>*
	<!-- {% include 'sabores.html' %} -->
	{% endfor %}
</div>
{% endblock %}
```

No template de sabores vamos configurar o modal para lista de sabores disponivel. Essa parte é bem chatinha então fica de olho nos detalhes. 

Primeiro é bom entender o conceito de “pai e filho” no modal. Para não acontencer de criar no card e sempre abrir o mesmo modal para todos. Esse tipo de problema é muito comum por isso já estou avisando voces. Para que isso não acontece precisamos dar nomes nos identificadores. exemplo: id="sabores_{{emb.id}}" essa é uma maneira de “linkar” corretamente as chamadas. 

**`*modal > sabores*`**

```python
<!-- Modal -->
 <div class="modal fade" id="sabores_{{emb.id}}" tabindex="-1" aria-labelledby="sabores_lLabel" aria-hidden="true">
	<div class="modal-dialog modal-lg modal-dialog-scrollable">
	  <div class="modal-content">
		<div class="modal-header">
		  <h1 class="modal-title fs-5" id="sabores_Label"></h1>
		  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
		</div> 
		
		<div>
			<img class="img-fluid" width="180" src="https://static1.minhavida.com.br/articles/cd/34/02/f6/essa-e-a-razao-pela-qual-voce-nao-deve-guardar-alimentos-no-pote-de-sorvete-orig-1.jpg" alt="">
			<h3>Pote de Sorvete {{emb.tipo}}</h3>
			<p>Você pode escolher {{emb.capacidade_maxima_bolas}} bolas e coberturas</p>  
		</div>
		
		<div class="modal-body"> 

				<!-- lista de sabores -->

 		</div>  
		<div class="modal-footer">
		  <button type="button" class="btn btn-primary btn-lg">Adicionar</button> 
		</div>
	  </div>
	</div>
  </div>
```

## Lista de sabores.

Como temos alguns relacionamento na tabela tipoSabor. Precisamos fazer 2 for para ter todas as informações que precisamos. 

Primeiro **for** temos acesso ao tipo de sabor (Tradicional, Premium, Sorvet (fruta), Açai) e a quantidade de bolas que podemos selecionar conforme o pote.

Segundo **for** estão relacionados a lista de sabores do modelo “Sabor” que tem um campo tipo onde está relacionando com a tabela “TipoSabor” por isso chamamos t.tipo_sabor.all para obter a lista. Esse tipo_sabor é o related_name que colocamos na tabela “Sabor”.

```html
{% for t in tipo_sabor %}
	<div class="d-flex justify-content-between bg-light border-3 p-3"> 
	<span class="fs-4 fw-bold">Sabores {{t.tipo}}</span>
	<span class="fs-4 fw-bold">0 / {{emb.capacidade_maxima_bolas}} <span class="badge bg-secondary">Obrigatório</span></span>
</div> 
{% for s in t.tipo_sabor.all %} 
<div class="d-flex align-items-center p-3 border"> 
	<div class="p-2 flex-grow-1 text-start">
		<img src="https://gelaboca.com.br/wp-content/webp-express/webp-images/doc-root/wp-content/uploads/2023/04/sabores-de-sorvete-morango-768x520.jpg.webp" class="" width="80" alt="..."> 
		<span class="fw-bold">{{s.nome}}</span> 
	</div>
	<div class="qty">
		<span class="minus bg-dark">-</span>
		<input type="number" class="count" name="qty" value="0">
		<span class="plus bg-dark">+</span>
	</div>
</div>
{% endfor %}
{% endfor %}
```

Como podem perceber ao selecionar a quantidade todos são selecionados. Vamos arrumar isso em jquery. 

**primeiro no seu HTML atualize:** 

```html
<input type="number" class="count"  data-saborid="{{s.id}}"  name="qty" value="0">
```

Esse **data-saborid** vamos utilizar para identificar o sabor especifico e realizar qualquer ação personalizada independente. 

No contexto do seu código JavaScript, quando você usa **`$(this).siblings('input.count')`**, você está procurando todos os elementos **`<input>`** com a classe **`.count`** que são irmãos do elemento que acionou o evento de clique (o botão "plus" neste caso).

Quando você usa **`.prop('disabled', true)`**, está basicamente definindo a propriedade **`disabled`** de todos os elementos com a classe **`.count`** como **`true`**

```python
{% block scripts %}
	<script>
		$(document).ready(function(){
			$('.count').prop('disabled', true);
		
			$(document).on('click', '.plus', function(){
				var input = $(this).siblings('input.count');
				var saborId = input.data('saborid');
				input.val(parseInt(input.val()) + 1); 
			});
		
			$(document).on('click', '.minus', function(){
				var input = $(this).siblings('input.count');
				var saborId = input.data('saborid');
				input.val(parseInt(input.val()) - 1);
				if (input.val() < 0) {
					input.val(0);
				} 
			});
		});
	</script>
{% endblock scripts %}
```

## Agora precisamos calcular o valor maximo selecionado

**Alternativas**

1. **Usando .closest() e .find():**

```jsx
var input_max = $(this).closest('.qty').find('input.selsabor');
```

Este código procura o ancestral mais próximo com a classe **`.qty`** e, em seguida, encontra o elemento **`input.selsabor`** dentro desse ancestral.

1. **Usando .parent() e .find():**

```jsx
var input_max = $(this).parent().find('input.selsabor');
```

Este código encontra o pai direto do botão "plus" e, em seguida, localiza o elemento **`input.selsabor`** dentro desse pai.

1. **Usando .prev():**

```jsx
var input_max = $(this).prev('input.selsabor');
```

Se o **`input.selsabor`** é o irmão anterior do botão "plus", você pode usar **`.prev()`**.

### Ajustes:

```python
<!-- Modal -->
<div class="modal-content">
	 ... 
	 
  <div class="d-flex justify-content-end align-items-center p-3">
		  <span class="fs-4 fw-bold"> <span id="resultselsabor">0</span> / {{emb.capacidade_maxima_bolas}} 
      <span class="badge bg-secondary">Obrigatório</span></span> 
  </div> 

  <div class="modal-body count-result"> 
        
		{% for t in tipo_sabor %}
    <div class="d-flex justify-content-between bg-light border-3 p-3"> 
        <span class="fs-4 fw-bold">Sabores {{t.tipo}}</span>
    </div> 
		 ...
    <div class="qty">
        <span class="minus bg-dark">-</span>
        <input type="hidden" class="selsabor" id="selsabor" data-capmax="{{emb.capacidade_maxima_bolas}}">
        <input type="number" class="count" data-saborid="{{s.id}}" name="qty" value="0">					
        <span class="plus bg-dark">+</span>
    </div> 
		 ...
```

```python
$(document).ready(function(){
		$('.count').prop('disabled', true);
	
		function atualizarTotalSelecionado() {
			var totalSelecionado = 0;
			$('.count').each(function() {
				totalSelecionado += parseInt($(this).val());
			});
			$('#resultselsabor').text(totalSelecionado);
		}
	
		$(document).on('click', '.plus', function() {
			var input = $(this).siblings('input.count');
			var saborId = input.data('saborid');
			var input_max = $(this).parent().find('input.selsabor');
			var capacidadeMaxima = input_max.data('capmax');
			var totalSelecionado = 0;
	
			// Calcular o total selecionado para todos os sabores
			$('.count').each(function() {
				totalSelecionado += parseInt($(this).val());
			});
	
			if ((totalSelecionado + 1) <= capacidadeMaxima) {
				input.val(parseInt(input.val()) + 1);
				console.log(parseInt(input.val()));
			} else {
				// Excedeu a capacidade máxima, você pode exibir uma mensagem ou tomar outra ação aqui.
				console.log('Capacidade máxima atingida');
			}
	
			// Atualizar o totalSelecionado após a adição
			atualizarTotalSelecionado();
		});
	
		$(document).on('click', '.minus', function(){
			var input = $(this).siblings('input.count');
			var saborId = input.data('saborid');
			input.val(parseInt(input.val()) - 1);
			if (input.val() < 0) {
				input.val(0);
			}
	
			// Atualizar o totalSelecionado após a subtração
			atualizarTotalSelecionado();
		});
});
```

**Agora tem um problema**. Cada modal tem sua lista de sabores para selecionar. Então precisamos dar “nomes aos boi” e tratar de forma corretamente. 

```python
<!-- Modal -->
<div class="modal fade" id="sabores_{{emb.id}}" data-modalid="{{emb.id}}" tabindex="-1" 
aria-labelledby="sabores_lLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-scrollable">
    <div class="modal-content">
    <div class="modal-header">
      <h1 class="modal-title fs-5" id="sabores_Label"></h1>
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>  

  <div>
    <img class="img-fluid" width="180" src="https://static1.minhavida.com.br/articles/cd/34/02/f6/essa-e-a-razao-pela-qual-voce-nao-deve-guardar-alimentos-no-pote-de-sorvete-orig-1.jpg" alt="">
    <h3>Pote de Sorvete {{emb.tipo}}</h3>
    <p>Você pode escolher {{emb.capacidade_maxima_bolas}} bolas e coberturas</p>  
  </div>

  <div class="d-flex justify-content-end align-items-center p-3">
    <span class="fs-4 fw-bold"> <span id="resultselsabor_{{emb.id}}">0</span> / {{emb.capacidade_maxima_bolas}} 
    <span class="badge bg-secondary">Obrigatório</span></span> 
  </div> 
  
  <div class="modal-body count-result"> 
    
    <!-- lista de sabores -->
    {% for t in tipo_sabor %}
    <div class="d-flex justify-content-between bg-light border-3 p-3"> 
      <span class="fs-4 fw-bold">Sabores {{t.tipo}}</span>
     </div> 
    {% for s in t.tipo_sabor.all %} 
    <div class="d-flex align-items-center p-3 border"> 
      <div class="p-2 flex-grow-1 text-start">
        <img src="https://gelaboca.com.br/wp-content/webp-express/webp-images/doc-root/wp-content/uploads/2023/04/sabores-de-sorvete-morango-768x520.jpg.webp" class="" width="80" alt="..."> 
        <span class="fw-bold">{{s.nome}}</span> 
      </div>
      <div class="qty">
        <span class="minus bg-dark">-</span>
        <input type="hidden" class="selsabor" id="selsabor_{{emb.id}}" data-modalid="{{emb.id}}" data-capmax="{{emb.capacidade_maxima_bolas}}">
        <input type="number" class="count_{{emb.id}}" data-saborid="{{s.id}}" name="qty" value="0">					
        <span class="plus bg-dark">+</span>
      </div> 
    </div>
    {% endfor %}
    {% endfor %}
    
  </div>  
  <div class="modal-footer">
    <button type="button" class="btn btn-primary btn-lg">Adicionar</button> 
  </div>
  </div>
</div>
</div>
```

Aqui vamos passar o **Id do modal** corretamente para fazer as modificações. 

Então as mudanças ficam assim. Vamos por partes.

```python
$(document).ready(function(){
	$('.count').prop('disabled', true);

	function atualizarTotalSelecionado(modalId) {
		var totalSelecionado = 0;
		$('.count_' + modalId).each(function() {
			totalSelecionado += parseInt($(this).val());
		});
		$('#resultselsabor_' + modalId).text(totalSelecionado);
	}

	$(document).on('click', '.plus', function() {
		var modalId = $(this).closest('.modal').data('modalid');
		var input = $(this).siblings('input.count_' + modalId);
		var capacidadeMaxima = $('#selsabor_' + modalId).data('capmax');
		var totalSelecionado = 0;

		// Calcular o total selecionado para todos os sabores
		$('.count_' + modalId).each(function() {
			totalSelecionado += parseInt($(this).val());
		});

		// Calcular o total selecionado para todos os sabores
		if ((totalSelecionado + 1) <= capacidadeMaxima) {
			input.val(parseInt(input.val()) + 1);
		} else {
			// Excedeu a capacidade máxima
			console.log('Capacidade máxima atingida');
		}

		// Atualizar o totalSelecionado após a adição
		atualizarTotalSelecionado(modalId);
	});

	$(document).on('click', '.minus', function() {
		var modalId = $(this).closest('.modal').data('modalid');
		var input = $(this).siblings('input.count_' + modalId);

		input.val(parseInt(input.val()) - 1);
		if (input.val() < 0) {
			input.val(0);
		}
		// Atualizar o totalSelecionado após a subtração
		atualizarTotalSelecionado(modalId);
	});
	
});
```

**Feito isso cada Modal está reagindo de maneira independente.**

Só faltou um detalhe que gostaria de passar. 
É uma melhoria visual para mostrar para usuario que já foi selecionado tudo. Só detalhe mesmo. Se quiser não precisa colocar.

**`*modal sabores.html*`**

```python
<span class="badge bg-secondary" id="impResponse{{emb.id}}">Obrigatório</span></span>

```

**`*cardapio.html*`**

```python
function atualizarColorSuccess(modalId) {
	$('#impResponse'+modalId).removeClass('bg-success')
	$('#impResponse'+modalId).addClass('bg-secondary')
}
function atualizarColorDanger(modalId) {
	$('#impResponse'+modalId).removeClass('bg-secondary')
	$('#impResponse'+modalId).addClass('bg-success')
} 
 
$(document).on('click', '.plus', function() {
	var modalId = $(this).closest('.modal').data('modalid');
	var input = $(this).siblings('input.count_' + modalId);
	var capacidadeMaxima = $('#selsabor_' + modalId).data('capmax');
	var totalSelecionado = 0;

	// Calcular o total selecionado para todos os sabores
	$('.count_' + modalId).each(function() {
		totalSelecionado += parseInt($(this).val());
	});

	// Calcular o total selecionado para todos os sabores
	if ((totalSelecionado + 1) <= (capacidadeMaxima)) {
		input.val(parseInt(input.val()) + 1);
		atualizarColorSuccess(modalId)

		if ((totalSelecionado + 1) == capacidadeMaxima) {
			atualizarColorDanger(modalId)
		}
	} else { 
		// Excedeu a capacidade máxima  
		atualizarColorDanger(modalId)
		console.log('Capacidade máxima atingida');

	}

	// Atualizar o totalSelecionado após a adição
	atualizarTotalSelecionado(modalId);
});

$(document).on('click', '.minus', function() {
	var modalId = $(this).closest('.modal').data('modalid');
	var input = $(this).siblings('input.count_' + modalId);

	input.val(parseInt(input.val()) - 1);
	if (input.val() < 0) {
		input.val(0);
	}
	atualizarColorSuccess(modalId)

	// Atualizar o totalSelecionado após a subtração
	atualizarTotalSelecionado(modalId);
});
```

**Cobertura vamos adicionar a lista de coberturas/adicionais no modal.**

**`*views.py*`**

```python
def cardapio(request):
    embalagens = Embalagem.objects.filter(ativo=True)
    tipo_sabor = TipoSabor.objects.filter(ativo=True)
    coberturas = Cobertura.objects.filter(ativo=True)
    context = {
        'embalagens': embalagens,
        'tipo_sabor': tipo_sabor,
        'coberturas': coberturas
    }
    return render(request, 'cardapio.html', context)
```

**`*sabores.html*`**

```python
...
<!-- Coberturas -->
<div class="d-flex justify-content-between bg-light border-3 p-3"> 
    <span class="fs-4 fw-bold">Coberturas</span>
</div> 
{% for c in coberturas %} 
<div class="d-flex align-items-center p-3 border"> 
    <div class="p-2 flex-grow-1 text-start">
        <img src="https://down-br.img.susercontent.com/file/179eac30b9e3dd59fb5e8b02fc108c21" class="" width="80" alt="..."> 
        <span class="fw-bold">{{c.nome}}</span> 
    </div>
    <div class="qty" >
        <span class="minus bg-dark">-</span>
        <input type="number" class="selcobertura_{{emb.id}}" data-coberturaid="{{c.id}}" 
            id="selcobertura_{{emb.id}}" name="selcobertura_{{emb.id}}" value="0" disabled>					
        <span class="plus bg-dark">+</span>
    </div>
</div>
{% endfor %}   
... 
```

**`*cardapio.html — scripts*`**

```python
// Coberturas/Adicionais 
$(document).on('click', '.plus', function(){
	var modalId = $(this).closest('.modal').data('modalid');
	var input = $(this).siblings('input.selcobertura_'+modalId); 
	input.val(parseInt(input.val()) + 1); 
});
$(document).on('click', '.minus', function(){
	var modalId = $(this).closest('.modal').data('modalid');
	var input = $(this).siblings('input.selcobertura_'+modalId); 
	input.val(parseInt(input.val()) - 1);
	if (input.val() < 0) {
		input.val(0);
	} 
});
```

**Agora vamos configurar a quantidade de potes que podemos selecionar.**

**`*sabores.html*`**

```html
<div class="modal-footer"> 
  <div class="qty" >
      <span class="minus item_minus bg-dark">-</span>
      <input type="number" class="qtdPote_{{emb.id}}" id="qtdPote_{{emb.id}}" name="qtdPote_{{emb.id}}" value="1" disabled>					
      <span class="plus item_plus bg-dark">+</span>
  </div>
  <button type="button" class="btn btn-primary btn-lg">Adicionar</button> 
</div>
```

**`*cardapio.html*`**

```html
// Quantidade de itens
$(document).on('click', '.item_plus, .item_minus', function(){
	var modalId = $(this).closest('.modal').data('modalid');
	var inputQtdPote = $(this).siblings('input.qtdPote_'+modalId); 
	
	var increment = $(this).hasClass('item_plus') ? 1 : -1;
	
	var newValue = parseInt(inputQtdPote.val()) + increment;
	inputQtdPote.val(Math.max(newValue, 1));
});
```