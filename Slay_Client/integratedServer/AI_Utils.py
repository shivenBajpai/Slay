import integratedServer.AI_Constants.AI_BaseConstants as BaseConstants
import integratedServer.AI_Constants.BuyTowerModifiers as TowerMods
import integratedServer.AI_Constants.BuyUnitModifiers as UnitMods
import integratedServer.AI_Constants.RemoveTreeModifiers as TreeMods
import integratedServer.AI_Constants.CaptureEnemyModifiers as EnemyCapMods
import integratedServer.AI_Constants.CaptureUnclaimedModifiers as UnclaimedCapMods
import integratedServer.AI_Constants.DoubleUpModifiers as DoubleupMods
import integratedServer.AI_Constants.RelocateModifiers as RelModifiers
import integratedServer.Hex_Utils as Hex_Utils
import integratedServer.Constants as Constants
import math

# Move would be a better name but would be confused with Move_Utils.Move
class AIMove:
    def __init__(self,actor,target,required,cost,priority,grid,description) -> None:
        self.actor = actor
        self.target = target
        self.required = required
        self.cost = cost
        self.requireSpending = cost > 0 
        self.priority = priority
        self.expected__target_state = (grid[self.target[0]][self.target[1]].color,grid[self.target[0]][self.target[1]].entity)
        self.expected_actor_state = (grid[self.actor[0]][self.actor[1]].color,grid[self.actor[0]][self.actor[1]].entity)
        self.affected_cells = []
        self.description = description

    def verify(self,grid,cities) -> tuple[bool,bool]: # returns verification, whether failure to Hex_Utils.verify was due to insufficient funds
        #print(f'------verifying type: {self.type} by {self.actor} on {self.target} \t\t prio {self.priority}')
        if (self.actor not in cities) and (not grid[self.actor[0]][self.actor[1]].playable): 
            #print(f'------Unplayable catch')
            return False,False
        if (grid[self.actor[0]][self.actor[1]].color,grid[self.actor[0]][self.actor[1]].entity) != self.expected_actor_state: 
            #print(f'------Changed actor state catch')
            return False,False
        if self.requireSpending and grid[grid[self.actor[0]][self.actor[1]].hall_loc[0]][grid[self.actor[0]][self.actor[1]].hall_loc[1]].gold < self.cost: 
            #print(f'------Cant afford catch')
            return False,True
        
        for type,data in self.required:
            if type == 'use unit':
                if not grid[data[0]][data[1]].playable: 
                    #print(f'------Unplayable (use unit) catch')
                    return False,False
            elif type == 'buy worth':
                if grid[self.actor[0]][self.actor[1]].gold < data: 
                    #print(f'------Cant afford (buy worth) catch')
                    return False,True

        if (grid[self.target[0]][self.target[1]].color,grid[self.target[0]][self.target[1]].entity) != self.expected__target_state: 
            #print(f'------Changed target state catch')
            return False,False

        return True,False
    
    def execute(self,grid,color) -> None:
        
        self.affected_cells = [] #List of all cells with changes, need not contain the cell unit was picked from and moved onto
        queued_security_updates = []
        affected_enemy_hall = None
        doubleup_flag = False

        selected_city = grid[self.actor[0]][self.actor[1]].hall_loc
        mouse_pos = self.target

        self.affected_cells.append(mouse_pos)
        self.affected_cells.extend(Hex_Utils.verify(Hex_Utils.neighbours(mouse_pos[0],mouse_pos[1],1)))
        queued_security_updates.append(mouse_pos)

        if len(self.required) > 0 and self.required[0][0] == 'use unit':
            consumed = self.required[0][1]
            consumed_entity = grid[consumed[0]][consumed[1]].entity
            self.affected_cells.append(selected_city)
            self.affected_cells.extend(Hex_Utils.verify(Hex_Utils.neighbours(consumed[0],consumed[1],1)))
            self.affected_cells.append(consumed)
            queued_security_updates.append(consumed)
            wage_change = math.floor(2*(3**(consumed_entity-Constants.MAN+1))-2*2*(3**(consumed_entity-Constants.MAN)))
            grid[selected_city[0]][selected_city[1]].wages += wage_change
            grid[selected_city[0]][selected_city[1]].net -= wage_change
            grid[self.actor[0]][self.actor[1]].entity = grid[self.actor[0]][self.actor[1]].entity + 1
            grid[consumed[0]][consumed[1]].playable = False
            grid[consumed[0]][consumed[1]].entity = Constants.NONE

        if len(self.required) > 0 and self.required[0][0] == 'buy worth':
            self.affected_cells.append(selected_city)
            wage_change = math.floor(2*(3**(consumed_entity-Constants.MAN+1))-2*(3**(consumed_entity-Constants.MAN)))
            grid[selected_city[0]][selected_city[1]].wages += wage_change
            grid[selected_city[0]][selected_city[1]].gold -= self.required[0][1]
            grid[selected_city[0]][selected_city[1]].net -= wage_change + self.required[0][1]
            grid[self.actor[0]][self.actor[1]].entity = grid[self.actor[0]][self.actor[1]].entity + 1

        if grid[self.actor[0]][self.actor[1]].entity == Constants.CITY:
            mouse_entity = self.required[0][1]
            pick_up_pos = None
        else:
            mouse_entity = grid[self.actor[0]][self.actor[1]].entity
            grid[self.actor[0]][self.actor[1]].entity = Constants.NONE
            pick_up_pos = self.actor
            self.affected_cells.extend(Hex_Utils.verify(Hex_Utils.neighbours(self.actor[0],self.actor[1],1)))
            self.affected_cells.append(self.actor)
            queued_security_updates.append(self.actor)

        # Reclaimed forest land, refund income loss
        if grid[mouse_pos[0]][mouse_pos[1]].hall_loc is not None and (grid[mouse_pos[0]][mouse_pos[1]].entity == Constants.TREE or grid[mouse_pos[0]][mouse_pos[1]].entity == Constants.PALM):
            refunded_city = grid[mouse_pos[0]][mouse_pos[1]].hall_loc
            if refunded_city not in self.affected_cells: self.affected_cells.append(refunded_city)
            Hex_Utils.appendifnotAppended(self.affected_cells,Hex_Utils.verify(Hex_Utils.neighbours(mouse_pos[0],mouse_pos[1],1)))
            Hex_Utils.appendifnotAppended(self.affected_cells,[mouse_pos])
            grid[refunded_city[0]][refunded_city[1]].income += 1
            grid[refunded_city[0]][refunded_city[1]].net += 1

        # doubling up
        if grid[mouse_pos[0]][mouse_pos[1]].entity == mouse_entity and grid[mouse_pos[0]][mouse_pos[1]].color == color: 
            self.affected_cells.append(selected_city)
            self.affected_cells.extend(Hex_Utils.verify(Hex_Utils.neighbours(mouse_pos[0],mouse_pos[1],1)))
            wage_change = math.floor(2*(3**(mouse_entity-Constants.MAN+1))-2*(3**(mouse_entity-Constants.MAN))*(1 if pick_up_pos is None else 2))
            grid[selected_city[0]][selected_city[1]].wages += wage_change
            grid[selected_city[0]][selected_city[1]].gold -= self.cost # This property was set during object creation
            grid[selected_city[0]][selected_city[1]].net -= wage_change + self.cost
            grid[mouse_pos[0]][mouse_pos[1]].entity = mouse_entity + 1
            doubleup_flag = True
        else: 

            # land capturing
            if grid[mouse_pos[0]][mouse_pos[1]].color != color:
                grid[mouse_pos[0]][mouse_pos[1]].color = color

                self.affected_cells.append(selected_city)
                self.affected_cells.extend(Hex_Utils.verify(Hex_Utils.neighbours(mouse_pos[0],mouse_pos[1],1)))
                grid[selected_city[0]][selected_city[1]].income += 1
                grid[selected_city[0]][selected_city[1]].net += 1
                grid[selected_city[0]][selected_city[1]].land.append(mouse_pos)

                # land belongs to enemy, update enemy centre
                if grid[mouse_pos[0]][mouse_pos[1]].hall_loc is not None:

                    if grid[mouse_pos[0]][mouse_pos[1]].entity == Constants.CITY:
                        # Captured enemy centre, move it
                        affected_enemy_hall = Hex_Utils.moveHall(grid,mouse_pos,self.affected_cells,queued_security_updates)
                    else:
                        # captured random enemy land
                        affected_enemy_hall = grid[mouse_pos[0]][mouse_pos[1]].hall_loc
                        self.affected_cells.append(affected_enemy_hall)
                        wage_change = math.floor(2*3**(grid[mouse_pos[0]][mouse_pos[1]].entity-Constants.MAN)) if grid[mouse_pos[0]][mouse_pos[1]].entity >= Constants.MAN else 0
                        grid[affected_enemy_hall[0]][affected_enemy_hall[1]].income -= 1
                        grid[affected_enemy_hall[0]][affected_enemy_hall[1]].wages -= wage_change
                        grid[affected_enemy_hall[0]][affected_enemy_hall[1]].net += wage_change - 1
                        grid[affected_enemy_hall[0]][affected_enemy_hall[1]].land.remove(mouse_pos)

                # check if this connects to even more land
                connections = Hex_Utils.GetConnectingTerritories(grid,color,mouse_pos,selected_city)

                for connection in connections:
                    #This connecting bit of land belongs to a city, join these two cities.

                    if grid[connection[0]][connection[1]].hall_loc == selected_city: continue
                    joining_city = grid[connection[0]][connection[1]].hall_loc
                    self.affected_cells.extend(grid[joining_city[0]][joining_city[1]].land)
                    queued_security_updates.append(joining_city)
                    Hex_Utils.convertCity(grid,joining_city,selected_city)

                #Now any connecting bit of land does not belong to city, therefore any indirectly connecting bits also dont beling to a city. Find them and add
                new_land = []
                Hex_Utils.color_aggregate(mouse_pos[0],mouse_pos[1],grid[selected_city[0]][selected_city[1]].land,new_land,grid)
                for cell in new_land:
                    self.affected_cells.append(cell)
                    grid[cell[0]][cell[1]].hall_loc = selected_city
                    grid[selected_city[0]][selected_city[1]].land.append(cell)
                    if grid[cell[0]][cell[1]].entity != Constants.TREE and grid[cell[0]][cell[1]].entity != Constants.PALM:
                        grid[selected_city[0]][selected_city[1]].income += 1
                        grid[selected_city[0]][selected_city[1]].net += 1

            # new unit
            if pick_up_pos is None:
                if selected_city not in self.affected_cells: self.affected_cells.append(selected_city)
                Hex_Utils.appendifnotAppended(self.affected_cells,Hex_Utils.verify(Hex_Utils.neighbours(mouse_pos[0],mouse_pos[1],1)))
                Hex_Utils.appendifnotAppended(self.affected_cells,[mouse_pos])
                wage_change = math.floor(2*(3**(mouse_entity-Constants.MAN))) if mouse_entity != Constants.TOWER else 0
                cost = (mouse_entity-Constants.CITY)*10 if mouse_entity != Constants.TOWER else 15
                grid[selected_city[0]][selected_city[1]].wages += wage_change
                grid[selected_city[0]][selected_city[1]].gold -= cost
                grid[selected_city[0]][selected_city[1]].net -= wage_change + cost

            grid[mouse_pos[0]][mouse_pos[1]].hall_loc = selected_city
            grid[mouse_pos[0]][mouse_pos[1]].entity = mouse_entity

            # check if we split a enemy city in two
            if affected_enemy_hall is not None:
                Hex_Utils.HandleSplits(grid,affected_enemy_hall,self.affected_cells,queued_security_updates)

        if pick_up_pos is not None:
            grid[pick_up_pos[0]][pick_up_pos[1]].playable = False
            queued_security_updates.append(pick_up_pos)
            self.affected_cells.extend(Hex_Utils.verify(Hex_Utils.neighbours(pick_up_pos[0],pick_up_pos[1],1)))

        for update in queued_security_updates: Hex_Utils.SecurityUpdate(grid,update)

        if not doubleup_flag: grid[mouse_pos[0]][mouse_pos[1]].playable = False
        return
        
