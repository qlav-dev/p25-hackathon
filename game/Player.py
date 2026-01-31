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
        jump_speed:float, 
        user_name : str,
        speed = Vector2(0,0)
    ):
        self.inventory : List[Holdables] = []
        self.sprite = sprite 
        self.rect = self.sprite.rect
        self.position = position
        self.speed = speed
        self.jump_speed = jump_speed
        self.user_name = user_name
        self.address_mac = None
        self.HP = 100

    def update(self, dt: float, level) -> None:

        mousePos = Vector2(pg.mouse.get_pos())
        if pg.mouse.get_pressed(3)[0]:
            v = (self.position + Vector2(self.sprite.rect.width / 2, self.sprite.rect.height / 2) - mousePos).normalize()
            self.speed += acc.length() * 10 * v * dt

        self.update_position(dt, level)
    
    def jump(self) -> None:
        self.speed = Vector2(self.speed.x, self.jump_speed)
    
    def snap_grid_x(self, level):
        return Vector2(16 * level.scale * round(self.position.x / (16 * level.scale)), self.position.y)
    
    def snap_grid_y(self, level):
        return Vector2(self.position.x, 16 * level.scale * round(self.position.y / (16 * level.scale)))
    
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

