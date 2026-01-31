import pygame as pg
from pygame import Vector2
from game.sprites import Sprite

class PhysicsEntity:
    def __init__(self, 
        sprite: Sprite,  
        position: Vector2,
        mass: int = 10,
        hitbox: pg.rect.Rect = None
    ):
        if hitbox == None:
            self.hitbox = sprite.rect
        else:
            self.hitbox = hitbox

        # Graphic
        self.sprite = sprite 
        self.rect = self.sprite.rect

        # Physics
        self.mass = mass

        self.position = position
        self.speed = Vector2(0,0)
        self.acc = Vector2(0, 0)

        self.grounded = False
        self.ground_friction = 1.2 
        self.grounded_timer = 10 # in frames, to prevent grounded from flickering
        self.grounded_time = 0

        self.HP = 50

    def update(self, dt: float, level) -> None:
        ...

    @property
    def world_hitbox(self) -> pg.rect.Rect:
        """Hitbox absolue dans le monde."""
        return pg.Rect(
            self.position.x + self.hitbox.topleft[0],
            self.position.y + self.hitbox.topleft[1],
            self.hitbox.width,
            self.hitbox.height
        )

    def collide_rect(self, rect: pg.rect.Rect) -> bool:
        return rect.colliderect(self.world_hitbox)

    def update_position(self, dt: float, level) -> None:

        self.speed += self.acc * dt

        # X
        self.position.x += self.speed.x * dt
        for c in level.map.map_collider:
            if self.collide_rect(c):
                if (self.speed.x > 0):
                    self.position.x = c.topleft[0] - self.sprite.rect.width + self.hitbox.topleft[0]
                else:
                    self.position.x = c.topleft[0] + c.width - self.hitbox.topleft[0]
                self.speed.x = 0
            
        # Y
        self.position.y += self.speed.y * dt
        self.grounded_time += 1

        for c in level.map.map_collider:
            if self.collide_rect(c):
                if (self.speed.y >= 0):
                    self.grounded_time = 0
                    self.position.y = c.topleft[1] - self.sprite.rect.height + self.hitbox.topleft[1] 
                    self.speed.x /= self.ground_friction
                else:
                    self.position.y = c.topleft[1] + c.height - self.hitbox.topleft[1]
                self.speed.y = 0
        
        self.grounded = self.grounded_time < self.grounded_timer