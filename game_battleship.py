import random
import os
import math
from _operator import pos
width_max = 11
height_max = 11
class grid:
#    enemy = True
    hit = []
    ship = []
    sunk = []
    miss = []
    max = [height_max, width_max]
    guess = []
    health_alive = []
#Initialize grid   
grid_enemy = grid()
grid_friendly = grid()
grid_friendly.enemy = False

class ship:
    enemy = True#true/false
    name = "" #
    health = 0 #starts between 5 and 2
    pos =[]
    hit = []
    live = []
    sunk = []
def convert_for_grid(in_string):
    result = [0,0]
    lon_str = in_string[0]
    try:
        lon_val = int(ord(lon_str.lower()) - 96)
        if lon_val > 0 and lon_val < 11: 
            result[1] = lon_val
        else:
            return([0,0])
    except:
        return([0,0])
    try: 
        lat_val = int(in_string[1:])
        if lat_val > 0 and lat_val < 11: 
            result[0] = lat_val
        else: 
            return([0,0])
    except:
        return([0,0])
    return result   

#Playable grid [1,1] through [10,10]
def grid_maker(hit, ship, sunk, miss, max):
    grid = [["   " for i in range(max[1])] for i in range(max[0])]
    for j in range(0,len(miss)):
        grid[miss[j][0]][miss[j][1]] = " + "
    for j in range(0,len(hit)):
        grid[hit[j][0]][hit[j][1]] = " X "
    for j in range(0,len(ship)):
        grid[ship[j][0]][ship[j][1]] = " O "
    for j in range(0,len(sunk)):
        grid[sunk[j][0]][sunk[j][1]] = " @ "
    grid[0][:] = ['   ', ' A ', ' B ', ' C ', ' D ', ' E ', ' F ', ' G ', ' H ', ' I ', ' J ']
    count = 1
    for j in range(1, height_max):
        grid[j][0]=' '+str(count)+' '
        if count > 9:
            grid[j][0] = str(count)+' '
        count = count +1
    return grid

#pos =[r,c] en=True for enemy
def is_occupied(pos, en ):
    result = False
    if en:
                
        if pos in grid_enemy.ship:
            result = True
        if pos[0]<1 or pos[1]<1:
            result = True
        if pos[0]>10 or pos[1]>10: 
            result = True
            
    else:
        if pos in grid_friendly.ship:
            result = True
            
        if pos[0]<1 or pos[1]<1:
            result = True
        if pos[0]>10 or pos[1]>10: #TODO: Review this
            result = True
    return result      

def draw_grid(desc):

    hit = []
    ship = []
    sunk = []
    miss = []
    grid_friendly.health_alive = []
    if desc == 'Friendly':
        miss = grid_friendly.miss
        for f in f_ships:
            hit = hit + f.hit
            ship = ship + f.pos
            #grid_friendly.ship = f.pos
            sunk = sunk + f.sunk
            grid_friendly.health_alive = grid_friendly.health_alive + [f.health]
            #miss = grid_friendly.miss
        grid_var = grid_maker(hit, ship, sunk,miss,grid_friendly.max)
        print('\n'.join(''.join(row) for row in grid_var))
        #used for AI
        grid_friendly.hit = hit
        grid_friendly.sunk = sunk
        
        
    if desc == 'Enemy':
        miss = grid_enemy.miss
        for e in e_ships:
            hit = hit + e.hit
            ship = ship + e.pos
            ship = []
            sunk = sunk + e.sunk
            #miss = grid_enemy.miss
        grid_var = grid_maker(hit, ship, sunk,miss,grid_friendly.max)
        print('\n'.join(''.join(row) for row in grid_var)) 
        
    if desc == 'End':
        miss = grid_enemy.miss
        for e in e_ships:
            hit = hit + e.hit
            ship = ship + e.pos
            sunk = sunk + e.sunk
            #miss = grid_enemy.miss
        grid_var = grid_maker(hit, ship, sunk,miss,grid_friendly.max)
        print('\n'.join(''.join(row) for row in grid_var)) 
    
          
def display(win):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Enemy')
    if win == 1:
        draw_grid('End')
    else:
        draw_grid('Enemy')
    print('    ')
    print('Player')
    draw_grid('Friendly')
    
    
