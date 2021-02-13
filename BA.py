import random
import string
import time
import csv
import re
import os, os.path
import math
import random
import matplotlib.pyplot as plt
from multiprocessing import Process, Manager, Lock
import numpy as np

path = 'C:/Users/shiva/PycharmProjects/BotTest'
files = os.listdir(path)
file_list =[]
for n in range(0,len(files)):
    if files[n].endswith('.csv'):
        file_list.append(files[n])
file_list.sort()
num_files = len(file_list) - 2








allexit = 1
allrsi = 1
days = 80

avgpcttest = .15
straighttest = .2
bpdtest = 100
winner = 1
mintest = 5


population = 1
generations = 1


def findstraight( x):
    straightness = 0
    for n in range(0, len(x) - 1):
        q = math.sqrt((-1) ** 2 + (x[n] - x[n + 1]) ** 2)
        straightness = straightness + q
    straight = straightness
    p = math.sqrt((len(x)**2) + (x[-1]**2))
    straight = p/straight
    return straight

def makearray():
    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    files = os.listdir(path)
    file_list =[]
    for n in range(0,len(files)):
        if files[n].endswith('.csv'):
            file_list.append(files[n])
    file_list.sort()
    rettot = 0
    ED = []
    PD = []
    TD = []


    for day in range (0,days):

        EE = np.array([],dtype=int)
        PP = np.array([],dtype=int)
        TT = np.array([])

        Entry_data = []
        Price_data = []
        Symbol_data = []
        Time_data = []

        sellrow = 0
        counter = 0
        shift = 0
        i = 0
        j = 0

        path = 'C:/Users/shiva/PycharmProjects/BotTest'
        filename = path + '/' + str(file_list[day])

        print("Reading ", str(file_list[day])," Day ", day + 1, " of ", days)
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            aa = 0
            for row in readCSV:
                if aa == 0:
                    aa = 1
                    continue
                if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                    i = i + 1
                    j = len(row) - 3
                else:
                    break
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            p = []
            a = []
            t = []
            for row in readCSV:
                # print(counter)
                if counter == 0:
                    counter = counter + 1
                    continue
                counter = counter + 1
                if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                    sellrow = counter + 1

                if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":
                    try:
                        p.append((float(row[j])))
                    except:
                        pass
                    t.append(row[j + 1])
                    b = []
                    for n in range(0, j):
                        try:
                            b.append((float(row[n])))
                        except:
                            b.append(row[n])
                    try:
                        a.append(b)
                    except:
                        pass
                else:
                    Price_data.append(p)
                    Entry_data.append(a)
                    Symbol_data.append(t)

                    try:
                        Time_data.append(row[1])
                    except:
                        print()
                    p = []
                    a = []
                    t = []




            ED.append(np.array(Entry_data))
            PD.append(np.array(Price_data))
            TD.append(np.array(Time_data))

            #ED.append(Entry_data)
            #PD.append(Price_data)
            #TD.append(Time_data)


    return PD, ED, TD

