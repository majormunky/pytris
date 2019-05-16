import pygame
import Config

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width, self.height = Config.get_screensize()
        self.move_distance = 32

    def move(self, new_rect, container, direction=None):
        if direction:
            if direction == "up":
                new_rect.y -= 32
            elif direction == "down":
                new_rect.y += 32
            elif direction == "left":
                new_rect.x -= 32
            elif direction == "right":
                new_rect.x += 32
        else:
            print("No direction given to camera")
            return False
        if container.contains(new_rect):
            self.x = new_rect.x
            self.y = new_rect.y
            print("We are moving the camera")
            return True
        else:
            return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)