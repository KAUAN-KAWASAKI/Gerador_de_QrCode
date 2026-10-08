"""
Gerador de QR Code em Python com vários tipos de entrada.

Tipos suportados:
    1. Texto simples
    2. Link (URL)
    3. Rede Wi-Fi (o celular conecta automaticamente ao ler)
    4. Contato (vCard - o celular oferece salvar na agenda)
    5. E-mail (abre o app de e-mail já com destinatário, assunto e mensagem)

Instalação da dependência:
    pip install qrcode[pil]

Uso:
    python main.py
"""

from urllib.parse import quote

import qrcode


# ---------------------------------------------------------------------------
# Funções auxiliares de entrada
# ---------------------------------------------------------------------------

def ler_obrigatorio(mensagem: str) -> str:
    """
    Pede um valor ao usuário e repete a pergunta até que ele digite algo.

    Parâmetros:
        mensagem: texto exibido no input.

    Retorna:
        O valor digitado, sem espaços nas pontas.
    """
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  Este campo é obrigatório. Tente novamente.")


def escapar_wifi(texto: str) -> str:
    r"""
    Escapa os caracteres especiais do formato Wi-Fi (\ ; , : ").

    Sem isso, uma senha como "abc;123" quebraria o QR Code, porque o
    ";" é usado como separador de campos nesse formato.
    """
    for caractere in ("\\", ";", ",", ":", '"'):
        texto = texto.replace(caractere, "\\" + caractere)
    return texto


# ---------------------------------------------------------------------------
# Funções que montam o conteúdo de cada tipo de QR Code
# ---------------------------------------------------------------------------

def montar_texto() -> str:
    """Retorna um texto livre digitado pelo usuário."""
    return ler_obrigatorio("Digite o texto: ")


def montar_link() -> str:
    """
    Pede um link e garante que ele comece com http:// ou https://.

    Sem o protocolo, muitos leitores de QR Code tratam o conteúdo como
    texto comum em vez de abrir o navegador.
    """
    link = ler_obrigatorio("Digite o link (ex: github.com): ")
    if not link.lower().startswith(("http://", "https://")):
        link = "https://" + link
    return link


def montar_wifi() -> str:
    """
    Monta o conteúdo no formato padrão de Wi-Fi:
        WIFI:T:<segurança>;S:<nome da rede>;P:<senha>;;

    Ao ler esse QR Code, Android e iPhone oferecem conectar à rede.
    """
    nome_rede = ler_obrigatorio("Nome da rede (SSID): ")

    print("Tipo de segurança: 1 - WPA/WPA2 (mais comum) | 2 - WEP | 3 - Sem senha")
    opcao = input("Escolha (Enter para 1): ").strip() or "1"
    seguranca = {"1": "WPA", "2": "WEP", "3": "nopass"}.get(opcao, "WPA")

    senha = ""
    if seguranca != "nopass":
        senha = ler_obrigatorio("Senha da rede: ")

    return (
        f"WIFI:T:{seguranca};"
        f"S:{escapar_wifi(nome_rede)};"
        f"P:{escapar_wifi(senha)};;"
    )


def montar_contato() -> str:
    """
    Monta um cartão de contato no formato vCard 3.0.

    Ao ler o QR Code, o celular mostra a opção de salvar o contato.
    Apenas o nome é obrigatório; os campos vazios são ignorados.
    """
    nome = ler_obrigatorio("Nome completo: ")
    telefone = input("Telefone (opcional): ").strip()
    email = input("E-mail (opcional): ").strip()
    empresa = input("Empresa (opcional): ").strip()

    linhas = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{nome}"]
    if telefone:
        linhas.append(f"TEL:{telefone}")
    if email:
        linhas.append(f"EMAIL:{email}")
    if empresa:
        linhas.append(f"ORG:{empresa}")
    linhas.append("END:VCARD")

    return "\n".join(linhas)


def montar_email() -> str:
    """
    Monta um link "mailto:" com destinatário, assunto e mensagem.

    O assunto e o corpo são codificados com quote() para que espaços
    e acentos funcionem corretamente dentro do link.
    """
    destinatario = ler_obrigatorio("E-mail do destinatário: ")
    assunto = input("Assunto (opcional): ").strip()
    corpo = input("Mensagem (opcional): ").strip()

    parametros = []
    if assunto:
        parametros.append("subject=" + quote(assunto))
    if corpo:
        parametros.append("body=" + quote(corpo))

    link = f"mailto:{destinatario}"
    if parametros:
        link += "?" + "&".join(parametros)
    return link


# Associa cada opção do menu ao seu nome e à função que monta o conteúdo.
# Para adicionar um novo tipo, basta criar a função e incluí-la aqui.
TIPOS = {
    "1": ("Texto simples", montar_texto),
    "2": ("Link (URL)", montar_link),
    "3": ("Rede Wi-Fi", montar_wifi),
    "4": ("Contato (vCard)", montar_contato),
    "5": ("E-mail", montar_email),
}


# ---------------------------------------------------------------------------
# Geração da imagem
# ---------------------------------------------------------------------------

def gerar_qrcode(conteudo: str, nome_arquivo: str = "qrcode.png") -> None:
    """
    Gera um QR Code a partir de um conteúdo e salva como imagem PNG.

    Parâmetros:
        conteudo: texto que será codificado no QR Code.
        nome_arquivo: caminho/nome do arquivo de saída.
    """
    qr = qrcode.QRCode(
        version=1,  # tamanho inicial da matriz (1 = 21x21); fit=True ajusta sozinho
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # recupera ~15% de dano
        box_size=10,  # tamanho de cada "quadradinho" em pixels
        border=4,  # margem em quadradinhos (mínimo recomendado é 4)
    )
    qr.add_data(conteudo)
    qr.make(fit=True)  # escolhe a menor versão que comporta o conteúdo

    imagem = qr.make_image(fill_color="black", back_color="white")
    imagem.save(nome_arquivo)
    print(f"\nQR Code salvo em: {nome_arquivo}")


def pedir_nome_arquivo() -> str:
    """Pede o nome do arquivo de saída e garante a extensão .png."""
    nome = input("Nome do arquivo (Enter para 'qrcode.png'): ").strip()
    if not nome:
        return "qrcode.png"
    if not nome.lower().endswith(".png"):
        nome += ".png"
    return nome


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def mostrar_menu() -> None:
    """Exibe as opções de tipo de QR Code disponíveis."""
    print("\n=== Gerador de QR Code ===")
    for codigo, (nome, _) in TIPOS.items():
        print(f"  {codigo} - {nome}")
    print("  0 - Sair")


def main() -> None:
    """
    Laço principal: mostra o menu, monta o conteúdo do tipo escolhido,
    gera a imagem e volta ao menu até o usuário escolher sair.
    """
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Até mais!")
            break

        if opcao not in TIPOS:
            print("Opção inválida.")
            continue

        nome_tipo, funcao_montar = TIPOS[opcao]
        print(f"\n--- {nome_tipo} ---")
        conteudo = funcao_montar()
        gerar_qrcode(conteudo, pedir_nome_arquivo())


if __name__ == "__main__":
    main()