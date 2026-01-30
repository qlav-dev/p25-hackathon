import pygame as pg
from pygame import Vector2

from game.sprites import Sprite
from game.holdables import Holdables

g = 30 # pesanteur
acc = Vector2(0, g)

class Player:
    
    def __init__(self, 
        sprite: Sprite,  
        position: Vector2, 
        jump_speed:float, 
        user_name : str,
        address_mac : int,
        speed = Vector2(0,0)
    ):
        self.inventory : List[Holdables] = []
        self.sprite = sprite 
        self.rect = self.sprite.rect
        self.position = position
        self.speed = speed
        self.jump_speed = jump_speed
        self.user_name = user_name
        self.address_mac = address_mac
        
    def update_position(self, dt: float) -> Vector2:
        self.speed += acc*dt
        self.position += self.speed*dt + acc * (dt ** 2) / 2
        if self.position.y>=1000 :
            self.speed.y = 0
            self.position.y = 1000-16*scale
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
        tp0 = self.position + 1/16*Vector2(self.width,0)
        tp1 = self.position + 15/16*Vector2(self.width, 0)
        tp2 = self.position + 1/16*Vector2(16*self.width, self.height)
        tp3 = self.position + 1/16*Vector2(16*self.width, 15*self.height)
        tp4 = self.position + 1/16*Vector2(15*self.width, 16*self.height)
        tp5 = self.position + 1/16*Vector2(self.width, 16*self.height)
        tp6 = self.position + 1/16*Vector2(0, 15*self.height)
        tp7 = self.position + 1/16*Vector2(0,self.height)

        corners = [topleft, topright,bottomright, bottomleft]
        trigger_points = [tp0,tp1,tp2,tp3,tp4,tp5,tp6,tp7]
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
    
    def gestion_collision(self):
        L = self.collision_direction()
        A = [2,3,6,7]
        if (0 in L[2]and L[3]) or (0 in L[0] and 0 in L[1]): # collision avec le sol ou le plafond
            self.position = self.snap_grid_y

        if (0 in L[0] and 0 in L[3]) or (0 in L[1] and 0 in L[2]): # collision avec mur gauche ou mur droit
            self.position = self.snap_grid_x

        elif (0 in L[0] ^ 0 in L[1] ^ 0 in L[2] ^ 0 in L[3]):
            index = 0
            for i in range(4):
                if 0 in L[i]:
                    index = i
            touch1 = False
            touch2 = False
            point1 = trigger_points[(2*index-1)%8]
            point2 = trigger_points[(2*index)%8]
            for platform in Map.platforms : 
                if self.point_in_rect(point1, platform):
                    touch1 = True
            for platform in Map.platforms : 
                if self.point_in_rect(point2, platform):
                    touch2 = True
            if touch1:
                if (2*index-1)%8 in A:
                    self.snap_grid_x
                else :
                    self.snap_grid_y
            if touch2:
                if (2*index)%8 in A:
                    self.snap_grid_x
                else:
                    self.snap_grid_y

            


if __name__=="__main__":
    player = Player(None, Vector2(5,5), 10, 10, Vector2(0,0), 4)

