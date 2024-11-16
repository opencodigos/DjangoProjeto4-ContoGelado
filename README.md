# 🍦 Sistema de Sorveteria com Envio de Mensagens para WhatsApp

## 📝 Descrição do Projeto

Este é um sistema simples de gerenciamento de sorveteria desenvolvido com Django, que permite ao usuário fazer pedidos de sorvetes e enviar as informações diretamente para o WhatsApp. O sistema oferece funcionalidades de cadastro de sabores, pedidos e integração com a API do WhatsApp para comunicação direta.

## ⚙️ Funcionalidades

- **Cadastro de Sabores**:
    - Possibilidade de adicionar, editar e excluir sabores de sorvete.
- **Pedidos**:
    - Os clientes podem selecionar os sabores desejados e realizar um pedido.
    - Geração de mensagem automática para WhatsApp com as informações do pedido.
- **Envio de Mensagens para WhatsApp**:
    - Após o pedido, o sistema envia os detalhes do pedido para um número de WhatsApp pré-configurado.
- **Integração com API do WhatsApp**:
    - Utilização de uma API para enviar a mensagem diretamente para o WhatsApp. (pywhatkit)

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python, Django
- **Banco de Dados**: SQLite3 (ou outro banco de dados configurado)
- **Frontend**: HTML, CSS, JavaScript, Ajax
- **API do WhatsApp**: API para envio de mensagens (pywhatkit)

## 📋 Pré-requisitos

Antes de iniciar o projeto, certifique-se de que os seguintes itens estão instalados:

- Python (python==3.*)
- Whatsapp (pywhatkit)
- Pip (gerenciador de pacotes do Python)

## 🌟 Fluxo do Sistema

- Cadastro de sabores de sorvete.
- Clientes podem realizar pedidos de sorvetes.
- Pedido é enviado para o número de WhatsApp configurado.

## 🖌️ Frontend

A interface foi construída com templates Django utilizando Ajax para enviar os dados do pedido sem a necessidade de recarregar a página.

**Vídeo de configuração do projeto:** [Assistir no YouTube](https://www.youtube.com/watch?v=tr3RkGkbEU4)