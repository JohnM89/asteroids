import pygame

class FontManager:
    def __init__(self):
        pygame.font.init()
        #dictionary to hold fonts
        self.fonts = {}
        #set a default fallback font
        self.fonts["default"] = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.text_surface = None

    def load_font(self, name, path, size):
        #load a font into the manager.
        if name not in self.fonts:
            self.fonts[name] = pygame.font.Font(path, size)

    #use a get font function to enable error handling 
    def get_font(self, name):
        #return a font by name
        return self.fonts[name]

    def render_text(self, surface, text, name, colour, x, y, width, height ):
        #render text using a selected font
        font = self.get_font(name)
        #print(rect)
        #check if font exists
        if font:
            text_surface = font.render(text, True, colour)
            #self.text_surface = text_surface
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()
            offset_x = x + (width - text_width) // 2
            offset_y = y + (height - text_height) // 2
            #draw text to surface
            surface.blit(text_surface, (offset_x, offset_y))
        else:
            raise Exception("font not found, reverting to default")
            font = self.get_font["default"]
            text_surface = font.render(text, True, colour)
            surface.bilt(text_surface, position)

