import AI_Utils
import Constants
import copy
from Move_Utils import Move,GameUpdate
from Net_Utils import Packet

def calculateAllMoves(grid,color,gridsize) -> list[AI_Utils.AIMove]:
    moves = []
    cities = []

    for x in range(0,gridsize[0]):
        for y in range(0,gridsize[1]):
            if grid[x][y].color != color: continue
            if grid[x][y].hall_loc is None: continue
            if grid[x][y].entity == Constants.CITY:
                moves.extend(AI_Utils.CityPlacementMoves(grid,color,(x,y)))
                cities.append((x,y))
                continue
            if grid[x][y].entity > Constants.CITY:
                moves.extend(AI_Utils.UnitMoves(grid,color,(x,y)))
    
    moves.sort(reverse=True,key=lambda e: e.priority)
    return moves, cities

def play(grid,color) -> Packet:
    savePrio = AI_Utils.BaseConstants.SAVE_MONEY
    movesPlayed = 0
    affected_cells = []
    print(f'AI PLAYER LOGS')
    print(f'--starting calculation for {color}')
    moves, cities = calculateAllMoves(grid,color, (len(grid),len(grid[0])))
    print(f'--done calculating, generated {len(moves)} possible moves')

    
    while len(moves) > 0:
        consideration = moves.pop(0)
        verification, fundIssue = consideration.verify(grid,cities)
        if fundIssue: savePrio+=1
        if not verification: 
            print(f'----Verification failed, {verification}, {fundIssue}\n')
            continue
        if consideration.requireSpending and consideration.priority <= savePrio: 
            print(f'----Verified but skipped to save money\n')
            continue
        print('----Verified and selected\n')
        consideration.execute(grid,color)
        AI_Utils.Hex_Utils.appendifnotAppended(affected_cells,consideration.affected_cells)
        movesPlayed +=1

    print(f'--done selecting, selected {movesPlayed} moves to play')
    print(f'--generating move packet from {len(affected_cells)} affected cells')

    total_move = Move({'source':color},GameUpdate([]),None,GameUpdate([]))
    for cell in affected_cells: total_move.preanimation.gridChanges.append((cell,copy.deepcopy(grid[cell[0]][cell[1]])))
    return Packet(Packet.UPDATE,total_move)