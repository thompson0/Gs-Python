import random
import pygame

pygame.init()

Mapa = [
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12
]

enchente = random.randint(0, 11)
print("Enchente em:", enchente)

screen = pygame.display.set_mode((640, 640))
fundo_img = pygame.image.load('fundo.png').convert()
fundo_img = pygame.transform.scale(fundo_img, (640, 640))

pygame.mouse.set_visible(1)

largura_quadrado = 80
altura_quadrado = 80
margem = 10

largura_grade = 4 * largura_quadrado + 3 * margem
altura_grade = 3 * altura_quadrado + 2 * margem

start_x = (640 - largura_grade) // 2
start_y = (640 - altura_grade) // 2
fonte = pygame.font.SysFont(None, 36)  

clock = pygame.time.Clock()
running = True

posicao_atual = 0  

while running:
    screen.blit(fundo_img, (0, 0))

    for l in range(3):  
        for c in range(4): 
            index = l * 4 + c
            valor = Mapa[index]

            x = start_x + c * (largura_quadrado + margem)
            y = start_y + l * (altura_quadrado + margem)

            if index == posicao_atual:
                cor = (255, 0, 0)
            else:
                cor = (0, 100, 200)
            pygame.draw.rect(screen, cor, (x, y, largura_quadrado, altura_quadrado))

            texto = fonte.render(str(valor), True, (255, 255, 255))     
            texto_rect = texto.get_rect(center=(x + largura_quadrado // 2, y + altura_quadrado // 2))
            screen.blit(texto, texto_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
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
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()
