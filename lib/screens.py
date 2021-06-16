#Screen module
import lib.settings
import lib.player
import lib.game
import pygame
import random
import time

#screen base is the base class of all screens
class Screen_Base():
    def __init__(self,setting,screen):
        self.name = 'null'
        self.id   = '000'
        self.setting = setting

        self.screen = screen

        self.player = None

        self.state  = -1
        self.has_on = 0
    
    def prepare_elements(self):
        pass
    
    def sleep(self):
        pass

    def has_end_moving(self):
        pass
        
    def draw(self):
        pass

    def get_event(self):
        pass

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
    

#screens
class Title(Screen_Base):
    def __init__(self,setting,event_queue,screen):
        super().__init__(setting,screen)

        self.name = 'title'
        self.id   = '001'

        self.state  = -1
        self.has_on = 0

        self.event_queue = event_queue
        self.prepare_elements()
    
    def show_setting(self):
        pass

    def return_to_main(self):
        pass

    def sleep(self):
        self.state  = -1
        self.has_on = 0

        for item in self.image_group.sprites():
            item.sleep()
        for item in self.button_group.sprites():
            item.sleep()
    
    def prepare_elements(self):
        self.image_group  = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()

        image_list = self.setting.title_info['static_img']
        for image_info in image_list:
            if image_info[0][0] == 'i':
                new_image = lib.settings.Image(image_info[0],image_info[1],image_info[2])
                self.image_group.add(new_image)
            elif image_info[0][0] == 'b':
                new_image = lib.settings.Button(image_info[0],image_info[1],image_info[2:])
                self.button_group.add(new_image)

        self.setting_template = lib.settings.Setting_Template('_st_',lib.settings.setting.game_info['setting_template_rect'],
                                                              self.setting.color['it_color'],self.setting,self)

    def has_end_moving(self,move_type):
        flag = 0
        if move_type == 'enter':
            for image in self.image_group.sprites():
                if image.state == lib.settings.Static_Base.ENTER:
                    flag = 1
            for button in self.button_group.sprites():
                if button.state == lib.settings.Static_Base.ENTER:
                    flag = 1
        elif move_type == 'leave':
            if self.has_on == 1:
                for image in self.image_group.sprites():
                    if image.state != lib.settings.Static_Base.FIN:
                        flag = 1
                for button in self.button_group.sprites():
                    if button.state != lib.settings.Static_Base.FIN:
                        flag = 1
        if flag == 0:
            return True
        else:
            return False

    def draw(self):
        self.screen.fill(self.setting.color['bg_color'])
        
        if self.state == -1:
            self.image_group.update()
            self.image_group.draw(self.screen)
            self.button_group.update()
            self.button_group.draw(self.screen)

            if self.has_end_moving('enter'):
                self.state = 0
                self.has_on = 1
        elif self.state == 0:
            self.image_group.draw(self.screen)

            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()

            self.button_group.draw(self.screen)
        elif self.state == 1:
            self.image_group.update()
            self.image_group.draw(self.screen)
            self.button_group.update()
            self.button_group.draw(self.screen)
        elif self.state == 2:
            self.image_group.update()
            self.image_group.draw(self.screen)
            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()
            self.button_group.update()
            self.button_group.draw(self.screen)
            self.setting_template.update()
            self.setting_template.draw(self.screen)

        pygame.display.update()
    def get_event(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.event_queue.append(self.setting.event['common']['exit'])
        else:
            if self.state == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            if button.cond == 0:
                                button.change_pic()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            event_type = self.get_event_type(button.name)

                            self.event_queue.append(self.setting.event['title'][event_type])
                            
                            if self.setting.event['title'][event_type][2] == '1':
                                self.state = 1
                                for image in self.image_group.sprites():
                                    image.state = lib.settings.Static_Base.LEAVE
                                for button in self.button_group.sprites():
                                    button.state = lib.settings.Static_Base.LEAVE
            elif self.state == 1:
                if not self.has_end_moving('leave'):
                    self.event_queue.append(self.setting.event['common']['pass'])
                else:
                    self.event_queue.append(self.setting.event['common']['fin'])
                    self.has_on = 0
            elif self.state == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    new_event = self.setting_template.check_event((x,y),'down')
                    if new_event != None:
                        self.event_queue.append(new_event)

                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    new_event = self.setting_template.check_event((x,y),'up')
                    if new_event != None:
                        self.event_queue.append(new_event)

                
            

class Profile(Screen_Base):
    def __init__(self,setting,event_queue,screen):
        super().__init__(setting,screen)

        self.name = 'profile'
        self.id   = '002'
        
        self.state  = -1
        self.previous_state = -1
        self.current_showing_info = 0

        self.event_queue = event_queue
        self.prepare_elements()
    
    def prepare_elements(self):
        self.image_group  = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()
        
        image_list = self.setting.profile_info['static_img']
        for image_info in image_list:
            if image_info[0][0] == 'i':
                new_image = lib.settings.Image(image_info[0],image_info[1],image_info[2])
                self.image_group.add(new_image)
            elif image_info[0][0] == 'b':
                new_image = lib.settings.Button(image_info[0],image_info[1],image_info[2:])
                self.button_group.add(new_image)
        
        self.info_template = lib.settings.Info_Template('it',self.setting.profile_info['profile_it_rect'],
                                                        self.setting.color['it_color'],self.setting)
        self.setting_template = lib.settings.Setting_Template('_st_',lib.settings.setting.game_info['setting_template_rect'],
                                                              self.setting.color['it_color'],self.setting,self)

    def has_end_moving(self,move_type):
        flag = 0
        if move_type == 'enter':
            for image in self.image_group.sprites():
                if image.state == 'enter':
                    flag = 1
            for button in self.button_group.sprites():
                if button.state == 'enter':
                    flag = 1
            if self.info_template.state == 'enter':
                flag = 1
        elif move_type == 'leave':
            for button in self.button_group.sprites():
                if button.state != 'fin':
                    flag = 1
            for image in self.image_group.sprites():
                if image.state != 'fin':
                    flag = 1
            if self.info_template.state != 'fin':
                flag = 1
        
        if flag == 0:
            return True
        else:
            return False

    def sleep(self):
        self.state = -1
        self.current_showing_info = 0

        if self.player != None:
            self.info_template.sleep(True)
        else:
            self.info_template.sleep(False)

        for button in self.button_group.sprites():
            button.sleep()
        for image in self.image_group.sprites():
            image.sleep()

    def info_pageup(self):
        self.info_template.page_up()
    
    def info_pagedown(self):
        self.info_template.page_down()
    
    def switch_infotemplate(self):
        if self.info_template.display == 0:
            self.info_template.display = 1
            self.state = 0
        elif self.info_template.display == 1:
            if self.info_template.state == lib.settings.Info_Template.TEXT:
                self.info_template.state = lib.settings.Info_Template.SELECT

            self.info_template.display = 0
            self.state = 1
    
    def draw(self):
        self.screen.fill(self.setting.color['bg_color'])
        self.image_group.update()
        self.image_group.draw(self.screen)

        if self.state == -1:
            self.button_group.update()
            self.button_group.draw(self.screen)
            self.info_template.update()
            if self.info_template.display == 1:   
                self.info_template.draw(self.screen)

            if self.has_end_moving('enter'):
                if self.player == None:
                    self.state = 0
                else:
                    self.state = 1
        elif self.state == 0:
            if self.player != None:
                self.player.show_msg(self.screen,self.current_showing_info)

            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()

            self.button_group.draw(self.screen)
            self.info_template.update()
            if self.info_template.display == 1:
                self.info_template.draw(self.screen)
        elif self.state == 1:
            if self.player != None:
                self.player.show_msg(self.screen,self.current_showing_info)

            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()

            self.button_group.draw(self.screen)
            self.info_template.update()
            if self.info_template.display == 1:   
                self.info_template.draw(self.screen)
        elif self.state == 2:
            self.button_group.update()
            self.button_group.draw(self.screen)
            
            self.info_template.update()
            if self.info_template.display == 1:
                self.info_template.draw(self.screen)
        elif self.state == 3:
            if self.player != None:
                self.player.show_msg(self.screen,self.current_showing_info)

            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()
            self.button_group.update()
            self.button_group.draw(self.screen)
            
            self.info_template.update()
            self.info_template.draw(self.screen)
        elif self.state == 4:
            if self.player != None:
                self.player.show_msg(self.screen,self.current_showing_info)
            
            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()
            self.button_group.update()
            self.button_group.draw(self.screen)

            self.setting_template.update()
            self.setting_template.draw(self.screen)
        
        pygame.display.update()
    
    def get_selected_player(self):
        return self.info_template.get_selected_player()
    
    def get_event(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.event_queue.append(self.setting.event['common']['exit'])
        else:
            if self.state == 0: 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    flag = 0
                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            if button.cond == 0:
                                button.change_pic()
                                flag = 1
                                break

                    if flag == 0:          
                        new_event = self.info_template.check_event((x,y),'down')
                        if new_event == self.setting.event['profile']['input']:
                            self.state = 3
                        self.event_queue.append(new_event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    flag = 0
                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            event_type = self.get_event_type(button.name)

                            flag = 1
                            if self.setting.event['profile'][event_type][2] == '1':
                                self.state = 2
                                for image in self.image_group.sprites():
                                    image.state = lib.settings.Static_Base.LEAVE
                                for button in self.button_group.sprites():
                                    button.state = lib.settings.Static_Base.LEAVE
                                self.info_template.state = lib.settings.Info_Template.LEAVE
                            self.event_queue.append(self.setting.event['profile'][event_type])
                            break
                    
                    if flag == 0:            
                        new_event = self.info_template.check_event((x,y),'up')
                        if new_event == self.setting.event['profile']['confirm']:
                            if self.info_template.not_empty():
                                self.event_queue.append(new_event)
                        elif new_event == self.setting.event['profile']['up']:
                            self.event_queue.append(new_event)
                        elif new_event == self.setting.event['profile']['down']:
                            self.event_queue.append(new_event)
                        elif new_event == self.setting.event['profile']['load']:
                            if self.info_template.current_selection != -1:
                                self.event_queue.append(new_event)
            elif self.state == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    flag = 0
                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            if button.cond == 0:
                                flag = 1
                                button.change_pic()
                                break
                    
                    if flag == 0:
                        for image in self.image_group.sprites():
                            if image.name[-1] == 'b':
                                if image.rect.collidepoint((x,y)):
                                    new_event = self.get_event_type(image.name)
                                    self.event_queue.append(self.setting.event['profile'][new_event])
                                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            event_type = self.get_event_type(button.name)

                            if self.setting.event['profile'][event_type][2] == '1':
                                self.state = 2
                                for image in self.image_group.sprites():
                                    image.state = lib.settings.Static_Base.LEAVE
                                for button in self.button_group.sprites():
                                    button.state = lib.settings.Static_Base.LEAVE
                                self.info_template.display = 0
                                self.info_template.state = lib.settings.Info_Template.LEAVE
                            self.event_queue.append(self.setting.event['profile'][event_type])
                            break   
            elif self.state == 2:
                if not self.has_end_moving('leave'):
                    self.event_queue.append(self.setting.event['common']['pass'])
                else:
                    self.event_queue.append(self.setting.event['common']['fin'])
            elif self.state == 3:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    new_event = self.info_template.check_event((x,y),'down')
                    if new_event == self.setting.event['profile']['cancel']:
                        self.state = 0
                        self.info_template.state = lib.settings.Info_Template.TEXT
                    self.event_queue.append(new_event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == 8:
                        self.info_template.text_block.delete_last()
                        self.event_queue.append(self.setting.event['profile']['input'])
                    elif event.key == 13 or event.key == 1073741912:
                        self.state = 0
                        self.info_template.state = lib.settings.Info_Template.TEXT
                        self.info_template.text_block.switch_state(0)
                        self.event_queue.append(self.setting.event['profile']['cancel'])
                    else:
                        self.info_template.text_block.set_input(event)
                        self.event_queue.append(self.setting.event['profile']['input'])
            elif self.state == 4:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    new_event = self.setting_template.check_event((x,y),'down')
                    if new_event != None:
                        self.event_queue.append(new_event)

                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    new_event = self.setting_template.check_event((x,y),'up')
                    if new_event != None:
                        self.event_queue.append(new_event)
                    

class Worlds(Screen_Base):
    def __init__(self,setting,event_queue,screen):
        super().__init__(setting,screen)

        self.name = 'worlds'
        self.id = '103'

        self.state = -1
        self.has_on = 0

        self.min_world = 1
        self.current_world = 1

        self.event_queue = event_queue

        self.prepare_elements()
    
    def prepare_elements(self):
        self.button_group = pygame.sprite.Group()
        self.image_group = pygame.sprite.Group()
        
        self.max_worlds = lib.settings.setting.world_info['world_count']
        self.world_dynamic_list = []
        self.world_button_list = []
        self.backgrounds = []
        self.maps = []
        for i in range(self.max_worlds):
            new_button_list = []
            self.world_button_list.append(new_button_list)
            new_dynamic_list = []
            self.world_dynamic_list.append(new_dynamic_list)
        
        for item in lib.settings.setting.world_info['static_img']:
            if item[0][0] == 'b':
                new_button = lib.settings.Button(item[0],item[1],item[2:])
                self.button_group.add(new_button)
            elif item[0][0] == 'i':
                new_image = lib.settings.Image(item[0],item[1],item[2])
                self.image_group.add(new_image)
            elif item[0][0] == 'g':
                new_background = lib.settings.Background(item[0],item[1],item[2])
                self.backgrounds.append(new_background)
            elif item[0][0] == 'm':
                new_map = lib.settings.Map(item[0],item[1],item[2:])
                self.maps.append(new_map)
        
        for item in lib.settings.setting.world_info['dynamic_img']:
            new_dynamic_group = lib.settings.Dynamic_Group(item[0],item[1],item[2],item[3],item[4:])
            self.world_dynamic_list[int(item[0][0]) - 1].append(new_dynamic_group)
        for button_list in self.world_button_list:  
            for level_count in lib.settings.setting.world_info['level_count']:
                for i in range(level_count[1] - level_count[0]):
                    new_name = 'b_level_' + str(self.current_world) + '_' + str(i + 1)
                    new_button = lib.settings.Level_Button(self.player,new_name,
                                                           lib.settings.setting.world_info['level_button_rect'][i][:3],
                                                           lib.settings.setting.world_info['level_button_rect'][i][4],
                                                           lib.settings.setting.world_info['level_image_list'])
                    button_list.append(new_button)
        
        self.level_msg_list = []
        self.current_bt = []
        self.set_current()
        self.prepare_msg()

        self.setting_template = lib.settings.Setting_Template('_st_',lib.settings.setting.game_info['setting_template_rect'],
                                                              self.setting.color['it_color'],self.setting,self)

    def next_world(self):
        if self.current_world < self.max_worlds:
            self.current_world += 1
            self.set_current()
            self.level_msg_list.clear()
        self.prepare_msg()

    def previous_world(self):
        if self.current_world > self.min_worlds:
            self.current_world -= 1
            self.set_current()
            self.level_msg_list.clear()
        self.prepare_msg()

    def set_current(self):
        self.current_bg = self.backgrounds[self.current_world - 1]
        self.current_dy = self.world_dynamic_list[self.current_world - 1]
        self.current_mp = self.maps[self.current_world - 1]
        self.current_bt = self.world_button_list[self.current_world - 1]

    def sleep(self):
        self.state = -1
        self.has_on = 0

        for button in self.button_group.sprites():
            button.sleep()
        for image in self.image_group.sprites():
            image.sleep()
        for m in self.maps:
            m.sleep()
        for dy_list in self.world_dynamic_list:
            for dy in dy_list:
                dy.sleep()
        for button in self.current_bt:
            button.sleep()
        
        self.level_msg_list.clear()
    
    def has_end_moving(self,move_type):
        flag = 0
        if move_type == 'enter':
            for image in self.image_group.sprites():
                if image.state == 'enter':
                    flag = 1
            for button in self.button_group.sprites():
                if button.state == 'enter':
                    flag = 1
            for button in self.current_bt:
                if button.state == 'enter':
                    flag = 1
            if self.current_mp.state == 'enter':
                flag = 1
        elif move_type == 'leave':
            for button in self.button_group.sprites():
                if button.state != 'fin':
                    flag = 1
            for image in self.image_group.sprites():
                if image.state != 'fin':
                    flag = 1
            for button in self.current_bt:
                if button.state != 'fin':
                        flag = 1
            if self.current_mp.state != 'fin':
                flag = 1

        if flag == 0:
            return True
        else:
            return False

    def prepare_msg(self):
        self.font = pygame.font.SysFont('impact',21)
        world_msg = 'WORLD ' + str(self.current_world) 
        self.world_msg = self.font.render(world_msg,True,
                                          lib.settings.setting.color['text_color'],
                                          lib.settings.setting.color['white'])
        self.world_rect = self.world_msg.get_rect()
        self.world_rect.center = (800,20)

        for button in self.current_bt:
            name = button.name[-3:]
            new_str = 'W' + str(name[0]) + '-' + str(name[2])
            new_msg = self.font.render(new_str,True,
                                       lib.settings.setting.color['text_color'],
                                       lib.settings.setting.color['white'])
            msg_rect = new_msg.get_rect()
            msg_rect.left,msg_rect.top = (button.fixed_rect[0] + 10,button.fixed_rect[1] + 60)
            self.level_msg_list.append((new_msg,msg_rect))          

    def draw(self):
        if self.has_on == 0:
            for button_list in self.world_button_list:
                for button in button_list:
                    button.player = self.player
                    button.check_has_on()

        for button in self.current_bt:
            button.player = self.player

        self.screen.fill(self.setting.color['bg_color'])
        self.screen.convert_alpha()
        self.screen.blit(self.current_bg.image,self.current_bg.rect)
        
        
        if self.state == -1:
            self.image_group.update()
            self.image_group.draw(self.screen)
            self.button_group.update()
            self.button_group.draw(self.screen)
            self.current_mp.update()
            self.screen.blit(self.current_mp.image,self.current_mp.rect)
            for button in self.current_bt:
                button.update()
                self.screen.blit(button.image,button.rect)
            
            if self.has_end_moving('enter'):
                self.state = 0
                self.has_on = 1
                self.prepare_msg()
                if self.player != None:
                    for button_list in self.world_button_list:  
                        for button in button_list:
                            if button.has_on:
                                button.change_pic()
        elif self.state == 0:
            self.image_group.update()
            self.image_group.draw(self.screen)
            for dy in self.current_dy:
                if dy.layer == 0:
                    dy.update()
                    dy.draw(self.screen)
            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()
            self.button_group.draw(self.screen) 
            self.current_mp.update()            
            self.screen.blit(self.current_mp.image,self.current_mp.rect)
            for button in self.current_bt:
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()
                button.update()
                self.screen.blit(button.image,button.rect)

            for dy in self.current_dy:
                if dy.layer == 1:
                    dy.update()
                    dy.draw(self.screen)

            self.screen.blit(self.world_msg,self.world_rect)
            for level_tuple in self.level_msg_list:
                self.screen.blit(level_tuple[0],level_tuple[1])
        elif self.state == 1:
            self.image_group.update()
            self.image_group.draw(self.screen)
            self.button_group.update()
            self.button_group.draw(self.screen)
            self.current_mp.update()
            self.screen.blit(self.current_mp.image,self.current_mp.rect)
            for button in self.current_bt:
                button.update()
                self.screen.blit(button.image,button.rect)
        elif self.state == 2:
            self.image_group.update()
            self.image_group.draw(self.screen)

            for dy in self.current_dy:
                if dy.layer == 0:
                    dy.draw(self.screen)

            self.button_group.update()
            self.button_group.draw(self.screen)
            self.current_mp.update()
            self.screen.blit(self.current_mp.image,self.current_mp.rect)
            
            for button in self.current_bt:
                button.update()
                self.screen.blit(button.image,button.rect)
            
            for dy in self.current_dy:
                if dy.layer == 1:
                    dy.draw(self.screen)
            
            self.setting_template.update()
            self.setting_template.draw(self.screen)

        pygame.display.update()

    def get_event(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.event_queue.append(self.setting.event['common']['exit'])
        elif self.state == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                flag = 0
                for button in self.button_group.sprites():
                    if button.is_clicked((x,y)):
                        if button.cond == 0:
                            button.change_pic()
                            flag = 1
                            break
                if flag == 0:
                    for button in self.current_bt:
                        if button.has_on == 1:
                            if button.is_clicked((x,y)):
                                if button.cond == 0:
                                    button.change_pic()
                                    break
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()

                flag = 0
                for button in self.button_group.sprites():
                    if button.is_clicked((x,y)):
                        flag = 1
                        event_type = self.get_event_type(button.name)
                if flag == 0:
                    for button in self.current_bt:
                        if button.has_on != 0:
                            if button.is_clicked((x,y)):
                                flag = 1
                                event_type = self.get_level_event(button.name)
                
                if flag == 0:
                    self.event_queue.append(self.setting.event['common']['pass'])
                else:
                    if self.setting.event['worlds'][event_type][2] == '1':
                        self.state = 1
                        for image in self.image_group.sprites():
                            image.state = lib.settings.Static_Base.LEAVE
                        for button in self.button_group.sprites():
                            button.state = lib.settings.Static_Base.LEAVE
                        self.current_mp.state = lib.settings.Static_Base.LEAVE
                        for button in self.current_bt:
                            button.state = lib.settings.Static_Base.LEAVE

                    self.event_queue.append(self.setting.event['worlds'][event_type])
        elif self.state == 1:
            if not self.has_end_moving('leave'):
                self.event_queue.append(self.setting.event['common']['pass'])
            else:
                self.event_queue.append(self.setting.event['common']['fin'])
        elif self.state == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    new_event = self.setting_template.check_event((x,y),'down')
                    if new_event != None:
                        self.event_queue.append(new_event)

                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    new_event = self.setting_template.check_event((x,y),'up')
                    if new_event != None:
                        self.event_queue.append(new_event)

    @staticmethod
    def get_level_event(name):
        '''
            this method gets the level name in the
            last of the level name.
        '''
        result = 'tog0'
        flag = 0
        
        for c in name:
            if c == '_':
                flag += 1
                continue
            
            if flag == 2:
                result += c + '0'
            elif flag == 3:
                result += c
            
        return result


class Level_0101(Screen_Base):
    def __init__(self,setting,event_queue,screen):
        super().__init__(setting,screen)

        self.name = 'g0101'
        self.id   = '201'

        self.platform_group = pygame.sprite.Group()
        self.button_group   = pygame.sprite.Group()
        self.image_group    = pygame.sprite.Group()
        self.bullet_group   = pygame.sprite.Group()
        self.enemy_group    = pygame.sprite.Group()
        self.character      = lib.game.Main_Character(lib.settings.setting.level_common_info['main_character_starting_pos'],
                                                      self)

        self.finish_intro   = 'Kill 15 Ducks To Win'
        self.victory_limit  = 15
        self.target_counter = 0
        self.point_counter  = 0
        self.check_ending   = 0
        self.fire_count     = 0
        self.damage_count   = 0

        self.event_queue = event_queue

        self.has_on = 0
        self.last_spawn_time   = -1
        self.enter_screen_time = -1

        self.prepare_elements()
    
    def prepare_elements(self):
        self.background = []
        for background in lib.settings.setting.levels_info['g0101']['background']:
            new_background = background[0].convert_alpha()
            self.background.append(new_background)

        for item in self.setting.level_common_info['static_img']:
            if item[0][0] == 'i':
                new_image = lib.settings.Image(item[0],item[1],item[2])
                if item[0][0] == 't':
                    new_image.image.convert_alpha()
                self.image_group.add(new_image)
            elif item[0][0] == 'b':
                new_image = lib.settings.Button(item[0],item[1],item[2:])
                self.button_group.add(new_image)
        for rect in self.setting.levels_info['g0101']['platform']:
            new_platform = lib.settings.Platform(rect[0],rect[1],rect[2])
            self.platform_group.add(new_platform)

        self.decreasing_bar_len = 292
        self.decreasing_mp_bar_len = 292
        self.cd_len = 50
        self.duration = 50
        
        self.weapon_font = pygame.font.SysFont('impact',60)
        self.hint_text = pygame.font.SysFont('impact',20)
        self.point_text = pygame.font.SysFont('impact',15)
        self.target_text = pygame.font.SysFont('impact',40)
        self.reload_hint = self.hint_text.render('R',True,lib.settings.setting.color['red'])

        self.finish_intro_text = pygame.font.SysFont('impact',80)
        self.finish_intro_msg  = self.finish_intro_text.render(self.finish_intro,True,lib.settings.setting.color['black'])
        self.finish_intro_rect = self.finish_intro_msg.get_rect()
        self.finish_intro_rect.centerx,self.finish_intro_rect.centery = 800,450
        self.end_intro = 0

        self.spawn_tick = 2

        self.setting_template = lib.settings.Setting_Template('_st_',lib.settings.setting.game_info['setting_template_rect'],
                                                              self.setting.color['it_color'],self.setting,self)
        self.skill_list = []

    def prepare_dynamic_msg(self):
        now = time.time()

        self.mp_len = 292 * (self.character.mp / self.character.max_mp)
        self.mp_bar = pygame.Rect(108,108,self.mp_len,34)
        if self.decreasing_mp_bar_len > self.mp_len:
            self.decreasing_mp_bar_len -= 1
        else:
            self.decreasing_mp_bar_len = self.mp_len
        self.decreasing_mp_bar = pygame.Rect(108,108,self.decreasing_mp_bar_len,35)

        self.hb_len = 292 * (self.character.hp / self.character.max_hp)
        self.health_bar = pygame.Rect(108,38,self.hb_len,34)
        if self.decreasing_bar_len > self.hb_len:
            self.decreasing_bar_len -= 1
        else:
            self.decreasing_bar_len = self.hb_len
        self.decreasing_bar = pygame.Rect(108,38,self.decreasing_bar_len,35)
        self.ammo_message = ""
        if self.character.current_weapon.weapon_type == 'gun':
            self.ammo_message = str(self.character.current_weapon.mag_ammo) + " / " + \
                                str(self.character.current_weapon.max_mag)
        elif self.character.current_weapon.weapon_type == 'knife':
            self.ammo_message = 'INFINITY'
        self.ammo_img  = self.weapon_font.render(self.ammo_message,True,lib.settings.setting.color['dark_grey'])
        self.ammo_rect = self.ammo_img.get_rect()
        self.ammo_rect.right = 1600
        self.ammo_rect.bottom = 850

        if self.character.state[3] == 1:
            self.reload_bar_len = self.ammo_rect.bottom - self.ammo_rect.top
            self.reload_bar     = pygame.Rect(self.ammo_rect.left - 20,self.ammo_rect.top,
                                            20,self.reload_bar_len * (self.character.reload_percentage()))
        
        target_msg = str(self.target_counter) + ' / 15'
        self.target_msg  = self.target_text.render(target_msg,True,lib.settings.setting.color['dark_grey'])
        self.target_rect = self.target_msg.get_rect()
        self.target_rect.centery = 80
        self.target_rect.left    = 530

        point_msg = 'Score:' + str(self.point_counter)
        self.point_msg  = self.point_text.render(point_msg,True,lib.settings.setting.color['black'])
        self.point_rect = self.point_msg.get_rect()
        self.point_rect.left = self.target_rect.left
        self.point_rect.top  = self.target_rect.bottom + 10

        self.q = 'Q'
        self.e = 'E'
        self.q_msg = self.point_text.render(self.q,True,lib.settings.setting.color['white'])
        self.e_msg = self.point_text.render(self.e,True,lib.settings.setting.color['white'])
        self.q_rect = self.q_msg.get_rect()
        self.e_rect = self.e_msg.get_rect()
        self.q_rect.right,self.q_rect.bottom = 790,880
        self.e_rect.right,self.e_rect.bottom = 880,880

        if self.character.skill_dict['q'].start_time != -1:
            used_time = now - self.character.skill_dict['q'].start_time

            self.q_cd_len = self.cd_len * (used_time / self.character.skill_dict['q'].colddown)
            
            if self.character.skill_dict['q'].duration == -1:
                self.e_duration_len = self.duration
            elif used_time <= self.character.skill_dict['q'].duration:
                self.q_duration_len = self.duration * (used_time / self.character.skill_dict['q'].duration)
            else:
                self.q_duration_len = self.duration
        else:
            self.q_cd_len = self.cd_len
            self.q_duration_len = self.duration

        if self.character.skill_dict['e'].start_time != -1:
            used_time = now - self.character.skill_dict['e'].start_time
            
            self.e_cd_len = self.cd_len * (used_time / self.character.skill_dict['e'].colddown)

            if self.character.skill_dict['e'].duration == -1:
                self.e_duration_len = self.duration
            elif used_time <= self.character.skill_dict['e'].duration:
                self.e_duration_len = self.duration * (used_time / self.character.skill_dict['e'].duration)
            else:
                self.e_duration_len = self.duration
        else:
            self.e_cd_len = self.cd_len
            self.e_duration_len = self.duration

        self.q_cd = pygame.Rect(730,805,self.q_cd_len,20)
        self.e_cd = pygame.Rect(820,805,self.e_cd_len,20)
        self.q_du = pygame.Rect(730,825,self.q_duration_len,20)
        self.e_du = pygame.Rect(820,825,self.e_duration_len,20)

    def has_end_moving(self,move_type):
        flag = 0
        if move_type == 'enter':
            for image in self.image_group.sprites():
                if image.state == 'enter':
                    flag = 1
            for button in self.button_group.sprites():
                if button.state == 'enter':
                    flag = 1
        elif move_type == 'leave':
            for button in self.button_group.sprites():
                if button.state != 'fin':
                    flag = 1
            for image in self.image_group.sprites():
                if image.state != 'fin':
                    flag = 1
        
        if flag == 0:
            return True
        else:
            return False
        
    def sleep(self):
        self.state = -1
        self.has_on = 0

        self.enter_screen_time = -1
        self.first_update_time = -1
        self.end_intro = 0
        self.target_counter = 0
        self.point_counter  = 0
        self.check_ending   = 0
        self.fire_count     = 0
        self.damage_count   = 0
        self.spawn_tick     = 2

        self.bullet_group.empty()
        self.enemy_group.empty()
        self.character.reset()
        self.skill_list = []

        for button in self.button_group.sprites():
            button.sleep()
        for image in self.image_group.sprites():
            image.sleep()

    def init_skill_weapon(self):
        self.character.skill_dict['q'] = self.player.selected_skill['q']
        self.character.skill_dict['e'] = self.player.selected_skill['e']
        for skill in self.character.skill_dict.values():
            skill.character = self.character

    def update(self):
        if self.has_on == 0:
            self.character.player = self.player
            for new_kv in self.character.skill_dict.items():
                self.skill_list.append(new_kv)
            self.has_on = 1

        if self.enter_screen_time == -1:
            self.enter_screen_time = time.time()

        if self.target_counter >= 8:
            self.spawn_tick = 0.85
        elif self.target_counter >= 3:
            self.spawn_tick = 1.4

        self.prepare_dynamic_msg()
        update_time = time.time()
        
        if self.state == -1:
            self.image_group.update()
            self.button_group.update()
            if self.has_end_moving('enter'):
                self.first_update_time = time.time()
                self.state = 0
        elif self.state == 0:
            self.bullet_group.update()
            for bullet in self.bullet_group.sprites():
                if bullet.state == 0:
                    self.bullet_group.remove(bullet)
            self.character.update()

            collide_dict = pygame.sprite.groupcollide(self.bullet_group,self.enemy_group,True,False)
            if collide_dict:
                for k,v in collide_dict.items():
                    for enemy in v:
                        if k.damage > enemy.hp:
                            self.point_counter += 10 * enemy.hp
                            self.damage_count  += enemy.hp
                            enemy.hp = 0
                        else:
                            enemy.hp -= k.damage
                            self.damage_count  += k.damage
                            self.point_counter += k.damage * 10
                        
                        if enemy.hp == 0:
                            self.target_counter += 1
                            self.point_counter += 100
              
            for enemy in self.enemy_group.sprites():
                if enemy.state == 0:
                    self.enemy_group.remove(enemy)
            if update_time - self.last_spawn_time > self.spawn_tick:
                new_enemy = lib.game.Duck(self.character.upper_rect.centery)
                new_enemy.set_facing(random.choice([1,-1]))
                if 5 <= self.target_counter < 12:
                    new_enemy.hor_speed += 0.8
                    new_enemy.ver_speed += 0.4
                elif self.target_counter >= 10:
                    new_enemy.hor_speed += 1.5
                    new_enemy.ver_speed += 0.8

                self.enemy_group.add(new_enemy)
                self.last_spawn_time = update_time

            self.enemy_group.update(update_time,self.character.upper_rect.centery)
            character_collide = pygame.sprite.spritecollideany(self.character,self.enemy_group)
            if character_collide:
                if self.character.state[4] != 1:
                    self.character.state[3] = 0
                    self.character.reload_start = -1
                    self.character.state[4] = 1
                    self.character.last_hit_time = update_time
                    self.character.hp -= 20
            
            self.image_group.update()
            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()
            self.button_group.update()
                
        elif self.state == 1:
            self.image_group.update()
            self.button_group.update()
        elif self.state == 2:
            self.setting_template.update()

        if self.end_intro == 0 and time.time() - self.enter_screen_time <= 3.5 :
            self.screen.blit(self.finish_intro_msg,self.finish_intro_rect)
        else:
            if self.end_intro != 1:
                self.end_intro = 1
        
        if self.target_counter >= self.victory_limit:
            return 1
        elif self.character.hp <= 0:
            return -1

        return 0
    
    def draw(self):
        self.screen.fill(self.setting.color['bg_color'])
        for background in self.background:
            self.screen.blit(background,(0,0))
        
        self.check_ending = self.update()
        if self.check_ending != 0:
            return

        if self.state == -1:
            self.image_group.draw(self.screen)
            self.button_group.draw(self.screen)
        elif self.state == 0:
            self.bullet_group.draw(self.screen)
            self.platform_group.update(self.screen)  
            self.enemy_group.draw(self.screen)      
            self.character.draw(self.screen)

            for kv in self.skill_list:
                new_image = self.setting.skill[kv[1].name]
                if kv[0] == 'q':
                    new_rect = self.setting.level_common_info['skill_q_pos']
                elif kv[0] == 'e':
                    new_rect = self.setting.level_common_info['skill_e_pos']
                self.screen.blit(new_image,new_rect[:2])
            self.screen.blit(self.q_msg,self.q_rect)
            self.screen.blit(self.e_msg,self.e_rect)
            
            self.image_group.draw(self.screen)  
            self.screen.blit(self.target_msg,self.target_rect)
            self.screen.blit(self.point_msg,self.point_rect)
            self.button_group.draw(self.screen)
            self.screen.fill(lib.settings.setting.color['red'],self.decreasing_bar)
            self.screen.fill(lib.settings.setting.color['green'],self.health_bar)
            self.screen.fill(lib.settings.setting.color['pure_blue'],self.decreasing_mp_bar)
            self.screen.fill(lib.settings.setting.color['light_blue'],self.mp_bar)
            self.screen.blit(self.ammo_img,self.ammo_rect)

            self.screen.fill(lib.settings.setting.color['light_blue'],self.q_cd)
            self.screen.fill(lib.settings.setting.color['light_blue'],self.e_cd)
            self.screen.fill(lib.settings.setting.color['orange'],self.q_du)
            self.screen.fill(lib.settings.setting.color['orange'],self.e_du)
            
            if self.character.state[3] == 0:
                if self.character.current_weapon.mag_ammo < self.character.current_weapon.max_mag:
                    self.hint_rect = self.reload_hint.get_rect()
                    self.hint_rect.bottom = self.ammo_rect.bottom
                    self.hint_rect.right  = self.ammo_rect.left
                    self.screen.blit(self.reload_hint,self.hint_rect)
            elif self.character.state[3] == 1:
                self.screen.fill(lib.settings.setting.color['dark_grey'],self.reload_bar)
        elif self.state == 1:
            self.image_group.draw(self.screen)
            self.bullet_group.draw(self.screen)
        elif self.state == 2:
            self.image_group.draw(self.screen)
            self.bullet_group.draw(self.screen)
            self.platform_group.update(self.screen)  
            self.enemy_group.draw(self.screen)      
            self.character.draw(self.screen)
            
            self.image_group.draw(self.screen)  
            self.screen.blit(self.target_msg,self.target_rect)
            self.screen.blit(self.point_msg,self.point_rect)
            self.button_group.draw(self.screen)
            self.screen.fill(lib.settings.setting.color['red'],self.decreasing_bar)
            self.screen.fill(lib.settings.setting.color['green'],self.health_bar)
            self.screen.fill(lib.settings.setting.color['pure_blue'],self.decreasing_mp_bar)
            self.screen.fill(lib.settings.setting.color['light_blue'],self.mp_bar)
            self.screen.blit(self.ammo_img,self.ammo_rect)
            
            if self.character.state[3] == 0:
                if self.character.current_weapon.mag_ammo < self.character.current_weapon.max_mag:
                    self.hint_rect = self.reload_hint.get_rect()
                    self.hint_rect.bottom = self.ammo_rect.bottom
                    self.hint_rect.right  = self.ammo_rect.left
                    self.screen.blit(self.reload_hint,self.hint_rect)

            self.setting_template.draw(self.screen)

        pygame.display.update()

    def get_event(self):
        event = pygame.event.poll()
        
        if event.type == pygame.QUIT:
            self.event_queue.append(self.setting.event['common']['exit'])
        else:
            if self.state == 0: 
                if self.check_ending == 1:
                    self.state = 1
                    self.player.current_record.last_level[0] = 0
                    self.player.current_record.last_level[1] = 1
                    self.player.current_record.bullet_shot += self.fire_count
                    self.player.current_record.enemy_killed += self.target_counter
                    self.player.current_record.score += self.point_counter
                    self.player.current_record.damage_dealt += self.damage_count
                    self.player.current_record.start_time = self.first_update_time
                    self.player.current_record.end_time = time.time()
                    self.player.current_record.get_played_time()
                    self.event_queue.append(self.setting.event['g0101']['victory'])
                elif self.check_ending == -1:
                    self.state = 1
                    self.player.current_record.last_level[0] = 0
                    self.player.current_record.last_level[1] = -1
                    self.player.current_record.death_count += 1
                    self.player.current_record.bullet_shot += self.fire_count
                    self.player.current_record.enemy_killed += self.target_counter
                    self.player.current_record.score += self.point_counter
                    self.player.current_record.damage_dealt += self.damage_count
                    self.player.current_record.start_time = self.first_update_time
                    self.player.current_record.end_time = time.time()
                    self.player.current_record.get_played_time()
                    self.event_queue.append(self.setting.event['g0101']['gameover'])
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x,y = pygame.mouse.get_pos()

                        flag = 0
                        for button in self.button_group.sprites():
                            if button.is_clicked((x,y)):
                                if button.cond == 0:
                                    button.change_pic()
                                    flag = 1
                                    break
                        if flag == 0:
                            self.character.state[5] = 1
                            if self.character.current_weapon.is_auto != 1:
                                new_bullet = self.character.fire()
                                if new_bullet != None:
                                    self.fire_count += 1
                                    self.character.interrupt_reload()
                                    new_bullet.get_direction((x,y),self.character.current_weapon.rect)
                                    self.bullet_group.add(new_bullet)  
                    elif event.type == pygame.MOUSEBUTTONUP:
                        x,y = pygame.mouse.get_pos()
                        
                        self.character.state[5] = 0
                        for button in self.button_group.sprites():
                            if button.is_clicked((x,y)):
                                event_type = self.get_event_type(button.name)

                                self.event_queue.append(self.setting.event['g0101'][event_type]) 
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.character.state[0] != 1:
                                self.character.state[0] = 1
                                self.character.vert_speed = -20
                        elif event.key == pygame.K_a:
                            self.character.state[1] = 1
                        elif event.key == pygame.K_s:
                            if self.character.state[0] == -1:
                                self.character.lower_rect.bottom = self.character.current_on_platform.rect.bottom
                                self.character.state[0] = 1
                                self.character.state[6] = 1
                        elif event.key == pygame.K_d:
                            self.character.state[2] = 1
                        elif event.key == pygame.K_r:
                            self.character.reload()
                        elif event.key == pygame.K_q:
                            if self.character.skill_active[0] != 1:
                                new_bullet = self.character.use_skill_q()
                                self.character.last_mp_used = time.time()
                                if isinstance(new_bullet,lib.game.Bullet):
                                    self.bullet_group.add(new_bullet)
                        elif event.key == pygame.K_e:
                            if self.character.skill_active[1] != 1:
                                new_bullet = self.character.use_skill_e()
                                self.character.last_mp_used = time.time()
                                if isinstance(new_bullet,lib.game.Bullet):
                                    self.bullet_group.add(new_bullet)
                        elif event.key == pygame.K_1:
                            self.character.change_to_weapon1()
                        elif event.key == pygame.K_2:
                            self.character.change_to_weapon2()
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            self.character.state[1] = 0
                        elif event.key == pygame.K_d:
                            self.character.state[2] = 0
            elif self.state == 1:
                self.event_queue.append(self.setting.event['common']['fin'])
            elif self.state == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    new_event = self.setting_template.check_event((x,y),'down')
                    if new_event != None:
                        self.event_queue.append(new_event)

                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    new_event = self.setting_template.check_event((x,y),'up')
                    if new_event != None:
                        self.event_queue.append(new_event)
                    

class Victory(Screen_Base):
    def __init__(self,setting,event_queue,screen):
        super().__init__(setting,screen)

        self.name = 'victory'
        self.id   = '901'

        self.has_on = 0

        self.event_queue = event_queue

        self.last_update = -1

        self.prepare_elements()

    def prepare_elements(self):
        self.button_group = pygame.sprite.Group()

        for image in lib.settings.setting.victory['static_img']:
            if image[0][0] == 'b':
                new_button = lib.settings.Button(image[0],image[1],image[2:])
                self.button_group.add(new_button)

        self.title_font = pygame.font.SysFont('impact',65)
        self.text_font  = pygame.font.SysFont('impact',30)

        firework = lib.settings.setting.victory['dynamic_img'][0]
        self.dynamic_group = lib.settings.Dynamic_Group(firework[0],firework[1],firework[2],firework[3],firework[4])

    def prepare_msg(self):
        self.last_level_id = self.player.current_record.last_level[0]
        for k in lib.settings.setting.levels_info:
            if lib.settings.setting.levels_info[k]['id'] == self.last_level_id:
                self.last_level_name = k
                break

        title_msg  = 'W' + self.last_level_name[2] + '-' + self.last_level_name[4] + ' Clear!'
        self.title_msg  = self.title_font.render(title_msg,True,lib.settings.setting.color['white'])
        self.title_rect = self.title_msg.get_rect()
        self.title_rect.centerx = 800
        self.title_rect.top = 100

        self.increasing_score  = 0
        self.increasing_kill   = 0
        self.increasing_bullet = 0
        self.increasing_damage = 0

    def has_end_moving(self,move_type):
        flag = 0
        if move_type == 'enter':
            for button in self.button_group.sprites():
                if button.state == lib.settings.Static_Base.ENTER:
                    flag = 1
        elif move_type == 'leave':
            for button in self.button_group.sprites():
                if button.state != lib.settings.Static_Base.FIN:
                    flag = 1
        
        if flag == 0:
            return True
        else:
            return False

    def prepare_dynamic_msg(self):
        self.new_score_msg = 'Score Get: ' + str(self.increasing_score)
        self.new_kill_msg  = 'Enemy Killed: ' + str(self.increasing_kill)
        self.new_bullet_msg = 'Bullet Fired: ' + str(self.increasing_bullet)
        self.new_damage_msg = 'Damage Dealt: ' + str(self.increasing_damage)
        
        if self.increasing_score < self.player.current_record.score:
            if self.increasing_score + 15 > self.player.current_record.score:
                self.increasing_score = self.player.current_record.score
            else:
                self.increasing_score += 15
        if self.increasing_kill < self.player.current_record.enemy_killed:
            self.increasing_kill += 1
        if self.increasing_bullet < self.player.current_record.bullet_shot:
            if self.increasing_bullet + 3 > self.player.current_record.bullet_shot:
                self.increasing_bullet = self.player.current_record.bullet_shot
            else:
                self.increasing_bullet += 3
        if self.increasing_damage < self.player.current_record.damage_dealt:
            if self.increasing_damage + 3 > self.player.current_record.damage_dealt:
                self.increasing_damage = self.player.current_record.damage_dealt
            else:
                self.increasing_damage += 3
        
        self.new_score_img   = self.text_font.render(self.new_score_msg,True,lib.settings.setting.color['white'])
        self.new_kill_img    = self.text_font.render(self.new_kill_msg,True,lib.settings.setting.color['white'])
        self.new_bullet_img  = self.text_font.render(self.new_bullet_msg,True,lib.settings.setting.color['white'])
        self.new_damage_img  = self.text_font.render(self.new_damage_msg,True,lib.settings.setting.color['white'])
        self.new_score_rect  = self.new_score_img.get_rect()
        self.new_kill_rect   = self.new_kill_img.get_rect()
        self.new_bullet_rect = self.new_bullet_img.get_rect()
        self.new_damage_rect = self.new_damage_img.get_rect()
        self.new_score_rect.centerx = 800
        self.new_score_rect.centery = 300
        self.new_kill_rect.centerx     = self.new_score_rect.centerx
        self.new_kill_rect.top         = self.new_score_rect.bottom + 10
        self.new_bullet_rect.centerx   = self.new_score_rect.centerx
        self.new_bullet_rect.top       = self.new_kill_rect.bottom + 10
        self.new_damage_rect.centerx   = self.new_score_rect.centerx
        self.new_damage_rect.top       = self.new_bullet_rect.bottom + 10

    def sleep(self):
        self.state  = -1
        self.has_on = 0

        for item in self.button_group.sprites():
            item.sleep()
        self.dynamic_group.sleep()

    def draw(self):
        update_time = time.time()
        
        if self.has_on == 0:
            self.prepare_msg()
            self.has_on = 1
        
        if update_time - self.last_update > 0.05:
            self.prepare_dynamic_msg()
            self.last_update = update_time
        
        self.screen.fill(lib.settings.setting.color['black'])
        self.screen.blit(self.title_msg,self.title_rect)

        if self.state == -1:
            self.button_group.update()
            self.button_group.draw(self.screen)

            if self.has_end_moving('enter'):
                self.state = 0
        elif self.state == 0:
            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()
            self.button_group.update()
            self.button_group.draw(self.screen)

            self.dynamic_group.update()
            self.dynamic_group.draw(self.screen)

            self.screen.blit(self.new_score_img,self.new_score_rect)
            self.screen.blit(self.new_kill_img,self.new_kill_rect)
            self.screen.blit(self.new_bullet_img,self.new_bullet_rect)
            self.screen.blit(self.new_damage_img,self.new_damage_rect)

        elif self.state == 1:
            self.button_group.update()
            self.button_group.draw(self.screen)
        
        pygame.display.update()

    def get_event(self):
        event = pygame.event.poll()
        
        if event.type == pygame.QUIT:
            self.event_queue.append(self.setting.event['common']['exit'])
        else:
            if self.state == 0:
                x,y = pygame.mouse.get_pos()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            if button.cond == 0:
                                button.change_pic()
                                break
                elif event.type == pygame.MOUSEBUTTONUP:
                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            event_type = self.get_event_type(button.name)
                            if self.setting.event['victory'][event_type][2] == '1':
                                self.state = 1
                                for button in self.button_group.sprites():
                                    button.state = lib.settings.Static_Base.LEAVE

                            self.event_queue.append(self.setting.event['victory'][event_type])
            elif self.state == 1:
                if not self.has_end_moving('leave'):
                    self.event_queue.append(self.setting.event['common']['pass'])
                else:
                    if self.player.current_record.last_level[1] == 1:
                        self.player.current_record.achievement_unlocked[self.player.current_record.last_level[0]] = 1
                    self.player.update()
                    self.player.clear_temp()
                    self.event_queue.append(self.setting.event['common']['fin'])


class Game_Over(Screen_Base):
    def __init__(self,setting,event_queue,screen):
        super().__init__(setting,screen)

        self.name = 'gameover'
        self.id   = '902'

        self.event_queue = event_queue

        self.prepare_elements()

    def prepare_elements(self):
        self.background   = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()

        for image in lib.settings.setting.gameover['static_img']:
            if image[0][0] == 'g':
                new_background = lib.settings.Background(image[0],image[1],image[2])
                self.background.add(new_background)
            elif image[0][0] == 'b':
                new_button = lib.settings.Button(image[0],image[1],image[2:])
                self.button_group.add(new_button)
    
    def sleep(self):
        self.state  = -1

        for item in self.button_group.sprites():
            item.sleep()

    def has_end_moving(self,move_type):
        flag = 0
        if move_type == 'enter':
            for button in self.button_group.sprites():
                if button.state == lib.settings.Static_Base.ENTER:
                    flag = 1
        elif move_type == 'leave':
            for button in self.button_group.sprites():
                if button.state != lib.settings.Static_Base.FIN:
                    flag = 1
        
        if flag == 0:
            return True
        else:
            return False

    def draw(self):
        self.background.draw(self.screen)

        if self.state == -1:
            self.button_group.update()
            self.button_group.draw(self.screen)

            if self.has_end_moving('enter'):
                self.state = 0
        elif self.state == 0:
            for button in self.button_group.sprites():
                if button.clicked_time != -1:
                    now = time.time()

                    if now - button.clicked_time >= 0.1:
                        button.repos()
            self.button_group.update()
            self.button_group.draw(self.screen)
        elif self.state == 1:
            self.button_group.update()
            self.button_group.draw(self.screen)
        
        pygame.display.update()
        
    def get_event(self):
        event = pygame.event.poll()
        
        if event.type == pygame.QUIT:
            self.event_queue.append(self.setting.event['common']['exit'])
        else:
            if self.state == 0:
                x,y = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            if button.cond == 0:
                                button.change_pic()
                                break
                elif event.type == pygame.MOUSEBUTTONUP:

                    for button in self.button_group.sprites():
                        if button.is_clicked((x,y)):
                            event_type = self.get_event_type(button.name)
                            if self.setting.event['gameover'][event_type][2] == '1':
                                self.state = 1
                                for button in self.button_group.sprites():
                                    button.state = lib.settings.Static_Base.LEAVE

                            self.event_queue.append(self.setting.event['gameover'][event_type])
            elif self.state == 1:
                if not self.has_end_moving('leave'):
                    self.event_queue.append(self.setting.event['common']['pass'])
                else:
                    self.player.update()
                    self.player.clear_temp()
                    self.event_queue.append(self.setting.event['common']['fin'])


screen_init = [Title,Profile,Worlds,Level_0101,Victory,Game_Over]