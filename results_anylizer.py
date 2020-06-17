import csv
import matplotlib.pyplot as plt
import numpy as np

iterations_num = 1000
topY = 0
results = []
for filename in ['Current_System', 'Improved_System']:
    with open(filename + '.csv', newline='') as csvfile:
        iterations_avarages = []
        iterations = []
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if 'new' in row[0]:
                newIter = []
                iterations.append(newIter)
            else:
                arrivalTime = int(float(row[0]))
                timeInSystem = int(float(row[1]))
                iterations[-1].append((arrivalTime, timeInSystem))
        if len(iterations) > iterations_num:
            for i in range(len(iterations)-iterations_num):
                iterations[i] = iterations[i] + iterations[i+iterations_num]
            iterations = iterations[:iterations_num]
        minLen = min(map(len, iterations))
        for i in range(len(iterations)):
            iterations[i].sort(key=lambda tup: tup[0])
            iterations[i] = iterations[i][:minLen]
        for iteration in iterations:
            iterSum = 0
            for res in iteration:
                iterSum += res[1]
            iterations_avarages.append(iterSum/len(iteration))
        results.append(iterations_avarages)
        average = []

        for i in range(minLen):
            studentsSum = 0
            for iter in iterations:
                studentsSum += iter[i][1]
            average.append(studentsSum/len(iterations))
        index = np.arange(minLen)
        plt.bar(index, average)
        plt.xlabel('Student Num', fontsize=15)
        plt.ylabel('Service Length', fontsize=15)
        plt.xticks(index, range(minLen), fontsize=8, rotation=30)
        plt.title(filename + ' , avarage=' + str(int(sum(average)/len(average))))
        axes = plt.gca()
        if topY > 0 :
            axes.set_ylim([0, topY])
        else:
            axes.set_ylim([0, max(average)])
            topY = max(average)
        plt.savefig(filename + '_ plot.png')
        plt.show()

from scipy import stats
np.random.seed(12345678)

print(stats.ttest_ind(results[0], results[1]))
print(stats.ttest_ind(results[0], results[1], equal_var = False))

