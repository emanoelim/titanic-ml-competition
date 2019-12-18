import pandas as pd


def name_to_title(row):
    name = row["Name"]
    titles = ['Mrs.', 'Mr.', 'Master.', 'Miss.', 'Major.', 'Rev.', 'Dr.', 'Ms.', 'Mlle.', 'Col.', 'Capt.', 'Mme.',
              'Countess.', 'Don.', 'Jonkheer.']
    titles.sort(key=lambda s: len(s), reverse=True)
    for title in titles:
        if title in name:
            return title


def simplify_title(row):
    title = row["Title"]
    if title in ["Don.", "Major.", "Capt.", "Jonkheer.", "Rev.", "Col."]:
        return "Mr."
    elif title in ["Countess.", "Mme."]:
        return "Mrs."
    elif title in ["Mlle.", "Ms."]:
        return "Miss."
    elif title in ["Master."]:
        return "Master."
    elif title == "Dr.":
        sex = row["Sex"]
        if sex == "male":
            return "Mr."
        else:
            return "Mrs."
    else:
        return title


def define_status(row):
    title = row["SimplifiedTitle"]
    if title in ['Mr.', 'Mrs.']:
        return 'married'
    else:
        return 'single'


def simplify_cabin(row):
    cabin = str(row["Cabin"])
    if 'A' in cabin:
        return 'A'
    elif 'B' in cabin:
        return 'B'
    elif 'C' in cabin:
        return 'C'
    elif 'D' in cabin:
        return 'D'
    elif 'E' in cabin:
        return 'E'
    elif 'F' in cabin:
        return 'F'
    elif 'G' in cabin:
        return 'G'
    elif 'T' in cabin:
        return 'T'
    else:
        return 'U'


def mean_age_younger_people(data):
    younger_people = data[data["Title"].isin(["Miss.", "Master."])]
    younger_people = younger_people.dropna(subset=["Age"])
    mean_age = int(younger_people["Age"].mean())
    # print(mean_age)
    return mean_age


def mean_age_older_people(data):
    older_people = data[data["Title"].isin(["Mr.", "Mrs."])]
    older_people = older_people.dropna(subset=["Age"])
    mean_age = int(older_people["Age"].mean())
    # print(mean_age)
    return mean_age


def fill_age_by_title(age, title):
    if pd.isna(age):
        if title in ["Miss.", "Master."]:
            age = mean_age_younger_people(data)
        else:
            age = mean_age_older_people(data)
    return age


def fill_missing_ages(data):
    data["Age"] = data.apply(lambda row: fill_age_by_title(row.Age, row.SimplifiedTitle), axis=1)


def fill_missing_fares(data):
    mean_fare = data["Fare"].mean()
    data["Fare"] = data["Fare"].fillna(mean_fare)


def fill_embarked(row):
    embarked = row["Embarked"]
    if pd.notna(embarked):
        if 'S' in embarked:
            return "Southampton"
        elif 'C' in embarked:
            return "Cherbourg"
        elif 'Q' in embarked:
            return "Queenstown"
    else:
        return "Southampton"


def age_range(row):
    age = row["Age"]
    if age < 15:
        return "Child"
    elif age < 21:
        return "Young"
    elif age < 60:
        return 'Adult'
    else:
        return "Old"

# ---------------------
file_name = "test.csv"
data = pd.read_csv(file_name)

# new columns, fill missing data
data["Title"] = data.apply(lambda row: name_to_title(row), axis = 1)
data["SimplifiedTitle"] = data.apply(lambda row: simplify_title(row), axis = 1)
fill_missing_ages(data)
fill_missing_fares(data)
data["Status"] = data.apply(lambda row: define_status(row), axis = 1)
data["SimplifiedCabin"] = data.apply(lambda row: simplify_cabin(row), axis = 1)
data["FamilySize"] = data.apply(lambda row: row.Parch + row.SibSp, axis=1)
data["Alone"] = data.apply(lambda row: 'not_alone' if row.FamilySize else 'alone', axis=1)
data["AgeRange"] =  data.apply(lambda row: age_range(row), axis = 1)
data["Embarked"] = data.apply(lambda row: fill_embarked(row), axis = 1)

# normalize
data["Age"] = ((data["Age"] - data["Age"].min()) / (data["Age"].max() - data["Age"].min()))
data["Fare"] = ((data["Fare"] - data["Fare"].min()) / (data["Fare"].max() - data["Fare"].min()))
data["Parch"] = ((data["Parch"] - data["Parch"].min()) / (data["Parch"].max() - data["Parch"].min()))
data["SibSp"] = ((data["SibSp"] - data["SibSp"].min()) / (data["SibSp"].max() - data["SibSp"].min()))
data["FamilySize"] = ((data["FamilySize"] - data["FamilySize"].min()) / (data["FamilySize"].max() - data["FamilySize"].min()))

# deal with categorical data
dummy_sex = pd.get_dummies(data["Sex"])
dummy_status = pd.get_dummies(data["Status"])
dummy_cabin = pd.get_dummies(data["SimplifiedCabin"])
dummy_alone = pd.get_dummies(data["Alone"])
dummy_age_range = pd.get_dummies(data["AgeRange"])
dummy_embarked = pd.get_dummies(data["Embarked"])
dummy_title = pd.get_dummies(data["SimplifiedTitle"])
data = pd.concat([data, dummy_sex, dummy_status, dummy_cabin, dummy_alone, dummy_age_range, dummy_embarked, dummy_title], axis=1)

# save file with columns that will be used
columns = ["Pclass", "Age", "female", "male", "Mrs.", "Miss.", "Master.", "Mr.", "alone", "not_alone", "Fare", "Survived"]
# columns = ["Pclass", "Age", "AgeRange", "Sex", "SimplifiedTitle", "SibSp", "Parch", "FamilySize", "Alone", "Status", "SimplifiedCabin", "Fare", "Embarked", "Survived"]
if "train" in file_name:
    new_data = data[columns]
else:
    features = columns.remove("Survived")
    new_data = data[columns]
new_data.to_csv("new_" + file_name)
# new_data.to_csv("analysis_" + file_name)

