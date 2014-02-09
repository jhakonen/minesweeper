import sys
import pygame
from pygame import Rect
from gui.boardview import BoardView
from gui.tile import TileRenderer
from gui.meterview import MeterView
from definitions import MouseButton

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
    transparency = 225
    title = None
    title_item_margin = 30
    item_margin = 20
    children = []

    _items = []

    def __init__(self):
        self.title_font = pygame.font.SysFont("monospace", 18, bold=True)

    def __setattr__(self, name, value):
        super(MenuView, self).__setattr__(name, value)
        if name is "title":
            self.children.append(value)

    def add_menu_item(self, item):
        self._items.append(item)
        self.children.append(item)

    def paint(self, screen):
        self.update_rects(screen.get_size())
        # darken the game view
        bg = pygame.Surface(screen.get_size())
        bg.set_alpha(self.transparency)
        bg.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

    def update_rects(self, screen_size):
        start_h = self.get_start_height(screen_size[1])
        screen_rect = Rect((0, 0), screen_size)

        s = self.title.get_preferred_size()
        self.title.geometry = Rect((0, start_h), s)
        self.title.geometry.centerx = screen_size[0] / 2
        start_h += self.title.geometry.height + self.title_item_margin

        for item in self._items:
            s = item.get_preferred_size()
            item.geometry = Rect((0, start_h), s)
            item.geometry.centerx = screen_size[0] / 2
            start_h += item.geometry.height + self.item_margin

    def get_start_height(self, screen_height):
        title_size = self.title.get_preferred_size()
        h = title_size[1]
        h += self.title_item_margin

        for item in self._items:
            s = item.get_preferred_size()
            h += s[1]
        h += max(len(self._items) - 1, 0) * self.item_margin
        return (screen_height - h) / 2

    def mouse_move_event(self):
        return True

    def mouse_button_down_event(self, button):
        return True

    def mouse_button_up_event(self, button):
        return True

class Button(object):
    geometry = Rect(0, 0, 0, 0)
    children = []

    _pressed = False

    def __init__(self, label):
        self._label = label
        self.children.append(label)

    def get_preferred_size(self):
        return self._label.get_preferred_size()

    def paint(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.geometry)
        inner_rect = self.geometry.copy()
        inner_rect.inflate_ip(-2, -2)

        inner_color = (255, 255, 255)
        if self.is_mouse_over() and self._pressed:
            inner_color = (50, 50, 50)
        pygame.draw.rect(screen, inner_color, inner_rect)

        self._label.geometry = self.geometry.copy()

    def is_mouse_over(self):
        return self.geometry.collidepoint(pygame.mouse.get_pos())

    def mouse_button_down_event(self, button):
        self._pressed = button is MouseButton.LEFT and self.is_mouse_over()
        return self._pressed

    def mouse_button_up_event(self, button):
        handled = False
        if button is MouseButton.LEFT:
            if self._pressed and self.is_mouse_over():
                print "button '" + self._label.text + "' clicked"
                handled = True
            self._pressed = False
        return handled

class TextLabel(object):
    geometry = Rect(0, 0, 0, 0)
    color = (0, 0, 0)
    font_name = ""
    font_size = 12
    bold = False
    text = ""

    def __init__(self, text):
        self.text = text

    def get_preferred_size(self):
        return self.get_text_image().get_size()

    def get_text_image(self):
        font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
        return font.render(self.text, 1, self.color)

    def paint(self, screen):
        text = self.get_text_image()
        text_rect = text.get_rect()
        text_rect.center = self.geometry.center
        screen.blit(text, text_rect)

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
    menuview.title = create_menu_title("Minesweeper")
    menuview.add_menu_item(create_menu_item("Create New Game"))
    menuview.add_menu_item(create_menu_item("Change Difficulty: Easy"))
    menuview.add_menu_item(create_menu_item("Change Difficulty: Normal"))
    menuview.add_menu_item(create_menu_item("Change Difficulty: Hard"))
    menuview.add_menu_item(create_menu_item("Exit Game"))
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

def create_menu_title(text):
    label = TextLabel(text)
    label.color = (255, 255, 255)
    label.font_size = 18
    label.font_name = "monospace"
    label.bold = True
    return label

def create_menu_item(text):
    label = TextLabel(text)
    label.color = (0, 0, 0)
    label.font_size = 16
    label.font_name = "monospace"
    label.bold = True
    button = Button(label)
    return button

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
