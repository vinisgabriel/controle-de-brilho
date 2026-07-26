import sys
import pygame
import screen_brightness_control as sbc

# Inicialização do Pygame
pygame.init()

LARGURA, ALTURA = 900, 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Brightness Control")
relogio = pygame.time.Clock()

# Tenta ler o brilho atual do monitor ao abrir
try:
    brilho_atual = sbc.get_brightness(display=0)[0]
except Exception:
    brilho_atual = 50

# Cores e Fontes
COR_FUNDO = (240, 240, 240)
COR_TEXTO_TITULO = (30, 30, 30)
COR_TEXTO_NUMERO = (20, 20, 20)
COR_CIRCULO_EXTERNO = (80, 80, 80)
COR_CIRCULO_INTERNO = (0, 0, 0)

fonte_titulo = pygame.font.SysFont("segoe ui", 22, bold=True)
fonte_numeros = pygame.font.SysFont("segoe ui", 16)

# Configurações da Grade de Radio Buttons (0 a 100)
COLUNAS = 11
LARGURA_CELULA = 75
ALTURA_CELULA = 42
MARGEM_X = 40
MARGEM_Y = 100


def obter_posicao_item(valor):
    linha = valor // COLUNAS
    coluna = valor % COLUNAS
    x = MARGEM_X + (coluna * LARGURA_CELULA)
    y = MARGEM_Y + (linha * ALTURA_CELULA)
    return x, y


rodando = True
while rodando:
    relogio.tick(60)
    pos_mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Verifica qual radio button foi clicado
            for i in range(101):
                x, y = obter_posicao_item(i)
                # Raio de clique cobrindo o círculo e o número
                retangulo_clique = pygame.Rect(x - 12, y - 10, 60, 24)
                if retangulo_clique.collidepoint(pos_mouse):
                    brilho_atual = i
                    try:
                        sbc.set_brightness(brilho_atual)
                    except Exception:
                        pass
                    break

    # Desenho da interface
    tela.fill(COR_FUNDO)

    # Títulos da janela
    texto_titulo = fonte_titulo.render("Controle de Brilho avançado", True, COR_TEXTO_TITULO)
    tela.blit(texto_titulo, (MARGEM_X, 25))

    texto_subtitulo = fonte_titulo.render("Controle o Brilho", True, COR_TEXTO_TITULO)
    tela.blit(texto_subtitulo, (MARGEM_X, 60))

    # Desenho dos 101 Radio Buttons (0 a 100)
    for i in range(101):
        x, y = obter_posicao_item(i)

        # Círculo externo do radio button
        pygame.draw.circle(tela, COR_CIRCULO_EXTERNO, (x, y), 8, width=1)
        pygame.draw.circle(tela, (255, 255, 255), (x, y), 7)

        # Se estiver selecionado, desenha o "ponto" interno
        if i == brilho_atual:
            pygame.draw.circle(tela, COR_CIRCULO_INTERNO, (x, y), 4)

        # Número ao lado do botão
        texto_num = fonte_numeros.render(str(i), True, COR_TEXTO_NUMERO)
        tela.blit(texto_num, (x + 12, y - 10))

    pygame.display.flip()

pygame.quit()
sys.exit()