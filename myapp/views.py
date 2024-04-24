import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from myapp.forms import PedidoUpdateForm
from .models import Cobertura, Embalagem, MontaPote, Pedido, SacolaItens, SelCobertura, SelSabor, TipoSabor

import pywhatkit as kit

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def cardapio(request):
    embalagens = Embalagem.objects.filter(ativo=True)
    tipo_sabor = TipoSabor.objects.filter(ativo=True)
    coberturas = Cobertura.objects.filter(ativo=True)
    context = {
        'embalagens': embalagens,
        'tipo_sabor': tipo_sabor,
        'coberturas': coberturas,
    }
    return render(request, 'cardapio.html', context) 

# Adicionar itens na sacola
@login_required(login_url="/admin/login/")
def adicionar_sacola(request):
    if request.method == "POST": 
        try: 
            dados_str = request.POST.get('dados', None)
            dados = json.loads(dados_str) 
            print(dados) 

            embalagem_id = dados.get('embalagem_id', None)
            quantidade_pote = int(dados.get('quantidade_pote', None))
                        
            # Tente obter a sacola existente do usuário
            pedido = Pedido.objects.filter(
                user=request.user, status=True).first()

            # Se não existir uma sacola, crie uma nova
            if not pedido: 
                # Crie um novo pedido e associe a sacola criada
                pedido = Pedido.objects.create(user=request.user, status=True, pago=False,
                                            itens_da_sacola=SacolaItens.objects.create())

            monta_pote = MontaPote.objects.create(
                embalagem_id=embalagem_id, quantidade=quantidade_pote)

            for sabor in dados['sabores_selecionados']:
                SelSabor.objects.create(pote=monta_pote, 
                            sabor_id=sabor['sabor_id'], 
                            quantidade_bolas=sabor['quantidade']) 
                
            for cobertura in dados['cobertura_selecionadas']:
                # Adicione a cobertura ao pote durante a criação
                SelCobertura.objects.create(pote=monta_pote, 
                                        cobertura_id=cobertura['cobertura_id'], 
                                        quantidade_cobertura=cobertura['quantidade'])

            pedido.itens_da_sacola.potes.add(monta_pote)
            pedido.itens_da_sacola.preco_total()


            return JsonResponse({'status': 'success', 
                                 'message': 'Item adicionado na sacola com sucesso.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Requisição inválida.'})


@login_required(login_url="/admin/login/")
def atualiza_quantidade_sacola(request):
    if request.method == 'POST':
        pedido = Pedido.objects.filter(user=request.user, status=True).first()        
        
        pote_id = request.POST.get('poteId', None)
        novaQuantidade = request.POST.get('novaQuantidade', None)
        
        print(pote_id)
        print(novaQuantidade)

        pote = get_object_or_404(MontaPote, id=pote_id)
        pote.quantidade = int(novaQuantidade)
        pote.save()

        response = {
            'status': 'success',
            'message': 'Atualizado', 
            'novo_valor': f'R$ {pedido.itens_da_sacola.preco_total()}' 
        }
        return JsonResponse(response)
    else:
        # Se a requisição não for do tipo POST, você pode retornar um erro 
        # ou outra resposta apropriada
        return JsonResponse(
            {'status': 'error', 'message': 'Método não permitido'}, status=405)
    

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


@login_required(login_url="/admin/login/")
def meus_pedidos(request):
    meus_pedidos = Pedido.objects.filter(user=request.user)
    return render(request, 'meus-pedidos.html', 
                  {'meus_pedidos': meus_pedidos})


@login_required(login_url="/admin/login/")
def todos_pedidos(request):
    if request.user.is_superuser:
        todos_pedidos = Pedido.objects.all()
    else:
        return redirect('cardapio')
    return render(request, 
                  'gerencia-pedidos.html', {'todos_pedidos': todos_pedidos})


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
        pedido = Pedido.objects.get(pk=pedido_id)
        pedido.status = status
        pedido.pago = pago
        pedido.entrega = entrega
        pedido.save() 
        
        return JsonResponse({'success': True})
    except Pedido.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pedido não encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

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

        Detalhes do Pedido:{format_message(pedido)} 
        '''
        # Envia para whatsapp 
        kit.sendwhatmsg_instantly(numero, mensagem)

        return JsonResponse({'success': mensagem})
    except Pedido.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pedido não encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def format_message(pedido):
    detalhes = [] 
    for pote in pedido.itens_da_sacola.potes.all(): 
        detalhes.append(f"\n\nPote: {pote.quantidade}x {pote.embalagem.tipo}")
        sabores_str = "".join([f'\n{sel_sabor.quantidade_bolas}x {sel_sabor.sabor.nome}' for sel_sabor in pote.pote.all()])
        detalhes.append(f"\nSabor: \n{sabores_str}")
        # detalhes.append(f"\nSabor: \n{pote.obter_descricao_sabores()}")
        descricao_coberturas = pote.obter_descricao_coberturas()
        if descricao_coberturas:
            detalhes.append("\nAdicionais:")
            detalhes.extend(f"- {desc}" for desc in descricao_coberturas.split(';'))
    detalhes.append(f"\n\nValor Total: R$ {pedido.itens_da_sacola.preco_total()}")
    return ''.join(detalhes)

