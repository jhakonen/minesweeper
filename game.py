import sys
import pygame
from pygame import Rect
from gui.boardview import BoardView
from gui.tile import TileRenderer
from gui.meterview import MeterView

class Root(object):
    children = []

class GameView(object):
    children = []

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

class MenuView(object):
    def paint(self, screen):
        # darken the game view
        bg = pygame.Surface(screen.get_size())
        bg.set_alpha(225)
        bg.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

    def mouse_move_event(self):
        return True

    def mouse_button_down_event(self, button):
        return True

    def mouse_button_up_event(self, button):
        return True

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

    root = Root()

    gameview = GameView(BG_TILE_IMG, FIELD_RECT)
    root.children.append(gameview)

    menuview = MenuView()
    menuview.visible = False
    root.children.append(menuview)

    boardview = BoardView(TileRenderer())
    boardview.geometry = Rect(50, 50, 300, 300)
    boardview.rows = 16
    boardview.cols = 16
    gameview.children.append(boardview)

    time_counter = MeterView("Time")
    time_counter.geometry = Rect(boardview.geometry.left, boardview.geometry.bottom + METER_BOARD_MARGIN, METER_WIDTH, METER_HEIGHT)
    gameview.children.append(time_counter)

    mine_counter = MeterView("Mines")
    mine_counter.geometry = Rect(boardview.geometry.right - METER_WIDTH, boardview.geometry.bottom + METER_BOARD_MARGIN, METER_WIDTH, METER_HEIGHT)
    gameview.children.append(mine_counter)

    while True:
        time_passed = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type is pygame.MOUSEMOTION:
                handle_event(root, "mouse_move")
            elif event.type is pygame.MOUSEBUTTONDOWN:
                handle_event(root, "mouse_button_down", button=event.button)
            elif event.type is pygame.MOUSEBUTTONUP:
                handle_event(root, "mouse_button_up", button=event.button)
            elif event.type is pygame.KEYDOWN:
                if event.key is pygame.K_ESCAPE:
                    menuview.visible = not is_visible(menuview)

        paint(screen, root)
        pygame.display.flip()

def paint(screen, target):
    if is_visible(target):
        get_method(target, "paint")(screen)
        # paint children recursively
        for child in get_children(target):
            paint(screen, child)

def is_visible(target):
    return getattr(target, "visible", True)

def get_method(target, name):
    def does_nothing(*args, **kwargs):
        pass
    return getattr(target, name, does_nothing)

def get_children(target):
    return getattr(target, "children", [])

def handle_event(target, name, *args, **kwargs):
    if is_visible(target):
        # call children's event handlers, leaving immediately if the handler tells
        # that it has handled the event
        for child in reversed(get_children(target)):
            if handle_event(child, name, *args, **kwargs) is True:
                return True
        # call 'target's' event handler method
        return get_method(target, name + "_event")(*args, **kwargs)

def exit_game():
    sys.exit()

run_game()