def direction_assign(pos_var, dir, h,en):
    #start at location
    result = [pos_var]
    offset = 1
    try:
        if dir=='N' or dir=='n':
            old_pos = pos_var
            while offset < h:
                new_pos_var = [old_pos[0]-1, old_pos[1]]
                if not is_occupied(new_pos_var,en):
                    result = result + [new_pos_var]
                    old_pos = new_pos_var
                    offset = offset+1
                else: 
                    old_pos = pos_var
                    while offset < h:
                        new_pos_var = [old_pos[0]+1, old_pos[1]] 
                        if not is_occupied(new_pos_var,en):
                            result = result + [new_pos_var]
                            old_pos = new_pos_var
                            offset = offset+1
                        else:
                            return([[0,0]])
                    
        elif dir=='S' or dir == 's':
            old_pos = pos_var
            while offset < h:
                new_pos_var = [old_pos[0]+1, old_pos[1]]
                if not is_occupied(new_pos_var,en):
                    result = result + [new_pos_var]
                    old_pos = new_pos_var
                    offset = offset+1
                else: 
                    old_pos = pos_var
                    while offset < h:
                        new_pos_var = [old_pos[0]-1, old_pos[1]] 
                        if not is_occupied(new_pos_var,en):
                            result = result + [new_pos_var]
                            old_pos = new_pos_var
                            offset = offset+1
                        else:
                            return([[0,0]])
        elif dir=='E' or dir=='e':
            old_pos = pos_var
            while offset < h:
                new_pos_var = [old_pos[0], old_pos[1]+1]
                if not is_occupied(new_pos_var,en):
                    result = result + [new_pos_var]
                    old_pos = new_pos_var
                    offset = offset+1
                else: 
                    old_pos = pos_var
                    while offset < h:
                        new_pos_var = [old_pos[0], old_pos[1]-1] 
                        if not is_occupied(new_pos_var,en):
                            result = result + [new_pos_var]
                            old_pos = new_pos_var
                            offset = offset+1
                        else:
                            return([[0,0]])
        elif dir=='W' or dir=='w':
            old_pos = pos_var
            while offset < h:
                new_pos_var = [old_pos[0], old_pos[1]-1]
                if not is_occupied(new_pos_var,en):
                    result = result + [new_pos_var]
                    old_pos = new_pos_var
                    offset = offset+1
                else: 
                    old_pos = pos_var
                    while offset < h:
                        new_pos_var = [old_pos[0], old_pos[1]+1] 
                        if not is_occupied(new_pos_var,en):
                            result = result + [new_pos_var]
                            old_pos = new_pos_var
                            offset = offset+1
                        else:
                            return([[0,0]])
        else:
            return([[0,0]])
                            
        return(result)
    except:
        print('Error finding direction')
        return([[0,0]])
    #continue in direction given h spaces
    #check for edge or others 
    #reverse direction
    #if still not done, return [[0,0]]
    #if fits, return ship coordinates
    
    
def assign_Ships(ship_name, health, enemy):
    s = ship()
    s.enemy = False
    s.name = ship_name
    s.health = health
    if enemy:
        s.enemy = True
        e_pos_check = True
        while e_pos_check:
            raw_guess = [random.randint(1,10),random.randint(1,10)] #change 5-> 10 for fair game
            if not is_occupied(raw_guess, True):
                ran_dir_list = ['N','S','E','W']
                raw_direction = ran_dir_list[random.randint(0,3)]
                new_ship_pos = direction_assign(raw_guess, raw_direction, health, s.enemy)
                if new_ship_pos != [[0,0]]:        
                    s.pos = new_ship_pos
                    s.live = s.pos
                    grid_enemy.ship = grid_enemy.ship + new_ship_pos
                    e_pos_check = False

    else:
        print('    ')
        print('Assign Ship:' + s.name + '(Health = {})'.format(s.health))
        pos_check = True
        while pos_check: 
            try:
                raw_input = input('Starting Position between A1 and J10:')
                pos_var = convert_for_grid(raw_input)
                if pos_var == [0,0]:
                    print('Please input a proper coordinate')
                else: 
                    if is_occupied(pos_var,False):
                            print('Coordinate is already taken')
                    else: 
                        #print('Valid coordinate')
                        #Direction
                        raw_dir = input('Assign Direction N/S/E/W: ')
                        ship_pos =  direction_assign(pos_var, raw_dir,health, s.enemy) 
                        if ship_pos != [[0,0]]:
                            pos_check = False
                            s.pos = ship_pos 
                            s.live = s.pos
                            grid_friendly.ship = grid_friendly.ship + ship_pos
                            #print(grid_friendly.ship)  
                        else:
                            print('Error assigning ship. Try again')
            except:
                print('Error assigning ship')
                        
    return(s)

#Player start

e_ships = []
f_ships = []
os.system('cls' if os.name == 'nt' else 'clear')
display(0)
ship_list = [['Carrier',5],['Battleship',4],['Cruiser',3],['Submarine',3],['Destroyer',2]]
for ss in ship_list:
    temp_f_ship = assign_Ships(ss[0],ss[1],False)
    f_ships = f_ships + [temp_f_ship]
    
    temp_e_ship = assign_Ships(ss[0],ss[1],True)
    e_ships = e_ships + [temp_e_ship]
    display(0)

