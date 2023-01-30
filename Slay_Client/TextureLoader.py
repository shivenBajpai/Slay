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
entities.append(0) #Tree
entities.append(0) #Palm
entities.append(0) #Grave
entities.append(0) #Tower
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