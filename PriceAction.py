import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf  # deep learning library. Tensors are just multi-dimensional arrays
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import time
import numpy as np
import os, os.path
import csv
import re

og = 1
days = 1
newman = 0
st = .5
ma = .5


def upanddown():
    # top = random.uniform(-.25,-.4)
    top = 1
    bottom = random.uniform(.25, .4)
    # top = -.3
    # bottom = -.3

    arr = [0] * 100

    a = random.randint(10, 20)
    b = random.randint(20, 30)
    c = random.randint(35, 45)
    d = random.randint(45, 55)
    e = random.randint(60, 70)
    f = random.randint(80, 95)
    #

    aa = random.uniform(0,1)
    bb = random.uniform(0,1)
    cc = random.uniform(0,1)
    dd = random.uniform(0,1)
    ee = random.uniform(0,1)
    ff =random.uniform(0,1)

    arr[0:a] = np.linspace(0, aa, a, endpoint=False)
    arr[a:b] = np.linspace(aa, bb, b - a, endpoint=False)
    arr[b:c] = np.linspace(bb, cc, c - b, endpoint=False)
    arr[c:d] = np.linspace(cc, dd, d - c, endpoint=False)
    arr[d:e] = np.linspace(dd, ee, e - d, endpoint=False)
    arr[e:f] = np.linspace(ee, ff, f - e, endpoint=False)

    arr[f:101] = np.linspace(ff, 1, 99 - f + 1, endpoint=False)
    arr = np.array(arr)

    return arr
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

    aa = random.uniform(.25,.45)
    bb = random.uniform(.1,.1)
    cc = random.uniform(.35,.55)
    dd = random.uniform(.40,.60)
    ee = random.uniform(.45,.65)
    ff = random.uniform(.50,.70)
    gg = random.uniform(.55,.85)
    arr[0:a] = np.linspace(0,aa,a,endpoint=False)
    arr[a:b] = np.linspace(aa,bb,b-a,endpoint=False)
    arr[b:c] = np.linspace(bb,cc,c-b, endpoint=False)
    arr[c:d] = np.linspace(cc,dd,d-c, endpoint=False)
    arr[d:e] = np.linspace(dd,ee,e-d, endpoint=False)
    arr[e:f] = np.linspace(ee,ff,f-e, endpoint=False)
    arr[f:101] = np.linspace(ff,gg,99-f+1, endpoint=False)
    arr =  np.array(arr)

    return arr
def incorrect():
    # top = random.uniform(-.25,-.4)
    top = 1
    bottom = random.uniform(.25,.4)
    # top = -.3
    # bottom = -.3

    arr = [0] * 100


    a = random.randint(15,25)
    b = random.randint(35,45)
    c = random.randint(45,55)
    d = random.randint(55,65)
    e = random.randint(65,75)
    f = random.randint(80,85)
    #

    aa = random.uniform(.15,.35)
    bb = random.uniform(.25,.45)
    cc = random.uniform(.35,.55)
    dd = random.uniform(.40,.65)
    ee = random.uniform(.55,.75)
    ff = random.uniform(.65,.85)
    gg = random.uniform(.75,.95)


    arr[0:a] = np.linspace(0,aa,a,endpoint=False)
    arr[a:b] = np.linspace(aa,bb,b-a,endpoint=False)
    arr[b:c] = np.linspace(bb,cc,c-b, endpoint=False)
    arr[c:d] = np.linspace(cc,dd,d-c, endpoint=False)
    arr[d:e] = np.linspace(dd,ee,e-d, endpoint=False)
    arr[e:f] = np.linspace(ee,ff,f-e, endpoint=False)

    arr[f:101] = np.linspace(ff,gg,99-f+1, endpoint=False)
    arr =  np.array(arr)


    return arr
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
    ID = []
    MD = []
    ii = np.empty((0,22*(newman+1)))
    #random.shuffle(file_list)

    for day in range (0,days):
        Entry_data = []
        input = []
        Price_data = []
        Symbol_data = []
        Time_data = []
        Min_data = []
        currmin = 0


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
            aa = []
            t = []
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
                        input.append(aa)
                    Symbol_data.append(t)
                    ttime = re.split(':', row[1])
                    ttime[0] = int(ttime[0])
                    ttime[1] = int(ttime[1])
                    Time_data.append(ttime)
                    if currmin != ttime[1]:
                        Min_data.append(p)
                        currmin = ttime[1]
                        newmins = newmins + 1
                    p = []
                    a = []
                    t = []
                    aa = []
                    # if len(Entry_data) > 500:
                    #     break
        if newmins >= newman:
            input = np.array(input)
        ID.append(input)
        MD.append(Min_data)
        a = np.concatenate(input)
        if og ==0:
            a = a.swapaxes(1, 2)
        ii = np.append(ii,a,axis=0)
        print("Read Day")
    return MD
