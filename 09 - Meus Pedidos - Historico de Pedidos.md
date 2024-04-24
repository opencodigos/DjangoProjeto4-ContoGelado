##Meus Pedidos / Historico de Pedidos

views.py

```python
@login_required(login_url="/admin/login/")
def meus_pedidos(request):
    meus_pedidos = Pedido.objects.filter(user=request.user)
    return render(request, 'meus-pedidos.html', {'meus_pedidos': meus_pedidos})
```

urls.py

```python
path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
```

Navbar.html

https://getbootstrap.com/docs/5.3/components/dropdowns/

```python
<!-- Meus Pedidos -->
<div class="link-dark dropdown">
    <a class="nav-link link-dark dropdown-toggle {% if request.path == '/meus-pedidos/' %}active{% endif %}"
            data-bs-toggle="dropdown" href="#" role="button" aria-expanded="false">
        <i class="fas fa-user"></i>  {{request.user.first_name}} {{request.user.last_name}}</a>
    <ul class="dropdown-menu dropdown-menu-dark">
        <li><a href="{% url 'meus_pedidos' %}" 
            class="dropdown-item rounded-2 {% if request.path == '/meus-pedidos/' %}active{% endif %}">Meus Pedidos</a></li> 
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item rounded-2" href="/admin/logout">Sair</a></li>
    </ul>
</div>  
```

meus-pedidos.html

```python
{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %} 
<div class="mb-5">
    <h2>Meus Pedidos</h2>
    <p>Lista de Pedidos ativos que estão processando</p>
    <div class="d-flex gap-1 justify-content-center align-content-center flex-wrap">
        {% for mp in meus_pedidos %}
        {% if not mp.entrega%}
        <div class="p-3 bg-warning rounded-5">
            <h4>Data do Pedido: {{ mp.data_pedido|date:"d/m/Y" }}</h4> 
            <p>Status do Pedido: {% if mp.status %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %} </p>
            <p>Status do Pagamento: {% if mp.pago %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %}</p> 
            <p>Status da Entrega: {% if mp.entrega %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %}</p> 

            <button type="button" class="btn btn-success whatsapp-btn" data-id="{{ mp.id }}">Acompanhar pelo Whatsapp</button>
        </div>
        {% endif %} 
        {% endfor %} 
    </div>
</div> 
{% endblock %}
{% block scripts %} {% endblock scripts %}
```

Historico de pedidos

```python

<h2>Historico de Pedidos</h2>
<p>Lista de Pedidos já finalizados</p>
<table class="table">
    <thead>
        <tr>
            <th>Data do Pedido</th>
            <th>Status do Pedido</th>
            <th>Status do Pagamento</th>
            <th>Status da Entrega</th>
        </tr>
    </thead>
    <tbody>
        {% for mp in meus_pedidos %}
        {% if mp.pago and mp.entrega %}
        <tr>
            <td>{{ mp.data_pedido|date:"d/m/Y" }}</td>
            <td>{% if mp.status %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %}</td>
            <td>{% if mp.pago %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %}</td>
            <td>{% if mp.entrega %}<i class="fas fa-check-circle link-success"></i>{% else %}<i class="fas fa-times-circle link-danger"></i>{% endif %}</td>
        </tr>
        {% endif %}
        {% endfor %}
    </tbody>
</table> 
```