def compute( Agent,  Price_Data,  Entry_Data,  Time_Data):
    prevhour = 0
    day = 0
    newday = 0
    fflag = 0
    fullarray = []
    buy_in = [0] * 24
    PL = 0
    Hourly_PL = [0] * 7
    Bal = 0
    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = [0] * 20
    mark_up = [0] * 20
    stop_loss = [0] * 20
    Entry_Price = [0] * 20
    Recent_Exit = [1] * 20
    hourly = [0] * 24
    totdiff = 0
    avgpercent = 0
    times_entered = [0] * 20
    sellstrat = Agent[0]
    strats = Agent[1:]
    strikes = 0


    for K in range(0,len(Entry_Data)):
        #Etemp = (Entry_Data[K].astype(float))/10000
        #Ptemp = (Price_Data[K].astype(float))/10000





        EEntry_Data = Entry_Data[K].tolist()
        PPrice_Data = Price_Data[K].tolist()
        TTime_Data = Time_Data[K].tolist()

        #EEntry_Data = Entry_Data[K]
        #PPrice_Data = Price_Data[K]
        #TTime_Data = Time_Data[K]








        for q, Entry in enumerate(EEntry_Data):




            ii = len(Entry)
            price = PPrice_Data[q]
            tyme = TTime_Data[q]
            t = re.split(':', tyme)
            hour = int(t[0])
            minute = int(t[1])


            qualifies = [1] * 20
            for y,signal in enumerate(Entry):
                for i, strat in enumerate(strats):
                    if strat == 0:
                        continue
                    if i != 8 and i != 14 and i != 17 and i != 18 and i != 19 and i != 20:
                        if (signal[i] * strat <= 0):
                            qualifies[y] = 0
                            break
                    if i == 8 or i == 14 or i == 20:
                        if((signal[i] - price[y]) * strat <= 0):
                            qualifies[y] = 0
                            break
                    if i == 17 or i == 18 or i == 19:
                         if (strat/abs(strat)) * signal[i] < strat:
                            qualifies[y] = 0
                            break


            stockval = 0
            numPos = 0
            for y,signal in enumerate(Entry):







                if (qualifies[y] > 0) and (((signal[15] - signal[16]) / price[y]) < .003) and (Pos[y] == 0) and (hour != 14 or minute != 59) and (hour != 8 or minute != 30):
                    numshare = 9 // signal[9]
                    if numshare == 0:
                        numshare = 1
                    Bal = Bal - (numshare * price[y])

                    Pos[y] = numshare
                    Entry_Price[y] = price[y]
                    Ins = Ins + 1
                    stop_loss[y] = price[y] - (signal[9] * sellstrat[0])
                    mark_up[y] = price[y] + (signal[9] * sellstrat[1])
                    times_entered[y] = 0
                if Pos[y] > 0:
                    if (price[y] < stop_loss[y]) and (times_entered[y] < 12):
                        stop_loss[y] = stop_loss[y] - (signal[9])
                        numshare = Pos[y] // 7
                        Entry_Price[y] = (Entry_Price[y] * Pos[y] + price[y] * numshare) / (Pos[y] + numshare)
                        Bal = Bal - (numshare * price[y])
                        Pos[y] = Pos[y] + numshare

                        times_entered[y] = times_entered[y] + 1
                        Ins = Ins + 1
                    if (price[y] > mark_up[y]) or (hour == 14 and minute == 59):
                            returnval = Pos[y] * price[y]

                            Bal = Bal + returnval
                            diff = price[y] - Entry_Price[y]
                            diff = diff / Entry_Price[y]
                            totdiff = totdiff + diff
                            avgpercent = 100 * totdiff / Ins
                            if price[y] > Entry_Price[y]:
                                win = win + 1
                                wintot = wintot + (Pos[y] * price[y] - Pos[y] * Entry_Price[y]) / (Entry_Price[y])
                                winav = wintot / win
                            else:
                                lose = lose + 1
                                losstot = losstot + (Pos[y] * Entry_Price[y] - Pos[y] * price[y]) / (
                                Entry_Price[y])
                                lossav = losstot / lose

                            Entry_Price[y] = 0
                            Pos[y] = 0
                            Recent_Exit[y] = 1
                            buy_in[y] = 0

                stockval = Pos[y] * price[y] + stockval
                if Pos[y] > 0:
                    numPos = numPos + 1
            if stockval > maxspend:
                maxspend = stockval
            PL = Bal + stockval
            Hourly_PL[hour - 8] = PL

            if hour != prevhour:
                prevhour = hour
                fullarray.append(PL)

            # if minute == 59 and fflag == 0:
            #     fullarray.append(PL)
            #     fflag = 1
            # if minute != 59:
            #     fflag = 0

    fullarray.append(PL)
    # plt.plot(fullarray)
    for n in range(0,len(fullarray)):
        if Ins > 0:
            factor = 22000 / maxspend
        else:
            factor = 0
        if fullarray[n] * factor < mintest * n:
            strikes = strikes + 1
    minline = 1 - strikes/len(fullarray)
    straight = findstraight(fullarray)
    fitscore = min(1, avgpercent / avgpcttest) * min(1, straight / straighttest) * min(1, ((Ins / days) / bpdtest)) * minline



    return [avgpercent, straight, Ins, minline, fitscore]





