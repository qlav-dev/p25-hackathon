import pygame

class Player:
    
    def __init__(self, sprite, top_left:pygame.Vector2, width : int, height:int):
        self.sprite = pygame.sprite.load(sprite).convert_alpha() 
        self.width = width
        self.heigth = height
        self.rect = pygame.Rect(top_left)
        


    def affiche():
        return None
    
    def collision():
        return None
    
    def move():
        return None
    
    def update_position():
        







