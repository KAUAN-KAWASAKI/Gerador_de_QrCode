# Gerador de QR Code

Gerador de QR Code em **Python**, via terminal, que cria imagens PNG a partir de diferentes tipos de conteúdo: texto, links, redes Wi-Fi, contatos e e-mails.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![qrcode](https://img.shields.io/badge/lib-qrcode-black)

---

## Funcionalidades

| Opção | Tipo | O que acontece ao ler o QR Code |
|:-----:|------|---------------------------------|
| 1 | **Texto simples** | Exibe o texto digitado |
| 2 | **Link (URL)** | Abre o navegador no endereço (adiciona `https://` automaticamente se faltar) |
| 3 | **Rede Wi-Fi** | O celular oferece conectar à rede automaticamente (WPA/WPA2, WEP ou sem senha) |
| 4 | **Contato (vCard)** | O celular oferece salvar o contato na agenda |
| 5 | **E-mail** | Abre o app de e-mail com destinatário, assunto e mensagem preenchidos |

Outros detalhes:

- Escapa caracteres especiais em nomes e senhas de Wi-Fi (`\ ; , : "`), evitando QR Codes inválidos.
- Codifica assunto e corpo do e-mail para suportar espaços e acentos.
- Ajusta o tamanho do QR Code automaticamente ao conteúdo.
- Usa correção de erro nível **M** (recupera ~15% de dano na imagem).
- Permite escolher o nome do arquivo de saída (padrão: `qrcode.png`).

---

## Como usar

### Pré-requisitos

- Python 3.8 ou superior

### Instalação

```bash
git clone https://github.com/KAUAN-KAWASAKI/Gerador_de_QrCode.git
cd Gerador_de_QrCode
pip install "qrcode[pil]"
```

### Execução

```bash
python main.py
```

### Exemplo

```text
=== Gerador de QR Code ===
  1 - Texto simples
  2 - Link (URL)
  3 - Rede Wi-Fi
  4 - Contato (vCard)
  5 - E-mail
  0 - Sair
Escolha uma opção: 3

--- Rede Wi-Fi ---
Nome da rede (SSID): MinhaCasa
Tipo de segurança: 1 - WPA/WPA2 (mais comum) | 2 - WEP | 3 - Sem senha
Escolha (Enter para 1):
Senha da rede: senha123
Nome do arquivo (Enter para 'qrcode.png'): wifi

QR Code salvo em: wifi.png
```

A imagem é salva na pasta em que o programa foi executado.

---

## Formatos gerados

| Tipo | Formato do conteúdo |
|------|---------------------|
| Wi-Fi | `WIFI:T:WPA;S:<rede>;P:<senha>;;` |
| Contato | vCard 3.0 (`BEGIN:VCARD` … `END:VCARD`) com nome, telefone, e-mail e empresa |
| E-mail | `mailto:<destinatario>?subject=...&body=...` |

---

## Adicionando um novo tipo

O menu é gerado a partir do dicionário `TIPOS` em `main.py`. Para adicionar um novo tipo de QR Code, crie uma função que retorne o conteúdo e registre-a:

```python
def montar_telefone() -> str:
    numero = ler_obrigatorio("Número de telefone: ")
    return f"tel:{numero}"

TIPOS = {
    # ...
    "6": ("Telefone", montar_telefone),
}
```

---

## Estrutura do projeto

```text
Gerador_de_QrCode/
├── main.py     # Código-fonte do gerador
└── README.md
```

---

## Autor

**Kauan Kawasaki** - [@KAUAN-KAWASAKI](https://github.com/KAUAN-KAWASAKI)
