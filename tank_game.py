import concurrent.futures
import sys
import threading
import time
import pygame

from pygame.sprite import Group
from tank import Tank, Map
from config import CONFIG, COLORS, GAME_STATUS

if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(CONFIG.WINDOW_SIZE)


    pygame.display.set_caption("Tank game")
    game_status = GAME_STATUS.IN_PROGRESS

    tanks = Group()
    shoots = Group()
    maps = Group()

    map = Map(0, 0)
    maps.add(map)
    tank = Tank(screen)
    tanks.add(tank)
    # def inp():
    #     while True:
    #         tank.accelerate = float(input(f'{tank.accelerate=} =>'))
    #         tank.max_speed = float(input(f'{tank.max_speed=} =>'))
    #         tank.friction = float(input(f'{tank.friction} =>'))
    #
    # t1 = threading.Thread(target=inp, daemon=True)
    # t1.start()
    def prt():
        while True:
            time.sleep(0.1)
            print(f'{tank.gun_angle=}')
            print(f'{tank.shot_power=}')

    t2 = threading.Thread(target=prt, daemon=True)
    t2.start()
    while game_status == GAME_STATUS.IN_PROGRESS:
        clock.tick(CONFIG.FPS)
        screen.fill(COLORS.WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_status = GAME_STATUS.GAME_IS_OVER
                # sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_status = GAME_STATUS.GAME_IS_OVER
                elif event.key == pygame.K_SPACE:
                    tank.shot_direction()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if len(shoots) < 5:
                        shoots.add(tank.shot())
                    tank.shot_power = tank.max_speed

        if maps.sprites()[-1].rect.x <= 0:
            maps.add(Map(CONFIG.WIDTH, 0))
        # screen.blit(image, (-100,0))
        # screen.blit(image, (CONFIG.WIDTH-100,0))
        maps.update()
        shoots.update()
        tanks.update()

        maps.draw(screen)
        shoots.draw(screen)
        tanks.draw(screen)

        pygame.display.flip()

    pygame.quit()