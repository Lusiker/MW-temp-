import lib.player
import lib.tool
import pygame
import random
import time

class Settings():
    def __init__(self):
        self.game_info = {
                            'name' : 'MiniWarbot',
                            'version' : '0.1.0',
                            'size' : (1600,900),
                            'icon' : pygame.image.load('lib/images/mgw_icon.bmp'),
                            'setting_template_rect' : (600,150,400,600),
                            'static_img' : [
                                ('s_resume_common',(90,450,100,100),pygame.image.load('lib/images/common/return.png'),
                                    pygame.image.load('lib/images/common/return_pushed.png')),
                                ('s_back_common',(210,450,100,100),pygame.image.load('lib/images/common/back.png'),
                                    pygame.image.load('lib/images/common/back_pushed.png'))
                            ]
                         }
        self.color = {
                        'bg_color'  : (230,230,230),
                        'it_color'  : (180,180,180),
                        'white'     : (255,255,255),
                        'black'     : (0,0,0),
                        'dark_grey' : (127,127,127),
                        'light_grey' : (210,210,210),
                        'tb_color_inactive' : (200,200,200),
                        'tb_color_active'   : (245,245,245),
                        'tb_color_invalid'  : (255,0,0),
                        'text_color' : (0,0,0),
                        'green' : (0,255,127),
                        'red'   : (220,20,60),
                        'blue'  : (0,200,0),
                        'pure_blue'  : (0,0,255),
                        'light_blue' : (65,105,225),
                        'orange'     : (255,140,0)
                     }
        self.achievement = {
            'total' : 1,
            'imgs'  : [
                (pygame.image.load('lib/images/achievements/medal01_locked.png'),
                    pygame.image.load('lib/images/achievements/medal01.png')),
            ]
        }
        self.event = {
                        'common' : {
                                        'pass' : '00000',
                                        'exit' : '00001',
                                        'fin'  : '99999'
                        },
                        'title' : {
                                    'exit'     : '00001',
                                    'setting'  : '00002',
                                    'profile'  : '00103',
                                    'start01'  : '00104',
                                    'start02'  : '00105',
                                    'resume'   : '00006'
                        },
                        'profile' : {
                                        'exit'      : '00001',
                                        'setting'   : '01002',
                                        'return'    : '01103',
                                        'new'       : '01004',
                                        'load'      : '01005',
                                        'confirm'   : '01006',
                                        'text'      : '01007',
                                        'input'     : '01008',
                                        'cancel'    : '01009',
                                        'back'      : '0100a',
                                        'profile'   : '0100b',
                                        'achieve'   : '0100c',
                                        'kill'      : '0100d',
                                        'statistic' : '0100e',
                                        'up'        : '0100f',
                                        'down'      : '01010',
                                        'select0'   : '01011',
                                        'select1'   : '01012',
                                        'select2'   : '01013',
                                        'select3'   : '01014',
                                        'select4'   : '01015',
                                        'save'      : '01016',
                                        'resume'    : '01017'
                        },
                        'worlds' : {
                            'exit'     : '00001',
                            'setting'  : '02002',
                            'return'   : '02103',
                            'previous' : '02004',
                            'next'     : '02005',
                            'tog0101'  : '02111',
                            'tog0102'  : '02112',
                            'tog0103'  : '02113',
                            'profile'  : '02106',
                            'resume'   : '02007'
                        },
                        'g0101' : {
                            'exit'      : '00001',
                            'setting'   : '11002',
                            'gameover'  : '11003',
                            'victory'   : '11004',
                            'resume'    : '11005',
                            'back'      : '11106'       
                        },
                        'victory'  : {
                            'exit'      : '00001',
                            'return'    : '21101'
                        },
                        'gameover' : {
                            'exit'     : '00001',
                            'continue' : '20101'
                        }
                     }
        self.title_info = {
                            'static_img' : [
                                        ('i_title',(400,150,800,300),pygame.image.load('lib/images/title/title.png')),
                                        ('b_exit_title',(20,780,100,100),pygame.image.load('lib/images/common/exit.png'),
                                            pygame.image.load('lib/images/common/exit_pushed.png')),
                                        ('b_setting_title',(140,780,100,100),pygame.image.load('lib/images/common/setting.png'),
                                            pygame.image.load('lib/images/common/setting_pushed.png')),
                                        ('b_profile_title',(260,780,100,100),pygame.image.load('lib/images/common/profile.png'),
                                            pygame.image.load('lib/images/common/profile_pushed.png')),
                                        ('b_start01_title',(700,600,200,50),pygame.image.load('lib/images/title/start01.png'),
                                            pygame.image.load('lib/images/title/start01_pushed.png')),
                                        #('b_start02_title',(700,670,200,50),pygame.image.load('lib/images/title/start02.png'),
                                        #    pygame.image.load('lib/images/title/start02_pushed.png')),
                                    ],
                    }
        self.profile_info = {
                                'profile_it_rect' : (600,150,400,600),
                                'profile_tb_rect' : (610,425,380,50),
                                'static_img' : [
                                    ('b_return_profile',(20,780,100,100),pygame.image.load('lib/images/common/return.png'),
                                        pygame.image.load('lib/images/common/return_pushed.png')),
                                    ('b_setting_profile',(140,780,100,100),pygame.image.load('lib/images/common/setting.png'),
                                        pygame.image.load('lib/images/common/setting_pushed.png')),
                                    ('b_profile_profile',(260,780,100,100),pygame.image.load('lib/images/common/profile.png'),
                                        pygame.image.load('lib/images/common/profile_pushed.png')),
                                    ('t_new_profile_0',(50,500,100,80),pygame.image.load('lib/images/profile/new.png'),
                                        pygame.image.load('lib/images/profile/new_pushed.png')),
                                    ('t_load_profile_0',(250,500,100,80),pygame.image.load('lib/images/profile/load.png'),
                                        pygame.image.load('lib/images/profile/load_pushed.png')),
                                    ('t_up_profile_0',(300,475,20,20),pygame.image.load('lib/images/profile/pageup.png'),
                                        pygame.image.load('lib/images/profile/pageup.png')),
                                    ('t_down_profile_0',(330,475,20,20),pygame.image.load('lib/images/profile/pagedown.png'),
                                        pygame.image.load('lib/images/profile/pagedown.png')),
                                    ('t_confirm_profile_1',(50,500,100,80),pygame.image.load('lib/images/profile/confirm.png'),
                                        pygame.image.load('lib/images/profile/confirm_pushed.png')),
                                    ('t_back_profile_1',(250,500,100,80),pygame.image.load('lib/images/profile/back.png'),
                                        pygame.image.load('lib/images/profile/back_pushed.png')),
                                    ('p_select_profile_',(30,40,340,70),pygame.image.load('lib/images/profile/player_button.png'),
                                        pygame.image.load('lib/images/profile/player_button_selected.png')),
                                    ('i_achieve_profile_b',(800,400,40,40),pygame.image.load('lib/images/profile/achbutton.png')),
                                    ('i_kill_profile_b',(850,400,40,40),pygame.image.load('lib/images/profile/killbutton.png')),
                                    ('i_statistic_profile_b',(900,400,40,40),pygame.image.load('lib/images/profile/statisticbutton.png')),
                                    ('i_playerinfo_profile',(800,450,750,400),pygame.image.load('lib/images/profile/playerinfo.png')),
                                    ('b_save_profile',(380,780,100,100),pygame.image.load('lib/images/profile/save.png'),
                                        pygame.image.load('lib/images/profile/save_pushed.png'))
                                ]
        }
        self.world_info = {
                            'world_count' : 1,
                            'level_count' : [(0,3)],
                            'level_button_rect' :[
                                (745,555,50,50,0),
                                (830,490,50,50,1),
                                (910,445,50,50,2),
                            ],
                            'level_image_list' : [
                                pygame.image.load('lib/images/world/level_disabled.png'),
                                pygame.image.load('lib/images/world/level.png'),
                                pygame.image.load('lib/images/world/level_pushed.png')
                            ],
                            'static_img' : [
                                ('i_header_world',(0,0,1600,40),pygame.image.load('lib/images/world/header.png')),
                                ('b_return_world',(20,780,100,100),pygame.image.load('lib/images/common/return.png'),
                                    pygame.image.load('lib/images/common/return_pushed.png')),
                                ('b_setting_world',(140,780,100,100),pygame.image.load('lib/images/common/setting.png'),
                                    pygame.image.load('lib/images/common/setting_pushed.png')),
                                ('b_profile_profile',(260,780,100,100),pygame.image.load('lib/images/common/profile.png'),
                                        pygame.image.load('lib/images/common/profile_pushed.png')),
                                ('b_previous_world',(10,425,50,50),pygame.image.load('lib/images/world/previous_world.png'),
                                    pygame.image.load('lib/images/world/previous_world_pushed.png')),
                                ('b_next_world',(1540,425,50,50),pygame.image.load('lib/images/world/next_world.png'),
                                    pygame.image.load('lib/images/world/next_world_pushed.png')),
                                ('g_1_world',(0,0,1600,900),pygame.image.load('lib/images/world/world1_background.png')),
                                ('m_1_world',(550,130,500,800),pygame.image.load('lib/images/world/world1_1.png'),
                                    pygame.image.load('lib/images/world/world1_2.png'),
                                    pygame.image.load('lib/images/world/world1_3.png'),
                                    pygame.image.load('lib/images/world/world1_4.png')),
                            ],
                            'dynamic_img' : [
                                ('1_cloud_world',(-200,800,100,100),5,0,pygame.image.load('lib/images/world/cloud.png')),
                                ('1_smoke_world',(935,380,30,30),1.5,1,pygame.image.load('lib/images/world/smoke.png'))
                            ]
        }
        self.level_common_info = {
                            'skill_q_pos' : (730,845,50,50),
                            'skill_e_pos' : (820,845,50,50),
                            'main_character_starting_pos' : (20,800),
                            'static_img' : [
                                ('i_healthbar_game',(30,30,370,50),pygame.image.load('lib/images/game/health.png')),
                                ('b_setting_game',(1490,10,100,100),pygame.image.load('lib/images/common/setting.png'),
                                    pygame.image.load('lib/images/common/setting_pushed.png')),
                                ('i_mpbar_game',(30,100,370,50),pygame.image.load('lib/images/game/mp.png')),
                                ('i_target_game_t',(420,30,100,100),pygame.image.load('lib/images/game/target.png'))
                            ]
        }
        self.levels_info = {
            'g0101' : {
                'id' : 0,
                'platform' : [
                    ((100.0,600.0,250,5),(190,180,80),0),
                    ((1250.0,600.0,250,5),(190,180,80),0)
                ],
                'background' : [
                    (pygame.image.load('lib/images/game/g_0101_l.png'),(0,0,1600,900)),
                    (pygame.image.load('lib/images/game/g_0101_u.png'),(0,0,1600,900))
                ],
                'enemy' : {
                    '101' : (0,pygame.image.load('lib/images/game/e_0101_1_1.png'),
                             pygame.image.load('lib/images/game/e_0101_1_2.png'),
                             pygame.image.load('lib/images/game/e_0101_1_d1.png'),
                             pygame.image.load('lib/images/game/e_0101_1_d2.png'),
                             pygame.image.load('lib/images/game/e_0101_1_d3.png')),
                }
            }

        }
        self.gameover = {
            'static_img' : [
                ('g_gameover',(0,0,1600,900),pygame.image.load('lib/images/gameover/GameOver.png')),
                ('b_continue_gameover',(700,750,200,100),pygame.image.load('lib/images/gameover/continue.png'),
                    pygame.image.load('lib/images/gameover/continue_pushed.png'))
            ]
        }
        self.victory = {
            'static_img' : [
                ('b_return_victory',(1490,790,100,100),pygame.image.load('lib/images/common/return.png'),
                    pygame.image.load('lib/images/common/return_pushed.png')),
            ],
            'dynamic_img' : [
                ('_firework_',(800,900,30,50),10,0,
                    (
                        (pygame.image.load('lib/images/victory/firework_0_r.png'),
                            pygame.image.load('lib/images/victory/firework_1_r.png')),
                        (pygame.image.load('lib/images/victory/firework_0_g.png'),
                            pygame.image.load('lib/images/victory/firework_1_g.png')),
                        (pygame.image.load('lib/images/victory/firework_0_y.png'),
                            pygame.image.load('lib/images/victory/firework_1_y.png'))
                    )
                )
            ]
        }
        self.character = {
                            'weapon_pos' : (30,30),
                            'upper' : [
                                pygame.image.load('lib/images/game/maincharacter_u_n.png'),
                                pygame.image.load('lib/images/game/maincharacter_u_h.png'),
                            ],
                            'lower' : [
                                pygame.image.load('lib/images/game/maincharacter_d_n.png'),
                                pygame.image.load('lib/images/game/maincharacter_d_m1.png'),
                                pygame.image.load('lib/images/game/maincharacter_d_m2.png'),
                                pygame.image.load('lib/images/game/maincharacter_d_m3.png'),
                            ]
        }
        self.weapon = {
                        '10001' : {
                            'images' : [
                                pygame.image.load('lib/images/game/pistol_0.png'),
                                pygame.image.load('lib/images/game/pistol_1.png'),
                                pygame.image.load('lib/images/game/pistol_2.png'),
                                pygame.image.load('lib/images/game/pistol_3.png')
                            ],
                            'bullet' : pygame.image.load('lib/images/game/bullet_small.png')
                        },
                        '10002' : {
                            'images' : [
                                pygame.image.load('lib/images/game/ak_0.png'),
                                pygame.image.load('lib/images/game/ak_1.png'),
                                pygame.image.load('lib/images/game/ak_2.png'),
                                pygame.image.load('lib/images/game/ak_3.png'),
                                pygame.image.load('lib/images/game/ak_4.png'),
                            ],
                            'bullet' : pygame.image.load('lib/images/game/bullet_mid.png')
                        },
                        '90001' : {
                            'bullet' : pygame.image.load('lib/images/game/fire_ball.png')
                        }
        }
        self.skill = {
            'super_reload' : pygame.image.load('lib/images/game/c_super_reload_icon.png'),
            'super_boost'  : pygame.image.load('lib/images/game/c_super_boost_icon.png'),
            'fire_ball'    : pygame.image.load('lib/images/game/c_fire_ball_icon.png')
        }


