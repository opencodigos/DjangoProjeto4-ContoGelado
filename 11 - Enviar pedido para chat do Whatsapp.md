**`views.py`**

```python
import pywhatkit as kit
```

```python
def enviar_whatsapp_pedido(request):
    pedido_id = request.POST.get('pedido_id', None) 
    
    print(pedido_id)
    try:
        pedido = Pedido.objects.get(pk=pedido_id) 
        # Número de telefone com código de país (por exemplo, +55 para BRA)
        numero = '+5516994256485'

        mensagem = f'''
        Data do Pedido: {pedido.data_pedido.strftime('%d/%m/%Y')}
        Status do Pedido: {'✅' if pedido.status else '❌'}
        Status do Pagamento: {'✅' if pedido.pago else '❌'}
        Status da Entrega: {'✅' if pedido.entrega else '❌'}

        Detalhes do Pedido: aqui

        Tempo estimado de entrega: 60min\n
        '''
        
        # Envie a mensagem
        kit.sendwhatmsg_instantly(numero, mensagem)
        return JsonResponse({'success': mensagem})
    except Pedido.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pedido não encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
```

```python
path('enviar-pedido-whatsapp/', views.enviar_whatsapp_pedido, name='enviar_whatsapp_pedido'),
```

**`meus-pedidos.html`**

```python
<script>
  $(document).ready(function() {
	  $('.whatsapp-btn').click(function() {
	      var id = $(this).data('id'); 
	      $.ajax({
	          url: "{% url 'enviar_whatsapp_pedido' %}", // Substitua pela URL correta
	          type: 'POST',
	          data: {
	              'pedido_id': id,
	              'csrfmiddlewaretoken': '{{ csrf_token }}' // Token CSRF
	          },
	          success: function(data) { 
	              // Feche o modal se necessário 
	              console.log(data)
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

**vamos da uma formatada na mensagem para adicionar os detalhes do nosso pedido**

```python
def format_message(pedido):
    detalhes = []
    for pote in pedido.itens_da_sacola.potes.all(): 
        detalhes.append(f"\n\nPote: {pote.quantidade}x {pote.embalagem.tipo}")
        sabores_str = "".join([f'\n{sel_sabor.quantidade_bolas}x {sel_sabor.sabor.nome}' for sel_sabor in pote.pote.all()])
        detalhes.append(f"\nSabor: \n{sabores_str}")
        descricao_coberturas = pote.obter_descricao_coberturas()
        if descricao_coberturas:
            detalhes.append("\nAdicionais:")
            detalhes.extend(f"- {desc}" for desc in descricao_coberturas.split(';'))
    detalhes.append(f"\n\nValor Total: R$ {pedido.itens_da_sacola.preco_total()}")
    return ''.join(detalhes)
```

```python
Detalhes do Pedido:{format_message(pedido)}
```