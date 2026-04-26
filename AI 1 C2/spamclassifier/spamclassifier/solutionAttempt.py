import numpy as np

training_spam = np.loadtxt(open("data/training_spam.csv"), delimiter=",")
# print("Shape of the spam training data set:", training_spam.shape)
# print(training_spam)

def estimate_log_class_priors(data):
    ttlEntries, ttlWidth = data.shape
    ttlSpam = 0
    accSpam = np.zeros(ttlWidth) # accumulations
    accHam = np.zeros(ttlWidth) # ignore the first entry, as that'll be ham/spam accumulation

    for i in data:
        if i[0] == 1:
            ttlSpam += 1
            for j in range(len(i)):
                if i[j] == 1:
                    accSpam[j] += 1
        elif i[0] == 0:
            for j in range(len(i)):
                if i[j] == 1:
                    accHam[j] += 1
    
    accAll = np.add(accSpam, accHam) # total words, this is w_i
    accAll = accAll[1:]

    ttlHam = ttlEntries - ttlSpam

    cSpam = ttlSpam / ttlEntries # p(C = 1)
    cHam = ttlHam / ttlEntries # p(C = 0)
    
    log_class_priors = np.array([np.log(cHam), np.log(cSpam)])
    return log_class_priors

def probabilityWSmooth(arr, alph):
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

def estimate_log_class_conditional_likelihoods(data, alpha=1.0):
    """
    Given a data set with binary response variable (0s and 1s) in the
    left-most column and binary features (words), calculate the empirical
    class-conditional likelihoods, that is,
    log(P(w_i | c)) for all features w_i and both classes (c in {0, 1}).
    
    Assume a multinomial feature distribution and use Laplace smoothing
    if alpha > 0.

    :param data: a two-dimensional numpy-array with shape = [n_samples, 1 + n_features]

    :return theta:
        a numpy array of shape = [2, n_features]. theta[j, i] corresponds to the
        logarithm of the probability of feature i appearing in a sample belonging 
        to class j.
    """

    # use laplace smoothing only when alpha > 0
    # Hint: many `numpy`-functions contain an `axis` argument. 
    # If you specify `axis=0`, you can perform column-wise (that is, feature-wise!) computations.

    ttlEntries, ttlWidth = data.shape
    ttlSpam = 0
    accSpam = np.zeros(ttlWidth) # accumulations
    accHam = np.zeros(ttlWidth) # ignore the first entry, as that'll be ham/spam accumulation

    for i in data:
        if i[0] == 1:
            ttlSpam += 1
            for j in range(len(i)):
                if i[j] == 1:
                    accSpam[j] += 1
        elif i[0] == 0:
            for j in range(len(i)):
                if i[j] == 1:
                    accHam[j] += 1
    
    accAll = np.add(accSpam, accHam) # total words, this is w_i
    accAll = accAll[1:]

    ttlHam = ttlEntries - ttlSpam

    cSpam = ttlSpam / ttlEntries # p(C = 1)
    cHam = ttlHam / ttlEntries # p(C = 0)
    # i don't have to use these yet
    # probsSpam = probabilityWSmooth(accSpam[1:], 1) # removing spam/ham value
    # probsHam = probabilityWSmooth(accHam[1:], 1)

    # # calculate log class priors. i'm not sure what
    # # the point of it is ?

    # # p(C = 1)
    # ttlSumS = 0;
    # for i in range(len(probsSpam)):
    #     ttlSumS += np.log(probsSpam[i]) * accAll[i]
    
    # # log(p(C = c)FULLPROD(wordGivenCond)^wordCount) 

    # # p(C = 0)
    # ttlSumH = 0;
    # for i in range(len(probsHam)):
    #     ttlSumH += np.log(probsHam[i]) * accAll[i]


    return theta

estimate_log_class_priors(training_spam)
lCPs = estimate_log_class_priors(training_spam)
print("result: ", lCPs)