setting = Settings()

#static image classes for simple item managing
class Static_Base(pygame.sprite.Sprite):
    #states
    ENTER = 'enter'
    ACTIVE = 'active'
    LEAVE = 'leave'
    FIN = 'fin'

    def __init__(self,name,rect):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.fixed_rect = rect

        self.state = Static_Base.ENTER
    
    def init_pos_info(self):
        pass

    def sleep(self):
        pass

    def update(self):
        pass

    def get_enter_direction(self):
        if self.fixed_rect[1] <= 450:
            self.speed_factor = 1
        else:
            self.speed_factor = -1
        

class Button(Static_Base):
    def __init__(self,name,rect,imgs):
        super().__init__(name,rect)
        
        self.cond = 0
        
        self.images = []
        for image in imgs:
            self.images.append(image)
        self.image = self.images[self.cond]
        self.rect  = self.image.get_rect()
        
        self.init_pos_info()

        self.clicked_time = -1
    
    def change_pic(self):
        if self.cond:
            self.cond = 0
        else:
            self.cond = 1

        self.image = self.images[self.cond]
        
        if self.clicked_time == -1:
            self.clicked_time = time.time()
    
    def repos(self):
        self.change_pic()
        self.clicked_time = -1
    
    def sleep(self):
        self.state = Static_Base.ENTER
        self.cond = 1
        self.repos()

        self.rect.left,self.rect.bottom = self.start_pos[0],self.start_pos[1]
    
    def init_pos_info(self):
        self.get_enter_direction()
        if self.speed_factor == 1:
            self.start_pos = (self.fixed_rect[0],-100 - self.fixed_rect[1])
        elif self.speed_factor == -1:
            self.start_pos = (self.fixed_rect[0],1700)
        
        self.rect.left,self.rect.top = self.start_pos[0],self.start_pos[1]

    def update(self):
        if self.state == Static_Base.ENTER:
            if self.speed_factor == 1:
            #if the item has arrived at the ending position
                if self.rect.top >= self.fixed_rect[1]:
                    self.state = Static_Base.ACTIVE
            elif self.speed_factor == -1:
                if self.rect.top <= self.fixed_rect[1]:
                    self.state = Static_Base.ACTIVE
        elif self.state == Static_Base.LEAVE:
            if self.speed_factor == 1:
            #if the item has arrived at the starting position
                if self.rect.bottom <= 0:
                    self.state = Static_Base.FIN
            elif self.speed_factor == -1:
                if self.rect.top >= 900:
                    self.state = Static_Base.FIN

        if self.state == Static_Base.ENTER:
        #state -1 means this item is entering the screen
            self.rect.y += self.speed_factor * 10
        elif self.state == Static_Base.LEAVE:
        #state 1 means this item is leaving the screen
            self.rect.y -= self.speed_factor * 10

    def is_clicked(self,pos):
        if pos[0] >= self.rect[0] and pos [0] <= self.rect[0] + self.rect[2]:
            if pos[1] >= self.rect[1] and pos[1] <= self.rect[1] + self.rect[3]:
                return True
    
        return False


