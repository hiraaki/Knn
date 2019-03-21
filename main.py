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

    randonList = randonintlist(len(ClassM.index), len(ClassM.index)/2)
    for x in randonList:
        training = training.append(pandas.Series(ClassM.iloc[x], index=columns), ignore_index=True)
    ClassM = ClassM.drop(randonList, axis=0)
    randonList.clear()
    ClassM = ClassM.reset_index(drop=True)

    randonList = randonintlist(len(ClassR.index), len(ClassR.index) / 2)
    for x in randonList:
        training = training.append(pandas.Series(ClassR.iloc[x], index=columns), ignore_index=True)
    ClassR = ClassR.drop(randonList, axis=0)
    randonList.clear()
    ClassR = ClassR.reset_index(drop=True)

    randonList = randonintlist(len(ClassM.index), len(ClassM.index)/2)
    for x in randonList:
        validation = validation.append(pandas.Series(ClassM.iloc[x], index=columns), ignore_index=True)
    ClassM = ClassM.drop(randonList, axis=0)
    randonList.clear()
    ClassM = ClassM.reset_index(drop=True)

    randonList = randonintlist(len(ClassR.index), len(ClassR.index) / 2)
    for x in randonList:
        validation = validation.append(pandas.Series(ClassR.iloc[x], index=columns), ignore_index=True)
    ClassR = ClassR.drop(randonList, axis=0)
    randonList.clear()
    ClassR = ClassR.reset_index(drop=True)

    test = test.append(ClassM)
    test = test.append(ClassR)

    return [training, validation, test]


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(training, testInstance, k):
    distancies = []
    for i in range(len(training.index)):
        distancies.append((euclideanDistance(training.iloc[i], testInstance, 60), i))
    distancies.sort(key=operator.itemgetter(0))
    neighbors =[]
    for x in range(k):
        neighbors.append(distancies[x])
    print(distancies)
    return neighbors


def responsebyvote(training, neighbors):
    mine = 0
    rock = 0
    for x in neighbors:
        #print(training.iloc[x[1]])
        if training.iloc[x[1]][60] == 'M':
            mine += 1
        else:
            rock += 1
    print(mine, rock)
    if mine < rock:
        print("Its a Rock")
    else:
        print("Its a Mine")


def inverseEuclidian(neighbors):
    inverse = []
    for x in neighbors:
        inverse.append(((1/x[0]), x[1]))
    return inverse


def responsebyinverseEuclidian(training, neighbors):
    mine = 0
    rock = 0
    print(neighbors)
    neighbors = inverseEuclidian(neighbors)
    neighbors.sort(key=operator.itemgetter(0))
    print(neighbors)

    for x in neighbors:
        #print(training.iloc[x[1]])
        if training.iloc[x[1]][60] == 'M':
            mine += x[0]
        else:
            rock += x[0]
    print(mine, rock)
    if mine > rock:
        print("Its a Rock")
    else:
        print("Its a Mine")


def normalizeddistance(neighbors):
    normalized = []
    aux1 = neighbors[len(neighbors)-1]
    aux2 = neighbors[0]
    den = aux1[0] - aux2
    for x in neighbors:
        normalized.append((((x[0]-aux2) / den), x[1]))
    return normalized


def responsebyweightedvote(training, neighbors):
    mine = 0
    rock = 0
    print(neighbors)
    neighbors = inverseEuclidian(neighbors)
    print(neighbors)
    for x in neighbors:
        #print(training.iloc[x[1]])
        if training.iloc[x[1]][60] == 'M':
            mine += (1 - x[0])
        else:
            rock += (1 - x[0])
    print(mine, rock)
    if mine > rock:
        print("Its a Rock")
    else:
        print("Its a Mine")



def findingthebestK(training,validatiuon,test):

    for x in range(10):
        training = pandas.DataFrame(columns=df.columns)
        validation = pandas.DataFrame(columns=df.columns)
        test = pandas.DataFrame(columns=df.columns)
        response = randonObjectList(training, validation, test, M, R, df.columns)
        training = response[0]
        validation = response[1]
        test = response[2]
        k = 1
        acertos = 0
        erros = 0

        neighbors = getNeighbors(training, test.iloc[0], k)
        print(neighbors)
        responsebyvote(training, neighbors)
        responsebyinverseEuclidian(training, neighbors)
        responsebyweightedvote(training, neighbors)


df = pandas.read_csv('Sonar - Maurício.csv')
M = df.loc[df['Class'] == 'M']
R = df.loc[df['Class'] == 'R']
M = M.reset_index(drop=True)
R = R.reset_index(drop=True)
#MR = pandas.DataFrame(columns=df.columns)
#MR = MR.append(pandas.Series(M.iloc[0], index=MR.columns), ignore_index=True)
#MR = MR.append(pandas.Series(R.iloc[0], index=MR.columns), ignore_index=True)
#MR = MR.append(pandas.Series(R.iloc[1], index=MR.columns), ignore_index=True)
#MR = MR.append(pandas.Series(R.iloc[3], index=MR.columns), ignore_index=True)
#print(MR)
#MR = MR.drop(MR.index[2])
#print(MR)
training = pandas.DataFrame(columns=df.columns)
validation = pandas.DataFrame(columns=df.columns)
test = pandas.DataFrame(columns=df.columns)
response = randonObjectList(training, validation, test, M, R, df.columns)
training = response[0]
validation = response[1]
test = response[2]
neighbors = getNeighbors(training, test.iloc[0], 10)
print(neighbors)
# print(training)
# print(validation)
# print(test)
responsebyvote(training, neighbors)
responsebyinverseEuclidian(training, neighbors)
responsebyweightedvote(training, neighbors)
print(test.iloc[0][60])
n = randonintlist(100, 10)
n.sort()



