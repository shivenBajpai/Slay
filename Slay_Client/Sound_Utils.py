import pygame.mixer as mixer

channel = None
pick_sound = None
drop_sound = None
click_sound = None

def restart_mixer() -> None:
    mixer.quit()
    mixer.init()
    return

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