class Level_Button(Button):
    def __init__(self,player,name,rect,lid,imgs):
        super().__init__(name,rect,imgs)

        self.images = setting.world_info['level_image_list']
        for image in self.images:
            image.convert_alpha

        self.player = player
        self.has_on = 0
        self.lid = lid

        if self.lid == 0:
            self.image = self.images[1]
            self.has_on = 1
        else:
            self.image = self.images[0]
    
    def init_pos_info(self):
        self.speed_factor = -1
        self.start_pos = (self.fixed_rect[0],1000)
      
        self.rect.left,self.rect.top = self.start_pos[0],self.start_pos[1]

    def check_has_on(self):
        if self.lid == 0:
            self.has_on = 1
        else:
            if self.player.finished_level[self.lid - 1] == 1:
                self.has_on = 1

    def sleep(self):
        self.state = Static_Base.ENTER
        self.cond = 0
        if self.has_on == 1:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        self.clicked_time = -1

    def repos(self):
        self.change_pic()
        self.clicked_time = -1
    
    def change_pic(self):
        if self.cond:
            self.cond = 0
        else:
            self.cond = 1

        self.image = self.images[self.cond + 1]
        
        if self.clicked_time == -1:
            self.clicked_time = time.time()

    def update(self):
        self.check_has_on()
        super().update()



