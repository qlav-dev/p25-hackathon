import pygame as pg
from pygame import Vector2
from game.sprites import Sprite
from game.holdables import Holdables

g = 50 # pesanteur
acc = Vector2(0, g)

class Player:
    
    def __init__(self, 
        sprite: Sprite,  
        position: Vector2, 
        user_name : str,
    ):
        self.inventory : List[Holdables] = []
        self.sprite = sprite 
        self.rect = self.sprite.rect
        self.position = position

        self.speed = Vector2(0,0)

        self.user_name = user_name
        self.mac_address = None

        self.HP = 100

    def update(self, dt: float, level) -> None:

        mousePos = Vector2(pg.mouse.get_pos())
        if pg.mouse.get_pressed(3)[0]:
            v = (self.position + Vector2(self.sprite.rect.width / 2, self.sprite.rect.height / 2) - mousePos).normalize()
            self.speed += acc.length() * 10 * v * dt

        self.update_position(dt, level)
    
    def collide_rect(self, rect):

        player_height = self.sprite.rect.height
        player_width = self.sprite.rect.width
        
        y_inside = abs(self.position.y + player_height / 2 - (rect.topleft[1] + rect.height / 2)) < (player_height + rect.height) / 2
        x_inside = abs(self.position.x + player_width / 2 - (rect.topleft[0] + rect.width / 2)) < (player_width + rect.width) / 2

        return x_inside and y_inside

    def update_position(self, dt: float, level) -> None:

        self.speed += acc * dt

        player_height = self.sprite.rect.height
        player_width = self.sprite.rect.width

        # X
        self.position.x += self.speed.x * dt + acc.x * (dt ** 2) / 2
        for c in level.map.map_collider:
            if self.collide_rect(c):
                if (self.speed.x > 0):
                    self.position.x = c.topleft[0] - player_width
                else:
                    self.position.x = c.topleft[0] + c.width
                self.speed.x = 0
            
        # Y
        self.position.y += self.speed.y * dt + acc.y * (dt ** 2) / 2
        for c in level.map.map_collider:
            if self.collide_rect(c):
                if (self.speed.y > 0):
                    self.position.y = c.topleft[1] - player_height
                else:
                    self.position.y = c.topleft[1] + c.height
                self.speed.y = 0

if __name__=="__main__":
    player = Player(None, Vector2(5,5), 10, 10, Vector2(0,0), 4)

