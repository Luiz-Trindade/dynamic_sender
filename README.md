# 🚀 Dynamic Sender

Envie mensagens em massa usando múltiplas sessões da API [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js) com controle inteligente de sessões para escalabilidade e desempenho.

---

## Tecnologias

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)
![ThreadPoolExecutor](https://img.shields.io/badge/ThreadPoolExecutor-Multithreading-blue?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-F97600?style=for-the-badge&logo=matplotlib&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF-red?style=for-the-badge)

---

## Funcionalidades

- Envio paralelo de mensagens via múltiplas sessões WhatsApp
- Controle do número máximo de sessões ativas
- Registro de mensagens com timestamp e sessão associada
- Escalonamento dinâmico para ativar/desativar sessões
- Suporta alta escala com milhares de mensagens

---

## Como usar

1. Instale dependências:
```bash
pip install matplotlib reportlab
```

2. Configure suas mensagens (exemplo em `sample_messages_10k.py`)

3. Defina o limite de sessões ativas em `max_active_sessions`

4. Execute:

```bash
python main.py
```

---

## Contato

Luiz Trindade — [luiz@example.com](mailto:luiz@example.com)

---

Made with ❤️ by Luiz
