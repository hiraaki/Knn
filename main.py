import pandas
import random
import math
import operator


def randonintlist(m, n):
    randonList = []
    for i in range(int(n)):
        r = random.randint(0, m)
        while (r in randonList) | (r >= m):
            r = random.randint(0, m)
        randonList.append(r)
    return randonList


# MR = pandas.DataFrame(columns=df.columns)
# MR = MR.append(pandas.Series(M.iloc[0], index=MR.columns), ignore_index=True)
# MR = MR.append(pandas.Series(R.iloc[0], index=MR.columns), ignore_index=True)

def randonObjectList(training, validation, test, ClassM, ClassR, columns):
    randonList = randonintlist(len(ClassM.index), len(ClassM.index) / 2)
   # print(randonList, len(ClassM.index), len(ClassM.index) / 2)
    for x in randonList:
        training = training.append(pandas.Series(ClassM.iloc[x], index=columns), ignore_index=True)
    ClassM = ClassM.drop(randonList, axis=0)
    randonList.clear()
    ClassM = ClassM.reset_index(drop=True)

    randonList = randonintlist(len(ClassR.index), len(ClassR.index) / 2)
    #print(randonList)
    for x in randonList:
        training = training.append(pandas.Series(ClassR.iloc[x], index=columns), ignore_index=True)
    ClassR = ClassR.drop(randonList, axis=0)
    randonList.clear()
    ClassR = ClassR.reset_index(drop=True)

    #print(training)

    randonList = randonintlist(len(ClassM.index), len(ClassM.index) / 2)
    #print(randonList)
    for x in randonList:
        validation = validation.append(pandas.Series(ClassM.iloc[x], index=columns), ignore_index=True)
    ClassM = ClassM.drop(randonList, axis=0)
    randonList.clear()
    ClassM = ClassM.reset_index(drop=True)

    randonList = randonintlist(len(ClassR.index), len(ClassR.index) / 2)
   # print(randonList)
    for x in randonList:
        validation = validation.append(pandas.Series(ClassR.iloc[x], index=columns), ignore_index=True)
    ClassR = ClassR.drop(randonList, axis=0)
    randonList.clear()
    ClassR = ClassR.reset_index(drop=True)

   # print(validation)
    test = test.append(ClassM, ignore_index=True)
    test = test.append(ClassR, ignore_index=True)

    #print(test)

    return [training, validation, test]


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        # print(instance1[x], instance2[x])
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def neigbors(training, testInstance, k):
    distancies = []
    for x in training.iterrows():
        distancies.append((euclideanDistance(x[1], testInstance, 60), x[0]))
    distancies.sort()
    close = []
    for x in range(k):
        close.append(distancies[x])
    return close


def responsebyvote(training, neighbors):
    mine = 0
    rock = 0
    for x in neighbors:
        # print(training.iloc[x[1]])
        if training.iloc[x[1]][60] == 'M':
            mine += 1
        else:
            rock += 1
    # print(mine, rock)
    if rock > mine:
        # print("Its a Rock")
        return 'R'
    else:
        # print("Its a Mine")
        return 'M'


def inverseEuclidian(neighbors):
    inverse = []
    for x in neighbors:
        inverse.append(((1 / x[0]), x[1]))
    return inverse


def responsebyinverseEuclidian(instance, neighbors):
    mine = 0
    rock = 0
    # print(neighbors)
    neighbors = inverseEuclidian(neighbors)
    neighbors.sort(key=operator.itemgetter(0))
    # print(neighbors)

    for x in neighbors:
        # print(instance.iloc[x[1]])
        if instance.iloc[x[1]][60] == 'M':
            mine += x[0]
        else:
            rock += x[0]
    # print(mine, rock)
    if rock > mine:
        return 'R'
        # print("Its a Rock")
    else:
        return 'M'
        # print("Its a Mine")


def normalizeddistance(neighbors):
    normalized = []
    aux1 = neighbors[len(neighbors) - 1]
    aux2 = neighbors[0]
    den = aux1[0] - aux2
    for x in neighbors:
        normalized.append((((x[0] - aux2) / den), x[1]))
    return normalized


def responsebyweightedvote(training, neighbors):
    mine = 0
    rock = 0
    # print(neighbors)
    neighbors = inverseEuclidian(neighbors)
    # print(neighbors)
    for x in neighbors:
        # print(training.iloc[x[1]])
        if training.iloc[x[1]][60] == 'M':
            mine += (1 - x[0])
        else:
            rock += (1 - x[0])
    # print(mine, rock)
    if rock > mine:
        return 'R'
        # print("Its a Rock")
    else:
        return 'M'
        # print("Its a Mine")


