import pygame

class FontManager:
    def __init__(self):
        pygame.font.init()
        #dictionary to hold fonts
        self.fonts = {}
        #set a default fallback font
        self.fonts["default"] = pygame.font.Font(pygame.font.get_default_font(), 24)


    def load_font(self, name, path, size):
        #load a font into the manager.
        if name not in self.fonts:
            self.fonts[name] = pygame.font.Font(path, size)

    #use a get font function to enable error handling 
    def get_font(self, name):
        #return a font by name
        return self.fonts[name]

    def render_text(self, surface, text, name, colour, position):
        #render text using a selected font
        font = self.get_font(name)
        #check if font exists
        if font:
            text_surface = font.render(text, True, colour)
            #draw text to surface
            surface.blit(text_surface, position)
        else:
            raise Exception("font not found, reverting to default")
            font = self.get_font["default"]
            text_surface = font.render(text, True, colour)
            surface.bilt(text_surface, position)

