#module player includes class Player that defines a player's
#basic infomation
import pygame
import struct
import time
import math
import os
import lib.settings

class Game_Record:
    def __init__(self):
        self.start_time = 0.0
        self.end_time   = 0.0
        self.last_level = [0,0]
        self.achievement_unlocked = [0,0,0,0,0,0]

        self.score = 0
        self.enemy_killed = 0
        self.bullet_shot = 0
        self.damage_dealt = 0

        self.death_count = 0

    def get_played_time(self):
        self.newly_played_time = self.end_time - self.start_time

    def show(self):
        print(self.start_time,self.end_time,self.last_level,self.achievement_unlocked,self.score,self.enemy_killed,
        self.bullet_shot,self.damage_dealt)

    def reset(self):
        self.start_time = 0.0
        self.end_time   = 0.0
        self.last_level = [0,0]
        self.achievement_unlocked = [0,0,0,0,0,0]
        
        self.score = 0
        self.enemy_killed = 0
        self.bullet_shot = 0
        self.damage_dealt = 0

        self.newly_played_time = 0.0
        
        self.death_count = 0


class Player:
    def __init__(self,name):
        self.name = name
        
        self.time = time.time()
        self.created_version = lib.settings.setting.game_info['version']
        self.last_changed = 0
        
        self.total_score = 0
        self.total_enemy_killed = 0
        self.total_bullet_shot = 0
        self.total_damage_dealt = 0

        self.total_played_time = 0.0
        self.total_death_count = 0
        self.finished_level = [0,0,0,0,0,0]
        self.achievements   = [0,0,0,0,0,0]

        self.selected_skill = {
            'q' : None,
            'e' : None
        }
        self.selected_weapon = {
            '1' : None,
            '2' : None
        }

        self.current_record = Game_Record()
    
        self.prep_msg()

    def prep_msg(self):
        self.created_time = time.localtime(self.time)
        self.name_msg = "Player name: " + self.name
        self.created_day_msg = "Save created: " + str(self.created_time.tm_year) + " " \
                                + str(self.created_time.tm_mon) + " " \
                                + str(self.created_time.tm_mday)
        self.created_time_msg = str(self.created_time.tm_hour) + " " \
                                + str(self.created_time.tm_min) + " " \
                                + str(self.created_time.tm_sec)
        self.total_score_msg = "Total Score: " + str(self.total_score)
        self.total_enemy_killed_msg = "Total Enemy Killed: " + str(self.total_enemy_killed)
        self.total_bullet_shot_msg = "Total Bullet Shot: " + str(self.total_bullet_shot)
        self.total_damage_dealt_msg = "Total Damage Dealt:" + str(self.total_damage_dealt)

        self.name_rect = pygame.Rect(20,20,200,80)
        self.time_rect1 = pygame.Rect(110,20,200,20)
        self.time_rect2 = pygame.Rect(140,20,200,20)
        self.font_name = pygame.font.SysFont(None,60)
        self.font_time = pygame.font.SysFont(None,25)
        self.font_info = pygame.font.SysFont('impact',30)
        
        self.name_img = self.font_name.render(self.name_msg,True,
                                              lib.settings.setting.color['text_color'],
                                              lib.settings.setting.color['white'])
        self.time_img1 = self.font_time.render(self.created_day_msg,True,
                                               lib.settings.setting.color['text_color'],
                                               lib.settings.setting.color['white'])
        self.time_img2 = self.font_time.render(self.created_time_msg,True,
                                               lib.settings.setting.color['text_color'],
                                               lib.settings.setting.color['white'])
        self.name_img_rect = self.name_img.get_rect()
        self.time_img1_rect = self.time_img1.get_rect()
        self.time_img2_rect = self.time_img2.get_rect()
        self.name_img_rect.left,self.name_img_rect.top = self.name_rect.left,self.name_rect.top
        self.time_img1_rect.left,self.time_img1_rect.top = self.name_img_rect.left,self.name_img_rect.bottom + 20
        self.time_img2_rect.left,self.time_img2_rect.top = self.time_img1_rect.right + 20,self.name_img_rect.bottom + 20

        self.achievement_rect = []
        self.starting_rect = (830,480)
        for num in range(6):
            if num < 4:
                new_rect = (self.starting_rect[0] + 180 * num ,self.starting_rect[1])
            else:
                new_rect = (self.starting_rect[0] + 180 * (num - 4) + 800,self.starting_rect[1] + 190)
            self.achievement_rect.append(new_rect)
    
    def update(self):
        self.last_changed = time.time()
        
        self.total_score += self.current_record.score
        self.total_enemy_killed += self.current_record.enemy_killed
        self.total_bullet_shot += self.current_record.bullet_shot
        self.total_damage_dealt += self.current_record.damage_dealt

        self.total_played_time += self.current_record.newly_played_time
        self.total_death_count += self.current_record.death_count
        if self.current_record.last_level[1] == 1:
            self.finished_level[self.current_record.last_level[0]] = 1
        
        for i in range(6):
            if self.current_record.achievement_unlocked[i] == 1:
                self.achievements[i] = 1

    def clear_temp(self):
        self.current_record.reset()

    def show_msg(self,screen,mode):
        self.prep_msg()

        screen.blit(self.name_img,self.name_img_rect)
        screen.blit(self.time_img1,self.time_img1_rect)
        screen.blit(self.time_img2,self.time_img2_rect)

        if mode == 0:
            for i in range(lib.settings.setting.achievement['total']):
                cond = self.achievements[i]
                screen.blit(lib.settings.setting.achievement['imgs'][i][cond],self.achievement_rect[i])       
        elif mode == 1:
            self.kill_msg = self.font_info.render(self.total_enemy_killed_msg,True,
                                                  lib.settings.setting.color['white'])
            self.damage_msg = self.font_info.render(self.total_damage_dealt_msg,True,
                                                  lib.settings.setting.color['white'])
            self.score_msg = self.font_info.render(self.total_score_msg,True,
                                                  lib.settings.setting.color['white'])
            self.bullet_msg = self.font_info.render(self.total_bullet_shot_msg,True,
                                                  lib.settings.setting.color['white'])
            self.kill_rect = self.kill_msg.get_rect()
            self.damage_rect = self.damage_msg.get_rect()
            self.score_rect = self.score_msg.get_rect()
            self.bullet_rect = self.bullet_msg.get_rect()

            self.kill_rect.left,self.kill_rect.top = self.starting_rect[0],self.starting_rect[1]
            self.damage_rect.left,self.damage_rect.top = self.kill_rect.left,self.kill_rect.bottom + 10
            self.score_rect.left,self.score_rect.top = self.damage_rect.left,self.damage_rect.bottom + 10
            self.bullet_rect.left,self.bullet_rect.top = self.score_rect.left,self.score_rect.bottom + 10

            screen.blit(self.kill_msg,self.kill_rect)
            screen.blit(self.damage_msg,self.damage_rect)
            screen.blit(self.score_msg,self.score_rect)
            screen.blit(self.bullet_msg,self.bullet_rect)
        elif mode == 2:
            minute = math.ceil(self.total_played_time / 60)
            second = self.total_played_time % 60
            self.total_played_time_msg = 'Total Played: ' + str(minute) + ":" + str(round(second,3))
            self.total_death_msg       = 'Total Death: ' + str(self.total_death_count)

            self.played_time_msg = self.font_info.render(self.total_played_time_msg,True,
                                                         lib.settings.setting.color['white'])
            self.death_msg       = self.font_info.render(self.total_death_msg,True,
                                                         lib.settings.setting.color['white'])

            self.played_time_rect = self.played_time_msg.get_rect()
            self.death_rect       = self.death_msg.get_rect()

            self.played_time_rect.left,self.played_time_rect.top = self.starting_rect[0],self.starting_rect[1]
            self.death_rect.left,self.death_rect.top = self.played_time_rect.left,self.played_time_rect.bottom + 10

            screen.blit(self.played_time_msg,self.played_time_rect)
            screen.blit(self.death_msg,self.death_rect)

    def load(self,file_name):
        with open('lib/savings/' + file_name,'rb') as f:
            name_len_b = f.read(4)
            name_len = struct.unpack('i',name_len_b)
            name_b = f.read(name_len[0])
            self.name = struct.unpack(str(name_len[0]) + 's',name_b)[0]
            self.name = self.name.decode('utf-8')

            ver_len_b = f.read(4)
            ver_len = struct.unpack('i',ver_len_b)
            ver_b = f.read(ver_len[0])
            self.created_version = struct.unpack(str(ver_len[0]) + 's',ver_b)[0]
            self.created_version = self.created_version.decode('utf-8')

            info_b = f.read(32)
            self.time,self.last_changed,self.total_score, \
            self.total_enemy_killed,self.total_bullet_shot, \
            self.total_damage_dealt,self.total_played_time, \
            self.total_death_count = struct.unpack('ffiiiifi',info_b)

            for i in range(6):
                level_b = f.read(4)
                new_info = struct.unpack('i',level_b)
                self.finished_level[i] = new_info[0]
            
            for i in range(6):
                achievement_b = f.read(4)
                new_achievement = struct.unpack('i',achievement_b)
                self.achievements[i] = new_achievement[0]

        self.prep_msg()

    def save(self):
        name = struct.pack(str(len(self.name)) + 's',self.name.encode('utf-8'))
        name_len_b = struct.pack('i',len(self.name))

        version = struct.pack(str(len(self.created_version)) + 's',self.created_version.encode(encoding = 'utf-8'))
        version_len_b = struct.pack('i',len(self.created_version))

        b_format = 'ffiiiifi'
        info_struct = struct.pack(b_format,self.time,self.last_changed,
                          self.total_score ,self.total_enemy_killed,self.total_bullet_shot,
                          self.total_damage_dealt,self.total_played_time,self.total_death_count) 
        file_name = self.name + ".sav"
        dir_list = os.listdir('lib/savings')
        with open('lib/savings/' + file_name,'wb') as f:
            f.write(name_len_b)
            f.write(name)
            f.write(version_len_b)
            f.write(version)
            f.write(info_struct)

            for i in range(6):
                new_level_b = struct.pack('i',self.finished_level[i])
                f.write(new_level_b)
            
            for i in range(6):
                new_achievement_b = struct.pack('i',self.achievements[i])
                f.write(new_achievement_b)
        