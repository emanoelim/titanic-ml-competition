from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

from common_functions import read_file, clean_samples, separate_features_and_classes


# --- training ---
training_samples = read_file('C:/Users/Manu/Documents/Python/ProjetosImagens/Titanic2/train_cleaned.csv')
test_samples = read_file('C:/Users/Manu/Documents/Python/ProjetosImagens/Titanic2/test_cleaned.csv')
samples = training_samples + test_samples
cleaned_samples = clean_samples(samples)
training_cleaned_samples = cleaned_samples[:891]
test_cleaned_samples = cleaned_samples[891:]

# separate by class:
survived = []
not_survived = []
for sample in training_cleaned_samples:
    if sample[0] == 1:
        survived.append(sample)
    else:
        not_survived.append(sample)

# get same number of sambles of each class for training (simpler approach)
balanced_samples = []
for i in range(0, int(len(survived) / 2)):
    balanced_samples.append(survived[i])
    balanced_samples.append(not_survived[i])
# print(balanced_samples)

# separate test and train sets
number_of_samples = len(balanced_samples)
training_set = balanced_samples[: int(number_of_samples * 0.85)]
test_set = balanced_samples[int(number_of_samples * 0.85):]

# separate features and classes
training_features, training_classes = separate_features_and_classes(training_set)
test_features, test_classes = separate_features_and_classes(test_set)

# training
# clf = SVC(C=3)
clf = GaussianNB()
# clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(training_features, training_classes)
pred = clf.predict(test_features)

# accuracy
accuracy = accuracy_score(pred, test_classes)
print(accuracy)


# --- classify test samples ---
training_features, training_classes = separate_features_and_classes(training_cleaned_samples)
test_features, test_classes = separate_features_and_classes(test_cleaned_samples)
clf.fit(training_features, training_classes)
pred = clf.predict(test_features)

# save a file with predictions
file = open('C:/Users/Manu/Documents/Python/ProjetosImagens/Titanic2/output.csv', 'w')
file.write('PassengerId,Survived\n')
i = 0
for sample in test_samples:
    passenger = sample.split(',')[0]
    file.write(passenger + ',' + str(int(pred[i])))
    file.write('\n')
    i += 1
file.close()