class Image(Static_Base):
    def __init__(self,name,rect,img):
        super().__init__(name,rect)

        self.image = img
        self.rect  = self.image.get_rect()

        self.init_pos_info()
    
    def sleep(self):
        self.state = Static_Base.ENTER

        self.rect.left,self.rect.bottom = self.start_pos[0],self.start_pos[1]
    
    def init_pos_info(self):
        self.get_enter_direction()
        if self.speed_factor == 1:
            self.start_pos = (self.fixed_rect[0],-100 - self.fixed_rect[1])
        elif self.speed_factor == -1:
            self.start_pos = (self.fixed_rect[0],1700)
        
        self.rect.left,self.rect.top = self.start_pos[0],self.start_pos[1]

    def update(self):
        if self.state == Static_Base.ENTER:
            if self.speed_factor == 1:
            #if the item has arrived at the ending position
                if self.rect.top >= self.fixed_rect[1]:
                    self.state = Static_Base.ACTIVE
            elif self.speed_factor == -1:
                if self.rect.top <= self.fixed_rect[1]:
                    self.state = Static_Base.ACTIVE
        elif self.state == Static_Base.LEAVE:
            if self.speed_factor == 1:
            #if the item has arrived at the starting position
                if self.rect.bottom <= 0:
                    self.state = Static_Base.FIN
            elif self.speed_factor == -1:
                if self.rect.top >= 900:
                    self.state = Static_Base.FIN

        if self.state == Static_Base.ENTER:
        #state -1 means this item is entering the screen
            self.rect.y += self.speed_factor * 5
        elif self.state == Static_Base.LEAVE:
        #state 1 means this item is leaving the screen
            self.rect.y -= self.speed_factor * 5


class Subimage(pygame.sprite.Sprite):
    def __init__(self,name,rect,imgs,surface):
        pygame.sprite.Sprite.__init__(self)

        self.name = name

        self.surface = surface
        self.images = imgs
        self.image = self.images[0]
        self.fixed_rect = rect
        self.rect  = self.image.get_rect()
        self.rect.left,self.rect.top = self.fixed_rect[0],self.fixed_rect[1]

        self.cond = 0
        self.clicked_time = -1
    
    def draw(self):
        self.surface.blit(self.image,self.rect)
    
    def change_pic(self):
        if self.cond:
            self.cond = 0
        else:
            self.cond = 1

        self.image = self.images[self.cond]
        
        if self.clicked_time == -1:
            self.clicked_time = time.time()

    def sleep(self):
        self.image = self.images[0]
        self.cond = 0
        self.clicked_time = -1
    
    def repos(self):
        self.change_pic()
        self.clicked_time = -1

    def get_realrect(self,rect):
        self.rect.left = self.fixed_rect[0] + rect.left
        self.rect.top  = self.fixed_rect[1] + rect.top
    
    def is_clicked(self,pos):
        if pos[0] >= self.rect[0] and pos [0] <= self.rect[0] + self.rect[2]:
            if pos[1] >= self.rect[1] and pos[1] <= self.rect[1] + self.rect[3]:
                return True
    
        return False


