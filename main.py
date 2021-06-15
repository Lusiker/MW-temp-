#the game starts from here
import lib.core
import lib.settings
import pygame

if __name__ == '__main__':
    pygame.init() #initialize pygame module
    pygame.display.set_icon(lib.settings.setting.game_info['icon']) #initialize game icon
    pygame.display.set_caption(lib.settings.setting.game_info['name']) #initialize game name
    
    #initialize a core object and run the game
    gamecore = lib.core.Core()
    gamecore.run_game()