def Overshoot(grid,city_loc,new_unit,doubleup_contributors=0):
    diff = -(grid[city_loc[0]][city_loc[1]].income - grid[city_loc[0]][city_loc[1]].wages - math.floor(2*(3**(new_unit-1))) + doubleup_contributors*math.floor(2*(3**(new_unit-2))))
    return diff if diff>0 else 0

def Influence(grid,color,pos):
    counter = 0
    for cell in Hex_Utils.verify(Hex_Utils.neighbours(pos[0],pos[1],2)):
        if grid[cell[0]][cell[1]].terrain and grid[cell[0]][cell[1]].color!=color: counter = counter + 1
    return counter

def unProtected(grid,color,pos):
    counter = 0
    for cell in Hex_Utils.verify(Hex_Utils.neighbours(pos[0],pos[1],2)):
        if grid[cell[0]][cell[1]].color != color: continue
        if len(grid[cell[0]][cell[1]].security_providers) == 1 and grid[cell[0]][cell[1]].security_providers[0] == pos: counter = counter + 1
    return counter

def Protected(grid,color,pos,new_sec):
    counter = 0
    for cell in Hex_Utils.verify(Hex_Utils.neighbours(pos[0],pos[1],2)):
        if grid[cell[0]][cell[1]].color != color: continue
        if grid[cell[0]][cell[1]].security < new_sec: counter = counter + 1
    return counter

