import numpy as np
from IPython.display import HTML,Javascript, display

training_spam = np.loadtxt(open("./testingData/trainingdata.csv"), delimiter=",").astype(int)
print("Shape of the spam training data set:", training_spam.shape)
print(training_spam)

testing_spam = np.loadtxt(open("./testingData/testdata.csv"), delimiter=",").astype(int)
print("Shape of the spam testing data set:", testing_spam.shape)
print(testing_spam)
# This skeleton code simply classifies every input as ham
#
# Here you can see there is a parameter k that is unused, the
# point is to show you how you could set up your own. You might
# also pass in extra data via a train method (also does nothing
# here). Modify this code as much as you like so long as the 
# accuracy test in the cell below runs.

class SpamClassifier:
    classConditionalProbabilities = []
    priorS = 0;
    priorH = 0;

    def __init__(self, k):
        self.k = k # k will hold the training data
        
    def train(self):
        self.priorS, self.priorH = self.getLogClassPriors(self.k)
        height, _ = self.k.shape
        alpha = 1
        if height > 100:
            alpha = height / 100
        self.classConditionalProbabilities = self.getLogClassCondLikes(self.k, alpha if alpha >= 1 else 1)
    
    def getLogClassPriors(self, data):
        ttlEntries, _ = data.shape
        ttlSpam = 0

        for i in data:
            if i[0] == 1:
                ttlSpam += 1

        ttlHam = ttlEntries - ttlSpam

        pHam = ttlHam / ttlEntries # p(C = 0)
        pSpam = ttlSpam / ttlEntries # p(C = 1)
        
        logClassPriors = np.array([np.log(pHam), np.log(pSpam)])
        return logClassPriors
    
    def probabilityWSmooth(self, arr, alph):
        alpha = alph
        arr = arr.copy()
        k = len(arr)
        wordCount = 0;
        for i in range(k): # smoothing
            arr[i] += alpha
            wordCount += arr[i]

        for i in range(k): # div all
            arr[i] /= wordCount

        return arr
    
    def logAll(self, arr):
        return np.array([np.log(x) for x in arr])
    
    def getLogClassCondLikes(self, data, alpha):
        
        _, ttlWidth = data.shape
        accHam = np.zeros(ttlWidth)
        accSpam = np.zeros(ttlWidth)

        for i in data:
            if i[0] == 1:
                for j in range(len(i)):
                    if i[j] == 1:
                        accSpam[j] += 1
            elif i[0] == 0:
                for j in range(len(i)):
                    if i[j] == 1:
                        accHam[j] += 1
        
        accAll = np.add(accSpam, accHam)
        accAll = accAll[1:]

        # removing spam/ham value
        probsHam = self.logAll(self.probabilityWSmooth(accHam[1:], alpha))
        probsSpam = self.logAll(self.probabilityWSmooth(accSpam[1:], alpha))

        theta = np.concat([[probsHam], [probsSpam]])
        return theta

    def predict(self, new_data):
        predictions = []
        for i in new_data:
            ifHam = self.evaluate(i, self.priorS, self.classConditionalProbabilities[0])
            ifSpam = self.evaluate(i, self.priorH, self.classConditionalProbabilities[1])
            predictions += [1 if ifSpam > ifHam else 0]
        
        predictions = np.array(predictions)
        return predictions
    
    def evaluate(self, email, logClassPrior, theta):
        sum = 0
        for i in range(len(email)):
            if (email[i] == 1):
                sum += theta[i]
        return (logClassPrior + sum)
    

def create_classifier():
    classifier = SpamClassifier(training_spam)
    classifier.train()
    return classifier

classifier = create_classifier()
print(classifier.predict(testing_spam))