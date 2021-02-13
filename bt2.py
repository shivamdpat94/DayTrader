import tensorflow as tf  # deep learning library. Tensors are just multi-dimensional arrays
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import time
from datetime import date
from datetime import datetime
import calendar
import csv
import re
import os.path
import matplotlib.pyplot as plt
import requests
import tosdb
import urllib
from xlwings import Book, Range
from splinter import Browser
import numpy as np
import random
og =1
days = 1
newman = 0
st = .25
ma = .25
loockback = 0

starttime = time.time()
Stocks = ["UDOW", "SDOW", "LABD", "LABU", "GUSH", "DRIP", "SQQQ", "TQQQ", "FAZ", "FAS", "JDST", "JNUG", "KOLD", "BOIL","UPRO","SPXU","NUGT","DUST","SRTY","URTY"]
Numstocks = len(Stocks)







buy_in = [0] * Numstocks
PL = 0
Bal = 0
Hourly_PL = [0] * 24
# PerStock = [[[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
#                 [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
#                 [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
#                 [[], 0, ["BUY"], ["SELL"]],[[], 0, ["BUY"], ["SELL"]],[[], 0, ["BUY"], ["SELL"]],[[], 0, ["BUY"], ["SELL"]],[[], 0, ["BUY"], ["SELL"]] ]
win = 0
winav = 0
wintot = 0
lose = 0
lossav = 0
losstot = 0
Ins = 0
maxspend = 0
numPos = 0
RealPos = [0] * Numstocks
CurrPos = [0] * Numstocks
Pos = [0] * Numstocks
mark_up = [0] * Numstocks
stop_loss = [0] * Numstocks
Entry_Price = [0] * Numstocks
Recent_Exit = [1] * Numstocks
full_replay_arr = [0]
totdiff = 0
avgpercent = 0
avgwin = 0
fullbal = 0
times_entered = [0] * Numstocks
avgatr = 0
Enter = [0] *20
buyhour = [0] *20
losshour = [0] *7
winhour = [0] * 7
percenthour = [0] * 7
active = 0
minmax = [0] * 20
logcount = 0
goodbuy = 0
failbuy = 0
goodsell = 0
failsell = 0
fails = 0
CurrNumPos = 0
CurIns = 0
tologbuy = [[]] * Numstocks
tologsell = [[]] * Numstocks
BIGERROR = 0
transaction = 0
trans = [0] * Numstocks
Whiletryerror = 0
h = 0

buy_timer = [0] * Numstocks
unfilled_buy = [0] * Numstocks
unfilled_sell = [0] * Numstocks
Sell_timer = [0] * Numstocks
sellstat = [0] * Numstocks

def correct():
    # top = random.uniform(-.25,-.4)
    top = 1
    bottom = random.uniform(.25,.4)
    # top = -.3
    # bottom = -.3

    arr = [0] * 100


    a = random.randint(15,20)
    b = random.randint(30,35)
    c = random.randint(45,50)
    d = random.randint(60,65)
    e = random.randint(75,80)
    f = random.randint(90,95)
    #

    aa = random.uniform(.20,.20)
    bb = random.uniform(.30,.30)
    cc = random.uniform(.40,.40)
    dd = random.uniform(.50,.50)
    ee = random.uniform(.60,.60)
    ff = random.uniform(.70,.70)
    gg = random.uniform(.8,.8)
    arr[0:a] = np.linspace(0,aa,a,endpoint=False)
    arr[a:b] = np.linspace(aa,bb,b-a,endpoint=False)
    arr[b:c] = np.linspace(bb,cc,c-b, endpoint=False)
    arr[c:d] = np.linspace(cc,dd,d-c, endpoint=False)
    arr[d:e] = np.linspace(dd,ee,e-d, endpoint=False)
    arr[e:f] = np.linspace(ee,ff,f-e, endpoint=False)
    arr[f:101] = np.linspace(ff,gg,99-f+1, endpoint=False)
    arr =  np.array(arr)

    return arr


arr  = correct()
lower = arr - .2
upper = arr + .2
five = 5
def to255(arr):
    array = []
    for n in range(0,len(arr)):
        a = np.zeros((100,101))
        for m in range(0,100):
            try:
                a[m][int(arr[n][m]*100)] = 255
            except:
                ddd = 4
        array.append(np.ndarray.flatten(a))
    return array
