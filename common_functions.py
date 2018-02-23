from sklearn.preprocessing import OneHotEncoder


def separate_features_and_classes(samples):
    features = []
    classes = []
    for sample in samples:
        classes.append(sample[0])
        features.append(sample[1:])
    return features, classes

def read_file(file_name):
    with open(file_name) as f:
        samples = f.readlines()
    return samples

def clean_samples(samples):
    cleaned_samples = []
    for sample in samples:
        aux = sample.replace('\n', '')
        aux = aux.split(',')
        aux = list(map(int, aux))
        ids = aux[0]
        survived = aux[1]
        pclass = aux[2]
        simplified_title = aux[3]
        status = aux[4]
        sex = aux[5]
        age = aux[6]
        sibsps = aux[7]
        parchs = aux[8]
        cabin = aux[9]
        enbarked = aux[10]
        cleaned_samples.append([survived, pclass, simplified_title, status, sex,
                                age, sibsps, parchs, cabin, enbarked])

    # deal with categorical data
    encoder = OneHotEncoder(categorical_features = [1, 2, 3, 4, 8, 9]) # pclass, titles, status, sex
    cleaned_samples = encoder.fit_transform(cleaned_samples).toarray()
    return cleaned_samples