def hit_check(pos,en):
    result = 'Error'
    if en:
        for e in e_ships:
            if pos in e.live: 
                result = 'Player: Hit'
                e.hit = e.hit + [pos]
                e.live.remove(pos)
                if e.live == []:
                    e.sunk = e.hit
                    e.hit = []
                    e.health = 0
                    result = 'Player: You sunk their {}!'.format(e.name)
        if result == 'Error':
            grid_enemy.miss = grid_enemy.miss + [pos]
            result = 'Player: Miss'
    else:
        for f in f_ships:
            if pos in f.live: 
                result = 'Enemy hit your {}!'.format(f.name)
                f.hit = f.hit + [pos]
                f.live.remove(pos)
                if f.live == []:
                    f.sunk = f.hit
                    f.hit = []
                    f.health = 0
                    result = 'Enemy sunk your {}!'.format(f.name)
        if result == 'Error':
            grid_friendly.miss = grid_friendly.miss + [pos]
            result = 'Enemy: Miss'
    return result  
    
def cpu_ai():
    ai_miss = grid_friendly.miss
    ai_hit = grid_friendly.hit
    ai_sunk = grid_friendly.sunk
    ai_health = grid_friendly.health_alive
    
    blank = ai_miss + ai_sunk
    total = blank + ai_hit
    
    #range of 1-10 for both x and y
    
    #find 2 or more hits in a row
    #    continue in a direction (by comparing to blanks)
    
    
    #find a hit and check the surroundings
    #    look at distance to surrounding blanks
    #    compare to length of health of ships
    result = []
    overflow = 0
    of1 = True
    coord_check = True
    #print(ai_hit)
    while coord_check:
        
        #result if no x or y    
        x1 = random.randint(1,5)*2
        y1 = random.randint(1,5)*2-1 #makes sure it is a grid when a random guess
        x2 = random.randint(1,5)*2-1 
        y2 = random.randint(1,5)*2
        xyr = random.randint(0,1)
        xa = [x1,x2]
        ya = [y1,y2]
        result = [ya[xyr],xa[xyr]]
        hit_avail = len(ai_hit)
        
        if hit_avail == 1:
            c = ai_hit[0]
            coord_hold = [  [c[0],c[1]-1]  ,  [c[0],c[1]+1]  ,  [c[0]-1,c[1]]  ,  [c[0]+1,c[1]]  ]
            c_pick = random.randint(0,3)
            result = coord_hold[c_pick]
            
        if hit_avail > 1:
            if ai_hit[0][0] == ai_hit[1][0]:
                max_x = max([sublist[1] for sublist in ai_hit]) +1
                min_x = min([sublist[1] for sublist in ai_hit]) -1
                x = [min_x, max_x][random.randint(0,1)]
                y = ai_hit[0][0]
                result = [y,x]
            if ai_hit[0][1] == ai_hit[1][1]:
                max_y = max([sublist[0] for sublist in ai_hit]) +1
                min_y = min([sublist[0] for sublist in ai_hit]) -1
                y = [min_y, max_y][random.randint(0,1)]
                x = ai_hit[0][1]
                result = [y,x]      
                                      
        overflow = overflow+1
        if overflow > 100 and hit_avail > 0:
            r = random.randint(0,hit_avail)
            ai_hit = ai_hit[:r]+ai_hit[r+1:]
            #print('overflow 1')
            
        if overflow > 500:
            x = random.randint(1,10)
            y = random.randint(1,10) 
            result = [y,x]
            #print('overflow 2')
            
        allowable = False
        if result[0] > 0 and result[1] > 0 and result[0] <11 and result[1]<11:
            allowable = True
        if result not in total and allowable:
            coord_check = False
    return(result)   




#Game Start
gameOn = True
msg1 = '    '
msg2 = '    '
while gameOn:
    display(0)
    print(msg1)
    print(msg2)
    guessing = True
    while guessing:
        #player turn
        try:
            raw_guess = input('Target: ')
            pos_guess = convert_for_grid(raw_guess)
            if pos_guess == [0,0]:
                print('Please input a proper coordinate')
            else: 
                if pos_guess in grid_enemy.guess:
                    print('You have already selected this coordinate')
                else:
                    msg1 = hit_check(pos_guess, True) #attacking en=True
                    guessing = False
                    grid_enemy.guess = grid_enemy.guess + [pos_guess]
        except:
            print('Please input a proper coordinate')
    while not guessing:
        #enemy turn
        pos_guess = cpu_ai()
        #pos_guess = [random.randint(1,10),random.randint(1,10)]
        if pos_guess not in grid_friendly.guess:
            msg2 =  hit_check(pos_guess,False) #getting hit en=False
            guessing = True
            grid_friendly.guess = grid_friendly.guess + [pos_guess]
        else: 
            print('Enemy did not attack properly')
    
    #check victory conditions 
    player_win = 0
    for e in e_ships:
        player_win = player_win + e.health
    if player_win == 0:
        gameOn = False
        msg3 = 'Congratulations! You Win!'
    enemy_win =0
    for f in f_ships:
        enemy_win = enemy_win + f.health
    if enemy_win == 0:
        gameOn = False
        msg3 = 'You lose!'
display(1)
print(msg3)
end_string = input('Game will close')
os.system('pause')


                
 


