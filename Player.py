import pygame as pg
from pygame import Vector2

g = 9.8 #pesanteur
acc = Vector2(0, -g)

class Player:
    
    def __init__(self, sprite, topleft:Vector2, width : int, height:int, position:Vector2, jump_speed:float, speed=Vector2(0,0)):
        self.sprite = sprite 
        self.width = width
        self.heigth = height
        self.rect = pg.Rect((0, 0), (width, height))
        self.position = position
        self.speed = speed
        self.jump_speed = jump_speed


    def affiche():
        return None
        
    def update_position(self, dt:float) -> Vector2:
        self.position += self.speed*dt
        return self.position
    
    def update_speed(self, dt:float)->Vector2:
        self.speed += acc*dt
        return self.speed
    
    def jump(self, )->None:
        self.speed = Vector2(self.speed.x, self.jump_speed)

    def point_in_rect(point:Vector2, rect : pg.Rect)->bool:
        return (rect.left<=point.x<=rect.left+rect.width) and (rect.top - rect.height<=point.y<=rect.top)
    
    def collision_direction():
        
        return None
    

if __name__=="__main__":
    player = Player(None, Vector2(5,5), 10, 10, Vector2(0,0), 4)

