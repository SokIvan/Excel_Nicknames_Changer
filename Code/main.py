from UI import create_UI
from libs import asyncio, threading,pygame
from Functional import play_music, Parse, Process



if __name__ == '__main__':

#Обновил правильно

    asyncio.run(create_UI('Intro_1',intro_name = "Welcome to Project",time_ = 1.05*1,fps = 0.02,ammount = 51,folder = '..\Images\Tayouko'))

    music_folder = '../music'  # Папка с музыкой
    with open('../Files/music', 'r') as f:
        vol = int(f.read().split(':')[-1])
    #Запускаем поток для воспроизведения музыки
    music_thread = threading.Thread(target=play_music, args=(music_folder,), daemon=True)
    music_thread.start()
    pygame.mixer.music.set_volume(vol/100)

    asyncio.run(create_UI('Main_Menu'))




    # Остановить музыку при выходе
    if pygame.mixer and pygame.mixer.get_init():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()


#Еще поменять ник c Luna⚡️на ⚡️LUna
