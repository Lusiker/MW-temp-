#module tool includes some screen items
import pygame
import os
import re
import lib.settings
import lib.player

class TextBar(pygame.sprite.Sprite):
    def __init__(self,pos,size,setting):
        pygame.sprite.Sprite.__init__(self)

        self.name = '_text_'

        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        
        self.setting = setting
        self.color   = self.setting.color['tb_color_inactive']
        
        self.font = pygame.font.SysFont(None,int(size[1] * 0.8))
        self.current_str = ""
        self.msg = self.font.render(self.current_str,True,
                                    self.setting.color['text_color'],self.setting.color['tb_color_active'])
        self.msg_rect = self.msg.get_rect()
        self.msg_rect.center = self.rect.center

        self.has_on = 0

    def update(self):
        if self.has_on == 0:
            new_msg = self.font.render(self.current_str,True,
                                        self.setting.color['text_color'],self.setting.color['tb_color_inactive'])
        elif self.has_on == 1:
            new_msg = self.font.render(self.current_str,True,
                                        self.setting.color['text_color'],self.setting.color['tb_color_active'])
        new_msg_rect = new_msg.get_rect()
        new_msg_rect.center = self.rect.center
        self.msg = new_msg
        self.msg_rect = self.msg.get_rect()
        self.msg_rect.center = self.rect.center
    
    def sleep(self):
        self.has_on = 0
        self.current_str = ""

    def switch_state(self,mode):
        if mode == 1:
            self.has_on = 1
            self.color = self.setting.color['tb_color_active']
        elif mode == 0:
            self.has_on = 0
            self.color = self.setting.color['tb_color_inactive']

    def delete_last(self):
        if len(self.current_str) > 0:
            self.current_str = "".join(self.current_str[:-1])

    def set_input(self,pygame_event):
        new_input = pygame_event.unicode
        self.current_str += new_input

        return lib.settings.setting.event['profile']['input']

    def check_input(self):
        if self.current_str:
            for c in self.current_str:
                if c in (' ','/','\\',':','*','"','<','>','|','?','.'):
                    return False
            return True
        else:
            self.color = self.setting.color['tb_color_invalid']
            return False
    
    def get_string(self):
        new_string = "".join(self.current_str)
        self.current_str = ""
        self.switch_state(0)
        self.update()

        return new_string
    
    def draw(self,screen):
        if self.has_on == 0:
            screen.fill(self.color,self.rect)
            screen.blit(self.msg,self.msg_rect)
        elif self.has_on == 1:
            screen.fill(self.color,self.rect)
            screen.blit(self.msg,self.msg_rect)


class Save_Reader:
    def __init__(self):
        self.name = 'save_reader'

        self.player_group = []
    
    def init_players(self):
        dir_list = os.listdir('lib/savings')
        for file_name in dir_list:
            if file_name[-4:] == '.sav':
                new_player = lib.player.Player('undefined')

                new_player.load(file_name)
                self.player_group.append(new_player)
        
        self.player_group.sort(key = lambda x : x.last_changed,reverse = True)
    
    def player_count(self):
        return len(self.player_group)
    
    def get_player(self,i):
        return self.player_group[i]
    
    def get_all_savs(self):
        return self.player_group