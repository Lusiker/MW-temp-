#Game objects and their derieved classes
import pygame
import random
import time
import math
import collections
import lib.settings


class Character_Event:
    def __init__(self,name,time,need_time,event_type):
        self.name = name
        self.time = time
        self.need_time = need_time
        self.event_type = event_type


class Character_Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = 'null'
        self.id = '000'

        self.hp = 0
        self.speed = 0
        self.skill_dict = {}
        self.buff_list = []


class Main_Character(Character_Base):
    SUPER_DEFENCE = 0

    def __init__(self,starting_pos,game_screen):
        super().__init__()

        self.name = 'main'
        self.id = '001'

        self.platform_group = game_screen.platform_group
        self.bullet_group   = game_screen.bullet_group
        self.player = None

        self.upper_image = {
            'n' : lib.settings.setting.character['upper'][0],
            'h' : lib.settings.setting.character['upper'][1]
        }
        self.lower_image = {
            'n' : lib.settings.setting.character['lower'][0],
            'm' : lib.settings.setting.character['lower'][1:]
        }
        self.get_reversed()

        self.lower_rect = self.lower_image['n'].get_rect()
        self.upper_rect = self.lower_image['n'].get_rect()
        self.current_u = self.upper_image['n']
        self.current_l = self.lower_image['n']
        self.current_move = self.lower_image['m'][0]
        self.move_index = 0
        self.lower_rect.left,self.lower_rect.top = starting_pos[0],starting_pos[1]

        self.max_hp = 100
        self.hp = 100
        self.mp = 100
        self.max_mp = 100
        self.delt_mp = 0.1
        self.mp_recovery = 0.0
        self.hori_speed = 2.8
        self.vert_speed = 0.0
         
        self.weapons = {
            '1' : Pistol(self),
            '2' : AK(self)
        }
        self.skill_dict = {
            'q' : Fire_Ball(self),
            'e' : Super_Boost(self)
        }
        self.current_weapon = self.weapons['1']

        self.buff_list = [0,0,0]
        self.skill_active = [0,0]
        self.environment = [1,0,0,0,0] #respectively gravity,
        self.state = [1,0,0,0,0,0,0] #respectively position, moving_left, moving_right,
                                 #is_reloading, has_been_hit, is_firing, moving_down
        self.current_on_platform = None

        self.previous_update    = -1
        self.previous_legchange = -1
        self.last_hit_time      = -1
        self.reload_start       = -1
        self.last_mp_added      = -1
        self.last_mp_used       = -1
        self.face = 1

    def reset(self):
        self.hp = 100
        self.mp = 100
        self.hori_speed = 2.8
        self.vert_speed = 0.0
        self.mp_recovery = 0.0

        starting_pos = lib.settings.setting.level_common_info['main_character_starting_pos']
        self.lower_rect.left,self.lower_rect.top = starting_pos[0],starting_pos[1]
        self.state = [1,0,0,0,0,0,0]
        self.current_on_platform = None

        self.move_index = 0

        self.previous_update    = -1
        self.previous_legchange = -1
        self.last_hit_time      = -1
        self.reload_start       = -1
        self.last_mp_added      = -1
        self.last_mp_used       = -1
        self.face = 1

        for weapon in self.weapons.values():
            weapon.reset()
        self.current_weapon = self.weapons['1']
        
        for skill in self.skill_dict.values():
            skill.reset()
        self.skill_active = [0,0]

    def get_reversed(self):
        reversed_u_n = pygame.transform.flip(self.upper_image['n'],True,False)
        reversed_u_h = pygame.transform.flip(self.upper_image['h'],True,False)
        self.reversed_upper_image = {
            'n' : reversed_u_n,
            'h' : reversed_u_h
        }
        reversed_l_n = pygame.transform.flip(self.lower_image['n'],True,False)
        reversed_l_m = []
        for image in self.lower_image['m']:
            new_reversed_l_m = pygame.transform.flip(image,True,False)
            reversed_l_m.append(new_reversed_l_m)
        self.reversed_lower_image = {
            'n' : reversed_l_n,
            'm' : reversed_l_m
        }
    
    def fire(self):
        new_bullet = self.current_weapon.fire()
        
        if new_bullet != None:
            return new_bullet
    
    def use_skill_q(self):
        result = self.skill_dict['q'].use()
        if result != None:
            return result

    def use_skill_e(self):
        result = self.skill_dict['e'].use()
        if result != None:
            return result
    
    def change_to_weapon1(self):
        self.current_weapon = self.weapons['1']
    
    def change_to_weapon2(self):
        self.current_weapon = self.weapons['2']

    def reload(self):
        if self.state[3] != 1:
            if self.current_weapon.mag_ammo < self.current_weapon.max_mag:
                self.state[3] = 1
                self.reload_start = time.time()
    
    def interrupt_reload(self):
        self.state[3] = 0
        self.reload_start = -1

    def update(self):
        update_time = time.time()
        if self.skill_active[0]:
            self.skill_dict['q'].backtrace(update_time)
        if self.skill_active[1]:
            self.skill_dict['e'].backtrace(update_time)

        if self.mp < 100:
            if update_time - self.last_mp_used > 3:
                if update_time - self.last_mp_added >= 1:
                    self.mp_recovery += self.delt_mp
                    if self.mp + self.mp_recovery > 100:
                        self.mp = 100
                    else:    
                        self.mp += self.mp_recovery
                    self.last_mp_added = update_time      
            else:
                self.mp_recovery = 0.0

        if self.state[5] == 1:
            if self.current_weapon.is_auto == 1:
                self.interrupt_reload()
                new_bullet = self.current_weapon.fire()
                
                if new_bullet != None:
                    self.player.current_record.bullet_shot += 1
                    x,y = pygame.mouse.get_pos()
                    new_bullet.get_direction((x,y),self.current_weapon.rect)
                    self.bullet_group.add(new_bullet)


        if self.state[3] == 1:
            if update_time - self.reload_start >= self.current_weapon.reload_time:
                self.current_weapon.reload()
                self.reload_start = -1
                self.state[3] = 0

        self.current_weapon.update(update_time)

        if self.state[0] == 1:
            if self.lower_rect.bottom > 900:
                self.lower_rect.bottom = 900
                self.state[0] = 0
                self.state[6] = 0
                self.vert_speed = 0.0
            else:
                if self.state[6] != 1:
                    for platform in self.platform_group.sprites():
                        if platform.rect.left < self.upper_rect.centerx < platform.rect.right:
                            if self.vert_speed > 0 and self.lower_rect.bottom > platform.rect.top:
                                self.current_on_platform = platform
                                self.state[0] = -1
                                break                       

        if self.state[0] == -1:
            if not self.current_on_platform.rect.left < self.upper_rect.centerx < self.current_on_platform.rect.right:
                self.state[0] = 1
            else:
                self.lower_rect.bottom = self.current_on_platform.rect.top
                self.vert_speed = 0.0
        elif self.state[0] == 1:
            self.vert_speed += 0.5

        if self.state[1] == 1:
            self.face = -1
        elif self.state[2] == 1:
            self.face = 1

        if self.state[1] != 0 or self.state[2] != 0:
            if update_time - self.previous_legchange > 0.08:
                if self.move_index != 2:
                    self.move_index += 1
                else:
                    self.move_index = 0
                self.previous_legchange = update_time
            
        if self.face == 1:
            if self.state[2] == 1:
                self.current_l = self.lower_image['m'][self.move_index]
            else:
                self.current_l = self.lower_image['n']
        elif self.face == -1:
            if self.state[1] == 1:
                self.current_l = self.reversed_lower_image['m'][self.move_index]
            else:
                self.current_l = self.reversed_lower_image['n']
        
        if self.state[4] == 1 and update_time - self.last_hit_time < 1.5:
            if self.face == 1:
                self.current_u = self.upper_image['h']
            elif self.face == -1:
                self.current_u = self.reversed_upper_image['h']
        else:
            if self.face == 1:
                self.current_u = self.upper_image['n']
            elif self.face == -1:
                self.current_u = self.reversed_upper_image['n']

            self.state[4] = 0
            self.last_hit_time = -1
        
        self.lower_rect.centery += self.vert_speed
        if self.upper_rect.left >= 0 and self.upper_rect.right <= 1600:
            if self.state[1] == 1:
                self.lower_rect.centerx -= self.hori_speed
            elif self.state[2] == 1:
                self.lower_rect.centerx += self.hori_speed
        else:
            if self.lower_rect.left < 0:
                self.lower_rect.left = 0
            elif self.lower_rect.right > 1600:
                self.lower_rect.right = 1600
        
        self.current_weapon.face = self.face
        self.previous_update = update_time
        self.rect = self.upper_rect
    
    def draw(self,screen):
        screen.blit(self.current_l,self.lower_rect)
        self.upper_rect.bottom = self.lower_rect.top + 10
        
        if self.state[2] == 1:
            self.upper_rect.centerx = self.lower_rect.centerx + 30
        elif self.state[1] == 1:
            self.upper_rect.centerx = self.lower_rect.centerx + 20
        elif self.state[1] + self.state[2] == 0:
            self.upper_rect.centerx = self.lower_rect.centerx
        screen.blit(self.current_u,self.upper_rect)
        if self.face == 1:
            self.current_weapon.rect.centerx,self.current_weapon.rect.centery = (self.upper_rect.left + lib.settings.setting.character['weapon_pos'][0],
                                                                    self.upper_rect.top + lib.settings.setting.character['weapon_pos'][1])
            screen.blit(self.current_weapon.current_image,self.current_weapon.rect)
        elif self.face == -1:
            self.current_weapon.rect.centerx,self.current_weapon.rect.centery = (self.upper_rect.left,
                                                                    self.upper_rect.top + lib.settings.setting.character['weapon_pos'][1])
            screen.blit(self.current_weapon.current_image,self.current_weapon.rect)

    def reload_percentage(self):
        now = time.time()
        result = (now - self.reload_start) / self.current_weapon.reload_time

        return result       


