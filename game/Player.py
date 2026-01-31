import pygame as pg
from pygame import Vector2
from game.sprites import Sprite
from game.holdables import Holdables

g = 200 # pesanteur

class Player:
    
    def __init__(self, 
        sprite: Sprite,  
        position: Vector2, 
        user_name : str,
        mass: float = 10
    ):
        # Inventory
        self.inventory : List[Holdables] = []
        self.holding: int = 0 # Which inventory item is the player holding

        # Graphic
        self.sprite = sprite 
        self.rect = self.sprite.rect

        # Physics
        self.mass = mass

        self.position = position
        self.speed = Vector2(0,0)
        self.acc = Vector2(0, 0)

        self.grounded = False

        # Online
        self.user_name = user_name
        self.mac_address = None

        self.HP = 100

    def update(self, dt: float, level) -> None:
        self.update_position(dt, level)
        self.acc = Vector2(0, level.g / self.mass) # After the update_position : If the gun is fired, resets the acc AFTER the position was updated
    
    def collide_rect(self, rect):

        player_height = self.sprite.rect.height
        player_width = self.sprite.rect.width
        
        y_inside = abs(self.position.y + player_height / 2 - (rect.topleft[1] + rect.height / 2)) < (player_height + rect.height) / 2
        x_inside = abs(self.position.x + player_width / 2 - (rect.topleft[0] + rect.width / 2)) < (player_width + rect.width) / 2

        return x_inside and y_inside

    def update_position(self, dt: float, level) -> None:

        self.speed += self.acc * dt

        player_height = self.sprite.rect.height
        player_width = self.sprite.rect.width

        # X
        self.position.x += self.speed.x * dt + self.acc.x * (dt ** 2) / 2
        for c in level.map.map_collider:
            if self.collide_rect(c):
                if (self.speed.x > 0):
                    self.position.x = c.topleft[0] - player_width
                else:
                    self.position.x = c.topleft[0] + c.width
                self.speed.x = 0
            
        # Y
        self.position.y += self.speed.y * dt + self.acc.y * (dt ** 2) / 2

        self.grounded = False
        for c in level.map.map_collider:
            if self.collide_rect(c):
                if (self.speed.y > 0):
                    self.grounded = True
                    self.position.y = c.topleft[1] - player_height
                else:
                    self.position.y = c.topleft[1] + c.height
                self.speed.y = 0

if __name__=="__main__":
    player = Player(None, Vector2(5,5), 10, 10, Vector2(0,0), 4)