def expand(arr):
    b = [0] * 100
    for i in range(0, len(arr) - 1):
        b[int(i * (len(b) / (len(arr) - 1))):int((i + 1) * (len(b) / (len(arr) - 1)))] = np.linspace(arr[i], arr[i + 1], int(len(b) / len(arr) + 1), endpoint=False)

    b = np.array(b)
    b = np.array(b)
    b = b - min(b)
    b = b / max(b)
    return b
def rand():
    x = np.random.randint(low=0, high=15, size=11)
    x[0] = 0
    x = x.tolist()
    arr = expand(x)
    return arr
def makemodel():
    train_input = []
    test_input = []

    train_lbl = []
    test_lbl = []

    print("making data")
    for i in range(0, 10000):
        if i%10000 == 0:
            print(i/10000)
        # a = random.randint(0,3)
        a = random.randint(0, 6)

        # if a == 0:
        #     train_input.append(headandshoulders())
        #     train_lbl.append(0)
        #     test_input.append(headandshoulders())
        #     test_lbl.append(0)
        if a == 0:
            train_input.append(correct())
            train_lbl.append(0)
            test_input.append(correct())
            test_lbl.append(0)
        if a == 1 or a == 2:
            train_input.append(upanddown())
            train_lbl.append(1)
            test_input.append(upanddown())
            test_lbl.append(1)
        if a == 5 or a == 6:
            train_input.append(incorrect())
            train_lbl.append(1)
            test_input.append(incorrect())
            test_lbl.append(1)
        if  a ==3 or a == 4:
            train_input.append(rand())
            train_lbl.append(1)
            test_input.append(rand())
            test_lbl.append(1)
    print("made data")
    train_input = to255(train_input)
    train_input = np.array(train_input)
    test_input = np.array(test_input)
    test_input = to255(test_input)


    train_lbl = np.array(train_lbl)
    test_lbl = np.array(test_lbl)

    train_lbl = keras.utils.to_categorical(train_lbl, 2)
    test_lbl = keras.utils.to_categorical(test_lbl, 2)

    model1 = Sequential()
    model1.add(Dense(300, activation='relu', input_shape=(10100,)))
    model1.add(Dense(100, activation='relu'))
    model1.add(Dense(50, activation='relu'))
    model1.add(Dense(2, activation='softmax'))
    model1.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
    history1 = model1.fit(train_input, train_lbl, batch_size=100, epochs=10, verbose=1, )
#    score1 = model1.evaluate(test_input,test_lbl, verbose=0)
#    print('Test loss: ',score1[0])
#    print('Test accuracy: ',score1[1])
    return model1
def labelanddata():
    MD = makearray()
    Price = []
    for day in range(0, days):
        Price.append([])
        numstocks = len(MD[day][0])
        for ii in range(0, numstocks):
            Price[day].append([])
        for stock in range(0, numstocks):
            for minute in range(0, len(MD[day])):
                Price[day][stock].append(MD[day][minute][stock])

    prices = []

    label = []
    input = []
    print("making labels")
    for day in range(0, len(Price)):
        for stock in range(0, len(Price[day])):
            for minutes in range(0, len(Price[day][stock]) - 11):
                prices.append(Price[day][stock][minutes:minutes + 11])
                a = Price[day][stock][minutes:minutes + 11]
                b = expand(a)
                b = b.tolist()
                b = np.array([b])
                c = model1.predict(b).argmax(axis=1)
                if c == 0:
                    any = 0
                    entry = a[-1]
                    mark = a[-1] + a[-1] * .01
                    stop = a[-1] - a[-1] * .01
                    for nextsec in range(minutes + 11, len(Price[day][stock])):
                        if Price[day][stock][nextsec] > mark:
                            input.append(a)
                            label.append(1)
                            break
                        if Price[day][stock][nextsec] < stop:
                            input.append(a)
                            label.append(0)
                            break
                        if nextsec == len(Price[day][stock]) - 1:
                            if Price[day][stock][nextsec] > entry:
                                input.append(a)
                                label.append(1)
                            else:
                                input.append(a)
                                label.append(0)

    pp = prices.copy()
    for x in range(0, len(prices)):
        prices[x] = expand(prices[x])

    prices = np.array(prices)
    prediction = model1.predict(prices)
    a = prediction.argmax(axis=1)
    unique, counts = np.unique(a, return_counts=True)
    print(dict(zip(unique, counts)))


# model1 = keras.models.load_model('C:/Users/shiva/PycharmProjects/PriceAction/mymodel')
model1 = makemodel()
model1.save('mymodel')