class Enemy_Base(Character_Base):
    def __init__(self):
        super().__init__()

        self.name = 'enemy'
        self.id   = '100'
    
    def get_reversed(self):
        pass


class Duck(Enemy_Base):
    def __init__(self,character_center_y):
        super().__init__()

        self.name = 'duck'
        self.id   = '101'
        self.type = lib.settings.setting.levels_info['g0101']['enemy'][self.id][0]

        self.hp = 2
        self.hor_speed = 1.2
        self.ver_speed = 2 * random.random()

        self.state = 1

        self.move_image  = lib.settings.setting.levels_info['g0101']['enemy'][self.id][1:3]
        self.get_reversed()
        self.death_image = lib.settings.setting.levels_info['g0101']['enemy'][self.id][3:]
        self.rect = self.move_image[0].get_rect()
        self.death_rect = self.death_image[0].get_rect()

        self.face = 0

        self.last_update = -1
        self.last_target = -1
        self.new_target  = character_center_y
        self.move_index  = 0
        self.death_index = -1
    
    def get_reversed(self):
        self.reversed_move_image = []
        for image in self.move_image:
            new_image = pygame.transform.flip(image,True,False)
            self.reversed_move_image.append(new_image)
        
    def set_facing(self,face):
        self.face = face

        if face == -1:
            self.current_imgs = self.move_image
        elif face == 1:
            self.current_imgs = self.reversed_move_image
        
        self.image = self.current_imgs[0]
        self.rect  = self.image.get_rect()

        if self.face == 1:
            self.rect.right = 0
            self.rect.bottom = 100 + 300 * random.random()
        elif self.face == -1:
            self.rect.left = 1600
            self.rect.bottom = 100 + 300 * random.random()
    
    def update(self,update_time,character_center_y):
        if self.death_index == 2:
            self.state = 0

        if self.hp <= 0 and self.state != 0:
            self.state = -1
            self.last_update = -1
            self.death_centerx,self.death_centery = self.rect.centerx,self.rect.centery

        if self.last_target == -1:
            self.last_target = update_time
        
        if self.rect.right < 0 or self.rect.left > 1600:
            self.state = 0
        
        if self.state == 1:
            if update_time - self.last_update > 0.8:
                if self.move_index != 1:
                    self.move_index += 1
                else:
                    self.move_index = 0
                self.last_update = update_time
                
                self.image = self.current_imgs[self.move_index]
                
            self.rect.centerx += self.face * self.hor_speed
            if update_time - self.last_target > 2:
                self.new_target = character_center_y - 100 * random.random()
                self.last_target = update_time
            if self.rect.centery > self.new_target:
                self.rect.centery -= self.ver_speed
            else:
                self.rect.centery += self.ver_speed
        elif self.state == -1:
            if update_time - self.last_update > 0.8: 
                if self.death_index == -1:
                    self.death_index = 0
                else:
                    if self.death_index < 2:
                        self.death_index += 1
                
                self.current_imgs = self.death_image
                self.image = self.current_imgs[self.death_index]
                self.rect = self.image.get_rect()
                self.rect.centerx,self.rect.centery = self.death_centerx,self.death_centery
                self.last_update = update_time
        

