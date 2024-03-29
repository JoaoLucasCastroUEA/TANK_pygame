import pygame
import math
from bullet import Bullet
from sound_manager import Sound_Manager
class Gun(pygame.sprite.Sprite):
    def __init__(self, player,obstacles, joystick,bullet_color):
        super().__init__()

        self.sound_manager = Sound_Manager()
        self.player = player
        self.orbit_radius = 35
        self.orbit_height = 0
        self.orbit_speed = 0.02
        self.rotation_speed = 5
        self.joystick = joystick
        self.analog_x = self.joystick.get_axis(2)
        self.analog_y = self.joystick.get_axis(3)
        self.bullet_color = bullet_color

        # Load the image with transparency
        self.original_image = pygame.image.load(
            "Sprites/img_gun.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (24, 24))
        self.original_image.set_colorkey((255, 0, 255))  # Set the transparent color (use the color of your background)

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.obstacles = obstacles


        self.angle = 0
        self.bullets = pygame.sprite.Group()


    def update(self):
        if abs(self.joystick.get_axis(2)) > 0.1:
            self.analog_x = self.joystick.get_axis(2)
        if abs(self.joystick.get_axis(3)) > 0.1:
            self.analog_y = self.joystick.get_axis(3)


        self.angle += self.orbit_speed
        self.angle %= 2 * math.pi

        self.rect.x = self.player.rect.x + self.orbit_radius * math.cos(self.angle)
        self.rect.y = self.player.rect.y + self.orbit_radius * math.sin(self.angle) + self.orbit_height

        mouse_pos = pygame.mouse.get_pos()
        look_direction = pygame.math.Vector2(mouse_pos[0] - self.player.rect.centerx,
                                             mouse_pos[1] - self.player.rect.centery)


        if not look_direction.length_squared() == 0:
            look_direction.normalize()

            angle = self.get_angle()

            self.angle = math.radians(angle)
            rotated_image = pygame.transform.rotate(self.original_image, -angle)
            self.image = rotated_image.convert_alpha()

        self.collider_bullets()
        self.bullets.update()

    def fire_bullet(self):
        self.sound_manager.play_shoot_sfx()
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle,self.obstacles,self.bullet_color)
        self.bullets.add(bullet)

    def get_angle(self):
        angle = math.degrees(math.atan2(self.analog_y, self.analog_x))
        return angle if angle >= 0 else 360 + angle

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)
        print(len(self.bullets))
    def collider_bullets(self):
        collision = pygame.sprite.groupcollide(self.bullets,self.obstacles, False, False)
        for bullet in collision:
            bullet.handle_collision('horizontal')
            bullet.handle_move_x()
        collision = pygame.sprite.groupcollide(self.bullets,self.obstacles, False, False)
        for bullet in collision:
            bullet.handle_collision('vertical')
            bullet.handle_move_y()








