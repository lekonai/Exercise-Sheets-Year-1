import numpy as np

def estimate_log_class_priors(data):
    ttlEntries, _ = data.shape
    ttlSpam = 0

    for i in data:
        if i[0] == 1:
            ttlSpam += 1

    ttlHam = ttlEntries - ttlSpam

    pHam = ttlHam / ttlEntries # p(C = 0)
    pSpam = ttlSpam / ttlEntries # p(C = 1)
    
    log_class_priors = np.array([np.log(pHam), np.log(pSpam)])
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

def logAll(arr):
    # all this does is log all, in case you want the data without the logs this has been placed in a separate container
    return np.array([np.log(x) for x in arr])

def estimate_log_class_conditional_likelihoods(data, alpha=1.0):

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
    probsHam = logAll(probabilityWSmooth(accHam[1:], 1))
    probsSpam = logAll(probabilityWSmooth(accSpam[1:], 1))

    theta = np.concat([[probsHam], [probsSpam]])
    return theta

def predict(new_data, log_class_priors, log_class_conditional_likelihoods):
    """
    Given a new data set with binary features, predict the corresponding
    response for each instance (row) of the new_data set.

    :param new_data: a two-dimensional numpy-array with shape = [n_test_samples, n_features].
    :param log_class_priors: the priors.
    :param log_class_conditional_likelihoods: theta.
    :return class_predictions: a numpy array containing the class predictions for each row
        of new_data.
    """

    # so we just have features for this new_data.

    # log ( p(C = c) ) + sum[totalTrainingWordCount * thetaCondWord]
    entries, _ = new_data.shape
    class_predictions = [] # is this optimal? i need to somehow initialise an array
    for i in new_data:
        ifHam = evaluate(i, log_class_priors[0], log_class_conditional_likelihoods[0])
        ifSpam = evaluate(i, log_class_priors[1], log_class_conditional_likelihoods[1])
        class_predictions += [1 if ifSpam > ifHam else 0]
    
    class_predictions = np.array(class_predictions)
    return class_predictions # array of 0s and 1s

def evaluate(email, logClassPrior, theta):
    sum = 0
    for i in range(len(email)):
        if (email[i] == 1):
            sum += theta[i]
    return (logClassPrior + sum)


###
# RUNTIME
training_spam = np.loadtxt(open("data/training_spam.csv"), delimiter=",")
test_spam = np.loadtxt(open("data/testing_spam.csv"), delimiter=",")

estimate_log_class_priors(training_spam)
lCPs = estimate_log_class_priors(training_spam)
lCCL = estimate_log_class_conditional_likelihoods(training_spam)

print(predict(test_spam[:, 1:], lCPs, lCCL))
# RUNTIME
###