#weapons
class Bullet(pygame.sprite.Sprite):
    def __init__(self,weapon_id,damage,speed):
        pygame.sprite.Sprite.__init__(self)

        self.image = lib.settings.setting.weapon[weapon_id]['bullet']
        self.rect  = self.image.get_rect()
        self.state = 1

        self.damage = damage
        self.speed = speed #this is horizonal speed

    def get_direction(self,mouse_pos,weapon_rect):
        d_x = mouse_pos[0] - weapon_rect.centerx
        d_y = mouse_pos[1] - weapon_rect.centery
        z   = math.sqrt(d_x ** 2 + d_y ** 2)

        sin = d_y / z
        cos = d_x / z

        if abs(sin) >= 0.02:
            self.ver_speed = self.speed * abs(sin)
        else:
            self.ver_speed = 0
        if abs(cos) >= 0.02:
            self.hor_speed = self.speed * abs(cos)
        else:
            self.hor_speed = 0

        if d_x < 0:
            self.hor_speed *= -1
        if d_y < 0:
            self.ver_speed *= -1

        self.rect.centerx,self.rect.centery = weapon_rect.centerx,weapon_rect.centery
    
    def update(self):
        if self.rect.bottom > 900 or self.rect.top < 0:
            self.state = 0
        if self.rect.left < 0 or self.rect.right > 1600:
            self.state = 0

        if self.state == 1:
            self.rect.centerx += self.hor_speed
            self.rect.centery += self.ver_speed
    

