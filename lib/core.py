import sys
import time
import pygame
from collections import deque
import lib.settings
import lib.screens
import lib.player

#the core of the game
class Core():
    '''
        Core object handles all the screen objects and the player, there is also
        an event processor object that process the events.
    '''
    def __init__(self):
        self.setting = lib.settings.setting 
        #attr setthing is a referrence of the setting entity
        #in setting module                                    
        
        self.ep = Event_Processor(self)
        
        #when the core is initialized, the screen surface is also initialized
        self.size   = self.setting.game_info['size']
        self.screen = pygame.display.set_mode(self.size)
        self.screen_initialize(self.ep.event_queue)

        #player is set to None, waiting to be acquired later
        self.player = None

    def screen_initialize(self,event_queue):
        '''
            this function initializes all screen objects in the screen module
            throung a list holding all the constructor of the screens
        '''
        self.screen_list = []

        for screen_constructor in lib.screens.screen_init:
            new_screen = screen_constructor(self.setting,event_queue,self.screen)
            self.screen_list.append(new_screen)

        self.current_screen  = self.screen_list[0]
    
    def set_player(self,new_player):
        '''
            this function sets the player in all screens whenever it is invoked
        '''

        self.player = new_player
        
        for screen in self.screen_list:
            screen.player = new_player
    
    def screen_switch(self,name):
        '''
            this function changes current screen by passing in the name string in.
            it traverses the screen list to find the same name, then sets the found screen
            to self.current_screen
        '''
        for screen in self.screen_list:
            if screen.name == name:
                index = self.screen_list.index(screen)
                break
        
        self.current_screen = self.screen_list[index]

    def run_game(self):
        '''
            run_game is an endleless loop.
        '''
        #for every time this loop processes
        #get an event from current screen and pass it to event processor
        #the event processor will check its id and act correspondingly
        while True:
            self.current_screen.draw()
            self.current_screen.get_event()
            self.ep.process_event()


