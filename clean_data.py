from sklearn.preprocessing import LabelEncoder


csv = 'C:/Users/Manu/Documents/Python/ProjetosImagens/Titanic2/test.csv'
cleaned_csv = 'C:/Users/Manu/Documents/Python/ProjetosImagens/Titanic2/test_cleaned.csv'

with open(csv) as f:
    samples = f.readlines()
samples = samples[1:]
# print (samples)

cleaned_samples = []
for sample in samples:
    aux = sample.replace('\n', '')
    aux = aux.split(';')
    cleaned_samples.append(aux)
# print(cleaned_samples)

# transpose data
samples = [list(i) for i in zip(*cleaned_samples)]
# print(samples)

ids = samples[0]
survived = samples[1]
pclass = samples[2]
name = samples[3]
sex = samples[4]
age = samples[5]
sibsps = samples[6]
parchs = samples[7]
tickets = samples[8]
fare = samples[9]
cabin = samples[10]
enbarked = samples[11]

encoder = LabelEncoder() # encode categorical data

# --- ids ---
ids = list(map(int, ids))
# print(ids)

# --- survived ---
if survived[0] != '':
    survived = list(map(int, survived))
else:
    survived = [3] * len(survived)
# print(survived)

# --- pclass ---
pclass = list(map(int, pclass))
# print(pclass)

# --- names ---
# get titles
title = []
options = ['Mrs', 'Mr', 'Master', 'Miss', 'Major', 'Rev', 'Dr', 'Ms', 'Mlle',
           'Col', 'Capt', 'Mme', 'Countess', 'Don', 'Jonkheer']
for x in name:
    for y in options:
        if y in x:
            title.append(y)
# print(title)

# simplify titles: Mr, Mrs, Mister, Miss
simplified_title = []
for x, y in zip(title, sex):
    if x in ['Don', 'Major', 'Capt', 'Jonkheer', 'Rev', 'Col']:
        simplified_title.append(0) # Mr
    elif x in ['Countess', 'Mme']:
        simplified_title.append(1) # Mrs
    elif x in ['Master']:
        simplified_title.append(2) # Master
    elif x in ['Mlle', 'Ms']:
        simplified_title.append(3) # Miss
    elif x =='Dr':
        if y == 'Male':
            simplified_title.append(0)
        else:
            simplified_title.append(1)
    else:
        simplified_title.append(4)
# print(simplified_title)

# create new feature: 1 - married, 0 - single
status = []
for x in simplified_title:
    if x in [0, 1]: # Mr or Mrs
        status.append(1)
    else:
        status.append(0)
# print(status)

# --- sex ---
sex = encoder.fit_transform(sex)
# print(sex)

# --- age ---
# get average age for kids and adults
kids = []
adults = []
for x in age:
    if x != '':
        if float(x) < 16:
            kids.append(x)
        else:
            adults.append(x)
kids = list(map(float, kids))
adults = list(map(float, adults))
avg_kids = int(sum(kids) / len(kids))
avg_adults = int(sum(adults) / len(adults))
# print(avg_kids, avg_adults)

# put average age where ages are missing
aux = []
for x, y in zip(age, simplified_title):
    if x == '':
        if y in [0, 1]:
            aux.append(avg_adults)
        else:
            aux.append(avg_kids)
    else:
        aux.append(float(x))
age = list(map(int, aux))
# print(age)

# --- sibsps ---
sibsps = list(map(int, sibsps))
# print(sibsps)

# --- parchs ---
parchs = list(map(int, parchs))
# print(parchs)

# --- cabin ---
aux = []
for x in cabin:
    if x != '':
        if 'A' in x:
            aux.append(1)
        elif 'B' in x:
            aux.append(2)
        elif 'C' in x:
            aux.append(3)
        elif 'D' in x:
            aux.append(4)
        elif 'E' in x:
            aux.append(5)
        elif 'F' in x:
            aux.append(6)
        elif 'G' in x:
            aux.append(7)
        elif 'T' in x:
            aux.append(8)
        else:
            aux.append(0)
    else:
        aux.append(0)
cabin = aux
# print(cabin)

# --- enbarked ---
enbarked = encoder.fit_transform(enbarked)
# print(enbarked)

cleaned_features = [ids, survived, pclass, simplified_title, status, sex, age, sibsps,
                    parchs, cabin, enbarked]
samples = [list(i) for i in zip(*cleaned_features)]
# print(samples)

# save cleaned csv
file = open(cleaned_csv, 'w')
for sample in samples:
    aux = str(sample)
    file.write(aux[1:-1])
    file.write('\n')
file.close()
