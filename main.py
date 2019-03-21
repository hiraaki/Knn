import pandas
import random
df = pandas.read_csv('Sonar - Maurício.csv')
M = df.loc[df['Class'] == 'M']
R = df.loc[df['Class'] == 'R']


def randonintlist(m, n):
    randonList = []
    for i in range(n):
        r = random.randint(0, m)
        while r in randonList:
            r = random.randint(0, m)
        randonList.append(r)
    return randonList


def randonObjectList(training, validation, test, ClassM, ClassR):
    sMTr = ClassM.size/2
    sMTV = ClassM.size/4
    sRTr = ClassR.size/2
    sRTV = ClassR.size/4

MR = pandas.DataFrame

pandas.concat(M.iloc[0], MR)

n = randonintlist(100, 10)
n.sort()
print(MR)