class Event_Processor():
    def __init__(self,core):
        self.core = core
        self.setting = self.core.setting
        self.event_queue = deque()
        
        self.blocked = 0
        self.next_screen = 'null'

    def process_event(self):
        while self.event_queue:
            new_event = self.event_queue.popleft()

            if self.blocked == 1:
                if new_event == self.setting.event['common']['exit']:
                    if self.core.player != None:
                        self.core.player.save()
                    sys.exit()
                elif new_event == self.setting.event['common']['fin']:
                    self.core.current_screen.sleep()
                    self.core.screen_switch(self.next_screen)
                    self.event_queue.clear()
                    self.blocked = 0
                    self.next_screen = 'null'
                    break
                else:
                    continue

            if self.core.current_screen.name == 'title':
                if new_event == self.setting.event['title']['exit']:
                    if self.core.player != None:
                        self.core.player.save()
                    sys.exit()
                elif new_event == self.setting.event['title']['setting']:
                    self.core.current_screen.state = 2
                elif new_event == self.setting.event['title']['profile']:
                    self.blocked = 1
                    self.next_screen = 'profile'
                elif new_event == self.setting.event['title']['start01']:
                    if self.core.player == None:
                        self.blocked = 1
                        self.next_screen = 'profile'
                    else:
                        self.blocked = 1
                        self.next_screen = 'worlds'
                elif new_event == self.setting.event['title']['resume']:
                    self.core.current_screen.state = 0
            elif self.core.current_screen.name == 'profile':
                if new_event == self.setting.event['profile']['exit']:
                    if self.core.player != None:
                        self.core.player.save()
                    sys.exit()
                elif new_event == self.setting.event['profile']['setting']:
                    self.core.current_screen.previous_state = self.core.current_screen.state
                    self.core.current_screen.state = 4
                elif new_event == self.setting.event['profile']['resume']:
                    self.core.current_screen.state = self.core.current_screen.previous_state
                    self.core.current_screen.previous_state = -1
                elif new_event == self.setting.event['profile']['return']:
                    self.blocked = 1
                    self.next_screen = 'title'
                elif new_event == self.setting.event['profile']['profile']:
                    self.core.current_screen.switch_infotemplate()
                elif new_event == self.setting.event['profile']['up']:
                    self.core.current_screen.info_pageup()
                elif new_event == self.setting.event['profile']['down']:
                    self.core.current_screen.info_pagedown()
                elif new_event == self.setting.event['profile']['achieve']:
                    self.core.current_screen.current_showing_info = 0
                elif new_event == self.setting.event['profile']['kill']:
                    self.core.current_screen.current_showing_info = 1
                elif new_event == self.setting.event['profile']['statistic']:
                    self.core.current_screen.current_showing_info = 2
                elif new_event == self.setting.event['profile']['confirm']:
                    if self.core.current_screen.info_template.not_empty():
                        if self.core.current_screen.info_template.check_input():
                            name = self.core.current_screen.info_template.get_string()

                            #if self.core.player == None:
                            new_player = lib.player.Player(name)
                            self.core.set_player(new_player)
                            self.core.current_screen.state = 1
                            self.core.current_screen.switch_infotemplate()
                            #else:
                            #    self.core.player.name = name
                            #    self.core.player.prep_msg()
                        else:
                            print('input invalid')
                elif new_event == self.setting.event['profile']['load']:
                    new_player = self.core.current_screen.get_selected_player()
                    self.core.set_player(new_player)
                    self.core.current_screen.state = 1
                    self.core.current_screen.switch_infotemplate()
                    self.core.player.prep_msg()
                elif new_event == self.setting.event['profile']['save']:
                    self.core.player.save()
            elif self.core.current_screen.name == 'worlds':
                if new_event == self.setting.event['worlds']['exit']:
                    if self.core.player != None:
                        self.core.player.save()
                    sys.exit()
                elif new_event == self.setting.event['worlds']['profile']:
                    self.blocked = 1
                    self.next_screen = 'profile'
                elif new_event == self.setting.event['worlds']['setting']:
                    self.core.current_screen.state = 2
                elif new_event == self.setting.event['worlds']['resume']:
                    self.core.current_screen.state = 0
                elif new_event == self.setting.event['worlds']['return']:
                    self.blocked = 1
                    self.next_screen = 'title'
                elif new_event == self.setting.event['worlds']['tog0101']:
                    self.blocked = 1
                    self.next_screen = 'g0101'
            elif self.core.current_screen.name == 'g0101':
                if new_event == self.setting.event['g0101']['exit']:
                    if self.core.player != None:
                        self.core.player.save()
                    sys.exit()
                elif new_event == self.setting.event['g0101']['setting']:
                    self.core.current_screen.state = 2
                elif new_event == self.setting.event['g0101']['resume']:
                    self.core.current_screen.state = 0
                elif new_event == self.setting.event['g0101']['back']:
                    self.core.current_screen.state = 1
                    self.blocked = 1
                    self.next_screen = 'worlds'
                elif new_event == self.setting.event['g0101']['gameover']:
                    self.blocked = 1
                    self.next_screen = 'gameover'
                elif new_event == self.setting.event['g0101']['victory']:
                    self.blocked = 1
                    self.next_screen = 'victory'
            elif self.core.current_screen.name == 'gameover':
                if new_event == self.setting.event['gameover']['exit']:
                    if self.core.player != None:
                        self.core.player.save()
                    sys.exit()
                elif new_event == self.setting.event['gameover']['continue']:
                    self.blocked = 1
                    self.next_screen = 'worlds'
            elif self.core.current_screen.name == 'victory':
                if new_event == self.setting.event['gameover']['exit']:
                    if self.core.player != None:
                        self.core.player.save()
                    sys.exit()
                elif new_event == self.setting.event['victory']['return']:
                    self.blocked = 1
                    self.next_screen = 'worlds'
