''' Grzegorz Krug

'''
import winsound
import random
import time
import pandas as pd
import math
import datetime
from matplotlib import pyplot as plt
import numpy as np
from copy import copy
from math import pi as PI
# from My_GA_Log import C_GA_Log


time.clock()

def cls():
    print("\n" * 20)


class CGenetic():

    def __init__(
            self, mode, UNITS=10, columns=27, rows=27,
            BORN_RANGE=10, sc_target=False,
            capacity=100):
        self.Mode = mode
        self.UNITS = UNITS
        print("Population initialized.")


        #VERIFYING INITIAL CONDITIONS
        if rows%2==0:
            rows += 1
            print("Rows must be ODD, new value: {0}".format(rows))
        if columns%2==0:
            columns += 1
            print("Columns must be ODD, new value: {0}".format(columns))

        self.COLUMNS = columns
        self.ROWS = rows
        self.MAP_LEN = columns * rows
        self.def_map(["Path","Home","Tesla"])
        self.BORN_RANGE = 3 # Empty, Home, TeslaTower
        # self.log = C_GA_Log()

        if ((self.Mode != "Int")
                and (self.Mode != "Real")
                and (self.Mode != "Both")):
            print("Wrong Mode! switching to REAL")
            self.Mode = "Real"

        self.MAP_LENabel=[]
        for j in range(self.MAP_LEN):
            self.MAP_LENabel.append("@"+str(j))
        self.Population = []
        self.Score=[]
        try:
            self.Population.append(np.loadtxt("D:\Python_64\City_Plan\Last_leader_2step.csv",\
                delimiter=";",dtype="int"))
            self.Score.append([])
        except FileNotFoundError:
            pass
        # self.Population.append(np.loadtxt("D:\Python_64\City_Plan/Golden_Try.csv",\
        #     delimiter=";",dtype="int"))
        # self.Score.append([])
        try:
            eta_now = np.loadtxt("D:\Python_64\City_Plan/Last_eta.csv",dtype="int")
            self.eta_now = int(eta_now[0])
        except:
            self.eta_now = 0
        # print(len(self.Population))



        self.Capacity = capacity


        self.f_sorted = 0
        self.Precision = 4
        self.Score_precision = 8
        self.Score_target = sc_target
        self.now = datetime.datetime.now()
        self.run_id = (str(self.now)[0:10]+"_"+str(self.now)[11:13]+\
        "_"+str(self.now)[14:16]+"_"+str(self.now)[17:19])
        self.refill()
        self.fitness()



    def calculate_score(self,dna):
        score=0
        CITY_MAP = self.get_map(dna)

        for row,Row in enumerate(CITY_MAP):

            for column,element in enumerate(Row):

                building = element.get("Building")
                if building == "Home" or building == "Good_Home_piece":

                    if element.get("Power") == True:
                        score += 10
                        if element.get("Reach") == True:
                            score += 20

                        else:
                            score -= 10
                elif building == "Tesla":
                    score -= 1
                elif building == "Bank":
                    if element.get("Power")==True and element.get("Reach")==True:
                        score += 10
                    # else:
                    #     score -= 100

                elif building == "Path":
                    pass
                # elif building == "Replace":
                #     score
                elif building == "Unused_Home_piece" or building == "Replace":
                    pass
                else:
                    pass



        score = round(score,self.Score_precision)
        #print('Calculated =',score)
        return [score, "none_score"]


    def change_dna(self, number=1, times = 1):
        '''Shake function '''
        Chance = {"Home":0.60,"Tesla":0.10}

        for k in range(times):
            for index,dna in enumerate(self.Population):
                experimental = copy(dna)
                for n in range(number):

                    # r_b = round(random.random()*dna_range)
                    row = round(random.random()*self.ROWS)
                    col = round(random.random()*self.COLUMNS)

                    roll = random.random()
                    # print("ROLED = {0}".format(roll))
                    try:
                        if Chance.get("Home") > roll:
                            # print("Rolled Home")
                            building = self.MAP_NUM.get("Home")

                            experimental[ row * self.ROWS + col] = building
                            experimental[ row * self.ROWS + col+1] = building
                            experimental[ (row+1) * self.ROWS + col] = building
                            experimental[ (row+1) * self.ROWS + col+1] = building

                        else:
                            roll -= Chance.get("Home")
                            # print("ROLED reduced= {0}".format(roll))
                            if Chance.get("Tesla") > roll and roll > 0:
                                # print("Rolled Tesla")

                                building = self.MAP_NUM.get("Tesla")
                                experimental[ row * self.ROWS + col] = building
                            else:
                                roll -= Chance.get("Tesla")
                                # print("ROLED reduced= {0}".format(roll))
                                if roll > 0:
                                    # print("Rolled Path")
                                    experimental[ row * self.ROWS + col] = 0

                    except IndexError:
                        pass

                score = self.calculate_score(experimental)
                if score[0] > self.Score[index][0]:
                    self.Score[index] = score
                    self.Population[index] = experimental
                    # self.log.log_this("shake",chance,self.eta_now,1)


    def def_map(self,List):
        self.MAP_MARKERS = {}
        self.MAP_NUM = {}
        for index,marker in enumerate(List):
            self.MAP_MARKERS.update({index:marker})
            self.MAP_NUM.update({marker:index})


    def fitness(self):
        print("\tFitness of {0}".format(self.UNITS))
        for i,dna in enumerate( self.Population ):
            self.Score[i] = self.calculate_score( dna )


    def fit_group(self,Population):
        score=[]
        for dna in Population:
            score.append( self.calculate_score( dna ))
        return score


    def get_map(self,dna):
        Map=[]
        for gen in dna:
            #Create map from Map Legend and index
            Map.append( self.MAP_MARKERS.get(gen,"Replace"))
            # if self.MAP_MARKERS.get(gen,"Out_of_markers") == "Out_of_markers":
            #     print(gen)

        Map = np.reshape(Map,(self.ROWS,self.COLUMNS))

        'Defining bank position and path around'
        mid_bank = (math.floor(self.ROWS / 2)-1,math.floor(self.ROWS / 2)+1)
        mid_path = (mid_bank[0]-1,mid_bank[1]+1)

        ###Inserting Bank markers
        ###Inserting Path markers around Bank'
        for a in range(mid_bank[0], mid_bank[1]+1):
            for b in range(mid_bank[0], mid_bank[1]+1):
                Map[a][b] = "Bank"
        for row in range(mid_path[0], mid_path[1]+1):
            for col in range(mid_path[0], mid_path[1]+1):
                if row in range(mid_path[0],mid_path[1]+1) and col in mid_path\
                or col in range(mid_path[0],mid_path[1]) and row in mid_path:
                    Map[row][col] = "Path"

        CityPlan = []
        for row,Row in enumerate(Map):
            ## Preparing Array of City plan for Analyzing
            CityPlan.append([]) # Create new row
            for col,building in enumerate(Row):
                CityPlan[row].append(\
                    {"Building":building,"Power":False,"Reach":False,\
                    "Occupied":False,"Activated":False})
                ### Outside Reach zone
                if row==0 or col==0 or row==self.ROWS-1 or col==self.COLUMNS-1:
                    CityPlan[row][col].update({"Reach":True})
                ### Outside power zone (range 8)
                if row<8 or row>=self.ROWS-8 or col<8 or col>=self.COLUMNS-8:
                    CityPlan[row][col].update({"Power":True})


        ##### Analyzing ### Segment ########
        'Loop 1: Power Loop'
        '+Loop 2: 4-Piece Home validation'
        '+Loop 3: Path(reach) checking Loop'
        for row,Row in enumerate(CityPlan):
            # path_map.append([])
            for col,element in enumerate(Row):
                building = element.get("Building")


        for row,Row in enumerate(CityPlan):
            # path_map.append([])
            for col,element in enumerate(Row):
                building = element.get("Building")
                if building =="Home" and element.get("Occupied") == False:
                    try:
                        if CityPlan[row+1][col].get("Building") == "Home"\
                        and CityPlan[row+1][col].get("Occupied") == False\
                        and CityPlan[row][col+1].get("Building") == "Home"\
                        and CityPlan[row][col+1].get("Occupied") == False\
                        and CityPlan[row+1][col+1].get("Building") == "Home"\
                        and CityPlan[row+1][col+1].get("Occupied") == False:
                            element.update({"Occupied":True})
                            for r,c in [[0,1],[1,1],[1,0]]:
                                CityPlan[row+r][col+c].update(\
                                        {"Building":"Good_Home_piece",\
                                        "Occupied":True})
                        else:
                            element.update({"Building":"Replace"})

                    except IndexError:
                        element.update({"Building":"Replace"})
                elif building == "Tesla" and element.get("Power")==True:
                # and element.get("Activated") == False:
                    tesla_range=range(-8,9)
                    for r in tesla_range:
                        for c in tesla_range:
                            try:
                                if r == 0 and c ==0:
                                    continue

                                elif abs(r)+abs(c) <=12:
                                    CityPlan[row+r][col+c].update({\
                                    "Power":True})

                                if CityPlan[row+r][col+c].get(\
                                "Building")=="Tesla"\
                                and (abs(r)<=4 and abs(c)<=4):
                                    CityPlan[row+r][col+c].update(\
                                    {"Building":"Replace"})
                            except IndexError:
                                pass

        # for row in range(self.ROWS):
        #     power_map.append([])
        #     for col in range(self.COLUMNS):
        #         power_map[row].append
        for k in range(22):
            f_path_updated = False
            for row,Row in enumerate(CityPlan):
                for col,element in enumerate(Row):
                    if  (element.get("Building") == "Path"\
                     or element.get("Building") == "None"\
                     or element.get("Building") == "Replace")\
                    and element.get("Reach")==True:

                        for r,c in zip([-1,0,0,1],[0,-1,1,0]):
                            try:
                                CityPlan[row+r][col+c].update({"Reach":True})
                                f_path_updated = True
                            except IndexError:
                                pass
            if f_path_updated == False:
                break
                # print(k)
        for row,Row in enumerate(CityPlan):
            for col,element in enumerate(Row):
                if element.get("Building") == "Home":

                    for r,c in [[0,0],[0,1],[1,1],[1,0]]:
                        try:
                            if CityPlan[row+r][col+c].get("Reach") == True:
                                for r,c in [[0,0],[0,1],[1,1],[1,0]]:
                                    CityPlan[row+r][col+c].update({"Reach":True})
                                break
                        except IndexError:
                            pass
        return CityPlan


    def insert_home(self):
        print("\t Insert home of 15")
        for index,unit in enumerate(self.Population):
            # experimental = copy(dna)
            # print("LEN OF experimental from insert home =",format(len(experimental)))
            # self.print_map(index=index)
            if index >=15:
                break

            for gen,chromosome in enumerate(unit):
                experimental = copy(self.Population[index])
                try:
                    experimental[gen] = self.MAP_NUM.get("Home")
                    experimental[gen + 1] = self.MAP_NUM.get("Home")
                    experimental[gen + self.ROWS] = self.MAP_NUM.get("Home")
                    experimental[gen + self.ROWS + 1] = self.MAP_NUM.get("Home")

                    score_exp = self.calculate_score(experimental)
                    # print(score_exp)

                    if score_exp[0] > self.Score[index][0]:

                        self.Score[index]= score_exp
                        self.Population[index] = experimental
                        # self.print_map(index=index)
                        # print("New Home")
                    # else:
                    #     experimental = copy(self.Population[index])
                except IndexError:
                    pass
        self.sort()

    def Map_Mutation(self,row=10,col=10,number=1,number2=2):
        '''PHASE 1, Mutating with leader'''
        print("\tMap mutation of ",len(self.Population))
        for index,Dna in enumerate(self.Population):
            experimental = copy(Dna)
            for n in range(number):
                gen =round(self.ROWS*self.ROWS*random.random()\
                         + self.COLUMNS*random.random())
                # print(self.ROWS,self.COLUMNS,gen)
                try:
                    for r in range(round(row*random.random())):
                        for c in range(round(col*random.random())):
                            experimental[gen+self.ROWS*r+c]\
                                = self.Population[0][gen+self.ROWS*r+c]
                except IndexError:
                    pass
            score_exp = self.calculate_score(experimental)
            if score_exp[0] > self.Score[index][0]:
                self.Population[index] = experimental
                self.Score[index] = score_exp

            #
            # '''PHASE 2, Mutating with random unit'''
            # index_random = round(random.random()*len(self.Population))
            # for n2 in range(number2):
            #     gen =round(self.ROWS*self.ROWS*random.random()\
            #              + self.COLUMNS*random.random())
            #     try:
            #         for r in range(round(row*random.random())):
            #             for c in range(round(col*random.random())):
            #                 experimental[gen+self.ROWS*r+c]\
            #                 = self.Population[index_random][gen+self.ROWS*r+c]
            #     except IndexError:
            #         pass
            # score_exp = self.calculate_score(experimental)
            # if score_exp[0] > self.Score[index][0]:
            #     self.Population[index] = experimental
            #     self.Score[index] = score_exp


    #
    # def mutation(self,index=0,mutants_density=0.25,mutation_factor=0.1):
    #     """ GroupA  : PHASE_1, Choosen unit self-mutating
    #         GroupB  : PHASE_2, Choosen unit mutating with weakers
    #         GroupC  : (DISABLED, ineffective) random units (nonsorted)
    #                     mutating with best """
    #
    #     if mutants_density > 1:
    #         mutants_density = 0.25
    #         print("Too many mutants")
    #     if mutants_density == 0:
    #         #Disabled Function by param
    #         return None
    #     if mutation_factor > 1:
    #         mutation_factor = 0.1
    #         print("Too many mutators")
    #
    #     mutants_number = math.ceil( len(self.Population) * mutants_density )
    #     genes_number = math.ceil( self.MAP_LEN * mutation_factor )
    #     random_units = \
    #             random.sample( range(index+1,len(self.Population)), mutants_number)
    #     ## --------------------- ##
    #     # timer_copy = time.clock()
    #     leader = self.Population[index].copy()
    #     groupA = []
    #     groupB = []
    #     # groupC = []
    #
    #     for mn in range(mutants_number):
    #         groupA.append( leader.copy() )
    #     # for rn in random_units:
    #     #     groupC.append( self.Population[rn].copy())
    #     # print("Copied in: {0}",str((time.clock()-timer_copy)*1000))
    #     ''' Phase 1  - Best group ~ SelfMutation
    #     ## gen_to_replace - Random Gene to read fromleader
    #     ## gen_samples - Random gene to overwrite in GroupA'''
    #     scoreA = self.fit_group(groupA)
    #
    #     for mn in range(mutants_number):
    #         gen_to_replace = random.sample( range(0,len(self.Population[0])),\
    #                 genes_number)
    #         gen_samples = random.sample( range(0,len(self.Population[0])),\
    #                 genes_number)
    #
    #         for gtr,gsample in zip(gen_to_replace,gen_samples):
    #             # if random.random() < chance:
    #             groupA[mn][gtr] = leader[gsample]
    #
    #     scoreA = self.fit_group(groupA)
    #     self.sort_group(groupA,scoreA)
    #
    #     if scoreA[0][0] > self.Score[index][0]:
    #         self.Score[index] = scoreA[0]
    #         self.Population[index] = groupA[0]
    #         # self.log.log_this("mutation_Phase1",mutation_factor,self.eta_now,1)
    #
    #     leader = self.Population[index].copy()
    #
    #     for mn in range(mutants_number):
    #         groupB.append( leader.copy() )
    #
    #     '''
    #     ### Phase 2  - Leader Mutating with genes from rest units'''
    #     gen_to_replace = random.sample( range(0,len(self.Population[0])),\
    #                                 genes_number)
    #     gen_samples = random.sample( range(0,len(self.Population[0])),\
    #                                 genes_number)
    #     for mn,ru in zip(range(mutants_number),random_units):
    #
    #         for gtr,gsample in zip(gen_to_replace,gen_samples):
    #             # if random.random() < chance:
    #             groupB[mn][gtr] = self.Population[ru][gsample]
    #             # if random.random() < chance:
    #             #     groupC[n][gtr] = leader[gsample]
    #
    #     scoreB = self.fit_group(groupB)
    #     self.sort_group(groupB,scoreB)
    #     if scoreB[0][0] > self.Score[index][0]:
    #         self.Score[index] = scoreB[0]
    #         self.Population[index] = groupB[0]
    #         # self.log.log_this("mutation_Phase2",mutation_factor,self.eta_now,1)


    def Normalize(self):
        print("\t Normalize of {0}".format(len(self.Population)))
        for index,dna in enumerate(self.Population):
            # f_updated = False
            # for k in range(10):
            dna = self.Population[index]
            for row,Row in enumerate(self.get_map(dna)):
                for col,element in enumerate(Row):
                    building = element.get("Building")

                    if building == "Out_of_markers"\
                    or building == "Replace"\
                    or building == "None"\
                    or building == "Unused_Home_piece":
                        self.Population[index][row*27+col] = self.MAP_NUM.get("Path")
                        # f_updated = True

                    elif building == "Path" and element.get("Reach") == False:
                        self.Population[index][row*27+col] = self.MAP_NUM.get("Home")
                        # print(row,col,self.Population[index][row*27+col])
                        # f_updated = True


                # if f_updated == False:
                #     break
        self.fitness()


    def print_unit(self,index=0,spacing=5):
        self.sort()
        text = "\n Score= "+str(self.Score[index][0])
        line = ""

        for row in range(self.ROWS):
            line=""

            for col in range(self.COLUMNS):
                line += (k*spacing-len(line))*" "
                line += str(self.Population[index][row*self.ROWS+col])

            text += "\n"+line
        print(text)


    def plot_map(self,index=0,block=True):
        # print("Len =",len(self.Population))
        Map = self.get_map(self.Population[index])
        plt.clf()

        for row,Row in enumerate(Map):
            for col,element in enumerate(Row):
                # X.append(col)
                # Y.append(row)
                building = element.get("Building")
                if building == "Path":
                    marker = "."
                    if element.get("Reach") == True:
                        color = "white"
                    else:
                        color = "red"
                elif building == "Home" or building == "Good_Home_piece":
                    marker = "s"
                    if element.get("Reach")==True and element.get("Power")==True:
                        color = "green"
                    elif element.get("Reach")==True:
                        color = "blue"
                    elif element.get("Power")==True:
                        color = "black"
                    else:
                        color = "red"

                elif building == "Bank":
                    marker = "*"
                    if element.get("Reach")==True and element.get("Power")==True:
                        color = "green"
                    elif element.get("Reach")==True:
                        color = "blue"
                    elif element.get("Power")==True:
                        color = "black"
                    else:
                        color = "red"

                elif building == "Tesla":
                    marker = "^"
                    color = "blue"
                elif building == "Unused_Home_piece":
                    marker ="*"
                    if element.get("Reach")==True:
                        color = "red"
                    else:
                        color = "purple"
                else:
                    print("Missing building ({building}) gen = {gen}".format(\
                    gen=self.Population[index][row*27+col],building=building))
                    marker = "x"
                    color = "red"
                # Marker.append(marker)
                # Color.append(color)
                plt.scatter(col,-row,marker=marker,c=color,s=50)
        plt.title(self.run_id+"\nETA = {0}\
        \nScore = {1}".format(self.eta_now,self.Score[index][0]))
        # output_file = "D:\Python_64\City_Plan/2step_pics/"+str(self.run_id)+"_score_{0}"\
        # .format(self.Score[index][0])+".png"
        output_file = "D:\Python_64\City_Plan/2step_pics/Eta_{eta}_score_{score}"\
        .format(eta=self.eta_now,score=self.Score[index][0])+".png"
        plt.savefig(output_file)
        if block == True:
            plt.show()



    def print_map(self,index=0,spacing=3):

        text = "\n Score= "+str(self.Score[index][0])
        line = ""
        Map = self.get_map(self.Population[0])

        for row,Row in enumerate(Map):
            line=""

            for col,element in enumerate(Row):
                line += (col*spacing-len(line))*" "
                building = element.get("Building")
                if building == "Path":
                    line += "."
                elif building == "Home" or building == "Good_Home_piece":
                    line += "H"
                elif building == "Tesla":
                    line += "T"
                elif building == "Bank":
                    line += "B"
                else:
                    line += "X"
                # line += str(Element)

            text += "\n"+line
        print(text)


    def print_path(self,index=0,spacing=3):

        text = "\n Score= "+str(self.Score[index][0])
        line = ""
        Map = self.get_map(self.Population[0])

        for row,Row in enumerate(Map):
            line=""

            for col,element in enumerate(Row):
                line += (col*spacing-len(line))*" "
                if element.get("Reach") == True:
                    line += "."
                else:
                    line += "x"
                # line += str(Element)

            text += "\n"+line
        print(text)


    def print_power(self,index=0,spacing=3):

        text = "\n Score= "+str(self.Score[index][0])
        line = ""
        Map = self.get_map(self.Population[0])

        for row,Row in enumerate(Map):
            line=""

            for col,element in enumerate(Row):
                line += (col*spacing-len(line))*" "
                if element.get("Power") == True:
                    line += "P"
                else:
                    line += "x"
                # line += str(Element)

            text += "\n"+line
        print(text)


    def print2_all(self,spacing=5,score_offset=5):

        line = ""
        text = ""

        for n in range(self.N):
            line = str(self.Score[n][0])+' '
            line += (score_offset+-len(line)-1)*" "
            line += "|"

            for k in range(self.MAP_LEN):
                line += (score_offset+k*spacing-len(line))*" "
                line += str(self.Population[n][k])
            text += "\n"+line

        print(text)


    def refill(self):
        missing_population = self.UNITS-len(self.Population)
        print("\tRefil {0}".format(missing_population))
        for n in range(missing_population):

            dna = []


            for m in range(self.MAP_LEN):
                    # dna.append(random.randrange(self.BORN_RANGE))
                    dna.append(round(random.random()*2))

            self.Population.append(dna)
            # self.Score.append([-1])
            self.Score.append( self.calculate_score( dna ))


    def save(self):
        self.sort()
        np.savetxt("D:\Python_64\City_Plan\Last_leader_2step.csv",\
        self.Population[0],delimiter =";",fmt="%s")
        np.savetxt("D:\Python_64\City_Plan\Last_eta.csv",\
        [self.eta_now,self.eta_now],fmt="%s")
        self.plot_map(block=False)
        # for s in range(10,16):
        # 	winsound.Beep(s*150+500,35)

    def select(self,select_ratio = 0.65):
        self.sort()
        if select_ratio>len(self.Population):
            n = len(self.Population)

        elif select_ratio >= 1:
            n = int(select_ratio)

        elif (select_ratio<1 and select_ratio>0):
            n = int(int(select_ratio*self.UNITS))

        else:
            select_ratio = 0.5
            n = int(int(q*self.UNITS))


        y = []
        sc = []

        for i in range(n):
            T = []
            #print("LenAttr = {0},LenItems = {1}".format(len(self.COLUMNSttr),
            #len(self.Population)))
            for l in range(self.MAP_LEN):
                T.append(self.Population[i][l])

            y.append(T)
            sc.append(self.Score[i])

        self.Population = y
        self.Score = sc


    def shake(self,force=10, chance=0.1):
        '''Shake function '''
        for i,Dna in enumerate(self.Population):
            dna = []
            for i2,gen in enumerate(Dna):

                if chance>=random.random():
                    gen += round(random.random()*2*force-force)

                dna.append(gen)
            score = self.calculate_score(dna)

            if score[0] > self.Score[i][0]:
                self.Score[i] = score
                self.Population[i] = dna
                # self.log.log_this("shake",chance,self.eta_now,1)


    def sort(self):
        y = []
        sc = []

        if self.f_sorted == 0:
            # self.fitness()
            y.append(copy(self.Population[0]))
            sc.append(self.Score[0])

            for n in range(1,len(self.Population)):
                T = copy(self.Population[n])

                for j in range(n):

                    if (self.Score[n][0] > sc[j][0]):
                        sc.insert(j,self.Score[n])
                        y.insert(j,T)
                        break

                if (len(sc) <= n):
                    sc.append(self.Score[n])
                    y.append(T)

            self.f_sorted = 1
            self.Population = y
            self.Score = sc

    # def sort_group(self,T,SC):
    #     _T = [T[0]]
    #     _SC = [SC[0]]
    #     for n in range(1,len(T)):
    #
    #         for j in range(n):
    #             if (SC[n][0] > _SC[j][0]):
    #                 _SC.insert(j,SC[n])
    #                 _T.insert(j,T[n])
    #                 break
    #
    #         if (len(_SC) <= n):
    #             _SC.append(SC[n])
    #             _T.append(T[n])
    #
    #     for n in range(len(_SC)):
    #         T[n] = _T[n]
    #         SC[n] = _SC[n]


    def train(self,eta=10000,break_time=200,select_rate=0.5,shake_force=5,\
                shake_chance=0.01,mutation_factor=0.01,\
                mutants_density=0.25):
        # try:
        #     self.Normalize()
        #     # self.fitness()
        #     leader = self.Score[0][0]
        # except IndexError:
        leader = 0

        # print("Train started. Training ETA = {eta}, Units = {units}".format(\
        #                                     eta=eta,units=self.UNITS))
        self.refill()

        # print(self.eta_now)


        for i in range(self.eta_now+1,eta+1+self.eta_now):
            self.eta_now = i
            print("Training {units} units. Leader = {score}, Eta = {eta}".format(\
                    units=self.UNITS,score=self.Score[0][0],eta=self.eta_now))
            self.refill()
            self.change_dna(number= 2, times= 3)
            self.change_dna(number= 10,times= 2)
            for k in range(10):
                self.Map_Mutation(row=10,col=10)
                self.Map_Mutation(row=15,col=15)
            self.sort()
            self.select()
            self.Normalize()
            # self.insert_home()

            # time_sort += math.floor(time.time()*1000) - time_now
            # if i%500 ==0:
            #     self.insert_home()
            #     winsound.Beep(150+500,155)
            self.save()

        self.save()
        print("\t Train finshed. Score = {score}".format(\
                eta=self.eta_now,score=self.Score[0][0]))



cls()
baza = CGenetic("Both",columns=27,rows=27,UNITS=500)


for k in range(100):
    baza.insert_home()
    baza.train(eta=100)
    # baza.change_dna()
# baza.insert_home()
# baza.print_map()
# baza.print_power()

# baza.train(eta=1)

baza.fitness()
baza.sort()
baza.save()

execute_hour = math.floor(time.clock()/(60*60))%24
execute_min = math.floor((time.clock()/60)%60)
execute_sec = math.floor(time.clock()%(60))

print("Excecution Time = {h}h:{m}m:{s}s".format(h=execute_hour,m=execute_min,\
                                              s=execute_sec))

print("\nFinal Eta = {}".format(baza.eta_now))

baza.plot_map()




input("Press Enter.....\n")
