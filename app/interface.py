import pygame as pg

pg.init()

color_inactive = pg.Color((53,102,102))
color_active = pg.Color((120, 240, 220))
color = color_inactive
font = pg.font.SysFont('arial', 32)

class InputBox:
    def __init__(self, x, y, w, h, text='Название кобинета'):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.text = ""
            else:
                self.active = False
            self.color = color_active if self.active else color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    return self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)

    def delete_text(self):
        self.text = ""
        self.txt_surface = font.render(self.text, True, self.color)
    def get_text(self):
        return self.text

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y-3))


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pg.font.Font(None, 20)
        self.value = 1

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        if self.text != '':
            text_image = self.font.render(self.text, True, (5, 0, 58))
            text_rect = text_image.get_rect(center=self.rect.center)
            screen.blit(text_image, text_rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

