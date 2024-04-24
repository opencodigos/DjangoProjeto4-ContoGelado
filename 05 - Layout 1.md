##Layout 1


Arquivo Base eu coloquei scripts de **jQuery** e **Font Awesome**

*base.html*

```html
    <script src="https://code.jquery.com/jquery-3.7.1.min.js" 
        integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"></script>
    
    <script defer src="https://use.fontawesome.com/releases/v5.15.4/js/all.js" 
        integrity="sha384-rOA1PnstxnOBLzCLMcre8ybwbTmemjzdNlILg8O7z1lUkLXozs4DHonlDtnE7fpc" crossorigin="anonymous"></script>
```

**Bootstrap Navbar (Exemplos)**

https://getbootstrap.com/docs/5.3/components/navbar/

*navbar.html*

```html
{% load static %}
<div class="d-flex flex-column flex-md-row align-items-center justify-content-between pb-3 mb-4">
    <a href="" class="link-dark text-decoration-none text-center">
        <img src="https://via.placeholder.com/200" alt="" width="100">
        <h2>Conto Gelado</h2>
    </a>

    <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
    
        <a class="me-3 py-2 link-dark text-decoration-none" href="#">Inicio</a>
        <a class="me-3 py-2 link-dark text-decoration-none" href="#">Contato</a>
        <a class="me-3 py-2 link-dark text-decoration-none" href="#">Cardápio</a>
        
        {% if request.user.is_authenticated %}
        <a class="me-3 py-2 link-dark text-decoration-none" href="#">Meus Pedidos</a> 
        <a class="me-3 py-2 text-bold link-dark" href="#">
            {{request.user.first_name}} {{request.user.last_name}}</a>

            <!-- Carrinho -->
            <button class="btn btn-transparent position-relative" type="button"
                    data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">
                <i class="fas fa-shopping-cart fa-2x"></i>
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                    3+ 
                </span>
            </button>
            
            <!-- {% include 'sacola.html' %} -->

        {% else %}
        <a class="py-2 btn btn-dark" href="/admin/login">Login</a>
        {% endif %} 
    </nav>
</div>
```

Atualizamos a pagina incluindo o navbar.html e adicionei 2 classes container e wrapper para deixar o conteudo centralizado. 

*base.html*

```html
<div class="container py-3"> 
        {% include 'navbar.html' %} 
        {% include 'messages.html' %} 
        <div class="wrapper">
        {% block content %} {% endblock %} 
        </div>
</div>
```

Depois aplica esse CSS.

```css
body {
    background-color: #ebebeb;
    margin: 0;
    padding: 0;
    font-family: 'Arial', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #333;
}

.wrapper {
    background-color: #f7f7f7;
    border-radius: 20px;
    padding: 10px;
}
```

**Vamos utilizar o Bootstrap Sidebar (offcanvasRight) para sacola de Itens.**

https://getbootstrap.com/docs/5.3/components/offcanvas/#examples

*sacola.html*

```html
<div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
    <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="sidebarSacolaLabel">Sacola de Itens</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
        <h4 class="d-flex justify-content-between align-items-center mb-3">
            <span class="text-primary">Meus Itens</span>
            <span class="badge bg-primary rounded-pill">3</span>
        </h4>
        <ul class="list-group mb-3">
            <li class="list-group-item d-flex justify-content-between lh-sm">
                <div class="text-start">
                    <h6 class="my-0">Pote 1L</h6>
                    <small class="text-body-secondary">6x morango;6x chocolate 1x cobertura de chocolate</small>
                </div>
                <span class="text-body-secondary">R$ 12,80</span>
            </li>
            <li class="list-group-item d-flex justify-content-between lh-sm">
                <div class="text-start">
                    <h6 class="my-0">Pote 1/5L</h6>
                    <small class="text-body-secondary">6x morango;6x chocolate 1x cobertura de chocolate</small>
                </div>
                <span class="text-body-secondary">R$ 8,80</span>
            </li>  
            <li class="list-group-item d-flex justify-content-between">
                <span>Total (R$)</span>
                <strong>R$ 20,99</strong>
            </li>
        </ul> 
        <button type="button" class="btn btn-success">Finalizar pedido</button> 
    </div>
</div>
```

**Uma pagina inicio de boas vindas que tem um botão para redirecionar para cardapio.**

renomei o arquivo **index** para **inicio.html**

