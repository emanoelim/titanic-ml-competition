from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression


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
for i in range(0, int(len(survived))):
    balanced_samples.append(survived[i])
    balanced_samples.append(not_survived[i])

# separate test and train sets
number_of_samples = len(balanced_samples)
last_training_sample = int(number_of_samples * 0.85)
training_set = balanced_samples[: last_training_sample]
test_set = balanced_samples[last_training_sample + 1:]

# separate features and classes
training_features, training_classes = separate_features_and_classes(training_set)
test_features, test_classes = separate_features_and_classes(test_set)

# cross validation
X, y = separate_features_and_classes(balanced_samples)
svm = SVC(kernel='linear', C=1)
scores = cross_val_score(svm, X, y, cv=3)
media = scores.mean()
dp = scores.std()
print("scores SVC:", scores, "- mean:", media, "- SD:", dp)

knn = KNeighborsClassifier(n_neighbors=3)
scores = cross_val_score(knn, X, y, cv=3)
media = scores.mean()
dp = scores.std()
print("scores KNN:", scores, "- mean:", media, "- SD:", dp)

dt = DecisionTreeClassifier()
scores = cross_val_score(dt, X, y, cv=3)
media = scores.mean()
dp = scores.std()
print("scores DT:", scores, "- mean:", media, "- SD:", dp)

lg = LogisticRegression()
scores = cross_val_score(lg, X, y, cv=3)
media = scores.mean()
dp = scores.std()
print("scores LR:", scores, "- mean:", media, "- SD:", dp)

rf = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(rf, X, y, cv=3)
media = scores.mean()
dp = scores.std()
print("scores RF:", scores, "- mean:", media, "- SD:", dp)

nb = GaussianNB()
scores = cross_val_score(nb, X, y, cv=3)
media = scores.mean()
dp = scores.std()
print("scores NB:", scores, "- mean:", media, "- SD:", dp)

print("Training...")
clf = GaussianNB()
clf.fit(training_features, training_classes)
pred = clf.predict(test_features)

print("Predicting...")
test_samples = read_file("new_test.csv")
test_features = []
for sample in test_samples:
    sample = sample.replace("\n", '')
    sample = sample.split(",")
    test_features.append(list(map(float, sample)))
pred = clf.predict(test_features)

print("Saving output file...")
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
