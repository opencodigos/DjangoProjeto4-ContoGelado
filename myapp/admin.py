from django.contrib import admin 
from .models import *

admin.site.register(Embalagem)
admin.site.register(TipoSabor)
admin.site.register(Sabor)
admin.site.register(Cobertura)


# Monta Pote
class SelSaborInline(admin.TabularInline):
    model = SelSabor
    extra = 0

@admin.register(MontaPote)
class MontaPoteAdmin(admin.ModelAdmin):
    inlines = [
        SelSaborInline
    ] 

# Sacola de Itens
class MontaPoteInline(admin.TabularInline):
    model = SacolaItens.potes.through
    extra = 0

class PedidoInline(admin.StackedInline):
    model = Pedido
    extra = 0

@admin.register(SacolaItens)
class SacolaItensAdmin(admin.ModelAdmin):
    fields = ('preco',)
    readonly_fields = ('preco',)  # Adicione o campo readonly para mostrar o preço total
    inlines = [PedidoInline,MontaPoteInline]