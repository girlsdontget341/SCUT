
import numpy as np
import pandas as pd
import sklearn as sk
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import os
from PIL import Image
import matplotlib.pyplot as plt
import pickle
import cv2 as cv
import random
from feature import NPDFeature
from ensemble import AdaBoostClassifier

facePath = 'C:\\Users\\86130\\PycharmProjects\\machine_learning_lab3\\datasets\\original\\face\\'
nonfacePath = 'C:\\Users\\86130\\PycharmProjects\\machine_learning_lab3\\datasets\\original\\nonface\\'

face_data_file = 'C:\\Users\\86130\\PycharmProjects\\machine_learning_lab3\\datasets\\original\\face_data.txt'
nonface_data_file = 'C:\\Users\\86130\\PycharmProjects\\machine_learning_lab3\\datasets\\original\\nonface_data.txt'

def dumpFeatures(path, label = 1):
    img_names = os.listdir(path)
    file = ''
    if label == 1:
        file = face_data_file
    else:
        file = nonface_data_file
    write = open(file, 'wb')
    feat = []
    for name in img_names:
        img_gray = cv.imread(path+name, cv.IMREAD_GRAYSCALE)
        img_resize = cv.resize(img_gray, (24,24))
        npd = NPDFeature(img_resize)
        feat.append(npd.extract())
    pickle.dump(feat, write)

def loadFeatures(filename):
    read = open(filename, 'rb')
    data = pickle.load(file=read)
    return np.matrix(data)

def addLabel(data, label):
    data = np.matrix(data)
    return np.concatenate((np.full(shape=(data.shape[0],1),fill_value=label), data), axis=1)

def split_train_valid(data, fraction = 0.9):
    data = np.matrix(data)
    return sk.model_selection.train_test_split(data[:,0],data[:,1:data.shape[1]],train_size=fraction, test_size=1-fraction)

dumpFeatures(facePath, label=1)
dumpFeatures(nonfacePath, label=0)




if __name__ == "__main__":
    face_data = loadFeatures(face_data_file)
    nonface_data = loadFeatures(nonface_data_file)

    face_data = addLabel(face_data, 1)
    nonface_data = addLabel(nonface_data, 0)

    print(face_data.shape)
    print(nonface_data.shape)

    data = np.concatenate((face_data, nonface_data), axis=0)

    fraction = 0.9
    X_train, X_valid, y_train, y_valid = sk.model_selection.train_test_split(data[:, 1:data.shape[1]], data[:, 0],
                                                                             train_size=fraction,
                                                                             test_size=1 - fraction)

    X_train = np.matrix(X_train)
    X_valid = np.matrix(X_valid)
    y_train = np.matrix(y_train)
    y_valid = np.matrix(y_valid)

    print(X_train.shape, X_valid.shape, y_train.shape, y_valid.shape)
    print(np.sum(y_train == 1), np.sum(y_valid == 1))

    weight = np.full(shape=(X_train.shape[0]), fill_value=1 / X_train.shape[0])
    weak_classifier = DecisionTreeClassifier()

    # weak_classifier.fit(X_train, y_train, sample_weight=weight)
    # train_score = weak_classifier.score(X_train, y_train)
    # valid_score = weak_classifier.score(X_valid, y_valid)

    classifier = AdaBoostClassifier(weak_classifier, 10)
    classifier.fit(X_train, y_train)
    # hx = classifier.predict(X_valid)
    train_score = classifier.predict_scores(X_train, y_train)
    valid_score = classifier.predict_scores(X_valid, y_valid)

    print('{}, {}'.format(train_score, valid_score))

    hx = classifier.predict(X_valid)
    print(hx)
    report_file = 'C:\\Users\\86130\\PycharmProjects\\machine_learning_lab3\\report.txt'
    file_write = open(report_file, 'wb')
    print(classification_report(y_valid, hx))
    reportContent = 'Accuracy = ' + '\n'
    reportContent += classification_report(y_valid, hx)
    with open(report_file, 'w') as report:
        report.write(reportContent)


