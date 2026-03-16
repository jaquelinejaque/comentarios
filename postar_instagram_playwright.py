"""
Automação para postar no Instagram usando Playwright.

Instale as dependências:
    pip install playwright
    playwright install chromium

Execute:
    python postar_instagram_playwright.py

Na primeira vez, o script fará login e salvará a sessão.
Nas próximas vezes, reutiliza a sessão salva (sem precisar logar de novo).
"""

import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ===================== CONFIGURAÇÃO =====================
# Login via Facebook
FACEBOOK_EMAIL = os.environ.get("FACEBOOK_EMAIL", "maicon@hotmail.com")
FACEBOOK_PASS = os.environ.get("FACEBOOK_PASS", "")
SESSION_DIR = os.path.join(os.path.dirname(__file__), ".instagram_session")
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "post_ia_futuro.png")

CAPTION = """🤖 O Futuro da Inteligência Artificial 🚀

A inteligência artificial está transformando o mundo como nunca antes. Veja o que nos espera:

🔮 Previsões para os próximos anos:

1️⃣ IA Generativa Avançada
2️⃣ Agentes Autônomos
3️⃣ IA na Saúde
4️⃣ Robótica Inteligente
5️⃣ IA Ética e Regulamentada

💡 O futuro não é sobre substituir humanos, mas sobre potencializar nossas capacidades!

via Pri Brand ✅

#InteligenciaArtificial #IA #FuturoDaTecnologia #AI #Tecnologia #Inovacao #TransformacaoDigital #FuturoDigital #IAGenerativa #MachineLearning
"""
# ========================================================


def verificar_credenciais():
    """Verifica se as credenciais do Facebook estão configuradas."""
    if not FACEBOOK_EMAIL or not FACEBOOK_PASS:
        print("=" * 60)
        print("⚠️  Configure suas credenciais do Facebook!")
        print()
        print("Opção 1 - Variáveis de ambiente:")
        print("  export FACEBOOK_EMAIL='maiconjjj@gmail.com'")
        print("  export FACEBOOK_PASS='sua_senha_do_facebook'")
        print()
        print("Opção 2 - Edite as variáveis no topo deste script")
        print("=" * 60)
        sys.exit(1)


def fazer_login(page):
    """Faz login no Instagram via Facebook."""
    print("🔐 Acessando Instagram...")
    page.goto("https://www.instagram.com/accounts/login/")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Aceitar cookies se aparecer
    for texto_cookie in ["Permitir todos os cookies", "Allow all cookies",
                         "Permitir cookies essenciais", "Allow essential"]:
        try:
            page.click(f"text={texto_cookie}", timeout=2000)
            time.sleep(1)
            break
        except PlaywrightTimeout:
            continue

    # Clicar em "Entrar com o Facebook" / "Log in with Facebook"
    print("📘 Entrando via Facebook...")
    fb_login_clicou = False
    fb_seletores = [
        'button:has-text("Entrar com o Facebook")',
        'button:has-text("Log in with Facebook")',
        'button:has-text("Continue with Facebook")',
        'button:has-text("Continuar com o Facebook")',
        '[data-testid="facebook-login-button"]',
        'text=Entrar com o Facebook',
        'text=Log in with Facebook',
    ]
    for seletor in fb_seletores:
        try:
            page.click(seletor, timeout=3000)
            fb_login_clicou = True
            break
        except PlaywrightTimeout:
            continue

    if not fb_login_clicou:
        print("❌ Não encontrou o botão 'Entrar com o Facebook'.")
        print("   Tentando login direto pelo Facebook...")
        page.goto("https://www.facebook.com/login/")
        page.wait_for_load_state("networkidle")
        time.sleep(2)

    # Aguardar a página do Facebook carregar
    time.sleep(3)

    # Se abriu popup do Facebook, trocar para ele
    if len(page.context.pages) > 1:
        fb_page = page.context.pages[-1]
        print("   Popup do Facebook detectado...")
    else:
        fb_page = page

    fb_page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Aceitar cookies do Facebook se aparecer
    for texto_cookie in ["Permitir todos os cookies", "Allow all cookies",
                         "Permitir cookies", "Allow cookies"]:
        try:
            fb_page.click(f"text={texto_cookie}", timeout=2000)
            time.sleep(1)
            break
        except PlaywrightTimeout:
            continue

    # Preencher email e senha do Facebook
    print(f"   E-mail: {FACEBOOK_EMAIL}")
    try:
        fb_page.fill('input[name="email"]', FACEBOOK_EMAIL)
        fb_page.fill('input[name="pass"]', FACEBOOK_PASS)
        time.sleep(1)
        fb_page.click('button[name="login"]', timeout=5000)
    except PlaywrightTimeout:
        try:
            fb_page.click('input[type="submit"]', timeout=3000)
        except PlaywrightTimeout:
            fb_page.click('button[type="submit"]', timeout=3000)

    print("   Aguardando autenticação...")
    time.sleep(5)

    # Se estava no popup, ele deve fechar. Voltar para a página principal
    if len(page.context.pages) > 1:
        try:
            # Aguardar popup fechar
            fb_page.wait_for_event("close", timeout=15000)
        except PlaywrightTimeout:
            # Se o popup pediu confirmação, clicar em continuar
            try:
                fb_page.click('button:has-text("Continuar")', timeout=3000)
            except PlaywrightTimeout:
                try:
                    fb_page.click('button:has-text("Continue")', timeout=3000)
                except PlaywrightTimeout:
                    pass

    # Voltar para a página do Instagram
    time.sleep(3)
    page.wait_for_load_state("networkidle")

    # Se foi redirecionado para o Facebook completo, navegar para o Instagram
    if "facebook.com" in page.url:
        page.goto("https://www.instagram.com/")
        page.wait_for_load_state("networkidle")
        time.sleep(3)

    # Verificar se o login funcionou
    if "/accounts/login" in page.url:
        print("❌ Falha no login via Facebook. Verifique suas credenciais.")
        print("   Dica: se tem autenticação de dois fatores, desative temporariamente.")
        sys.exit(1)

    # Fechar popups pós-login
    fechar_popups(page)
    print("✅ Login via Facebook realizado com sucesso!")