def findingthebestK(training, validation):
    acuraciV = []
    for k in range(1, 21, 2):
        acertos = 0
        for x in validation.iterrows():
            neighbors = neigbors(training, x[1], k)
            resp = responsebyvote(training, neighbors)
            if resp == x[1][60]:
                acertos += 1
        acuraciV.append([acertos / len(test.index), k, acertos])
        acuraciV.sort(reverse=True)
    print(acuraciV)
    acuraciI = []
    for k in range(1, 21, 2):
        acertos = 0
        for x in validation.iterrows():
            neighbors = neigbors(training, x[1], k)
            resp = responsebyvote(training, neighbors)
            if resp == x[1][60]:
                acertos += 1
        acuraciI.append([acertos / len(test.index), k, acertos])
        acuraciI.sort(reverse=True)
    print(acuraciI)
    acuraciW = []
    for k in range(1, 21, 2):
        acertos = 0
        for x in validation.iterrows():
            neighbors = neigbors(training, x[1], k)
            resp = responsebyvote(training, neighbors)
            if resp == x[1][60]:
                acertos += 1
        acuraciW.append([acertos / len(test.index), k, acertos])
        acuraciW.sort(reverse=True)
    print(acuraciW)
    return [acuraciV, acuraciI, acuraciW]


def mediaacuracia(M, R, df, k):
    acuraciV = []
    acuraciI = []
    acuraciW = []

    for x in range(10):
        print(x)
        training = pandas.DataFrame(columns=df.columns)
        validation = pandas.DataFrame(columns=df.columns)
        test = pandas.DataFrame(columns=df.columns)
        response = randonObjectList(training, validation, test, M, R, df.columns)
        training = response[0]
        validation = response[1]
        test = response[2]
        acertos = 0
        for x in validation.iterrows():
            neighbors = neigbors(training, x[1], k[0])
            resp = responsebyvote(training, neighbors)
            if resp == x[1][60]:
                acertos += 1
        acuraciV.append(acertos / len(test.index))

        training = pandas.DataFrame(columns=df.columns)
        validation = pandas.DataFrame(columns=df.columns)
        test = pandas.DataFrame(columns=df.columns)
        response = randonObjectList(training, validation, test, M, R, df.columns)
        training = response[0]
        validation = response[1]
        test = response[2]
        acertos = 0
        for x in validation.iterrows():
            neighbors = neigbors(training, x[1], k[1])
            resp = responsebyvote(training, neighbors)
            if resp == x[1][60]:
                acertos += 1
        acuraciI.append(acertos / len(test.index))

        training = pandas.DataFrame(columns=df.columns)
        validation = pandas.DataFrame(columns=df.columns)
        test = pandas.DataFrame(columns=df.columns)
        response = randonObjectList(training, validation, test, M, R, df.columns)
        training = response[0]
        validation = response[1]
        test = response[2]
        acertos = 0
        for x in validation.iterrows():
            neighbors = neigbors(training, x[1], k[2])
            resp = responsebyvote(training, neighbors)
            if resp == x[1][60]:
                acertos += 1
        acuraciW.append(acertos / len(test.index))

    return [acuraciV, acuraciI, acuraciW]


df = pandas.read_csv('Sonar - Maurício.csv')
M = df.loc[df['Class'] == 'M']
R = df.loc[df['Class'] == 'R']
M = M.reset_index(drop=True)
R = R.reset_index(drop=True)

ks = [3, 3, 3]
rar = mediaacuracia(M, R, df, ks)
print(rar[0])
print(rar[1])
print(rar[2])



#
# training = pandas.DataFrame(columns=df.columns)
# validation = pandas.DataFrame(columns=df.columns)
# test = pandas.DataFrame(columns=df.columns)
# response = randonObjectList(training, validation, test, M, R, df.columns)
# training = response[0]
# validation = response[1]
# test = response[2]
# #
# # # neighbors = neigbors(training, test.iloc[0], 1)
# # # print(neighbors)
# # print(training)
# # print(validation)
# # print(test)
# # dist = DistanceMetric.get_metric('euclidean')
# # print(training.iloc[0, :59])
# # print(training.iloc[1, :59])
#
# distancies = []
#
# print(euclideanDistance(df.iloc[1], df.iloc[0], 60))
# for x in df.iterrows():
#     distancies.append([euclideanDistance(x[1], df.iloc[0], 60), x[0]])
# print(distancies)
# distancies.sort()
# print(distancies)
# close = []
# for x in range(2):
#     close.append(distancies[x])
# print(close)
#
# close = neigbors(training, test.iloc[0], 3)
# print(close)
# print(responsebyvote(training, close))
# print(responsebyinverseEuclidian(training, close))
# print(responsebyweightedvote(training, close))
#
#
# print(findingthebestK(training, validation))

# print(test.iloc[0][60])
# n = randonintlist(100, 10)
# n.sort()