def TowerProtectsHall(grid,pos):
    if grid[pos[0]][pos[1]].hall_loc not in Hex_Utils.neighbours(pos[0],pos[1],1): return 0
    if grid[grid[pos[0]][pos[1]].hall_loc[0]][grid[pos[0]][pos[1]].hall_loc[1]].security >= Constants.TOWER_SECURITY: return 0
    return 1

def CanTreeSpread(grid,pos):
    for cell in Hex_Utils.verify(Hex_Utils.neighbours(pos[0],pos[1],1)):
        if grid[cell[0]][cell[1]].entity == Constants.NONE: return 1
    return 0

def DoubleupPartners(grid,color,pos):
    partners = []
    for cell in Hex_Utils.verify(Hex_Utils.neighbours(pos[0],pos[1],2)):
        if grid[cell[0]][cell[1]].color != color: continue
        if grid[cell[0]][cell[1]].entity != grid[pos[0]][pos[1]].entity: continue
        if grid[cell[0]][cell[1]].hall_loc != grid[pos[0]][pos[1]].hall_loc: continue
        partners.append(cell)
    return partners

def CityPlacementMoves(grid,color,city_loc,turn):
    moves = []
    maxunit = math.floor(grid[city_loc[0]][city_loc[1]].gold/10) # Max unit affordable to buy
    if maxunit>4: maxunit = 4

    unit_bonus = BaseConstants.NO_UNITS_ON_GROUND_BONUS*(1 if grid[city_loc[0]][city_loc[1]].wages == 0 and len(grid[city_loc[0]][city_loc[1]].land)>3 else (0.5 if grid[city_loc[0]][city_loc[1]].wages < 8 and len(grid[city_loc[0]][city_loc[1]].land)>3 else 0))
    tower_bonus = BaseConstants.BOX_IN_STRATEGY_BONUS*(1 if len(grid[city_loc[0]][city_loc[1]].land)<=3 and len(Hex_Utils.getValidMoves(city_loc,grid,color,Constants.MAN)) == 0 else 0)

    for i in range(1,maxunit+1):
        for pos in Hex_Utils.getValidPlacementSpots(city_loc,grid,Constants.CITY+i):

            if grid[pos[0]][pos[1]].color != color:
                prio = BaseConstants.CAPTURE_ENEMY + len(Hex_Utils.GetConnectingTerritories(grid,color,pos,city_loc))*EnemyCapMods.CONNECTSTOCITY + len(Hex_Utils.GetConnectingUnclaimed(grid,color,pos))*EnemyCapMods.CONNECTSTOMORE + unProtected(grid,color,pos)*EnemyCapMods.UNPROTECT + Protected(grid,color,pos,Constants.CITY+i)*UnclaimedCapMods.PROTECT + EnemyCapMods.HASTREE*(1 if grid[pos[0]][pos[1]].entity > Constants.NONE and grid[pos[0]][pos[1]].entity <= Constants.GRAVE else 0) + EnemyCapMods.ENEMYCAPITAL*(1 if grid[pos[0]][pos[1]].entity == Constants.CITY else 0) + EnemyCapMods.ENEMYTOWER*(1 if grid[pos[0]][pos[1]].entity == Constants.TOWER else 0) + EnemyCapMods.ENEMYUNIT*(1 if grid[pos[0]][pos[1]].entity > Constants.CITY else 0) + EnemyCapMods.WAGEOVERSHOOT*Overshoot(grid,city_loc,i)+unit_bonus
                moves.append(AIMove(city_loc,pos,[('new unit',Constants.CITY+i)],10*(i),prio,grid,'new unit capture'))

            elif grid[pos[0]][pos[1]].entity == Constants.NONE:
                prio = BaseConstants.BUY_UNIT + Influence(grid,color,pos)*UnitMods.INFLUENCE + unProtected(grid,color,pos)*UnitMods.UNPROTECTS + Protected(grid,color,pos,i)*UnitMods.PROTECTS + UnitMods.WAGEOVERSHOOT*Overshoot(grid,city_loc,i)+unit_bonus
                moves.append(AIMove(city_loc,pos,[('new unit',Constants.CITY+i)],10*(i),prio,grid,'new unit empty'))

            elif grid[pos[0]][pos[1]].entity <= Constants.GRAVE:
                for i in range(1,maxunit+1):
                    prio = BaseConstants.BUY_UNIT + Influence(grid,color,pos)*UnitMods.INFLUENCE + unProtected(grid,color,pos)*UnitMods.UNPROTECTS + Protected(grid,color,pos,i)*UnitMods.PROTECTS + UnitMods.WAGEOVERSHOOT*Overshoot(grid,city_loc,i) + TreeMods.CANSPREAD*CanTreeSpread(grid,pos) + (1 if grid[pos[0]][pos[1]].entity == Constants.PALM else 0)+unit_bonus
                    moves.append(AIMove(city_loc,pos,[('new unit',Constants.CITY+i)],10*(i),prio,grid,'new unit tree'))

            elif grid[pos[0]][pos[1]].entity > Constants.CITY:
                if maxunit >= grid[pos[0]][pos[1]].entity-Constants.CITY:
                    newlevel = grid[pos[0]][pos[1]].entity-Constants.CITY
                    prio = BaseConstants.DOUBLE_UP + Protected(grid,color,pos,newlevel)*DoubleupMods.PROTECT + UnitMods.WAGEOVERSHOOT*Overshoot(grid,city_loc,i,1)+unit_bonus
                    moves.append(AIMove(city_loc,pos,[('new unit',newlevel)],10*newlevel,prio,grid,'new unit double'))

    if grid[city_loc[0]][city_loc[1]].gold > 14:
        for pos in grid[city_loc[0]][city_loc[1]].land:
            if grid[pos[0]][pos[1]].entity == Constants.NONE:
                prio = BaseConstants.BUY_TOWER + Protected(grid,color,pos,Constants.TOWER_SECURITY)*TowerMods.PROTECT + TowerProtectsHall(grid,pos)*TowerMods.PROTECTHALL + tower_bonus
                moves.append(AIMove(city_loc,pos,[('new unit',Constants.TOWER)],15,prio,grid,'new tower empty'))
            elif grid[pos[0]][pos[1]].entity <= Constants.GRAVE:
                prio = BaseConstants.BUY_TOWER + Protected(grid,color,pos,Constants.TOWER_SECURITY)*TowerMods.PROTECT + TowerProtectsHall(grid,pos)*TowerMods.PROTECTHALL  + TreeMods.CANSPREAD*CanTreeSpread(grid,pos) + (1 if grid[pos[0]][pos[1]].entity == Constants.PALM else 0) + tower_bonus
                moves.append(AIMove(city_loc,pos,[('new unit',Constants.TOWER)],15,prio,grid,'new tower tree'))

    return moves


