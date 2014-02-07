import sys
import pygame
from pygame import Rect
from gui.boardview import BoardView
from gui.tile import TileRenderer
from gui.meterview import MeterView
from utils import CallableWrapper

event_listeners = CallableWrapper()
paintables = CallableWrapper()

class Background(object):
    def __init__(self, tile_img_file, field_rect):
        self.tile_img_file = tile_img_file
        self.field_rect = field_rect

    def paint(self, screen):
        tile_img = pygame.image.load(self.tile_img_file).convert_alpha()
        img_rect = tile_img.get_rect()

        nrows = int(screen.get_height() / img_rect.height) + 1
        ncols = int(screen.get_width() / img_rect.width) + 1

        for y in range(nrows):
            for x in range(ncols):
                img_rect.topleft = (x * img_rect.width,
                                    y * img_rect.height)
                screen.blit(tile_img, img_rect)

        field_color = (109, 41, 1)
        boundary_rect = Rect(   self.field_rect.left - 4,
                                self.field_rect.top - 4,
                                self.field_rect.width + 8,
                                self.field_rect.height + 8)
        pygame.draw.rect(screen, (0, 0, 0), boundary_rect)
        pygame.draw.rect(screen, field_color, self.field_rect)


def run_game():
    # Game parameters
    SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
    FIELD_RECT = Rect(50, 50, 300, 300)
    BG_TILE_IMG = 'gui/images/brick_tile.png'
    METER_WIDTH = 100
    METER_HEIGHT = 30
    METER_BOARD_MARGIN = 10

    pygame.init()
    screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    bg = Background(BG_TILE_IMG, FIELD_RECT)

    boardview = BoardView(TileRenderer())
    boardview.geometry = Rect(50, 50, 300, 300)
    boardview.rows = 16
    boardview.cols = 16

    time_counter = MeterView("Time")
    time_counter.geometry = Rect(boardview.geometry.left, boardview.geometry.bottom + METER_BOARD_MARGIN, METER_WIDTH, METER_HEIGHT)

    mine_counter = MeterView("Mines")
    mine_counter.geometry = Rect(boardview.geometry.right - METER_WIDTH, boardview.geometry.bottom + METER_BOARD_MARGIN, METER_WIDTH, METER_HEIGHT)

    event_listeners.append(boardview)
    paintables.append(bg)
    paintables.append(boardview)
    paintables.append(time_counter)
    paintables.append(mine_counter)

    while True:
        time_passed = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type is pygame.MOUSEMOTION:
                event_listeners.mouse_move_event()
            elif event.type is pygame.MOUSEBUTTONDOWN:
                event_listeners.mouse_button_down_event(button=event.button)
            elif event.type is pygame.MOUSEBUTTONUP:
                event_listeners.mouse_button_up_event(button=event.button)

        paintables.paint(screen)
        pygame.display.flip()

def exit_game():
    sys.exit()

run_game()
