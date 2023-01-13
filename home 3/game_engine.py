"""
Author: Changhui He
Unikey: chhe9599
Due Date: 07/11/2021
Assignment 2

"""

import config
from space_object import SpaceObject
import math

class Engine:
    #Some static variables
    asteroids_obj_list = []
    bullet_obj_list=[]
    fuel = None
    score = None
    temp = None
    remain_75 = False
    remain_50 = False
    remain_25 = False
    upcoming_asteroids_obj_list = []
    bullet_id=0
    bullet_id_list = []
    def __init__(self, game_state_filename, player_class, gui_class):
        self.import_state(game_state_filename) #Call mathod "import_state" to get info from the state file
        self.game_state_filename = game_state_filename
        self.player = player_class()
        self.GUI = gui_class(Engine.width,Engine.height) #Set the range of picture
    def import_state(self, game_state_filename):
        # define a list to store the info in the state file
        game_state_list = []
        #Every valid key name in the state file
        key_list = ["width","height","score","spaceship","fuel","asteroids_count","asteroid_large","asteroid_small","bullets_count","upcoming_asteroids_count","upcoming_asteroid_large","upcoming_asteroid_small"]
        #Raise error when file is not exist
        try:
            f = open(game_state_filename,"r") #read file
        except FileNotFoundError:
            raise FileNotFoundError("Error: unable to open {}".format(game_state_filename))
        i=0
        while True:
            line = f.readline().split() #read each line in the txt file
            if len(line) == 0:
                break
            else: 
                #Handle some basic error
                if line[0] not in key_list: #When the key is not a valid key, raise ValueError
                    raise ValueError("Error: unexpected key: {} in line {}".format(line[0],i+1))
                if len(line) < 2:#When a key or a value is missing, raise ValueError
                    raise ValueError(f"Error: expecting a key and value in line {i+1}")

                #when a line is describing asteroid info, check the value is valid or not. If not, raise ValueError
                if line[0] == "asteroid_large" or line[0] == "asteroid_small" or line[0] == "upcoming_asteroid_large" or line[0] == "upcoming_asteroid_small" or line[0] == "spaceship":
                    if len(line[1].split(",")) != 4:
                        raise ValueError(f"Error: invalid data type in line {i+1}")
                elif line[0] in ["width", "height","score","asteroids_count","fuel","bullets_count","upcoming_asteroids_count"]:
                    if len(line)!= 2:
                        raise ValueError(f"Error: invalid data type in line {i+1}")
                

            game_state_list.append(line) #save lines in the list
            i+=1
        asteroids_count = 0
        bullets_count = 0
        upcoming_asteroids_count = 0
        check = True
        check_b = True
        bullet_count=0
        spicified_key_order = ["width","height","score","spaceship","fuel"]
        asteroids_list = [["asteroid_large","asteroid_small"],["upcoming_asteroid_large","upcoming_asteroid_small"]]
        i=0
        # Traverse state file list and check every line if it valid
        while i < len(game_state_list):
            key = game_state_list[i][0]
            # print(i)
            if i<3 :
                if key != spicified_key_order[i]:
                    raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                else:
                    try:
                        int(game_state_list[i][1])
                    except:
                        raise ValueError(f"Error: invalid data type in line {i+1}")
                    i+=1
                    continue
            if i == 3:
                if key != "spaceship":
                    raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                else:
                    i+=1
                    continue
            
            if i == 4:
                if key != "fuel":
                    raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                else:
                    try:
                        int(game_state_list[i][1])
                    except:
                        raise ValueError(f"Error: invalid data type in line {i+1}")
                    i+=1
                    continue

            
            if i==5:
                # print(game_state_list[i])
                if key == "asteroids_count":
                    try:
                        asteroids_count = int(game_state_list[i][1])
                    except:
                        raise ValueError(f"Error: invalid data type in line {i+1}")
                else:
                    raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                i+=1
                continue
            
            if asteroids_count != 0 and check == True:
                z=0
                while z<asteroids_count:
                    key = game_state_list[i][0]
                    if key not in asteroids_list[0]:
                        raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                    else:
                        try:
                            float(game_state_list[i][1].split(",")[0])
                            float(game_state_list[i][1].split(",")[1])
                            int(game_state_list[i][1].split(",")[2])
                            int(game_state_list[i][1].split(",")[3])
                        except:
                            raise ValueError(f"Error: invalid data type in line {i+1}")
                    z+=1
                    i+=1
                # print(i,"end",asteroids_count)
                if i == 5+asteroids_count+1:
                    key = game_state_list[i][0]
                    if key != "bullets_count":
                        raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                    else:
                        try:
                            bullet_count = int(game_state_list[i][1])
                        except:
                            raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                check = False
                
            if bullet_count != 0 and check_b == True:
                z=0
                while z<bullet_count:
                    key = game_state_list[i][0]
                    if key != "bullet":
                        raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                    else:
                        try:
                            float(game_state_list[i][1].split(",")[0])
                            float(game_state_list[i][1].split(",")[1])
                            int(game_state_list[i][1].split(",")[2])
                            int(game_state_list[i][1].split(",")[3])
                        except:
                            raise ValueError(f"Error: invalid data type in line {i+1}")
                    z+=1
                    i+=1
                check_b = False



            if i == 5+asteroids_count+bullet_count+2:
                key = game_state_list[i][0]
                if key != "upcoming_asteroids_count":
                    raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                else:
                    try:
                        upcoming_asteroids_count = int(game_state_list[i][1])
                    except:
                        raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
            
            if i > 5+asteroids_count+2:
                k=0
                while k < upcoming_asteroids_count:
                    try:
                        key = game_state_list[i][0]
                    except IndexError:
                        raise ValueError('Error: game state incomplete')
                    if key not in asteroids_list[1]:
                        raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
                    else:
                        try:
                            float(game_state_list[i][1].split(",")[0])
                            float(game_state_list[i][1].split(",")[1])
                            int(game_state_list[i][1].split(",")[2])
                            int(game_state_list[i][1].split(",")[3])
                        except:
                            raise ValueError(f"Error: invalid data type in line {i+1}")
                    i+=1
                    k+=1
                try:
                    key =game_state_list[i][0] 
                except IndexError:
                    break
                raise ValueError("Error: unexpected key: {} in line {}".format(key,i+1))
            i+=1
        if i < 8:
            raise ValueError('Error: game state incomplete')
        line_count = upcoming_asteroids_count + bullets_count + asteroids_count + 8
        
        if len(game_state_list) != line_count:
            raise ValueError('Error: game state incomplete')

        
        for i in game_state_list:
            if i[0] == "asteroids_count":
                asteroids_count = int(i[1])
            elif i[0] == "bullets_count":
                bullets_count = int(i[1])
            elif i[0] == "upcoming_asteroids_count":
                upcoming_asteroids_count = int(i[1])
        
        
                    
                        



        f.close()

        
        Engine.width = int(game_state_list[0][1])
        Engine.height = int(game_state_list[1][1])
        Engine.score = int(game_state_list[2][1])
        Engine.fuel = int(game_state_list[4][1])
        Engine.fuel_full = int(game_state_list[4][1])
        Engine.temp = game_state_list[3][1].split(",")
        Engine.spaceship = SpaceObject(float(Engine.temp[0]),float(Engine.temp[1]),int(Engine.width),int(Engine.height),int(Engine.temp[2]),"spaceship",Engine.temp[3])
        i=5
        k=0
        while True: 
            if game_state_list[i][0] == "asteroids_count":
                k=int(game_state_list[i][1])
                z=i+k
                while i < z:
                    i+=1
                    Engine.temp = game_state_list[i][1].split(",")
                    Engine.obj_type = game_state_list[i][0]
                    # print(i,z)
                    Engine.asteroids_obj_list.append(SpaceObject(float(Engine.temp[0]),float(Engine.temp[1]),int(Engine.width),int(Engine.height),int(Engine.temp[2]),Engine.obj_type,int(Engine.temp[3])))
                
            if game_state_list[i][0] =="bullets_count":
                k=int(game_state_list[i][1])
                z=i+k
                if k ==0:
                    i+=1
                else:
                    while i < z:
                        i+=1
                        Engine.temp = game_state_list[i][1].split(",")
                        Engine.obj_type = game_state_list[i][0]
                        Engine.bullet_obj_list.append(SpaceObject(float(Engine.temp[0]),float(Engine.temp[1]),int(Engine.width),int(Engine.height),int(Engine.temp[2]),Engine.obj_type,int(Engine.temp[3])))
                
            if game_state_list[i][0] =="upcoming_asteroids_count":
                k=int(game_state_list[i][1])
                z=i+k
                while i < z:
                    i+=1
                    Engine.temp = game_state_list[i][1].split(",")
                    Engine.obj_type = game_state_list[i][0]
                    Engine.upcoming_asteroids_obj_list.append([game_state_list[i][0],game_state_list[i][1].split(",")])
                break
            
            i+=1
        for i in Engine.upcoming_asteroids_obj_list:
            if i[0] == "upcoming_asteroid_large":
                i[0] = "asteroid_large"
            if i[0] == "upcoming_asteroid_small":
                i[0] = "asteroid_small"
            if i[0] == "bullets_count":
                Engine.bullet_id = i[1]


        return game_state_list
        



        # Enter your code here


    def export_state(self, game_state_filename):
        
        f = open(game_state_filename,'w')
        
        f.write(f"width {Engine.width}\n")
        f.write(f"height {Engine.height}\n")
        f.write(f"score {Engine.score}\n")
        f.write(f"{Engine.spaceship}\n")
        f.write(f"fuel {Engine.fuel}\n")
        f.write(f"asteroids_count {len(Engine.asteroids_obj_list)}\n")
        i=0
        while i < len(Engine.asteroids_obj_list):
            f.write(f"{Engine.asteroids_obj_list[i]}\n")
            i+=1
        f.write(f"bullets_count {len(Engine.bullet_obj_list)}\n")
        i=0
        while i < len(Engine.bullet_obj_list):
            f.write(f"{Engine.bullet_obj_list[i]}\n")
            i+=1
        f.write(f"upcoming_asteroids_count {len(Engine.upcoming_asteroids_obj_list)}\n")
        i=0
        while i < len(Engine.upcoming_asteroids_obj_list):
            f.write(f"upcoming_{Engine.upcoming_asteroids_obj_list[i][0]} {Engine.upcoming_asteroids_obj_list[i][1][0]},{Engine.upcoming_asteroids_obj_list[i][1][1]},{Engine.upcoming_asteroids_obj_list[i][1][2]},{Engine.upcoming_asteroids_obj_list[i][1][3]}\n")
            i+=1
        
   

 
        f.close()

        


    def run_game(self):
        frame_count = 1
        while True:
            #Receive player input
            Engine.player_input = self.player.action(Engine.spaceship,Engine.asteroids_obj_list,Engine.bullet_obj_list,Engine.fuel,Engine.score)
            
            #Manoeuvre the spaceship
            if Engine.player_input[1]== True:
                Engine.spaceship.turn_left()
            if Engine.player_input[2]== True:
                Engine.spaceship.turn_right()
            if Engine.player_input[0]== True:
                Engine.spaceship.move_forward()

            #Update positions of asteroids
            for i in Engine.asteroids_obj_list:
                i.move_forward()
            
            #launch a new bullet
            if Engine.player_input[3]== True:
                if Engine.fuel <config.shoot_fuel_threshold:
                    print("Cannot shoot due to low fuel")
                else:
                    Engine.bullet_obj_list.append(SpaceObject(Engine.spaceship.x,Engine.spaceship.y,Engine.width,Engine.height,Engine.spaceship.angle,"bullet",Engine.bullet_id))
                    Engine.fuel -= config.bullet_fuel_consumption
                    Engine.bullet_id += 1
            
            
            #remove expired bullets
            for i in Engine.bullet_obj_list:
                i.bullet_life += 1
            for i in Engine.bullet_obj_list:
                if i.bullet_life>config.bullet_move_count:
                    Engine.bullet_obj_list.remove(i)
            
            #update positions of bullets
            for i in Engine.bullet_obj_list:
                i.move_forward()
    
            
            
            #Deduct fuel
            Engine.fuel_warning_1 = config.fuel_warning_threshold[0]
            Engine.fuel_warning_2 = config.fuel_warning_threshold[1]
            Engine.fuel_warning_3 = config.fuel_warning_threshold[2]
            Engine.fuel -= config.spaceship_fuel_consumption
            if Engine.fuel <= math.floor(Engine.fuel_full * Engine.fuel_warning_1*0.01) and Engine.remain_75 == False:
                print(f"{Engine.fuel_warning_1}% fuel warning: {Engine.fuel} remaining")
                Engine.remain_75 = True
            elif Engine.fuel <= math.floor(Engine.fuel_full * Engine.fuel_warning_2*0.01) and Engine.remain_50 == False:
                print(f"{Engine.fuel_warning_2}% fuel warning: {Engine.fuel} remaining")
                Engine.remain_50 = True
            elif Engine.fuel <= math.floor(Engine.fuel_full * Engine.fuel_warning_3*0.01) and Engine.remain_25 == False:
                print(f"{Engine.fuel_warning_3}% fuel warning: {Engine.fuel} remaining")
                Engine.remain_25 = True

            
            
            #If a bullet collides with an asteroid
            add_ast = 0
            for i in Engine.bullet_obj_list:
                for k in Engine.asteroids_obj_list:
                    if k.collide_with(i) == True:
                        # print(k.bullet_life)
                        add_ast += 1

                        if k.obj_type == "asteroid_small":
                            Engine.score += config.shoot_small_ast_score
                        if k.obj_type == "asteroid_large":
                            Engine.score += config.shoot_large_ast_score
                        
                        print(f"Score: {Engine.score} \t [Bullet {i.id} has shot asteroid {k.id}]")
                        Engine.asteroids_obj_list.remove(k)
                        # print(len(Engine.upcoming_asteroids_obj_list))
                        Engine.bullet_obj_list.remove(i)
           
            #If the spaceship collides with an asteroid        
            for ast in Engine.asteroids_obj_list:
                if Engine.spaceship.collide_with(ast):
                    add_ast += 1
                    Engine.score += config.collide_score
                    print(f"Score: {Engine.score} \t [Spaceship collided with asteroid {ast.id}]")
                    Engine.asteroids_obj_list.remove(ast)
            
            #replenish asteroids
            i=0
            b = False
            while i < add_ast:
                if len(Engine.upcoming_asteroids_obj_list) !=0:
                    Engine.asteroids_obj_list.append(SpaceObject(float(Engine.upcoming_asteroids_obj_list[0][1][0]),float(Engine.upcoming_asteroids_obj_list[0][1][1]),Engine.width,Engine.height,int(Engine.upcoming_asteroids_obj_list[0][1][2]),Engine.upcoming_asteroids_obj_list[0][0],int(Engine.upcoming_asteroids_obj_list[0][1][3])))
                    print(f"Added asteroid {Engine.asteroids_obj_list[-1].id}")
                    del Engine.upcoming_asteroids_obj_list[0]
                else:
                    print("Error: no more asteroids available")
                    b = True
                    break
                i += 1
            if b :
                break

    
            


            
            

            
            # 2. Process game logic

            # 3. Draw the game state on screen using the GUI class
            

            self.GUI.update_frame(Engine.spaceship,Engine.asteroids_obj_list,Engine.bullet_obj_list,Engine.score,Engine.fuel)
            frame_count +=1
            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            # - no more asteroids are available

            
            if Engine.fuel <= 0:
                break
            elif len(Engine.asteroids_obj_list) == 0:
                break

        # Display final score
        self.GUI.finish(Engine.score)

    # You can add additional methods if required