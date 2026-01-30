import pygame as pg
from pygame import Vector2
from game.sprites import Sprite
from game.holdables import Holdables

g = 30 # pesanteur
acc = Vector2(0, g)
scale = 3

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
        
    def update_position(self, dt: float) -> Vector2:
        self.speed += acc*dt
        self.position += self.speed*dt + acc * (dt ** 2) / 2
        # if self.position.y>=16*scale :
        #     self.speed.y = 0
        #     self.position.y = 16*scale
        return self.position

    def update(self, dt: float) -> None:
        self.update_position(dt)
    
    def jump(self, )->None:
        self.speed = Vector2(self.speed.x, self.jump_speed)

    def point_in_rect(self, point:Vector2, rect : pg.Rect)->bool:
        return (rect.left<=point.x<=rect.left+rect.width) and (rect.top + rect.height>=point.y>=rect.top)
    
    def collision_direction(self, level)->list[list[int]]:
        """
        [] : collision avec rien
        0 : " mur 
        1 : " projectile
        2 : " other player
        """
        topleft = self.position
        topright = self.position + Vector2(self.rect.width,0)
        bottomright = self.position + Vector2(self.rect.width, self.rect.height)
        bottomleft = self.position + Vector2(0, self.rect.height)

        corners = [topleft, topright,bottomright, bottomleft]
        
        ls_collisions = [[],[],[],[]]

        for platform in level.map.map_collider:
            for i in range(4):
                if (not (0 in ls_collisions[i])) and self.point_in_rect(corners[i], platform):
                    ls_collisions[i].append(0)
        # for projectiles in Game.entities.projectiles :
        #     for i in range(4):
        #         if (not (1 in ls_collisions[i])) and self.point_in_rect(corners[i], object):
        #             ls_collisions.append(1)
        # for player in Game.entities.players :
        #     for i in range(4):
        #         if (not (2 in ls_collisions[i])) and self.point_in_rect(corners[i], object):
        #             ls_collisions.append(2)

        return ls_collisions
    
    
    
    def snap_grid_x(self):
        return Vector2(16*scale*round(self.position.x/(16*scale)), self.position.y)
    
    def snap_grid_y(self):
        return Vector2(self.position.x, 16*scale*round(self.position.y/(16*scale)))
    
    def wall_collision_manager(self, level)->None:
        """
        Permet de snap le personnage sur la grille en cas de collision avec les plateformes
        Trigger points : permet de préciser le contact avec un obstacle dans le cas où un seul coin touche
        2 trigger points par coin espacés d'1/16 de sa taille
        Trigger points numérotés dans le sens horaire en partant du coin en haut à gauche (cf convention)
        A = ensemble des trigger points qui si activés impliquent snap sur abscisses (O serait par exemple [0,1,4,5])

        """
        tp0 = self.position + 1/16*Vector2(self.rect.width,0)
        tp1 = self.position + 15/16*Vector2(self.rect.width, 0)
        tp2 = self.position + 1/16*Vector2(16*self.rect.width, self.rect.height)
        tp3 = self.position + 1/16*Vector2(16*self.rect.width, 15*self.rect.height)
        tp4 = self.position + 1/16*Vector2(15*self.rect.width, 16*self.rect.height)
        tp5 = self.position + 1/16*Vector2(self.rect.width, 16*self.rect.height)
        tp6 = self.position + 1/16*Vector2(0, 15*self.rect.height)
        tp7 = self.position + 1/16*Vector2(0,self.rect.height)
        trigger_points = [tp0,tp1,tp2,tp3,tp4,tp5,tp6,tp7]
        L = self.collision_direction(level)
        A = [2,3,6,7]
        if (0 in L[2]and L[3]) or (0 in L[0] and 0 in L[1]): # collision avec le sol ou le plafond
            self.position = self.snap_grid_y()

        if (0 in L[0] and 0 in L[3]) or (0 in L[1] and 0 in L[2]): # collision avec mur gauche ou mur droit
            self.position = self.snap_grid_x()

        elif ((0 in L[0]) ^ (0 in L[1]) ^ (0 in L[2]) ^ (0 in L[3])): # collision d'un seul coin
            index = 0
            # On récupère l'indice du coin entré en collision
            for i in range(4):
                if 0 in L[i]:
                    index = i
            # On nomme les deux trigger points associés au coin
            point1 = trigger_points[(2*index-1)%8] 
            point2 = trigger_points[(2*index)%8]
            touch1 = False
            touch2 = False
            # On regarde lequel des deux touche qqch
            for platform in level.map.map_collider : 
                if self.point_in_rect(point1, platform):
                    touch1 = True
            for platform in level.map.map_collider : 
                if self.point_in_rect(point2, platform):
                    touch2 = True
            # Si c'est un point abscisse, on snap l'abscisse, sinon l'ordonnée
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

    def proj_collision_manager(self)->None:
        return None



if __name__=="__main__":
    player = Player(None, Vector2(5,5), 10, 10, Vector2(0,0), 4)

