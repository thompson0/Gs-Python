import random
import pygame
import webbrowser

import pygame.locals

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('sound_effect/rain.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

# Variáveis
linhas = 10
colunas = 10
total_casas = linhas * colunas
total_bombas = 10
link_aberto = False

def gerar_mapa():
    mapa = [0] * total_casas
    enchentes = random.sample(range(total_casas), total_bombas)
    for bomba in enchentes:
        linha = bomba // colunas
        coluna = bomba % colunas
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                nl = linha + dl
                nc = coluna + dc
                if 0 <= nl < linhas and 0 <= nc < colunas:
                    vizinho = nl * colunas + nc
                    if vizinho not in enchentes:
                        mapa[vizinho] += 1
    return mapa, enchentes

Mapa, enchentes = gerar_mapa()

# Layout
largura_quadrado = 60
altura_quadrado = 60
margem = 5
largura_grade = colunas * largura_quadrado + (colunas - 1) * margem
altura_grade = linhas * altura_quadrado + (linhas - 1) * margem
start_x = (800 - largura_grade) // 2
start_y = (800 - altura_grade) // 2
fonte = pygame.font.SysFont(None, 28)
fonte_grande = pygame.font.SysFont(None, 40)

# Janela
screen = pygame.display.set_mode((800, 800))
fundo_inicial = pygame.image.load('imgs/fundo.png').convert()
fundo_inicial = pygame.transform.scale(fundo_inicial, (800, 800))
fundo_game_over = pygame.image.load('imgs/game_over.png').convert()
fundo_game_over = pygame.transform.scale(fundo_game_over, (800, 800))
fundo_vitoria = pygame.image.load('imgs/vitoria.png').convert()
fundo_vitoria = pygame.transform.scale(fundo_vitoria, (800, 800))
casa_abrigo = pygame.image.load('imgs/abrigo.png').convert_alpha()
casa_abrigo = pygame.transform.scale(casa_abrigo, (largura_quadrado, altura_quadrado))
casa_enchente = pygame.image.load('imgs/enchente.png').convert()
casa_enchente = pygame.transform.scale(casa_enchente, (largura_quadrado, altura_quadrado))
msg_inicial = 'Chuvas intensas causaram alagamentos pela cidade.'
msg_explicao = 'Encontre os abrigos seguros!'
msg_entrada = 'Pressione ENTER para começar'
comandos = 'Os números nos abrigos clicados representam o número de enchentes por perto'
pygame.mouse.set_visible(1)

# Cores
cor_normal = (30, 60, 90)
cor_clicado = (59, 122, 165)
cor_texto = (169, 169, 169)
cor_texto_claro = (220, 220, 220)
cor_rect_texto = (0, 0, 0)

# Estados
clicados = set()
revelados = set()
game_over = False
vitoria = False
tela_inicial = True
clock = pygame.time.Clock()
running = True

def revelar_em_cadeia(index):
    if index in revelados or index in enchentes:
        return
    revelados.add(index)
    if Mapa[index] == 0:
        linha = index // colunas
        coluna = index % colunas
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                nl = linha + dl
                nc = coluna + dc
                if 0 <= nl < linhas and 0 <= nc < colunas:
                    vizinho = nl * colunas + nc
                    revelar_em_cadeia(vizinho)

while running:
    screen.fill((0, 0, 0))

    if tela_inicial:
        screen.blit(fundo_inicial, (0, 0))
        texto1 = fonte_grande.render(msg_inicial, True, cor_texto_claro)
        texto1_rect = texto1.get_rect(center=(400, 200))
        screen.blit(texto1, texto1_rect)
        texto2 = fonte_grande.render(msg_entrada, True, cor_texto_claro)
        texto2_rect = texto2.get_rect(center=(400, 660))
        screen.blit(texto2, texto2_rect)
        texto3 = fonte_grande.render(msg_explicao, True, cor_texto_claro)
        texto3_rect = texto3.get_rect(center=(400, 260))
        screen.blit(texto3, texto3_rect)

    elif game_over:
        screen.blit(fundo_game_over, (0, 0))

        # Botão Saiba Mais
        botao_info = pygame.Rect(300, 580, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), botao_info, border_radius=8)
        texto_info = fonte_grande.render("Saiba mais", True, (255, 255, 255))
        texto_info_rect = texto_info.get_rect(center=botao_info.center)
        screen.blit(texto_info, texto_info_rect)

        # Botão Reiniciar
        botao_rect = pygame.Rect(300, 650, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), botao_rect, border_radius=8)
        texto_botao = fonte_grande.render("Reiniciar", True, (255, 255, 255))
        texto_botao_rect = texto_botao.get_rect(center=botao_rect.center)
        screen.blit(texto_botao, texto_botao_rect)

    elif vitoria:
        screen.blit(fundo_vitoria, (0, 0))
        botao_rect = pygame.Rect(300, 720, 200, 50)
        pygame.draw.rect(screen, (0,0,0), botao_rect, border_radius=8)
        texto_botao = fonte_grande.render("Reiniciar", True, (255, 255, 255))
        texto_botao_rect = texto_botao.get_rect(center=botao_rect.center)
        screen.blit(texto_botao, texto_botao_rect)

    else:
        screen.blit(fundo_inicial, (0, 0))
        texto4 = fonte.render(comandos, True, cor_texto_claro)
        texto4_rect = texto4.get_rect(center=(400, 50))
        screen.blit(texto4, texto4_rect)
        for l in range(linhas):
            for c in range(colunas):
                index = l * colunas + c
                x = start_x + c * (largura_quadrado + margem)
                y = start_y + l * (altura_quadrado + margem)

                if index in revelados:
                    pygame.draw.rect(screen, cor_clicado, (x, y, largura_quadrado, altura_quadrado), border_radius=5)
                    if Mapa[index] > 0:
                        texto = fonte.render(str(Mapa[index]), True, cor_rect_texto)
                        texto_rect = texto.get_rect(center=(x + largura_quadrado // 2, y + altura_quadrado // 2))
                        screen.blit(texto, texto_rect)
                    ''' descomente esse codigo para ver onde as bombas estao
                    elif index in enchentes:
                        pygame.draw.rect(screen, (255, 0, 0), (x, y, largura_quadrado, altura_quadrado), border_radius=5)
                        screen.blit(casa_enchente, (x,y))
                    '''
                else:
                    screen.blit(casa_abrigo, (x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if tela_inicial and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            tela_inicial = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if game_over:
                botao_rect = pygame.Rect(300, 650, 200, 50)
                if botao_rect.collidepoint((mouse_x, mouse_y)):
                    Mapa, enchentes = gerar_mapa()
                    clicados.clear()
                    revelados.clear()
                    game_over = False
                    vitoria = False
                    tela_inicial = True
                    link_aberto = False
                    continue

                botao_info = pygame.Rect(300, 580, 200, 50)
                if botao_info.collidepoint((mouse_x, mouse_y)) and not link_aberto:
                    webbrowser.open("https://x.com/home")
                    link_aberto = True

            if vitoria:
                botao_rect = pygame.Rect(300, 720, 200, 50)
                if botao_rect.collidepoint((mouse_x, mouse_y)):
                    Mapa, enchentes = gerar_mapa()
                    clicados.clear()
                    revelados.clear()
                    game_over = False
                    vitoria = False
                    tela_inicial = True
                    link_aberto = False
                    continue

            if not tela_inicial and not vitoria and not game_over:
                for l in range(linhas):
                    for c in range(colunas):
                        index = l * colunas + c
                        x = start_x + c * (largura_quadrado + margem)
                        y = start_y + l * (altura_quadrado + margem)
                        rect = pygame.Rect(x, y, largura_quadrado, altura_quadrado)
                        if rect.collidepoint(mouse_x, mouse_y) and index not in revelados:
                            if index in enchentes:
                                game_over = True
                            else:
                                revelar_em_cadeia(index)
                            if total_casas - len(revelados) == total_bombas:
                                vitoria = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
