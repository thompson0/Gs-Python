import random
import pygame

pygame.init()

Mapa = [
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12
]

enchente = random.randint(2, 12)
print("Enchente em:", enchente)

screen = pygame.display.set_mode((640, 640))
fundo_inicial = pygame.image.load('imgs/tela_inicial.png').convert()
fundo_inicial = pygame.transform.scale(fundo_inicial, (640, 640))
msg_inicial = 'Este jogo destaca a importância dos abrigos em enchentes.'
msg_entrada = 'Pressione ENTER para começar'

fundo_img = pygame.image.load('imgs/fundo.png').convert()
fundo_img = pygame.transform.scale(fundo_img, (640, 640))

fundo_game_over = pygame.image.load('imgs/game_over.png').convert()
fundo_game_over = pygame.transform.scale(fundo_game_over, (640, 640))

pygame.mouse.set_visible(1)

largura_quadrado = 80
altura_quadrado = 80
margem = 10

largura_grade = 4 * largura_quadrado + 3 * margem
altura_grade = 3 * altura_quadrado + 2 * margem

start_x = (640 - largura_grade) // 2
start_y = (640 - altura_grade) // 2
fonte = pygame.font.SysFont(None, 28)
fonte_grande = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()
running = True

posicao_atual = 0
game_over = False
tela_inicial = True

cor_normal = (30, 60, 90)
cor_jogador = (200, 50, 50)
cor_texto = (255, 255, 255)

while running:
    if tela_inicial:
        screen.blit(fundo_inicial, (0, 0))

        texto1 = fonte.render(msg_inicial, True, cor_texto)
        texto1_rect = texto1.get_rect(center=(320, 260))
        screen.blit(texto1, texto1_rect)

        texto2 = fonte_grande.render(msg_entrada, True, cor_texto)
        texto2_rect = texto2.get_rect(center=(320, 320))
        screen.blit(texto2, texto2_rect)
    elif game_over:
        screen.blit(fundo_game_over, (0, 0))
    else:
        screen.blit(fundo_img, (0, 0))

        for l in range(3):
            for c in range(4):
                index = l * 4 + c
                valor = Mapa[index]

                x = start_x + c * (largura_quadrado + margem)
                y = start_y + l * (altura_quadrado + margem)

                if index == posicao_atual:
                    cor = cor_jogador
                else:
                    cor = cor_normal

                pygame.draw.rect(screen, cor, (x, y, largura_quadrado, altura_quadrado), border_radius=8)

                texto = fonte.render(str(valor), True, cor_texto)
                texto_rect = texto.get_rect(center=(x + largura_quadrado // 2, y + altura_quadrado // 2))
                screen.blit(texto, texto_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if tela_inicial and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                tela_inicial = False

        elif not tela_inicial and not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and posicao_atual + 4 < 12:
                posicao_atual += 4
            elif event.key == pygame.K_UP and posicao_atual - 4 >= 0:
                posicao_atual -= 4
            elif event.key == pygame.K_RIGHT and (posicao_atual % 4) < 3:
                posicao_atual += 1
            elif event.key == pygame.K_LEFT and (posicao_atual % 4) > 0:
                posicao_atual -= 1
            if posicao_atual + 1 == enchente:
                print('perdeu')
                game_over = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