class Weapon_Base:
    def __init__(self,character):
        self.name = 'null'
        self.id = '00000'
        self.weapon_type = 'null'
        self.rarity = 0

        self.character = character

        self.damage = 0
        self.atk_speed = 0

        self.image = None
        self.backimage = None

        self.last_used_time = -1
    
    def get_reversed(self):
        self.reversed_image = []
        for image in self.image:
            new_image = pygame.transform.flip(image,True,False)
            self.reversed_image.append(new_image)
    
    def reset(self):
        pass


class Gun(Weapon_Base):
    RELOAD    = 'rl'
    COLDDOWN  = 'cd'
    OUTOFAMMO = 'oa'

    def __init__(self,character):
        super().__init__(character)

        self.id = '10000'
        self.weapon_type = 'gun'
        
        self.blocked = 0

        self.max_mag = 0
        self.back_ammo = 0
        self.mag_ammo = 0
        
        self.is_auto = -1
        self.atk_speed = -1
        self.last_used_time = -1
        
        self.reload_time = -1
        self.reload_start = -1
    
    def reload(self):
        if self.mag_ammo < self.max_mag:
            self.mag_ammo = self.max_mag


class Pistol(Gun):
    def __init__(self,character):
        super().__init__(character)

        self.name = 'pistol'
        self.id = '10001'

        self.damage = 1
        self.back_ammo = -1
        self.max_mag = 7
        self.mag_ammo = 7

        self.is_auto = -1
        self.atk_speed = 0.6
        self.last_used_time = -1

        self.bullet_speed = 8

        self.image = lib.settings.setting.weapon['10001']['images']
        self.get_reversed()
        self.face = 1
        self.pic_index = 0
        self.current_image = self.image[self.pic_index]
        self.rect = self.current_image.get_rect()

        self.reload_time = 1.2
        self.reload_start = -1

        self.last_picchange = -1
        
    def reset(self):
        self.mag_ammo = 7
        self.last_used_time = -1

        self.face = 1
        self.pic_index = 0
        self.current_image = self.image[self.pic_index]

        self.reload_start = -1
        self.last_picchange = -1

    def fire(self):
        if self.mag_ammo > 0:
            now = time.time()
            if now - self.last_used_time >= self.atk_speed:
                self.last_used_time = now
                self.mag_ammo -= 1
                new_rect = self.character.upper_rect
                return Bullet(self.id,self.damage,self.bullet_speed)
        return None
    
    def update(self,time):
        if self.last_used_time != -1:
            if time - self.last_picchange > 0.1:
                if self.pic_index != 3:
                    self.pic_index += 1
                else:
                    self.pic_index = 0
                    self.last_used_time = -1
                self.last_picchange = time

        if self.face == 1:        
            self.current_image = self.image[self.pic_index]
        elif self.face == -1:
            self.current_image = self.reversed_image[self.pic_index]


