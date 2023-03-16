import pygame

cells = []
entities = []
buttons = []

#load cells
cells.append([
    pygame.image.load('./Slay_Assets/bg.png').convert_alpha(),
    pygame.image.load('./Slay_Assets/bg.png').convert_alpha()
])
cells.append([
    pygame.image.load('./Slay_Assets/blue.png').convert_alpha(),
    pygame.image.load('./Slay_Assets/blue_selected.png').convert_alpha()
])
cells.append([
    pygame.image.load('./Slay_Assets/yellow.png').convert_alpha(),
    pygame.image.load('./Slay_Assets/yellow_selected.png').convert_alpha()
])
cells.append([
    pygame.image.load('./Slay_Assets/red.png').convert_alpha(),
    pygame.image.load('./Slay_Assets/red_selected.png').convert_alpha()
])
cells.append([
    pygame.image.load('./Slay_Assets/green.png').convert_alpha(),
    pygame.image.load('./Slay_Assets/green_selected.png').convert_alpha()
])

#load entites
entities.append(0) #Placeholder
entities.append(
    pygame.image.load('./Slay_Assets/tree.png').convert_alpha()
)
entities.append(
    pygame.image.load('./Slay_Assets/palm.png').convert_alpha()
)
entities.append(
    pygame.image.load('./Slay_Assets/grave.png').convert_alpha()
)
entities.append(
    pygame.image.load('./Slay_Assets/tower.png').convert_alpha()
)
entities.append(
    pygame.image.load('./Slay_Assets/city.png').convert_alpha()
)
entities.append(
    pygame.image.load('./Slay_Assets/man.png').convert_alpha()
)
entities.append(
    pygame.image.load('./Slay_Assets/spearman.png').convert_alpha()
)
entities.append(
    pygame.image.load('./Slay_Assets/baron.png').convert_alpha()
)
entities.append(
    pygame.image.load('./Slay_Assets/knight.png').convert_alpha()
)


#load buttons
buttons.append([
    pygame.image.load('./Slay_Assets/end_turn.png').convert_alpha(),
    pygame.image.load('./Slay_Assets/end_turn_hover.png').convert_alpha(),
    pygame.image.load('./Slay_Assets/end_turn_disabled.png').convert_alpha()
])

debugOverlay = pygame.image.load('./Slay_Assets/debug_overlay.png').convert_alpha()