def expand(arr):
    b = [0] * 100
    for i in range(0, len(arr) - 1):
        b[int(i * (len(b) / (len(arr) - 1))):int((i + 1) * (len(b) / (len(arr) - 1)))] = np.linspace(arr[i], arr[i + 1], int(len(b) / len(arr) + 1), endpoint=False)

    b = np.array(b)
    # b = np.array(b)
    b = b - min(b)
    b = b / max(b)
    return b


# model1 = keras.models.load_model('C:/Users/shiva/PycharmProjects/PriceAction/mymodel')
#
model = keras.models.load_model('C:/Users/shiva/PycharmProjects/Tensorflow/mymodel')


file_list = ([name for name in os.listdir('.') if os.path.isfile(name)])
num_files = len([name for name in os.listdir('.') if os.path.isfile(name)]) - 2


actuallogdate = "C:/Users/shiva/PycharmProjects/BotTest/log/%s-log-actual.csv" % date.today()
theorylogdate = "C:/Users/shiva/PycharmProjects/BotTest/log/%s-log-theory.csv" % date.today()
mergelogdate = "C:/Users/shiva/PycharmProjects/BotTest/log/%s-log-merge.csv" % date.today()

for nn in range(0, days):
    mydate = file_list[nn]
    a = str(mydate)
    filename = a
    Entry_data = []
    Price_data = []
    Symbol_data = []
    Input_data = []
    Time_data = []
    Min_data = []
    Price_by_min = []
    currmin = 0
    sig = [0] * 20
    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0

    # reads replay data
    if 1:
        print("reading", mydate)
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            a = 0
            for row in readCSV:
                if a == 0:
                    a = 1
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
            aa = []
            newmins = 0
            ccount=0
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
                        p.append(float(row[j]))
                    except:
                        pass
                    t.append(row[j + 1])
                    b = []
                    for n in range(0, j+1):
                        try:
                            b.append(float(row[n]))
                        except:
                            b.append(row[n])
                    try:
                        a.append(b)
                        if newmins >= newman:
                            manbat = []
                            for x in range(0,newman):
                                if og == 1:
                                    manbat.extend(Min_data[newmins-(newman-x)][ccount])
                                else:
                                    manbat.append(Min_data[newmins-(newman-x)][ccount])
                            if og == 1:
                                manbat.extend(b)
                            else:
                                manbat.append(b)
                            aa.append(manbat)

                    except:
                        pass
                    ccount = ccount+1

                else:
                    ccount = 0
                    Price_data.append(p)
                    Entry_data.append(a)
                    if newmins >= newman:
                        Input_data.append(aa)
                    Symbol_data.append(t)
                    ttime = re.split(':', row[1])
                    ttime[0] = int(ttime[0])
                    ttime[1] = int(ttime[1])
                    Time_data.append(ttime)
                    if currmin != ttime[1]:
                        Min_data.append(a)
                        currmin = ttime[1]
                        newmins = newmins + 1
                        Price_by_min.append(p)

                    p = []
                    a = []
                    t = []
                    aa = []
                    #if len(Entry_data) > 5000:
                    #    break
        Entry_data = Entry_data[len(Entry_data) - len(Input_data):]
        Price_data = Price_data[len(Price_data) - len(Input_data):]
        Time_data = Time_data[len(Time_data) - len(Input_data):]
        e = np.array(Input_data)
        ee = np.concatenate(e)
        if og == 0:
            ee = ee.swapaxes(1,2)
        ee = ee/ee[:,[-1]]
        prediction = model.predict(ee).argmax(axis=1)
        print("read", mydate)  #

    onetime = 0
    # while 1:
    #     try:
    onetime2 = 0
    auth_factor = 0
    loop_counter = 0
    xxx = 0
    minspassed = 'na'
    mincounter=0
    Price_by_min = np.array(Price_by_min)
    Price_by_min = Price_by_min.swapaxes(0, 1)
    predd = [1] * i
    while 1:
        # print(xxx)
        mydate = date.today()
        today = calendar.day_name[mydate.weekday()]
        now = datetime.now()
        Entry = []
        price = []
        RT_Pos = []



        loop_counter = loop_counter + 1









        try:
            price = Price_data[shift]
            Entry = Entry_data[shift]
            symbol = Symbol_data[shift]
            # predictions = prediction[shift*i:(shift + 1)*i]
            shift = shift + 1
            t = Time_data[shift]
            hour = int(t[0])
            minute = int(t[1])
            try:
                sec = int(t[2])
            except:
                sec = 0
            predict=1
            flag = 0
            if minspassed != minute:
                minspassed = minute
                mincounter = mincounter + 1
                flag = 1
            if mincounter > loockback and flag == 1:
                arr = []
                for n in range(0,len(Price_by_min)):
                    arr.append(Price_by_min[n][mincounter-loockback-1:mincounter].tolist())

                sig = [0] * 20
                for n in range(0,len(arr)):
                    arr[n] = expand(arr[n])
                    arr[n] = arr[n] - arr[n][0]
                    if all(a == False for a in arr[n] > upper) and all(a == False for a in arr[n] < lower):
                        sig[n] = 1

                arr255 = to255(arr)
                pred = model1.predict(np.array([arr255]))
                predd = pred[0].argmax(axis = 1)



        except:
            break

        if 1:
            flag = 0
            active = 1




            for y in range(0, i):  # Buy for 5M+15M Entr# y

                Enter[y] = prediction[y] == 1
                if Enter[y] and (((Entry[y][15] - Entry[y][16]) / price[y]) < .003) and (unfilled_sell[y] == 0) and (Pos[y] == 0) and (hour != 14 or minute != 59) and (hour != 8 or minute != 30):
                    numshare = int(25 // Entry[y][9])
                    if numshare == 0:
                        numshare = 1








                    transaction = transaction + 1
                    Bal = Bal - (numshare * price[y])
                    Pos[y] = numshare
                    Entry_Price[y] = price[y]
                    Ins = Ins+1
                    # PerStock[y][1] = PerStock[y][1] - (numshare * price[y])
                    stop_loss[y] = price[y] - (Entry[y][9] * st)
                    mark_up[y] = price[y] + (Entry[y][9] * ma)
                    buyhour[y] = hour
                    buy_in[y] = 0
                    times_entered[y] = 0

                    # PerStock[y][2].append(str(hour%12) + ':' + str("{:02d}".format(min))  + '(' + str(price[y])+')')


            # Sell Conditions
            for y in range(0,i):  # Sell for 5M+15M Exit
                if ((Pos[y] > 0)):
                    if ((price[y] > mark_up[y]) or (price[y] < stop_loss[y])) or (hour == 14 and minute == 59):
                        transaction = transaction + 1
                        returnval = Pos[y]*price[y]
                        Bal = Bal + returnval
                        # PerStock[y][1] = PerStock[y][1] + (Pos[y] * price[y])
                        # PerStock[y][3].append(str(hour % 12) + ':' + str("{:02d}".format(min)) + '(' + str(price[y])+')')
                        diff = price[y] - Entry_Price[y]
                        diff = diff/Entry_Price[y]
                        totdiff = totdiff + diff
                        avgpercent = 100 * totdiff/Ins
                        if price[y] > Entry_Price[y]:
                            win = win + 1
                            wintot = wintot + (Pos[y]*price[y] - Pos[y]*Entry_Price[y])/(Entry_Price[y])
                            winav = wintot/win
                            winhour[buyhour[y] - 8] = winhour[buyhour[y] - 8] + 1
                        else:
                            lose = lose + 1
                            losstot = losstot + (Pos[y]*Entry_Price[y] - Pos[y]*price[y])/(Entry_Price[y])
                            lossav = losstot/lose
                            losshour[buyhour[y] - 8] = losshour[buyhour[y] - 8] + 1
                        Entry_Price[y] = 0
                        Recent_Exit[y] = 1
                        Pos[y] = 0

            stockval = 0
            numPos = 0
            for y in range(0,i):
                stockval = Pos[y]*price[y] + stockval

                if Pos[y] > 0:
                    numPos = numPos + 1
            if stockval > maxspend:
                maxspend = int(stockval)
            PL = Bal + stockval
            Hourly_PL[hour - 8] = int(PL)

        xxx = xxx + 1
    print(" PL: ", PL, "         ", "wins:", win, "     avgwin:", round(winav,3),"%","     losses", lose, "     avgloss:", round(lossav,3),"%", "     Active: ", numPos, "    Buys:", Ins, "  ", "  maxspend:", maxspend, "  avgpct: ", avgpercent, "%   ",)



    full_replay_arr = full_replay_arr + Hourly_PL[:7]





    Recent_Exit = [1] * 200







# #



print('That took {} seconds'.format(time.time() - starttime))



plt.plot(full_replay_arr, label = "12.4")
plt.annotate("12.4",xy = (7*num_files,full_replay_arr[-1]))

#
for n in range(0, (len(full_replay_arr))//7):
    plt.axvline(x= n*7)
plt.ylabel('some numbers')
plt.legend(loc="upper left")
plt.show()
print(h)




