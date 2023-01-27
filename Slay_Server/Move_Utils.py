entities = None

class Animation:
    def __init__(self,entity: int,startpos: tuple,endpos: tuple) -> None:
        self.entity = entity
        self.startpos = startpos
        self.endpos = endpos
        
    def prepare(self) -> None:
        if (self.startpos[1]%2==1):
            start = ((self.startpos[0]+0.5)*48,self.startpos[1]*36)
        else:
            start = (self.startpos[0]*48,self.startpos[1]*36)

        if (self.endpos[1]%2==1):
            end = ((self.endpos[0]+0.5)*48,self.endpos[1]*36)
        else:
            end = (self.endpos[0]*48,self.endpos[1]*36)

        self.frame = 0
        self.frames = []

        for x in range(1,101):
            self.frames.append(
                (((100-x)/100)*start[0])+((x/100)*end[0]),
                (((100-x)/100)*start[0])+((x/100)*end[0])
            )

    def animate(self,screen) -> bool:

        screen.blit(entities[self.entity],(self.frames[self.frame]))

        self.frame += 1
        if self.frame == 100: return True
        return False

class GameUpdate:
    def __init__(self,gridChanges: list[tuple],stateChanges: dict) -> None:
        self.gridChanges = gridChanges
        self.stateChanges = stateChanges

    def apply(self,grid,state) -> None:
        for pos, newState in self.gridChanges:
            grid[pos[0]][pos[1]] = newState

        state.update(self.stateChanges)

class Move: # just a data struct
    def __init__(self,meta,preanim: GameUpdate,anim: Animation,postanim: GameUpdate) -> None:
        self.metadata = meta
        self.preanimation = preanim
        self.animation = anim
        self.postanimation = postanim