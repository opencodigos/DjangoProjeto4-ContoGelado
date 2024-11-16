### Envio de Mensagem com PyWhatKit

Para enviar mensagens, utilizaremos a biblioteca **pywhatkit**, que é simples, eficiente e atende às nossas necessidades sem a necessidade de serviços pagos.

### Exemplo de Código (`main.py`):

```python
import pywhatkit as kit

# Número de telefone com código de país (exemplo: +55 para Brasil)
numero = '+5516994256485'

# Mensagem a ser enviada
mensagem = '''\\
Açaí na Tigela 400g
Sabor: Açaí Tradicional

Adicionais:
- 1x Creme de Ninho
- 1x Leite Ninho
- 1x Morango

Pote: 1/5 litro

Sabores:
- 1x Chocolate Trufado
- 1x Flocos
- 1x Laka Cremoso

Adicionais:
- 1x Creme de Ninho
- 1x Leite Ninho
- 1x Morango

Total: R$ 45,99

Tempo estimado de entrega: 60min
'''

# Envio da mensagem instantânea
kit.sendwhatmsg_instantly(numero, mensagem)

```

### Detalhes:

- **`pywhatkit`** é uma biblioteca para automação de tarefas no WhatsApp.
- **`sendwhatmsg_instantly()`** envia a mensagem de forma instantânea para o número especificado.
- O número deve ser incluído com o código do país (por exemplo, `+55` para Brasil).
- A mensagem pode ser personalizada conforme necessário.