def UnitMoves(grid,color,unit_loc):
    moves = []
    targets = Hex_Utils.getValidMoves(unit_loc,grid,color,grid[unit_loc[0]][unit_loc[1]].entity)
    targets.remove(unit_loc)
    partners = DoubleupPartners(grid,color,unit_loc)
    curr_influence = Influence(grid,color,unit_loc)
    city_loc = grid[unit_loc[0]][unit_loc[1]].hall_loc

    if grid[unit_loc[0]][unit_loc[1]].entity < Constants.KNIGHT and len(partners) > 0:
        doubleupmoves = Hex_Utils.getValidMoves(unit_loc,grid,color,grid[unit_loc[0]][unit_loc[1]].entity+1)
    else:
        doubleupmoves = []
    
    for pos in targets:  

        try: doubleupmoves.remove(pos)
        except Exception: pass
        if grid[pos[0]][pos[1]].color != color:    
            if grid[pos[0]][pos[1]].hall_loc is None:
                prio = BaseConstants.CAPTURE_UNCLAIMED + len(Hex_Utils.GetConnectingTerritories(grid,color,pos,city_loc))*UnclaimedCapMods.CONNECTSTOCITY + len(Hex_Utils.GetConnectingUnclaimed(grid,color,pos))*UnclaimedCapMods.CONNECTSTOMORE + unProtected(grid,color,pos)*UnclaimedCapMods.UNPROTECT + Protected(grid,color,pos,grid[unit_loc[0]][unit_loc[1]].entity-Constants.CITY)*UnclaimedCapMods.PROTECT + UnclaimedCapMods.HASTREE*(1 if grid[pos[0]][pos[1]].entity > Constants.NONE and grid[pos[0]][pos[1]].entity <= Constants.GRAVE else 0)
                moves.append(AIMove(unit_loc,pos,[],0,prio,grid,'unit move unclaimed'))
            else:
                prio = BaseConstants.CAPTURE_ENEMY + len(Hex_Utils.GetConnectingTerritories(grid,color,pos,city_loc))*EnemyCapMods.CONNECTSTOCITY + len(Hex_Utils.GetConnectingUnclaimed(grid,color,pos))*EnemyCapMods.CONNECTSTOMORE + unProtected(grid,color,pos)*EnemyCapMods.UNPROTECT + Protected(grid,color,pos,grid[unit_loc[0]][unit_loc[1]].entity-Constants.CITY)*UnclaimedCapMods.PROTECT + EnemyCapMods.HASTREE*(1 if grid[pos[0]][pos[1]].entity > Constants.NONE and grid[pos[0]][pos[1]].entity <= Constants.GRAVE else 0) + EnemyCapMods.ENEMYCAPITAL*(1 if grid[pos[0]][pos[1]].entity == Constants.CITY else 0) + EnemyCapMods.ENEMYTOWER*(1 if grid[pos[0]][pos[1]].entity == Constants.TOWER else 0) + EnemyCapMods.ENEMYUNIT*(1 if grid[pos[0]][pos[1]].entity > Constants.CITY else 0)
                moves.append(AIMove(unit_loc,pos,[],0,prio,grid,'unit move capture'))
        else:
            if grid[pos[0]][pos[1]].entity == Constants.NONE:
                prio = BaseConstants.RELOCATE + RelModifiers.DELTAINFLUENCE*(Influence(grid,color,pos)-curr_influence)
                moves.append(AIMove(unit_loc,pos,[],0,prio,grid,'unit rel empty'))
            elif grid[pos[0]][pos[1]].entity <= Constants.GRAVE:
                prio = BaseConstants.REMOVE_TREE + TreeMods.CANSPREAD*CanTreeSpread(grid,pos) + TreeMods.ISPALM*(1 if grid[pos[0]][pos[1]].entity == Constants.PALM else 0)
                moves.append(AIMove(unit_loc,pos,[],0,prio,grid,'unit rel tree'))
            elif grid[pos[0]][pos[1]].entity == grid[unit_loc[0]][unit_loc[1]].entity:
                newlevel = grid[unit_loc[0]][unit_loc[1]].entity - Constants.CITY
                prio = BaseConstants.DOUBLE_UP + Protected(grid,color,pos,newlevel)*DoubleupMods.PROTECT + DoubleupMods.WAGEOVERSHOOT*Overshoot(grid,city_loc,grid[unit_loc[0]][unit_loc[1]].entity - Constants.CITY +1,2)
                moves.append(AIMove(unit_loc,pos,[],0,prio,grid,'unit rel double'))

    for pos in doubleupmoves:
        if grid[pos[0]][pos[1]].color == color: continue
        for partner in partners:
            prio = BaseConstants.CAPTURE_ENEMY + len(Hex_Utils.GetConnectingTerritories(grid,color,pos,city_loc))*EnemyCapMods.CONNECTSTOCITY + len(Hex_Utils.GetConnectingUnclaimed(grid,color,pos))*EnemyCapMods.CONNECTSTOMORE + unProtected(grid,color,pos)*EnemyCapMods.UNPROTECT + Protected(grid,color,pos,grid[unit_loc[0]][unit_loc[1]].entity-Constants.CITY)*UnclaimedCapMods.PROTECT + EnemyCapMods.HASTREE*(1 if grid[pos[0]][pos[1]].entity > Constants.NONE and grid[pos[0]][pos[1]].entity <= Constants.GRAVE else 0) + EnemyCapMods.ENEMYCAPITAL*(1 if grid[pos[0]][pos[1]].entity == Constants.CITY else 0) + EnemyCapMods.ENEMYTOWER*(1 if grid[pos[0]][pos[1]].entity == Constants.TOWER else 0) + EnemyCapMods.ENEMYUNIT*(1 if grid[pos[0]][pos[1]].entity > Constants.CITY else 0) + EnemyCapMods.REQUIREDOUBLE + EnemyCapMods.WAGEOVERSHOOT*Overshoot(grid,city_loc,grid[unit_loc[0]][unit_loc[1]].entity - Constants.CITY +1,2)
            moves.append(AIMove(unit_loc,pos,[('use unit',partner)],0,prio,grid,'unit double and move'))

        # Buy a double
        prio = BaseConstants.CAPTURE_ENEMY + len(Hex_Utils.GetConnectingTerritories(grid,color,pos,city_loc))*EnemyCapMods.CONNECTSTOCITY + len(Hex_Utils.GetConnectingUnclaimed(grid,color,pos))*EnemyCapMods.CONNECTSTOMORE + unProtected(grid,color,pos)*EnemyCapMods.UNPROTECT + Protected(grid,color,pos,grid[unit_loc[0]][unit_loc[1]].entity-Constants.CITY)*UnclaimedCapMods.PROTECT + EnemyCapMods.HASTREE*(1 if grid[pos[0]][pos[1]].entity > Constants.NONE and grid[pos[0]][pos[1]].entity <= Constants.GRAVE else 0) + EnemyCapMods.ENEMYCAPITAL*(1 if grid[pos[0]][pos[1]].entity == Constants.CITY else 0) + EnemyCapMods.ENEMYTOWER*(1 if grid[pos[0]][pos[1]].entity == Constants.TOWER else 0) + EnemyCapMods.ENEMYUNIT*(1 if grid[pos[0]][pos[1]].entity > Constants.CITY else 0) + EnemyCapMods.REQUIREDOUBLE + EnemyCapMods.WAGEOVERSHOOT*Overshoot(grid,city_loc,grid[unit_loc[0]][unit_loc[1]].entity - Constants.CITY +1,1)
        moves.append(AIMove(unit_loc,pos,[('buy worth',grid[unit_loc[0]][unit_loc[1]].entity*10)],grid[unit_loc[0]][unit_loc[1]].entity*10,prio,grid,'unit buy double and move'))

    return moves