def genstrats( popsize):


    strats = [[[],[]]] * popsize
    for n in range(0,popsize):
        strat = [0] * 22
        for m in range(0,len(strat)):
            if m == 0:
                if allexit == 1:
                    strat[0] = [round(random.uniform(0.2,2.0),2), round(random.uniform(0.2,2.0),2)]
                else:
                    rand = random.randint(0,7)
                    if rand == 0:
                        strat[0] = [.5,.5]
                    if rand == 1:
                        strat[0] = [1,.5]
                    if rand == 2:
                        strat[0] = [.5,1]
                    if rand == 3:
                        strat[0] = [1,1]
                    if rand == 4:
                        strat[0] = [1.5,.5]
                    if rand == 5:
                        strat[0] = [.5,1.5]
                    if rand == 6:
                        strat[0] = [2,1]
                    if rand == 7:
                        strat[0] = [1,2]
            if m != 0 and m != 10  and m != 16 and m != 17 and m != 18 and m != 19 and m != 20:
                strat[m] = random.randint(-1,1)
            if m == 10 or m == 16 or m == 17:
                strat[m] = 0
            if m == 18 or m == 19 or m == 20:
                if allrsi == 1:
                    if random.randint(0,1):
                        strat[m] = random.randint(-70,-30)
                    else:
                        strat[m] = random.randint(30,70)
                else:
                    rand =random.randint(0,5)
                    if rand == 0:
                        strat[m] = -40
                    if rand == 1:
                        strat[m] = -50
                    if rand == 2:
                        strat[m] = -60
                    if rand == 3:
                        strat[m] = 40
                    if rand == 4:
                        strat[m] = 50
                    if rand == 5:
                        strat[m] = 60


        avgpercent = 0
        straightness = 0
        buys = 0
        minline = 0
        fitscore = 0

        strats[n] = [strat,[avgpercent,straightness, buys, minline, fitscore]]
    return strats













