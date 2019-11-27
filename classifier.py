from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier


def read_file(file_name):
    with open(file_name) as f:
        samples = f.readlines()
    return samples[1:]


def separate_features_and_classes(samples):
    features = []
    classes = []
    for sample in samples:
        classes.append(int(sample[-1]))
        features.append(list(map(float, sample[:-1])))
    return features, classes


print("Training...")
training_samples = read_file("new_train.csv")

# separate by class:
survived = []
not_survived = []
for sample in training_samples:
    sample = sample.replace("\n", '')
    sample = sample.split(",")
    if int(sample[-1]) == 1:
        survived.append(sample)
    else:
        not_survived.append(sample)

# get same number of samples of each class (simpler approach)
balanced_samples = []
for i in range(0, int(len(survived) / 2)):
    balanced_samples.append(survived[i])
    balanced_samples.append(not_survived[i])

# separate test and train sets
number_of_samples = len(balanced_samples)
last_training_sample = int(number_of_samples * 0.80)
training_set = balanced_samples[: last_training_sample]
test_set = balanced_samples[last_training_sample + 1:]

# separate features and classes
training_features, training_classes = separate_features_and_classes(training_set)
test_features, test_classes = separate_features_and_classes(test_set)

# training
clf = GaussianNB()
clf.fit(training_features, training_classes)
pred = clf.predict(test_features)

# accuracy
accuracy = accuracy_score(pred, test_classes)
print("Classifier accuracy: ", accuracy)

print("----------------------------------------")
print("Predict...")
# predict test set
test_samples = read_file("new_test.csv")
test_features = []
for sample in test_samples:
    sample = sample.replace("\n", '')
    sample = sample.split(",")
    test_features.append(list(map(float, sample)))
pred = clf.predict(test_features)

# save a file with predictions
file = open('output.csv', 'w')
file.write('PassengerId,Survived\n')
i = 0
p_id = 892
for sample in test_samples:
    file.write(str(p_id) + ',' + str(int(pred[i])))
    file.write('\n')
    p_id += 1
    i += 1
file.close()
print("File saved!")