class Save_Block(pygame.sprite.Sprite):
    def __init__(self,i,name,rect,imgs,surface,player_info,page):
        pygame.sprite.Sprite.__init__(self)

        self.name = name + str(i % 5)
        self.seq = i
        self.page = page

        self.selected = 0

        self.player = player_info
        
        self.surface = surface
        self.images = imgs
        self.image = self.images[0]
        self.fixed_rect = tuple(rect)
        self.rect  = self.image.get_rect()
        self.rect.left,self.rect.top = self.fixed_rect[0],self.fixed_rect[1]

        self.font = pygame.font.SysFont(None,30)
        self.small_font = pygame.font.SysFont(None,20)
        self.prepare_msg()
    
    def prepare_msg(self):
        self.name_msg = self.font.render(self.player.name,True,
                                         setting.color['white'],setting.color['dark_grey'])
        self.name_rect = self.name_msg.get_rect()
        self.version_msg = self.small_font.render(self.player.created_version,True,
                                            setting.color['white'],setting.color['dark_grey'])
        self.ver_rect = self.version_msg.get_rect()
        new_time = time.localtime(self.player.time)
        new_time_info = str(new_time.tm_year) + " " + str(new_time.tm_mon) + " " \
                        + str(new_time.tm_wday) + " " + str(new_time.tm_hour) + " " \
                        + str(new_time.tm_min) + " " + str(new_time.tm_sec)   
        self.time_msg = self.small_font.render(new_time_info,True,
                                         setting.color['white'],setting.color['dark_grey'])
        self.time_rect = self.time_msg.get_rect()                               

    def change_state(self):
        if self.selected == 0:
            self.image = self.images[1]
            self.prepare_msg()
            self.selected = 1
        
        elif self.selected == 1:
            self.image = self.images[0]
            self.prepare_msg()
            self.selected = 0
    
    def get_realrect(self,rect):
        self.rect.left = self.fixed_rect[0] + rect.left
        self.rect.top  = self.fixed_rect[1] + rect.top
    
    def sleep(self):
        self.selected = 1
        self.change_state()

    def draw(self,screen):
        self.name_rect.center = self.rect.center
        self.time_rect.center = self.name_rect.center
        self.time_rect.top = self.name_rect.top + 20
        self.ver_rect.right = self.rect.right
        self.ver_rect.bottom = self.rect.bottom

        screen.blit(self.name_msg,self.name_rect)
        screen.blit(self.version_msg,self.ver_rect)
        screen.blit(self.time_msg,self.time_rect)
        

