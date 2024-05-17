# Imports
import pygame


class Image(pygame.surface.Surface):
    def __init__(self, path, alpha=255):
        image = pygame.image.load(path).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        super().__init__([width, height], pygame.SRCALPHA, 32)
        self.blit(image, [0, 0])
        self.set_alpha(alpha)


class Sound(pygame.mixer.Sound):

    def __init__(self, path, volume=1.0):
        super().__init__(path)
        self.set_volume(volume)
        self.on = True

    def play(self):
        if self.on:
            super().play()
    
    def mute(self):
        self.on = False
        # stop active sounds or just let them play out?

    def unmute(self):
        self.on = True


class Music():

    def __init__(self, path, volume, loops=-1):
        self.path = path
        self.volume = volume
        self.loops = loops
        self.on = True
            
    def play(self):
        pygame.mixer.music.load(self.path)

        if self.on:
            self.unmute()
        else:
            self.mute()
        
        pygame.mixer.music.play(self.loops) 

    def stop(self, fadeout_time=0):
        pygame.mixer.music.fadeout(fadeout_time)

    def pause(self):
        pygame.mixer.music.pause()

    def restart(self):
        pygame.mixer.music.rewind()
    
    def mute(self):
        pygame.mixer.music.set_volume(0)
        self.on = False

    def unmute(self):
        pygame.mixer.music.set_volume(self.volume)
        self.on = True


class Font(pygame.font.Font):
    def __init__(self, path, size):
        super().__init__(path, size)

