import tensorflow as tf  # deep learning library. Tensors are just multi-dimensional arrays
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import time
import csv
import re
import os, os.path
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import sklearn

days = 1


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
    #random.shuffle(file_list)

    for day in range (0,days):

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
                    #if len(Entry_data) > 500:
                        #break
        Entry_data = np.array(Entry_data)
        Price_data = np.array(Price_data)
        Time_data = np.array(Time_data)

        ED.append(Entry_data)
        PD.append(Price_data)
        TD.append(Time_data)



    return PD, ED, TD

def makelabels( ED, PD, TD):

    LABEL = []
    for K in range(0,days):
        print("Day ",K)
        eed = ED[K].tolist()
        ppd = PD[K].tolist()
        label = []
        for k in range(0,len(eed)):
            label.append([])
            for kk in range(0,len(eed[0])):
                label[k].append(-1)
        starttime = time.time()
        for i in range(0,len(eed)):
            Entry_Price= [0]* len(eed[0])
            stop = [0] * len(eed[0])
            mark = [0] * len(eed[0])
            for k in range(0,len(eed[0])):
                Entry_Price[k] = ppd[i][k]
                stop[k] = Entry_Price[k] - (eed[i][k][9] *.25)
                mark[k] = Entry_Price[k] + (eed[i][k][9] * .25)
            for j in range(i,len(eed)):
                any = 0
                for k in range(0, len(eed[0])):
                    if label[i][k] == -1:
                        any = 1
                        if ppd[j][k] > mark[k]:
                            label[i][k] = 1
                            continue
                        if ppd[j][k] < stop[k]:
                            label[i][k] = 0
                            continue
                        if j == len(eed) - 1:
                            if ppd[j][k] > Entry_Price[k]:
                                label[i][k] = 1
                            else:
                                label[i][k] = 0

                if any == 0:
                    break
        llabel = np.array(label)
        LABEL.append(llabel)
    return LABEL

def makemodel():


    PD, ED, TD = makearray()
    label = makelabels(ED,PD,TD)
    LABEL = np.array(label)
    ed = ED[0].reshape(len(ED[0])*len(ED[0][0]), len(ED[0][0][0]))
    lbl = np.concatenate(LABEL[0])
    for n in range(1,len(ED)):
        a = ED[n].reshape(len(ED[n])*len(ED[n][0]), len(ED[n][0][0]))
        b = np.concatenate(LABEL[n])
        ed = np.concatenate((ed,a))
        lbl = np.concatenate((lbl,b))




    #ed,lbl = sklearn.utils.shuffle(ed, lbl)

    EDD = ed
    LBL = keras.utils.to_categorical(lbl,2)
    model1 = Sequential()
    model1.add(Dense(20, activation = 'relu', input_shape=(22,)))
    #model1.add(Dense(50, activation = 'relu'))
    model1.add(Dense(2, activation='softmax'))
    model1.compile(loss= 'categorical_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])
    history1 = model1.fit(EDD,LBL,batch_size=100,epochs=10,verbose=1,)
    score1 = model1.evaluate(EDD,LBL, verbose=0)
    print('Test loss: ',score1[0])
    print('Test accuracy: ',score1[1])
    wrong = 0
    length = len(EDD)
    raw_predictions = model1.predict(EDD)
    predictions = raw_predictions.argmax(axis=1)
    llabel = LBL.argmax(axis=1)
    comp = predictions == llabel
    wrong = len(comp) - np.count_nonzero(comp)
    print(np.count_nonzero(comp), " out of ", len(comp), " were right.")
    return model1



newmodel = 1
model = makemodel()
model.save('mymodel')





