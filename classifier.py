import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt


# separate by class:
from sklearn.naive_bayes import GaussianNB

training_samples = pd.read_csv("new_train.csv")
survived = training_samples.loc[training_samples['Survived'] == 1]
not_survived = training_samples.loc[training_samples['Survived'] == 0]
len_survived = len(survived.index)

# get same number of survived and not survived samples
not_survived = not_survived[0:len_survived]
len_not_survived = len_survived

# separate test and train sets
perc = 0.85
survived_training = survived[0:int(len_survived*perc)]
survived_test = survived[int(len_survived*perc):]
not_survived_training = not_survived[0:int(len_not_survived*perc)]
not_survived_test = not_survived[int(len_not_survived*perc):]
training_samples = survived_training.append(not_survived_training)
test_samples = survived_test.append(not_survived_test)

# separete features and classes
training_classes = training_samples["Survived"]
training_features = training_samples.drop("Survived", 1)
test_classes = test_samples["Survived"]
test_features = test_samples.drop("Survived", 1)

print("############ Training ############")
clf = RandomForestClassifier(n_estimators=50, max_features='sqrt')
clf.fit(training_features, training_classes)

# features importance
features = pd.DataFrame()
features['feature'] = training_features.columns
features['importance'] = clf.feature_importances_
features.sort_values(by=['importance'], ascending=True, inplace=True)
features.set_index('feature', inplace=True)
features.plot(kind='barh', figsize=(25, 25))
plt.show()

print("############ Classifier with best features ############")
clf = GaussianNB()
training_features = training_samples[["Fare", "Age", "female", "male", "FamilySize", "Master.", "Miss.", "Mr.", "Mrs."]]
test_features = test_features[["Fare", "Age", "female", "male", "FamilySize", "Master.", "Miss.", "Mr.", "Mrs."]]
clf.fit(training_features, training_classes)
pred = clf.predict(test_features)
acc = accuracy_score(pred, test_classes)
print("Accuracy: ", acc)

print("############ Predict ############")
test_features = pd.read_csv("new_test.csv")
test_features = test_features[["Fare", "Age", "female", "male", "FamilySize", "Master.", "Miss.", "Mr.", "Mrs."]]
pred = clf.predict(test_features)

print("Saving output file...")
file = open('output.csv', 'w')
file.write('PassengerId,Survived\n')
i = 0
p_id = 892
for i in pred:
    file.write(str(p_id) + ',' + str(int(pred[i])))
    file.write('\n')
    p_id += 1
    i += 1
file.close()
print("File saved!")
