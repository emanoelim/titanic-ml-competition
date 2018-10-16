from pandas import read_csv


def name_to_tile(row):
    name = row["Name"]
    titles = ['Mrs.', 'Mr.', 'Master.', 'Miss.', 'Major.', 'Rev.', 'Dr.', 'Ms.', 'Mlle.', 'Col.', 'Capt.', 'Mme.',
              'Countess.', 'Don.', 'Jonkheer.']
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
    title = row["Simplified_title"]
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


file_name = "train.csv"
data = read_csv(file_name)

# deal with missing ages
mean_age = data["Age"].mean()
data["Age"] = data["Age"].fillna(mean_age)

# deal with missing fares
mean_fare = data["Fare"].mean()
data["Fare"] = data["Fare"].fillna(mean_fare)

# new features
data["Title"] = data.apply(lambda row: name_to_tile(row), axis = 1)
data["Simplified_title"] = data.apply(lambda row: simplify_title(row), axis = 1)
data["Status"] = data.apply(lambda row: define_status(row), axis = 1)
data["Simplified_cabin"] = data.apply(lambda row: simplify_cabin(row), axis = 1)

# deal with categorical data
data["Status"] = data["Status"].astype('category')
data["Simplified_cabin"] = data["Simplified_cabin"].astype('category')

data["Status"] = data["Status"].cat.codes
data["Simplified_cabin"] = data["Simplified_cabin"].cat.codes

# save file with featuras that will be used
if "train" in file_name:
    new_data = data[["Pclass", "Age", "SibSp", "Parch", "Fare", "Status", "Simplified_cabin", "Survived"]]
else:
    new_data = data[["Pclass", "Age", "SibSp", "Parch", "Fare", "Status", "Simplified_cabin"]]
new_data.to_csv("new_" + file_name)

