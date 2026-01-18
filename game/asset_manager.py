from pathlib import Path    
import pygame   

class AssetManager:
    def __init__(self, root):
        self.root = Path(root)
        self.images = {}
        #dict{key_tuple(path_str, size_tuple(int, int) OR None) : pygame.Surface}

    def image(self, relative_path, size=None):
        key = (relative_path, size)
        if key not in self.images:
            surface = pygame.image.load(self.root / relative_path).convert_alpha()
            #handle scale as well   
            if size:
                surface = pygame.transform.scale(surface, size)
            self.images[key] = surface  
        return self.images[key]

    def images_in(self, relative_directory, size=None):
        directory = self.root / relative_directory
        return [self.image(str(Path(relative_directory) / entry.name), size) for entry in sorted(directory.iterdir()) if entry.is_file()]