def ga():
    agents = init_agents(population)
    agents[0] = [[[2,2],0,0,1,1,1,1,1,0,-1,0,0,0,-1,1,0,0,0,0,0,0,0], [0, 0, 0,0]]




    PD, ED, TD = makearray()
    print("READ ALL FILES")


    for generation in range(generations):

        print('Generation: ' + str(generation))

        agents = fitness(agents, PD, ED, TD)
        for agent in agents:
            if agent[1][4] >= winner:
                print('Threshold met!')
                agents.sort(key=lambda x: x[1][4], reverse=True)
                for agent in agents:
                    print("METRIC: ", round(agent[1][4], 3), "    ", "   avgpercent: ",round(agent[1][0], 3), "    straightness: ", round(agent[1][1], 3),  "Buys: ", agent[1][2] ,"     BpD: ", agent[1][2]//days,"      Minline: ", agent[1][3], "     ", agent[0])
                exit(0)

        agents = selection(agents)
        agents = crossover(agents)
        #agents = mutation(agents)



def init_agents( population):
    # return [Agent(length) for _ in range(population)]
    a = genstrats(population)
    return a

def fitness( agents,  PD,  ED,  TD):

    starttime = time.time()
    for n in range(0,len(agents)):
        tarttime = time.time()
        agents[n] = [agents[n][0],compute(agents[n][0], PD, ED, TD)]
        print('Completed ',n,' of ',len(agents), 'in {} seconds'.format(time.time()-tarttime))
    print('That took {} seconds'.format(time.time() - starttime))
    return agents




def selection( agents):
    agents.sort(key=lambda x: x[1][4], reverse=True)
    for agent in agents:
        print("METRIC: ", round(agent[1][4], 3), "    ", "   avgpercent: ",round(agent[1][0], 3), "    straightness: ", round(agent[1][1], 3), "Buys: ", agent[1][2] ,"     BpD: ", agent[1][2]//days,"      Minline: ", agent[1][3], "     ", agent[0])
    agents = agents[:int(0.2 * len(agents))]

    return agents



def crossover( agents):

    for _ in range((population - len(agents))//2):
        flag = 1
        while(flag == 1):
            flag = 0
            children = []
            parent1 = random.choice(agents)
            if len(agents) > 1:
                parent2 = random.choice(agents)
                while (parent2 == parent1):
                    parent2 = random.choice(agents)
            # child1 = Agent(in_str_len)
            # child2 = Agent(in_str_len)
            child1 = [[],[]]
            child2 = [[],[]]
            split = random.randint(0, len(parent1[0]))
            #child1[0] = parent1[0][0:split] + parent2[0][split:]
            #child2[0] = parent2[0][0:split] + parent1[0][split:]

            for n in range(0,len(parent1[0])):
                if n == 0:
                    if random.randint(0,1):
                        child1[0].append([parent1[0][n][0],parent2[0][n][1]])
                    else:
                        child1[0].append([parent2[0][n][0],parent1[0][n][1]])
                else:
                    if random.randint(0,1):
                        child1[0].append(parent1[0][n])
                    else:
                        child1[0].append(parent2[0][n])


                if n == 0:
                    if random.randint(0,1):
                        child2[0].append([parent1[0][n][0],parent2[0][n][1]])
                    else:
                        child2[0].append([parent2[0][n][0],parent1[0][n][1]])
                else:
                    if random.randint(0,1):
                        child2[0].append(parent1[0][n])
                    else:
                        child2[0].append(parent2[0][n])


            child1[1] = [0,0,0,0,0]
            child2[1] = [0,0,0,0,0]

            children.append(child1)
            children.append(child2)
            children = mutation(children)
            child1 = children[0]
            child2 = children[1]

            if child1 == child2:
                flag = 1
            for n in range(0,len(agents)):
                if child1[0] == agents[n][0] or child2[0] == agents[n][0]:
                    flag = 1


        agents.append(child1)
        agents.append(child2)
    return agents



def mutation( agents):

    for agent in agents:

        # for idx, param in enumerate(agent.string):
        #
        #     if random.uniform(0.0, 1.0) <= 0.1:
        #
        #         agent.string = agent.string[0:idx] + random.choice(string.ascii_letters) + agent.string[idx+1:in_str_len]

        for m in range(0,len(agent[0])):
            if m == 0:
                if allexit == 1:
                    if random.uniform(0.0,1.0) <= 0.2:
                        agent[0][0] = [round(random.uniform(0.2, 2.0),2), agent[0][0][1]]
                    if random.uniform(0.0,1.0) <= 0.2:
                        agent[0][0] = [agent[0][0][0], round(random.uniform(0.2, 2.0),2)]
                else:
                    rand = random.randint(0,7)
                    if rand == 0:
                        agent[0][0] = [.5,.5]
                    if rand == 1:
                        agent[0][0] = [1,.5]
                    if rand == 2:
                        agent[0][0] = [.5,1]
                    if rand == 3:
                        agent[0][0] = [1,1]
                    if rand == 4:
                        agent[0][0] = [1.5,.5]
                    if rand == 5:
                        agent[0][0] = [.5,1.5]
                    if rand == 6:
                        agent[0][0] = [2,1]
                    if rand == 7:
                        agent[0][0] = [1,2]


            else:
                if random.uniform(0.0,1.0) <= 0.1:
                    if m == 0:
                        agent[0][0] = [round(random.uniform(0.2, 2.0),2), round(random.uniform(0.2, 2.0),2)]

                    if m != 0 and m != 10 and m != 16 and m != 17 and m != 18 and m != 19 and m != 20:
                        agent[0][m] = random.randint(-1, 1)

                    if m == 10 or m == 16 or m == 17:
                        agent[0][m] = 0
                    if m == 18 or m == 19 or m == 20:
                        if allrsi == 1:
                            if random.randint(0,1):
                                agent[0][m] = random.randint(-70, -30)
                            else:
                                agent[0][m] = random.randint(30, 70)
                        else:
                            rand =random.randint(0,5)
                            if rand == 0:
                                agent[0][m] = -40
                            if rand == 1:
                                agent[0][m] = -50
                            if rand == 2:
                                agent[0][m] = -60
                            if rand == 3:
                                agent[0][m] = 40
                            if rand == 4:
                                agent[0][m] = 50
                            if rand == 5:
                                agent[0][m] = 60



    return agents


if 1:
    ga()