def fechar_popups(page):
    """Fecha popups comuns do Instagram (notificações, salvar login, etc)."""
    popups = [
        "text=Agora não",
        "text=Not Now",
        "text=Agora Não",
        "text=Salvar informações",
        "text=Save Info",
    ]
    for popup in popups:
        try:
            page.click(popup, timeout=3000)
            time.sleep(1)
        except PlaywrightTimeout:
            pass


def postar_imagem(page, image_path, caption):
    """Posta uma imagem no Instagram."""
    image_abs = str(Path(image_path).resolve())

    if not Path(image_abs).exists():
        print(f"❌ Imagem não encontrada: {image_abs}")
        print("   Execute primeiro: python post_instagram.py")
        sys.exit(1)

    print(f"📸 Preparando post com imagem: {image_abs}")

    # Clicar no botão de criar post (ícone +)
    try:
        # Tentar diferentes seletores para o botão de criar
        criar_seletores = [
            'svg[aria-label="Nova publicação"]',
            'svg[aria-label="New post"]',
            'svg[aria-label="Novo post"]',
            '[aria-label="Nova publicação"]',
            '[aria-label="New post"]',
        ]
        clicou = False
        for seletor in criar_seletores:
            try:
                page.click(seletor, timeout=3000)
                clicou = True
                break
            except PlaywrightTimeout:
                continue

        if not clicou:
            # Fallback: tentar pelo menu lateral
            page.click('a[href="/create/"]', timeout=3000)

    except PlaywrightTimeout:
        print("❌ Não foi possível encontrar o botão de criar post.")
        print("   O layout do Instagram pode ter mudado.")
        sys.exit(1)

    time.sleep(2)

    # Upload da imagem
    print("📤 Enviando imagem...")
    file_input = page.locator('input[type="file"]')
    file_input.set_input_files(image_abs)
    time.sleep(3)

    # Avançar etapas do criador de post
    avancar_labels = [
        "text=Avançar",
        "text=Next",
        "text=Próximo",
    ]

    # Etapa 1: Cortar/ajustar -> Avançar
    for label in avancar_labels:
        try:
            page.click(label, timeout=5000)
            break
        except PlaywrightTimeout:
            continue
    time.sleep(2)

    # Etapa 2: Filtros -> Avançar
    for label in avancar_labels:
        try:
            page.click(label, timeout=5000)
            break
        except PlaywrightTimeout:
            continue
    time.sleep(2)

    # Etapa 3: Escrever legenda
    print("✍️  Escrevendo legenda...")
    try:
        legenda_seletores = [
            'textarea[aria-label="Escreva uma legenda..."]',
            'textarea[aria-label="Write a caption..."]',
            'div[aria-label="Escreva uma legenda..."]',
            'div[aria-label="Write a caption..."]',
            'textarea',
        ]
        for seletor in legenda_seletores:
            try:
                campo = page.locator(seletor).first
                campo.click(timeout=3000)
                campo.fill(caption)
                break
            except (PlaywrightTimeout, Exception):
                continue
    except Exception as e:
        print(f"⚠️  Não foi possível adicionar legenda: {e}")

    time.sleep(1)

    # Compartilhar
    print("🚀 Publicando...")
    compartilhar_labels = [
        "text=Compartilhar",
        "text=Share",
        "text=Publicar",
    ]
    for label in compartilhar_labels:
        try:
            page.click(label, timeout=5000)
            break
        except PlaywrightTimeout:
            continue

    # Aguardar conclusão
    time.sleep(5)

    # Verificar se apareceu confirmação
    try:
        page.wait_for_selector("text=Sua foto foi compartilhada", timeout=15000)
        print("✅ Post publicado com sucesso no Instagram!")
    except PlaywrightTimeout:
        try:
            page.wait_for_selector("text=Your photo was shared", timeout=5000)
            print("✅ Post publicado com sucesso no Instagram!")
        except PlaywrightTimeout:
            print("⚠️  Post possivelmente publicado. Verifique seu perfil no Instagram.")


def main():
    verificar_credenciais()

    print("=" * 60)
    print("🤖 Instagram Auto-Poster com Playwright")
    print(f"   Login via Facebook: {FACEBOOK_EMAIL}")
    print(f"   Imagem:  {IMAGE_PATH}")
    print("=" * 60)

    with sync_playwright() as p:
        # Usar contexto persistente para salvar sessão
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            viewport={"width": 430, "height": 932},
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        # Verificar se já está logado
        page.goto("https://www.instagram.com/")
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # Fechar popups iniciais
        fechar_popups(page)

        # Checar se precisa logar
        if "/accounts/login" in page.url or page.locator('input[name="username"]').count() > 0:
            fazer_login(page)

        # Postar
        postar_imagem(page, IMAGE_PATH, CAPTION)

        time.sleep(3)
        browser.close()

    print("\n🎉 Processo finalizado!")


if __name__ == "__main__":
    main()
