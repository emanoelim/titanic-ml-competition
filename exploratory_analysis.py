import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


file_name = "analysis_train.csv"
titanic = pd.read_csv(file_name)

survived_by_class = titanic[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_class)

survived_by_sex = titanic[['Sex', 'Survived']].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_sex)

survived_by_alone = titanic[['Alone', 'Survived']].groupby(['Alone'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_alone)

survived_by_age = titanic[['AgeRange', 'Survived']].groupby(['AgeRange'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_age)

survived_by_sibsp = titanic[['SibSp', 'Survived']].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_sibsp)

survived_by_parch = titanic[['Parch', 'Survived']].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_parch)

survived_by_family = titanic[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_family)

survived_by_status = titanic[['Status', 'Survived']].groupby(['Status'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_status)

survived_by_title = titanic[['SimplifiedTitle', 'Survived']].groupby(['SimplifiedTitle'], as_index=False).mean().sort_values(by='Survived', ascending=False)
print(survived_by_title)

plt.subplot(4, 3, 1)
sns.countplot(x = "Survived", data = titanic)
plt.subplot(4, 3, 2)
sns.countplot(x = "Pclass", hue = "Survived", data = titanic)
plt.subplot(4, 3, 3)
sns.countplot(x = "Sex", hue = "Survived", data = titanic)
plt.subplot(4, 3, 4)
sns.countplot(x = "Alone", hue = "Survived", data = titanic)
plt.subplot(4, 3, 5)
sns.countplot(x = "Status", hue = "Survived", data = titanic)
plt.subplot(4, 3, 6)
sns.countplot(x = "SimplifiedCabin", hue = "Survived", data = titanic)
plt.subplot(4, 3, 7)
sns.countplot(x = "AgeRange", hue = "Survived", data = titanic)
plt.subplot(4, 3, 8)
sns.countplot(x = "Embarked", hue = "Survived", data = titanic)
plt.subplot(4, 3, 9)
sns.countplot(x = "SimplifiedTitle", hue = "Survived", data = titanic)
plt.subplot(4, 3, 10)
sns.countplot(x = "Embarked", hue = "Pclass", data = titanic)
plt.subplot(4, 3, 11)
sns.distplot(titanic["Age"].dropna())

plt.show()

