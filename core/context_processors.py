# from myapp import models

from myapp.models import Pedido


def context_social(request):
    return {'social': 'Exibir este contexto em qualquer lugar!'}

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