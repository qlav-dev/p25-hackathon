import pygame as pg
from pygame import Vector2

from game.sprites import Sprite
from game.holdables import Holdables

g = 9.8 # pesanteur
acc = Vector2(0, -g)

class Player:
    
    def __init__(self, 
        sprite: Sprite, 
        topleft: Vector2, 
        width : int, 
        height: int, 
        position: Vector2, 
        jump_speed:float, 
        speed = Vector2(0,0)
    ):
        self.inventory : List[Holdables] = []
        self.sprite = sprite 
        self.width = width
        self.heigth = height
        self.rect = pg.Rect((0, 0), (width, height))
        self.position = position
        self.speed = speed
        self.jump_speed = jump_speed
        
    def update_position(self, dt: float) -> Vector2:
        self.speed += acc*dt
        self.position += self.speed*dt + acc * (dt ** 2) / 2
        return self.position

    def update(self, dt: float) -> None:
        self.update_position(dt)
    
    def jump(self, )->None:
        self.speed = Vector2(self.speed.x, self.jump_speed)

    def point_in_rect(point:Vector2, rect : pg.Rect)->bool:
        return (rect.left<=point.x<=rect.left+rect.width) and (rect.top - rect.height<=point.y<=rect.top)
    
    def collision_direction(self)->list[list[int]]:
        """
        [] : collision avec rien
        0 : " mur 
        1 : " projectile
        2 : " other player
        """
        topleft = self.position
        topright = self.position + Vector2(self.width,0)
        bottomright = self.position + Vector2(self.width, self.heigth)
        bottomleft = self.position + Vector2(0, -self.height)
        
        corners = [topleft, topright,bottomright, bottomleft]
        ls_collisions = [[]*4]

        for object in Game.objects:
            for i in range(4):
                if (not (0 in ls_collisions[i])) and self.point_in_rect(corners[i], object):
                    ls_collisions.append(0)
        for projectiles in Game.entities.projectiles :
            for i in range(4):
                if (not (1 in ls_collisions[i])) and self.point_in_rect(corners[i], object):
                    ls_collisions.append(1)
        for player in Game.entities.players :
            for i in range(4):
                if (not (2 in ls_collisions[i])) and self.point_in_rect(corners[i], object):
                    ls_collisions.append(2)

        return ls_collisions
    
    def snap_grid_x(self):
        return Vector2(16*scale*round(self.position.x/(16*scale)), self.position.y)
    
    def snap_grid_y(self):
        return Vector2(self.position.x, 16*scale*round(self.position.y/(16*scale)))

if __name__=="__main__":
    player = Player(None, Vector2(5,5), 10, 10, Vector2(0,0), 4)