class Info_Template(Static_Base):
    #states
    ENTER = 'enter'
    SELECT = 'select'
    TEXT = 'text'
    INPUT = 'input'
    LEAVE = 'leave'
    FIN = 'fin'

    def __init__(self,name,rect,background_color,setting):
        super().__init__(name,rect)

        self.setting = setting

        self.state = Info_Template.ENTER
        self.display = 1
        self.current_page = 0
        self.current_selection = -1

        self.previous_selected_button = None

        self.color = background_color
        self.image = pygame.Surface((400,600))
        self.image.fill(self.color)
        self.image.fill((220,220,220),(20,20,360,450))
        self.rect  = self.image.get_rect()
        
        self.save_reader = lib.tool.Save_Reader()
        self.text_block = lib.tool.TextBar((self.setting.profile_info['profile_tb_rect'][0],
                                    self.setting.profile_info['profile_tb_rect'][1]),
                                    (self.setting.profile_info['profile_tb_rect'][2],
                                    self.setting.profile_info['profile_tb_rect'][3]),
                                    self.setting)
        self.player_button = pygame.sprite.Group()
        self.image_group_0 = pygame.sprite.Group()
        self.image_group_1 = pygame.sprite.Group()
        self.active_button = self.image_group_0

        self.save_reader.init_players()
        self.player_button_list = []
        self.init_image()
        self.init_pos_info()
    
    def init_image(self):
        for image in setting.profile_info['static_img']:
            if image[0][0] == 't':
                if image[0][-1] == '0':
                    new_image = Subimage(image[0],image[1],image[2:],self.image)
                    self.image_group_0.add(new_image)
                elif image[0][-1] == '1':
                    new_image = Subimage(image[0],image[1],image[2:],self.image)
                    self.image_group_1.add(new_image)
            elif image[0][0] == 'p':
                player_bar_info = image
        
        sav_list = self.save_reader.get_all_savs()
        self.max_page = 0

        for i in range(len(sav_list)):
            new_rect = list(player_bar_info[1])
            new_rect[1] += 85 * (i % 5)
            new_player_button = Save_Block(i,player_bar_info[0],new_rect,
                                           player_bar_info[2:],self.image,sav_list[i],int(i / 5))
            self.player_button_list.append(new_player_button)

            if int(i / 5) > self.max_page:
                self.max_page = int(i / 5)

        for button in self.player_button_list:
            if button.page == self.current_page:
                self.player_button.add(button)
    
    def page_down(self):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.player_button.empty()

        for button in self.player_button_list:
            if button.page == self.current_page:
                self.player_button.add(button)
    
    def page_up(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.player_button.empty()

        for button in self.player_button_list:
            if button.page == self.current_page:
                self.player_button.add(button)
    
    def get_selected_player(self):
        return self.save_reader.player_group[self.current_selection]

    def init_pos_info(self):
        self.get_enter_direction()

        self.start_pos = (self.fixed_rect[0],-600 - self.fixed_rect[1])
        self.rect.left,self.rect.top = self.start_pos[0],self.start_pos[1]
    
    def update(self):
        if self.state == Info_Template.ENTER:
            if self.rect.top >= self.fixed_rect[1]:
            #if the item has arrived at the ending position
                self.state = Info_Template.SELECT
        elif self.state == Info_Template.SELECT:
            self.image.fill(self.color)
            self.image.fill((220,220,220),(20,20,360,450))
            self.active_button = self.image_group_0
        elif self.state == Info_Template.TEXT:
            self.image.fill(self.color)
            self.active_button = self.image_group_1
        elif self.state == Info_Template.INPUT:
            self.image.fill(self.color)
            self.text_block.update()
        elif self.state == Info_Template.LEAVE:
            if self.display == 1:
                if self.rect.bottom <= 0:
                #if the item has arrived at the starting position
                    self.state = Info_Template.FIN
            elif self.display == 0:
                self.rect.left,self.rect.top = self.start_pos[0],self.start_pos[1]
                self.state = Info_Template.FIN
        
        if self.state == Info_Template.ENTER:
            #state -1 means this item is entering the screen
            self.rect.y += self.speed_factor * 5
        elif self.state == Info_Template.LEAVE:
            self.rect.y -= self.speed_factor * 5
          
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        
        for image in self.active_button.sprites():
            if isinstance(image,Subimage):
                if image.clicked_time != -1:
                    now = time.time()

                    if now - image.clicked_time >= 0.1:
                        image.repos()

            image.get_realrect(self.rect)
        self.active_button.draw(screen)

        for player in self.player_button.sprites():
            player.get_realrect(self.rect)

        if self.state == Info_Template.TEXT or self.state == Info_Template.INPUT:
            self.text_block.draw(screen)
        elif self.state == Info_Template.SELECT:
            self.player_button.draw(screen)
            for player_bar in self.player_button.sprites():
                player_bar.draw(screen)
    
    def sleep(self,has_player):
        self.state = Info_Template.ENTER
        self.previous_selected_button = None
        self.current_selection = -1
        self.current_page = 0
        self.player_button.empty()
        for button in self.player_button_list:
            if button.page == self.current_page:
                self.player_button.add(button)

        if has_player:
            self.display = 0
        else:
            self.display = 1
        
        self.active_button = self.image_group_0
        for item in self.image_group_0.sprites():
            item.sleep()
        for item in self.image_group_1.sprites():
            item.sleep()
        for player in self.player_button_list:
            player.sleep()
        self.text_block.sleep()

    def not_empty(self):
        if len(self.text_block.current_str):
            return True
        else:
            return False

    def check_input(self):
        return self.text_block.check_input()

    def get_string(self):
        return self.text_block.get_string()

    def check_event(self,pos,event_type,key = None):
        if self.state == Info_Template.SELECT:
            flag = 0
            if event_type == 'up':
                for player_bar in self.player_button.sprites():
                    if player_bar.rect.collidepoint(pos):
                        flag = 1
                        if player_bar.selected == 0:
                            player_bar.change_state()
                            self.current_selection = player_bar.seq

                            if self.previous_selected_button != None and self.previous_selected_button != player_bar:
                                self.previous_selected_button.sleep()

                            self.previous_selected_button = player_bar
                        else:
                            player_bar.sleep()
                            self.current_selection = -1
                    
            if flag == 0:
                for item in self.active_button.sprites():
                    if item.rect.collidepoint(pos):
                        if event_type == 'down':
                            item.change_pic()
                        elif event_type == 'up':
                            new_event_type = self.get_event_type(item.name)
                            new_event = setting.event['profile'][new_event_type]

                            if new_event == setting.event['profile']['new']:
                                self.state = Info_Template.TEXT
                        
                            return new_event

            return setting.event['common']['pass']
        elif self.state == Info_Template.TEXT:
            for item in self.active_button.sprites():
                if item.rect.collidepoint(pos):
                    if event_type == 'down':
                        item.change_pic()
                    elif event_type == 'up':
                        new_event_type = self.get_event_type(item.name)
                        new_event = setting.event['profile'][new_event_type]

                        if new_event == setting.event['profile']['back']:
                            self.state = Info_Template.SELECT
                        elif new_event == setting.event['profile']['confirm']:
                            if len(self.text_block.current_str):
                                self.state = Info_Template.SELECT
                        
                        return new_event
            
            if self.text_block.rect.collidepoint(pos) and event_type == 'down':
                self.text_block.switch_state(1)
                self.state = Info_Template.INPUT
                new_event = setting.event['profile']['input']

                return new_event
            
            return setting.event['common']['pass']
        elif self.state == Info_Template.INPUT:
            if event_type == 'down':
                new_event = setting.event['profile']['cancel']
                self.text_block.switch_state(0)
                self.state = Info_Template.TEXT

                return new_event
            else:
                return setting.event['common']['pass']
   
    @staticmethod
    def get_event_type(name):
        '''
            this method gets the event type between
            two underbars in the button's name.
        '''
        result = ''
        flag = 0
        
        for c in name:
            if c == '_':
                flag += 1
                continue
            
            if flag == 1:
                result += c
            elif flag > 1:
                break
            
        return result


class Setting_Template(Static_Base):
    def __init__(self,name,rect,background_color,setting,screen_obj):
        super().__init__(name,rect)

        self.screen_obj = screen_obj

        self.setting = setting

        self.color = background_color
        self.image = pygame.Surface((400,600))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = rect[0],rect[1]

        self.prepare_elements()

    def prepare_elements(self):
        self.button_group = pygame.sprite.Group()

        for image in setting.game_info['static_img']:
            if image[0][0] == 's':
                new_button = Subimage(image[0],image[1],image[2:],self.screen_obj.screen)
                new_button.get_realrect(self.rect)
                if self.screen_obj.name[0] == 'g':
                    self.button_group.add(new_button)
                else:
                    if new_button.name != 's_back_common':
                        new_button.rect.centerx = 800
                        self.button_group.add(new_button)
        
        self.title_font = pygame.font.SysFont('impact',60)
        self.info_font  = pygame.font.SysFont(None,30)
        self.ver_font   = pygame.font.SysFont(None,18)

        self.title = 'PAUSE'
        self.title_msg  = self.title_font.render(self.title,True,setting.color['black'])
        self.title_rect = self.title_msg.get_rect()
        self.title_rect.top = self.rect.top + 20
        self.title_rect.centerx = 800

        self.version_msg = self.ver_font.render(setting.game_info['version'],True,
                                                setting.color['white'])
        self.version_rect = self.version_msg.get_rect()
        self.version_rect.right,self.version_rect.bottom = self.rect.right,self.rect.bottom

        self.screen_name_msg = self.info_font.render(self.screen_obj.name,True,setting.color['white'])
        self.screen_name_rect = self.screen_name_msg.get_rect()
        self.screen_name_rect.top = self.title_rect.bottom + 20
        self.screen_name_rect.centerx = 800
    
    def update(self):
        new_time = time.localtime()
        self.time_text = str(new_time.tm_year) + "/" + str(new_time.tm_mon) + "/" + str(new_time.tm_mday) + \
                        " " + str(new_time.tm_hour) + ":" + str(new_time.tm_min) + ":" + str(new_time.tm_sec)
        self.time_msg = self.ver_font.render(self.time_text,True,setting.color['light_grey'])
        self.time_rect = self.time_msg.get_rect()
        self.time_rect.top = self.screen_name_rect.bottom + 20
        self.time_rect.centerx = 800            

    def draw(self,screen):
        screen.blit(self.image,self.rect)

        screen.blit(self.title_msg,self.title_rect)
        screen.blit(self.screen_name_msg,self.screen_name_rect)
        screen.blit(self.time_msg,self.time_rect)
        screen.blit(self.version_msg,self.version_rect)

        for button in self.button_group.sprites():
            if button.clicked_time != -1:
                now = time.time()

                if now - button.clicked_time >= 0.1:
                    button.repos()
        self.button_group.update()
        self.button_group.draw(screen)
    
    def check_event(self,pos,event_type):
        for button in self.button_group.sprites():
            if button.rect.collidepoint(pos):
                if event_type == 'down':
                    button.change_pic()
                elif event_type == 'up':
                    new_event_type = self.get_event_type(button.name)
                    new_event = setting.event[self.screen_obj.name][new_event_type]

                    return new_event
            
    
    @staticmethod
    def get_event_type(name):
        '''
            this method gets the event type between
            two underbars in the button's name.
        '''
        result = ''
        flag = 0
        
        for c in name:
            if c == '_':
                flag += 1
                continue
            
            if flag == 1:
                result += c
            elif flag > 1:
                break
            
        return result






        
class Background(Static_Base):
    def __init__(self,name,rect,image):
        super().__init__(name,rect)

        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = self.fixed_rect[0],self.fixed_rect[1]


class Map(Static_Base):
    def __init__(self,name,rect,imgs):
        super().__init__(name,rect)

        self.seq = self.get_seq()

        self.imgs = imgs
        self.current_image = 0
        self.image = self.imgs[self.current_image]
        self.rect = self.image.get_rect()
        self.update_time = -1

        self.init_pos_info()

    def init_pos_info(self):
        self.speed_factor = -1
        self.start_pos = (self.fixed_rect[0],1000)
      
        self.rect.left,self.rect.top = self.start_pos[0],self.start_pos[1]

    def update(self):
        if self.state == Static_Base.ENTER:
            if self.rect.top <= self.fixed_rect[1]:
                self.state = Static_Base.ACTIVE
                self.update_time = time.time()
            else:
                self.rect.top += 15 * self.speed_factor
        elif self.state == Static_Base.ACTIVE:
            now = time.time()

            if now - self.update_time > 0.07:
                self.update_time = now
                if self.current_image != len(self.imgs) - 1:
                    self.current_image += 1
                    self.image = self.imgs[self.current_image]
                else:
                    self.current_image = 0
                    self.image = self.imgs[self.current_image]
        elif self.state == Static_Base.LEAVE:
            if self.rect.top >= 900:
                self.state = Static_Base.FIN
            else:
                self.rect.y -= self.speed_factor * 15

    def sleep(self):
        self.state = Static_Base.ENTER
        self.current_image = 0
        self.image = self.imgs[0]
        self.update_time = -1

    def get_seq(self):
        '''
            this method gets the map's sequence between
            two underbars in the map's name.
        '''
        flag = 0
        
        for c in self.name:
            if c == '_':
                flag += 1
                continue
            
            if flag == 1:
                self.seq = c
            elif flag > 1:
                break


#dynamic_base is the base class of all moving game items
class Dynamic_Image(pygame.sprite.Sprite):
    def __init__(self,name,rect,speed,image):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        if len(image) == 1:
            self.image = image[0]
        else:
            self.imgs = image
            self.image = image[0]
        
        self.starting_rect = rect
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = self.starting_rect[0],self.starting_rect[1]

        self.speed = speed

        self.has_on = 0
        self.state = 0
        self.last_change = -1
    
    def update(self):
        if self.rect.left >= 1600 or self.rect.bottom <= 0:
            self.state = 1
        
        if self.state == 0:
            if self.name == 'smoke':
                if self.has_on == 0:
                    self.next_angle = 0
                    self.has_on = 1
                
                self.rect.y -= self.speed
                self.rect.x += self.speed * self.next_angle
                
                if self.next_angle != 1:
                    self.next_angle += 0.1
            elif self.name == 'cloud':
                if self.has_on == 0:
                    self.rect.y -= 700 * random.random()
                    self.has_on = 1
                
                self.rect.x += self.speed
            elif self.name == 'firework':
                if self.has_on == 0:
                    self.destination = (self.rect.centerx + (800 * random.uniform(-1,1)),800 - (700 * random.random()))
                    self.rect.centerx = self.destination[0]
                    self.has_on = 1

                if self.rect.top >= self.destination[1]:
                    self.rect.centery -= self.speed
                else:
                    self.state = 2
                    self.image = self.imgs[1]
                    self.blossom = time.time()
                    self.last_change = self.blossom
        elif self.state == 2:
            if self.name == 'firework':
                now = time.time()

                if now - self.blossom >= 4:
                    self.state = 1
                elif now - self.last_change > 1:
                    x = self.rect.right - self.rect.left
                    y = self.rect.bottom - self.rect.top
                    self.image = pygame.transform.scale(self.image,(x * 2,y * 2))
                    self.rect = self.image.get_rect()
                    self.rect.centerx,self.rect.centery = self.destination[0],self.destination[1]
                    self.last_change = now


class Dynamic_Group():
    def __init__(self,name,rect,speed,layer,image):
        self.name = name
        self.get_dynamic_type()
        if self.name != '_firework_':
            self.imgs = list(image)
            for image in self.imgs:
                image = image.convert_alpha()
        else:
            self.imgs = list(image)
            for firework_group in self.imgs:
                for image in firework_group:
                    image = image.convert_alpha()
        self.speed = speed
        self.layer = layer

        self.start_rect = rect

        self.last_update = -1

        self.dynamic_group = pygame.sprite.Group()
    
    def update(self):
        for dy in self.dynamic_group.sprites():
            if dy.state == 1:
                self.dynamic_group.remove(dy)

        if self.dy_type == 'smoke':
            if self.last_update == -1:
                new_dy = Dynamic_Image(self.dy_type,self.start_rect,self.speed,self.imgs)
                self.dynamic_group.add(new_dy)
                self.last_update = time.time()
            else:
                now = time.time()
                self.dynamic_group.update()
                
                if now - self.last_update >= 0.8:
                    new_dy = Dynamic_Image(self.dy_type,self.start_rect,self.speed,self.imgs)
                    self.dynamic_group.add(new_dy)
                    self.last_update = now
        elif self.dy_type == 'cloud':
            if self.last_update == -1:
                new_dy = Dynamic_Image(self.dy_type,self.start_rect,self.speed,self.imgs)
                self.dynamic_group.add(new_dy)
                self.last_update = time.time()
            else:
                now = time.time()
                self.dynamic_group.update()
                
                if now - self.last_update >= 0.3:
                    if len(self.dynamic_group) <= 8:
                        new_image = pygame.transform.scale(self.imgs[0],(int(self.start_rect[2] + 100 * random.random()),
                                                                    int(self.start_rect[3] + 100 * random.random())))
                        new_image_list = [new_image]
                        new_dy = Dynamic_Image(self.dy_type,self.start_rect,self.speed,new_image_list)
                        self.dynamic_group.add(new_dy)
                        self.last_update = now
        elif self.dy_type == 'firework':
            if self.last_update == -1:
                new_color = random.choice([0,1,2])
                new_dy = Dynamic_Image(self.dy_type,self.start_rect,self.speed,self.imgs[new_color])
                self.dynamic_group.add(new_dy)
                self.last_update = time.time()
            else:
                now = time.time()
                self.dynamic_group.update()
                
                if now - self.last_update >= 1.2:
                    new_color = random.choice([0,1,2])
                    new_dy = Dynamic_Image(self.dy_type,self.start_rect,self.speed,self.imgs[new_color])
                    self.dynamic_group.add(new_dy)
                    self.last_update = now

    def sleep(self):
        self.last_update = -1
        self.dynamic_group.empty()
    
    def draw(self,screen):
        self.dynamic_group.update()
        self.dynamic_group.draw(screen)

    def get_dynamic_type(self):
        '''
            this method gets the dynamic object type between
            two underbars in the object's name.
        '''
        result = ''
        flag = 0
        
        for c in self.name:
            if c == '_':
                flag += 1
                continue
            
            if flag == 1:
                result += c
            elif flag > 1:
                break

            self.dy_type = result


class Platform(pygame.sprite.Sprite):
    def __init__(self,rect,color,new_type):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(rect[0],rect[1],rect[2],rect[3])
        self.fixed_rect = rect
        self.color = color

        self.platform_type = new_type
        if self.platform_type == 0:
            self.move_direction = 0
        elif self.platform_type == 1:
            self.move_direction = 1
        elif self.platform_type == 2:
            self.move_direction = 2

    def update(self,screen):
        if self.platform_type == 1:
            if self.move_direction == 1:
                if self.rect.top >= self.fixed_rect[1] + 200:
                    self.move_direction = -1
            elif self.move_direction == -1:
                if self.rect.top <= self.fixed_rect[1] - 200:
                    self.move_direction = 1
        elif self.platform_type == 2:
            if self.move_direction == 2:
                if self.rect.left >= self.fixed_rect[0] + 200:
                    self.move_direction = -2
            elif self.move_direction == -2:    
                if self.rect.right <= self.fixed_rect[0] - 200:
                    self.move_direction = 2
            
        if self.move_direction == 1:
            self.rect.centery += 1
        elif self.move_direction == -1:
            self.rect.centery -= 1
        elif self.move_direction == 2:
            self.rect.centerx -= 1
        elif self.move_direction == -2:
            self.rect.centerx += 1

        screen.fill(self.color,self.rect)