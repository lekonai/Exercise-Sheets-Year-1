import numpy as np

training_spam = np.loadtxt(open("training_spam.csv"), delimiter=",")
print("Shape of the spam training data set:", training_spam.shape)
print(training_spam)