```html
{% extends 'base.html' %}

{% block title %}Inicio{% endblock %}

{% block content %}  
<div class="pricing-header p-3 pb-md-4 mx-auto text-center">
    <h1 class="display-4 fw-normal text-body-emphasis">Conto Gelado - Açaí e Sorvetes</h1>
    <p class="fs-5 text-body-secondary">Bem-vindo ao Conto Gelado, o seu destino para sabores gelados e momentos especiais! </p>
        <p class="fs-5 text-body-secondary">Agora, com nosso cardápio online e serviço de entrega, você pode desfrutar dos nossos deliciosos sorvetes no conforto da sua casa. Explore nossa diversificada seleção de sabores, desde os clássicos até opções veganas. Garantimos entregas rápidas e frescas, trazendo a alegria do Conto Gelado até você. Celebramos momentos e indulgências do dia a dia.</p>
        <p class="fs-5 text-body-secondary">Faça seu pedido e permita-nos adoçar seus dias com a magia do sorvete.</p>
        <a class="btn btn-dark btn-lg" href="{% url 'cardapio' %}" role="button">Ver Cardápio</a>
</div> 
{% endblock %}
```

Com essas mudanças alteramos a chamada na views.py e urls.py

**views e urls** 

```html
**views.py**
def inicio(request):
    return render(request, 'inicio.html')

def cardapio(request):
    return render(request, 'cardapio.html')

**urls.py**
from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.inicio, name='inicio'), 
    path('cardapio', views.cardapio, name='cardapio'), 
]
```

**Layout da pagina do Cardapio fica assim. Repeti alguns só para dar volume na ideia dos cards.**

https://getbootstrap.com/docs/5.3/components/card/#example

cardapio.html

