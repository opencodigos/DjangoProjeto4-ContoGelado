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