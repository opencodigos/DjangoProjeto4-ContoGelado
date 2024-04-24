##Gerenciar Pedidos


views.py

```python
@login_required(login_url="/admin/login/")
def todos_pedidos(request):
    todos_pedidos = Pedido.objects.all()
    return render(request, 'gerencia-pedidos.html', {'todos_pedidos': todos_pedidos})
```

urls.py

```python
path('gerencia-pedidos/', views.todos_pedidos, name='todos_pedidos'),
```

gerencia-pedidos.html

```python
{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %}  
<h2>Todos os Pedidos</h2>
<p>Gerencia todos os Pedidos feitos de todos os clientes</p>
<table class="table table-hover">
    <thead>
        <tr>
            <th>Data do Pedido</th>
            <th>Status do Pedido</th>
            <th>Status do Pagamento</th>
            <th>Status da Entrega</th>
        </tr>
    </thead>
    <tbody>
        {% for tp in todos_pedidos %}
        <tr class="clickable">
            <td>{{ tp.data_pedido|date:"d/m/Y" }}</td>
            <td>{% if tp.status %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %}</td>
            <td>{% if tp.pago %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %}</td>
            <td>{% if tp.entrega %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %}</td>
        </tr> 
    {% endfor %}
    </tbody>
</table> 
{% endblock %}
{% block scripts %}  {% endblock scripts %} 
```

navbar.html

```python
{% if request.user.is_superuser %}
<a class="me-3 py-2 link-dark text-decoration-none 
    {% if request.path == '/gerencia-pedidos/' %}active{% endif %}" href="{% url 'todos_pedidos' %}">
        Gerencia Pedidos</a>
{% endif %}
```

```python
@login_required(login_url="/admin/login/")
def todos_pedidos(request):
    if request.user.is_superuser:
        todos_pedidos = Pedido.objects.all()
    else:
        return redirect('cardapio')
    return render(request, 
                    'gerencia-pedidos.html', {'todos_pedidos': todos_pedidos})
```

Vamos Editar esse pedido

**Adicionado modal e preparar**

gerencia-pedidos.html

```python
<div class="modal fade" id="dtlPedido{{ tp.id }}" tabindex="-1" aria-labelledby="dtlPedidoLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="dtlPedidoLabel">Pedido {{ tp.data_pedido|date:"d/m/Y" }}</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="form-check">
                    <input class="form-check-input status-checkbox" type="checkbox" value="" id="statusCheckbox{{ tp.id }}" {% if tp.status %}checked{% endif %}>
                    <label class="form-check-label" for="statusCheckbox{{ tp.id }}">Status do Pedido</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input pago-checkbox" type="checkbox" value="" id="pagoCheckbox{{ tp.id }}" {% if tp.pago %}checked{% endif %}>
                    <label class="form-check-label" for="pagoCheckbox{{ tp.id }}">Pagamento</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input entrega-checkbox" type="checkbox" value="" id="entregaCheckbox{{ tp.id }}" {% if tp.entrega %}checked{% endif %}>
                    <label class="form-check-label" for="entregaCheckbox{{ tp.id }}">Entregue</label>
                </div>
                <button type="button" class="btn btn-dark atualizar-pedido" data-id="{{ tp.id }}">Atualizar</button>
            </div>
        </div>
    </div>
</div>
```

```python
<tr class="clickable" data-bs-toggle="modal" data-bs-target="#dtlPedido{{ tp.id }}">
```

Por enquando está estatico não tem nenhum evendo para enviar os dados atualizados para servidor. Vamos fazer isso agora.

views.py

```python
@login_required(login_url="/admin/login/")
def atualizar_pedido(request):
    dados_str = request.POST.get('dados', None)
    dados = json.loads(dados_str) 
        
    pedido_id = dados.get('id', None)
    status = dados.get('status', None)
    pago = dados.get('pago', None)
    entrega = dados.get('entrega', None)

    print(pedido_id, status, pago, entrega)
    try: 
        return JsonResponse({'success': True})
    except Pedido.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pedido não encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
```

```python
path('atualizar-pedido/', views.atualizar_pedido, name='atualizar_pedido'),
```

Podemos configurar o script para passar os dados para views.

```python
<script>
$(document).ready(function() {
    $('.atualizar-pedido').click(function() {
        var id = $(this).data('id');
        var dados = {
            'id': id,
            'status': $('#statusCheckbox' + id).prop('checked'),
            'pago': $('#pagoCheckbox' + id).prop('checked'),
            'entrega': $('#entregaCheckbox' + id).prop('checked'), 
        } 
        console.log(dados)
        $.ajax({
            url: "{% url 'atualizar_pedido' %}", // Substitua pela URL correta
            type: 'POST',
            data: {
                'dados': JSON.stringify(dados),
                'csrfmiddlewaretoken': '{{ csrf_token }}' // Token CSRF
            },
            success: function(data) { 
                console.log(data);
            },
            error: function(error) {
                console.log(error);
                alert('Erro ao atualizar o pedido.');
            }
        });
    });
});
</script>
```

no servidor

```python
pedido = Pedido.objects.get(pk=pedido_id)
pedido.status = status
pedido.pago = pago
pedido.entrega = entrega
pedido.save()
```

no retorno do scripts

```python
success: function(data) { 
    console.log(data);
    // Feche o modal se necessário 
    $('#dtlPedido' + id).modal('hide');
    location.reload();
},
```