```html

{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %}
<h2 class="pb-2 border-bottom">Cardápio</h2>
<p>Selecione o recipiente para montar seu sorvete. A quantidade de bolas de sorvete pode variar, e você pode escolher diferentes sabores.</p>

<div class="row row-cols-1 row-cols-lg-4 align-items-stretch g-4 py-5">
    <div class="col">
        <a href="" class="link-dark text-decoration-none" data-bs-toggle="modal" data-bs-target="#exampleModal">
        <div class="card border-0" style="height: 250px; background-size: cover; background-image: url('https://http2.mlstatic.com/D_NQ_NP_917685-MLB49794642888_042022-O.webp');">
            <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                <ul class="d-flex list-unstyled mt-auto text-dark">
                    <li class="d-flex align-items-center me-3"> 
                        <h1>1L</h1>
                    </li>
                    <li class="d-flex align-items-center">
                        <svg class="bi me-2" width="1em" height="1em">
                            <use xlink:href="#calendar3"></use>
                        </svg>
                        <h2>12 Bolas</h2>
                    </li>
                </ul>
            </div>
        </div>
        </a>
    </div> 
    
    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel"></h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div> 
        <div class="modal-body"> 
    
                <img class="img-fluid" width="180" src="https://static1.minhavida.com.br/articles/cd/34/02/f6/essa-e-a-razao-pela-qual-voce-nao-deve-guardar-alimentos-no-pote-de-sorvete-orig-1.jpg" alt="">
                <div>
                    <h3>Pote de Sorvete 1L</h3>
                    <p>Você pode escolher 12 bolas e coberturas</p>  
                </div>  
                
                <div class="d-flex justify-content-between bg-light border-3 p-3"> 
                    <span class="fs-4 fw-bold">Sabores Tradicionais</span>
                    <span class="fs-4 fw-bold">0 / 12 <span class="badge bg-secondary">Obrigatório</span></span>
                </div>
                <div class="d-flex align-items-center p-3 border"> 
                    <div class="p-2 flex-grow-1 text-start">
                        <img src="https://gelaboca.com.br/wp-content/webp-express/webp-images/doc-root/wp-content/uploads/2023/04/sabores-de-sorvete-morango-768x520.jpg.webp" class="" width="80" alt="..."> 
                        <span class="fw-bold">Morango</span> 
                    </div>
                    <div class="qty">
                        <span class="minus bg-dark">-</span>
                        <input type="number" class="count" name="qty" value="0">
                        <span class="plus bg-dark">+</span>
                    </div>
                </div>

                <div class="d-flex justify-content-between bg-light border-3 p-3">
                    <span class="fs-4 fw-bold">Sabores Premium</span> 
                </div>
                <div class="d-flex align-items-center p-3 border"> 
                    <div class="p-2 flex-grow-1 text-start">
                        <img src="https://gelaboca.com.br/wp-content/webp-express/webp-images/doc-root/wp-content/uploads/2023/04/sabores-de-sorvete-morango-768x520.jpg.webp" class="" width="80" alt="..."> 
                        <span class="fw-bold">Morango</span> 
                    </div>
                    <div class="qty">
                        <span class="minus bg-dark">-</span>
                        <input type="number" class="count" name="qty" value="0">
                        <span class="plus bg-dark">+</span>
                    </div>
                </div> 
    
        </div>  
        <div class="modal-footer">
            <button type="button" class="btn btn-primary btn-lg">Adicionar</button> 
        </div>
        </div>
    </div>
    </div>

    <div class="col">
        <div class="card border-0" style="height: 250px; background-size: cover; background-image: url('https://http2.mlstatic.com/D_NQ_NP_917685-MLB49794642888_042022-O.webp');">
            <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                <ul class="d-flex list-unstyled mt-auto text-dark">
                    <li class="d-flex align-items-center me-3"> 
                        <h1>1L</h1>
                    </li>
                    <li class="d-flex align-items-center">
                        <svg class="bi me-2" width="1em" height="1em">
                            <use xlink:href="#calendar3"></use>
                        </svg>
                        <h2>12 Bolas</h2>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="col">
        <div class="card border-0" style="height: 250px; background-size: cover; background-image: url('https://http2.mlstatic.com/D_NQ_NP_917685-MLB49794642888_042022-O.webp');">
            <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                <ul class="d-flex list-unstyled mt-auto text-dark">
                    <li class="d-flex align-items-center me-3"> 
                        <h1>1L</h1>
                    </li>
                    <li class="d-flex align-items-center">
                        <svg class="bi me-2" width="1em" height="1em">
                            <use xlink:href="#calendar3"></use>
                        </svg>
                        <h2>12 Bolas</h2>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="col">
        <div class="card border-0" style="height: 250px; background-size: cover; background-image: url('https://http2.mlstatic.com/D_NQ_NP_917685-MLB49794642888_042022-O.webp');">
            <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                <ul class="d-flex list-unstyled mt-auto text-dark">
                    <li class="d-flex align-items-center me-3"> 
                        <h1>1L</h1>
                    </li>
                    <li class="d-flex align-items-center">
                        <svg class="bi me-2" width="1em" height="1em">
                            <use xlink:href="#calendar3"></use>
                        </svg>
                        <h2>12 Bolas</h2>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="col">
        <div class="card border-0" style="height: 250px; background-size: cover; background-image: url('https://http2.mlstatic.com/D_NQ_NP_917685-MLB49794642888_042022-O.webp');">
            <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                <ul class="d-flex list-unstyled mt-auto text-dark">
                    <li class="d-flex align-items-center me-3"> 
                        <h1>1L</h1>
                    </li>
                    <li class="d-flex align-items-center">
                        <svg class="bi me-2" width="1em" height="1em">
                            <use xlink:href="#calendar3"></use>
                        </svg>
                        <h2>12 Bolas</h2>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div> 
{% endblock %}
{% block scripts %}
    <script>
        $(document).ready(function(){
            $('.count').prop('disabled', true);
            $(document).on('click','.plus',function(){
                $('.count').val(parseInt($('.count').val()) + 1 );
            });
            $(document).on('click','.minus',function(){
                $('.count').val(parseInt($('.count').val()) - 1 );
                    if ($('.count').val() == -1) {
                        $('.count').val(0);
                    }
                });
        });
    </script>
{% endblock scripts %}
```

```css
/* Contador */ 
.qty {
    width: 150px;
}
.qty .count {
    color: #000;
    display: inline-block;
    vertical-align: top;
    font-size: 25px;
    font-weight: 700;
    line-height: 30px;
    padding: 0 2px
    ;min-width: 35px;
    text-align: center;
}
.qty .plus {
    cursor: pointer;
    display: inline-block;
    vertical-align: top;
    color: white;
    width: 30px;
    height: 30px;
    font: 30px/1 Arial,sans-serif;
    text-align: center;
    border-radius: 50%;
    }
.qty .minus {
    cursor: pointer;
    display: inline-block;
    vertical-align: top;
    color: white;
    width: 30px;
    height: 30px;
    font: 30px/1 Arial,sans-serif;
    text-align: center;
    border-radius: 50%;
    background-clip: padding-box;
}
div {
    text-align: center;
}
.minus:hover{
    background-color: #717fe0 !important;
}
.plus:hover{
    background-color: #717fe0 !important;
}
/*Prevent text selection*/ 
input{  
    border: 0;
    width: 20%;
    text-align: center;
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
input:disabled{
    background-color:white;
}
```