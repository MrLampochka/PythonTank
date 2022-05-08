from dataclasses import dataclass


@dataclass(frozen=True)
class CONFIG:
    # screen config
    WIDTH = 1200
    HEIGHT = 600
    WINDOW_SIZE = (WIDTH, HEIGHT)
    FPS = 60

    # tank config
    GRAVITATION = 0.1
    TANK_POSITION = (WIDTH/100,HEIGHT - HEIGHT/20)
    MAX_SPEED = 6
    ACCELERATE = 0.5
    MAX_SHOT_POWER = 100
    TANK_SIZE = (HEIGHT/4, HEIGHT/4)

    #bullet config
    BULLET_TTL = 10
    BULLET_SIZE = (15, 15)




@dataclass(frozen=True)
class COLORS:
    WHITE = (255, 255, 255)
    BG_COLOR = (0, 0, 0)
    BULLET = (0, 0, 0)


@dataclass(frozen=True)
class GAME_STATUS:
    IN_PROGRESS = True
    GAME_IS_OVER = False