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

days = 60





avgpcttest = .5
straighttest = 1
buytest = 100
winner = 1
mintest = 15

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
    num_files = len(file_list) - 1
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
                        p.append(int(float(row[j])* 10000))
                    except:
                        pass
                    t.append(row[j + 1])
                    b = []
                    for n in range(0, j):
                        try:
                            b.append(int(float(row[n])*10000))
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


            EE = np.array(Entry_data)
            PP = np.array(Price_data)
            TT = np.array(Time_data)
            #
            ED.append(EE)
            PD.append(PP)
            TD.append(TT)
            #
            #ED.append(Entry_data)
            #PD.append(Price_data)
            #TD.append(Time_data)


    return PD, ED, TD


def compute(  Agent, Price_Data, Entry_Data, Time_Data):
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


    length = len(Price_Data)



    for K in range(0,len(Entry_Data)):
        Etemp = (Entry_Data[K].astype(float))/10000
        Ptemp = (Price_Data[K].astype(float))/10000
        #
        EEntry_Data = Etemp.tolist()
        PPrice_Data = Ptemp.tolist()
        TTime_Data = Time_Data[K].tolist()
        #
        #EEntry_Data = Entry_Data[K]
        #PPrice_Data = Price_Data[K]
        #TTime_Data = Time_Data[K]


        #EEntry_Data = Etemp
        #PPrice_Data = Ptemp
        #TTime_Data = Time_Data[K]





        for q, Entry in enumerate(EEntry_Data):




            ii = len(Entry)
            price = PPrice_Data[q]
            tyme = TTime_Data[q]
            t = re.split(':', tyme)
            hour = int(t[0])
            minute = int(t[1])



            if (hour == 14 and minute == 59) and newday == 0:
                day = day + 1
                newday = 1
            if newday == 1 and (hour != 14 or minute != 59):
                newday = 0







            stockval = 0
            numPos = 0
            qualifies = [1] * 20
            for y,signal in enumerate(Entry):


                for i, strat  in enumerate(strats):
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




                if (qualifies[y] == 1) and (((signal[15] - signal[16]) / price[y]) < .003) and (Pos[y] == 0) and (hour != 14 or minute != 59) and (hour != 8 or minute != 30):
                    try:
                        numshare = 25 // signal[9]
                    except:
                        print()
                    if numshare == 0:
                        numshare = 1
                    Bal = Bal - (numshare * price[y])

                    Pos[y] = numshare
                    Entry_Price[y] = price[y]
                    Ins = Ins + 1

                    stop_loss[y] = price[y] - (signal[9] * sellstrat[0])
                    mark_up[y] = price[y] + (signal[9] * sellstrat[1])

                if Pos[y] > 0:
                    if (price[y] > mark_up[y]) or (price[y] < stop_loss[y]) or (hour == 14 and minute == 59):
                        if qualifies[y] == 1:
                            stop_loss[y] = price[y] - (signal[9] * sellstrat[0])
                            mark_up[y] = price[y] + (signal[9] * sellstrat[1])
                        else:
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
    for n in range(0,len(fullarray)):
        if Ins > 0:
            factor = 22000 / maxspend
        else:
            factor = 0
        if fullarray[n] * factor < mintest * n:
            strikes = strikes + 1
    minline = 1 - strikes/len(fullarray)
    straight = findstraight(fullarray)
    fitscore = min(1, avgpercent / avgpcttest) * min(1, straight / straighttest) * min(1, ((Ins / days) / buytest)) * minline

    return [avgpercent, straight, Ins, minline, fitscore]






def genstrats( original):
    strats = []
    strats.append(original)
    strats1 = []
    for m in range(0,25):
        for n in range(0,25):
            newstrat = [[[m/10,n/10]] + original[0][1:],[0,0,0,0,0]]
            strats1.append(newstrat)
    strats.extend(strats1)

    strats2 = []
    for m in range(0,15):
        k = m
        if m ==0  or m == 10 or m == 16 or m == 17:
            k = k + 1
        for n in range(-1,2):
            newstrat = [original[0][:k] + [n] + original[0][k+1:],[0,0,0,0,0]]
            strats2.append(newstrat)
    strats.extend(strats2)

    strats3 = []
    for m in range(0,3):
        for n in range(0,61):
            if n == 60:
                rsi = 0
            elif n < 30:
                rsi = 70 - n
            elif n >= 30:
                rsi = -70 + n - 30
            newstrat = [original[0][:m+18] + [rsi] + original[0][m+18+1:],[0,0,0,0,0]]
            strats3.append(newstrat)
    strats.extend(strats3)
    return strats





def fitness( agents, PD, ED, TD):
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
        print("METRIC: ", round(agent[1][4], 3), "    ", "   avgpercent: ",round(agent[1][0], 3), "    straightness: ", round(agent[1][1], 3), "     Bpd: ", agent[1][2]/days,"      Minline: ", agent[1][3], "     ", agent[0])
    return agents




PD, ED, TD = makearray()
original = [[[0.51, 0.54], -1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -66, 0], [0, 0, 0,0,0]]


flag = 1

while(flag == 1):
    strats  = genstrats(original)
    strats = fitness(strats, PD, ED, TD)
    strats = selection(strats)
    best = strats[0][1][4]
    if best > original[1][4]:
        original =strats[0]
    else:
        flag = 0
print("COMPLETED")
print(original, "     is the best")