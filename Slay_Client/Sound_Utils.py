import pygame.mixer as mixer
from pygame import error

pick_sound = None
drop_sound = None
click_sound = None

class DummySound():
    def play(self): return

def restart_mixer(volume) -> None:
    mixer.quit()
    try:
        mixer.init()
        loadSounds(volume)
    except error as err:
        print('Error loading sounds')
        print(err)
        loadDummySounds()

def SetVolume(volume) -> None:
    pick_sound.set_volume(volume)
    drop_sound.set_volume(volume)
    click_sound.set_volume(volume)

def loadSounds(volume) -> None:
    global pick_sound,drop_sound,click_sound
    pick_sound = mixer.Sound('./Slay_Assets/pick.ogg')
    drop_sound = mixer.Sound('./Slay_Assets/drop.ogg')
    click_sound = mixer.Sound('./Slay_Assets/end.ogg')
    SetVolume(volume)

def loadDummySounds():
    global pick_sound,drop_sound,click_sound
    pick_sound = DummySound()
    drop_sound = DummySound()
    click_sound = DummySound()