class AK(Gun):
    def __init__(self, character):
        super().__init__(character)

        self.name = 'ak'
        self.id   = '10002'

        self.damage = 4
        self.back_ammo = -1
        self.max_mag = 30
        self.mag_ammo = 30

        self.is_auto = 1
        self.atk_speed = 0.1
        self.last_used_time = -1

        self.bullet_speed = 12

        self.image = lib.settings.setting.weapon['10002']['images']
        self.get_reversed()
        self.face = 1
        self.pic_index = 0
        self.current_image = self.image[self.pic_index]
        self.rect = self.current_image.get_rect()

        self.reload_time = 2
        self.reload_start = -1

        self.last_picchange = -1

    def reset(self):
        self.damage = 4
        self.mag_ammo = 30

        self.is_auto = 1
        self.atk_speed = 0.1
        self.last_used_time = -1

        self.face = 1
        self.pic_index = 0
        self.current_image = self.image[self.pic_index]

        self.reload_start = -1
        self.last_picchange = -1

    def fire(self):
        if self.mag_ammo > 0:
            now = time.time()
            if now - self.last_used_time >= self.atk_speed:
                self.last_used_time = now
                self.mag_ammo -= 1
                new_rect = self.character.upper_rect
                return Bullet(self.id,self.damage,self.bullet_speed)
        return None

    def update(self,time):
        if self.last_used_time != -1:
            if time - self.last_picchange > 0.06:
                if self.pic_index != 4:
                    self.pic_index += 1
                else:
                    self.pic_index = 0
                    self.last_used_time = -1
                self.last_picchange = time

        if self.face == 1:        
            self.current_image = self.image[self.pic_index]
        elif self.face == -1:
            self.current_image = self.reversed_image[self.pic_index]


class Knife(Weapon_Base):
    def __init__(self):
        pass


class Katana(Knife):
    def __init__(self):           
        pass
        

