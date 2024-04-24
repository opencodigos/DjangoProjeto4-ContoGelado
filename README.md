## Conto Gelado
Sistema simples de Sorveteria que envia mensagem para WhatsApp. 

Para envio de mensagem como vocês viram na previa vamos utilizar a biblioteca pywhatkit que é simples e muito eficiente. E vai atender nossas necessidades sem precisar de serviços pagos.

main.py

```jsx
import pywhatkit as kit

# Número de telefone com código de país (por exemplo, +55 para BRA)
numero = '+5516994256485'
mensagem = '''\
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

# Envie a mensagem
kit.sendwhatmsg_instantly(numero, mensagem)
```

Nesse tutorial vamos desenvolver um sistema de sorveteria com Django.

Pode iniciar o projeto pelo repositório abaixo. Ou assistir o video de configuração.

[Default (Completa)](https://www.notion.so/Default-Completa-1209d5cc61154078bc4865cbe145455e?pvs=21) 

**Github:**https://github.com/codloom/DjangoProjetoConfiguracao/tree/DjangoProjetoConfiguracaoCompleta

**Vídeo:** https://www.youtube.com/watch?v=tr3RkGkbEU4

Depois de feito as configurações iniciais e executado o projeto. 

Vamos para estrutura do projeto, vou começar pelo Backend. Depois vamos para frontend fazendo as views e tratamento no template. Vou usar Ajax, se preparem.