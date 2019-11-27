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
    return int(younger_people["Age"].mean())


def mean_age_older_people(data):
    older_people = data[data["Title"].isin(["Mr.", "Mrs."])]
    older_people = older_people.dropna(subset=["Age"])
    return int(older_people["Age"].mean())


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


file_name = "test.csv"
data = pd.read_csv(file_name)

data["Title"] = data.apply(lambda row: name_to_title(row), axis = 1)
data["SimplifiedTitle"] = data.apply(lambda row: simplify_title(row), axis = 1)
data["Status"] = data.apply(lambda row: define_status(row), axis = 1)
data["SimplifiedCabin"] = data.apply(lambda row: simplify_cabin(row), axis = 1)
fill_missing_ages(data)
fill_missing_fares(data)

# deal with categorical data
dummy_sex = pd.get_dummies(data["Sex"])
dummy_status = pd.get_dummies(data["Status"])
dummy_cabin = pd.get_dummies(data["SimplifiedCabin"])
data = pd.concat([data, dummy_sex, dummy_status, dummy_cabin], axis=1)

# new columns
data["FamilySize"] = data.apply(lambda row: row.Parch + row.SibSp, axis=1)
data["Alone"] = data.apply(lambda row: 0 if row.FamilySize else 1, axis=1)

# save file with columns that will be used
columns = ["Pclass", "Age", "female", "male", "SibSp", "Parch", "Alone", "married", "single", "A", "B", "C", "D", "E", "F", "G", "U", "Fare", "Survived"]
if "train" in file_name:
    new_data = data[columns]
else:
    features = columns.remove("Survived")
    new_data = data[columns]
new_data.to_csv("new_" + file_name)