class Buff_Base:
    def __init__(self):
        pass


#skills
class Skill_Base:
    def __init__(self,character):
        self.name = 'null'
        self.id = '000'
        self.cat = 'null'
        self.key = pygame.NOEVENT

        self.character = character

        self.cost_type = 'none'
        self.cost = 0
        self.start_time = -1
        self.colddown = 0
        self.duration = 0

    def reset(self):
        self.start_time = -1


class Super_Reload(Skill_Base):
    def __init__(self,character):
        super().__init__(character)

        self.name = 'super_reload'
        self.id   = '001'
        self.cat  = 'active'
        self.key  = pygame.K_q

        self.image = lib.settings.setting.skill[self.name]
        self.rect  = self.image.get_rect()

        self.cost_type = 'mp'
        self.cost = 40
        self.colddown = 30
        self.duration = 10
    
    def use(self):
        if self.character.mp >= self.cost:
            self.character.mp -= self.cost
            self.start_time = time.time()
            if self.key == pygame.K_q:
                self.character.skill_active[0] = 1
            elif self.key == pygame.K_e:
                self.character.skill_active[1] = 1

            self.old_reload_time = {}
            for key,weapon in self.character.weapons.items():
                self.old_reload_time[key] = weapon.reload_time
                weapon.reload_time *= 0.2

    def backtrace(self,update_time):
        if update_time - self.start_time >= self.colddown:
            self.start_time = -1
            if self.key == pygame.K_q:
                self.character.skill_active[0] = 0
            elif self.key == pygame.K_e:
                self.character.skill_active[1] = 0
        
        if update_time - self.start_time >= self.duration:
            for key in self.old_reload_time.keys():
                self.character.weapons[key].reload_time = self.old_reload_time[key]


class Super_Boost(Skill_Base):
    def __init__(self,character):
        super().__init__(character)

        self.name = 'super_boost'
        self.id   = '002'
        self.cat  = 'active'
        self.key  = pygame.K_e

        self.cost_type = 'mp'
        self.cost      = 25
        self.colddown  = 20
        self.duration  = 6

    def use(self):
        if self.character.mp >= self.cost:
            self.character.mp -= self.cost
            self.start_time = time.time()
            if self.key == pygame.K_q:
                self.character.skill_active[0] = 1
            elif self.key == pygame.K_e:
                self.character.skill_active[1] = 1

            self.old_speed = self.character.hori_speed
            self.character.hori_speed *= 2

    def backtrace(self,update_time):
        if update_time - self.start_time >= self.colddown:
            self.start_time = -1
            if self.key == pygame.K_q:
                self.character.skill_active[0] = 0
            elif self.key == pygame.K_e:
                self.character.skill_active[1] = 0
        
        if update_time - self.start_time >= self.duration:
            self.character.hori_speed = self.old_speed


class Fire_Ball(Skill_Base):
    def __init__(self,character):
        super().__init__(character)

        self.name = 'fire_ball'
        self.id   = '003'
        self.cat  = 'instant'
        self.key  = pygame.K_q

        self.damage = 150
        self.speed  = 10

        self.cost_type = 'mp'
        self.cost = 20
        self.colddown = 8
        self.duration = -1

    def use(self):
        if self.character.mp >= self.cost:
            self.character.mp -= self.cost
            self.start_time = time.time()
            if self.key == pygame.K_q:
                self.character.skill_active[0] = 1
            elif self.key == pygame.K_e:
                self.character.skill_active[1] = 1

            new_bullet = Bullet('90001',self.damage,self.speed)
            new_bullet.get_direction(pygame.mouse.get_pos(),self.character.current_weapon.rect)
            return new_bullet

    def backtrace(self,update_time):
        if update_time - self.start_time >= self.colddown:
            self.start_time = -1
            if self.key == pygame.K_q:
                self.character.skill_active[0] = 0
            elif self.key == pygame.K_e:
                self.character.skill_active[1] = 0