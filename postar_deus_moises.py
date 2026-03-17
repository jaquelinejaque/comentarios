"""
Script para postar o post do Deus de Moisés no Instagram usando instagrapi.

Na sua máquina local:
    pip install instagrapi Pillow
    python postar_deus_moises.py

Configuração via variáveis de ambiente (opcional):
    export INSTAGRAM_USER="seu_email"
    export INSTAGRAM_PASS="sua_senha"
"""

import os
import sys
from pathlib import Path

try:
    from instagrapi import Client
except ImportError:
    print("❌ Biblioteca instagrapi não instalada.")
    print("   Execute: pip install instagrapi Pillow")
    sys.exit(1)

# ===================== CONFIGURAÇÃO =====================
INSTAGRAM_USER = os.environ.get("INSTAGRAM_USER", "maiconpode@hotmail.com")
INSTAGRAM_PASS = os.environ.get("INSTAGRAM_PASS", "Maicon26.")
IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "post_deus_moises.png")

CAPTION = """🔥 O DEUS DE MOISÉS 🔥

O Deus que abriu o Mar Vermelho é o mesmo Deus que abre caminhos na sua vida!

📖 Lições poderosas da história de Moisés:

1️⃣ Deus chama os imperfeitos — Moisés gaguejava, mas Deus o escolheu para libertar um povo inteiro. Suas limitações não limitam Deus!

2️⃣ A sarça que arde e não se consome — Deus se revelou no lugar mais improvável. Ele pode se revelar a você hoje, onde você estiver.

3️⃣ "EU SOU O QUE SOU" — Deus não precisa de apresentação. Ele é o mesmo ontem, hoje e sempre. (Êxodo 3:14)

4️⃣ O Mar se abriu! — Quando não havia saída, Deus criou um caminho no meio do impossível. Ele faz o mesmo por você!

5️⃣ O deserto tem propósito — 40 anos no deserto não foram castigo, foram preparação. Seu deserto também tem propósito!

💪 Se Deus é por nós, quem será contra nós? (Romanos 8:31)

🙏 O mesmo Deus de Moisés é o SEU Deus. Confie!

#DeusDeMoises #Fe #Biblia #DeusEFiel #PalavradeDeus #ExodoBiblico #MarVermelho #Jesus #Cristo #VidaCrista #FeCrista #DevocionalDiario #MensagemDeDeus
"""
# ========================================================


def gerar_imagem():
    """Gera a imagem do post se ela não existir."""
    if Path(IMAGE_PATH).exists():
        print(f"✅ Imagem já existe: {IMAGE_PATH}")
        return

    print("🎨 Gerando imagem do post...")
    from post_deus_moises import criar_imagem
    criar_imagem(IMAGE_PATH)


def postar():
    """Faz login e posta no Instagram."""
    if not Path(IMAGE_PATH).exists():
        gerar_imagem()

    if not Path(IMAGE_PATH).exists():
        print("❌ Imagem não encontrada e não foi possível gerar.")
        sys.exit(1)

    print("=" * 50)
    print("🔥 POSTANDO NO INSTAGRAM - DEUS DE MOISÉS")
    print(f"   Conta: {INSTAGRAM_USER}")
    print(f"   Imagem: {IMAGE_PATH}")
    print("=" * 50)

    # Login
    print("\n🔐 Fazendo login no Instagram...")
    cl = Client()

    session_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".instagrapi_session.json")
    try:
        if Path(session_file).exists():
            cl.load_settings(session_file)
            cl.login(INSTAGRAM_USER, INSTAGRAM_PASS)
            cl.get_timeline_feed()
            print("   Sessão anterior reutilizada!")
        else:
            raise Exception("Sem sessão salva")
    except Exception:
        print("   Fazendo login novo...")
        cl = Client()
        cl.login(INSTAGRAM_USER, INSTAGRAM_PASS)

    cl.dump_settings(session_file)
    print("✅ Login realizado com sucesso!")

    # Postar
    print("\n📤 Enviando post...")
    media = cl.photo_upload(
        path=IMAGE_PATH,
        caption=CAPTION,
    )
    print(f"\n🎉 POST PUBLICADO COM SUCESSO!")
    print(f"   ID do post: {media.pk}")
    print(f"   Link: https://www.instagram.com/p/{media.code}/")


if __name__ == "__main__":
    postar()
