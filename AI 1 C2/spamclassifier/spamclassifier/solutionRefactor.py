import numpy as np
from IPython.display import HTML,Javascript, display

training_spam = np.loadtxt(open("data/training_spam.csv"), delimiter=",").astype(int)
print("Shape of the spam training data set:", training_spam.shape)
print(training_spam)

testing_spam = np.loadtxt(open("data/testing_spam.csv"), delimiter=",").astype(int)
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
        self.k = k # k will act as the handler for the training data if it can just be anything
        
    def train(self):
        self.priorS, self.priorH = self.getLogClassPriors(self.k)
        self.classConditionalProbabilities = self.getLogClassCondLikes(self.k)
    
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
        for i in range(k): # smoothened
            arr[i] += alpha
            wordCount += arr[i]

        for i in range(k): # div all and get probabilities. already conditional.
            arr[i] /= wordCount

        # smoothing process is:
        # given word = n(c,w) + alpha / n(c) + kalpha
        # where k is the total amount of words (in this case, 54)
        return arr
    
    def logAll(self, arr):
        # all this does is log all, in case you want the data without the logs this has been placed in a separate container
        return np.array([np.log(x) for x in arr])
    
    def getLogClassCondLikes(self, data, alpha=1.0):

        # use laplace smoothing only when alpha > 0
        # Hint: many `numpy`-functions contain an `axis` argument. 
        # If you specify `axis=0`, you can perform column-wise (that is, feature-wise!) computations.
        
        _, ttlWidth = data.shape
        accHam = np.zeros(ttlWidth) # ignore the first entry, as that'll be ham/spam accumulation
        accSpam = np.zeros(ttlWidth) # accumulations

        for i in data:
            if i[0] == 1:
                for j in range(len(i)):
                    if i[j] == 1:
                        accSpam[j] += 1
            elif i[0] == 0:
                for j in range(len(i)):
                    if i[j] == 1:
                        accHam[j] += 1
        
        accAll = np.add(accSpam, accHam) # total words, this is w_i
        accAll = accAll[1:]

        # removing spam/ham value
        probsHam = self.logAll(self.probabilityWSmooth(accHam[1:], 1))
        probsSpam = self.logAll(self.probabilityWSmooth(accSpam[1:], 1))

        theta = np.concat([[probsHam], [probsSpam]])
        return theta

    def predict(self, new_data):
        # log ( p(C = c) ) + sum[totalTrainingWordCount * thetaCondWord]
        entries, _ = new_data.shape
        predictions = [] # is this optimal? i need to somehow initialise an array
        for i in new_data:
            ifHam = self.evaluate(i, self.priorS, self.classConditionalProbabilities[0])
            ifSpam = self.evaluate(i, self.priorH, self.classConditionalProbabilities[1])
            predictions += [1 if ifSpam > ifHam else 0]
        
        predictions = np.array(predictions)
        return predictions # array of 0s and 1s
    
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