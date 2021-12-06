import random
import numpy as np
import sklearn.datasets as sd
import sklearn.model_selection as sms
import matplotlib.pyplot as plt

X, y = sd.load_svmlight_file('a9a.txt',n_features = 123)
X_train, x_test, y_train, y_test = sms.train_test_split(X, y)

X_train = X_train.toarray()
x_test = x_test.toarray()
y_train = y_train.reshape(len(y_train),1)
y_test = y_test.reshape(len(y_test),1)

X_train = np.concatenate((np.ones((X_train.shape[0],1)), X_train), axis = 1)
x_test = np.concatenate((np.ones((x_test.shape[0],1)), x_test), axis = 1)

def sigmoid(x):
    return 1/(1+np.exp(-x))

def logistic_loss(x,y,theta):
    re = sigmoid(x.dot(theta))
    loss = np.multiply((1+y),np.log(1+re)+np.multiply((1-y),np.log(1-re)))
    return  -loss.mean()/2

theta = np.zeros((X_train.shape[1],1))
loss = logistic_loss(X_train,y_train,theta)

def logistic_gradient(x,y,theta):
    return x.T.dot(sigmoid(x.dot(theta)) - y)

def logistic_score(x,y,theta):
    re = sigmoid((x.dot(theta)))
    re[re>=0.5] = 1
    re[re<0.5] = -1
    re = (re==y)
    return np.mean(re)

def logistic_descent(X, y, theta, alpha, num_iters, batch_size, X_valid, y_valid):
    loss_train = np.zeros((num_iters,1))
    loss_valid = np.zeros((num_iters,1))
    data = np.concatenate((y, X), axis=1)
    for i in range(num_iters):
        sample = np.matrix(random.sample(data.tolist(), batch_size))
        grad = logistic_gradient(sample[:,1:125], sample[:,0], theta)
        theta = theta - alpha * grad
        loss_train[i] = logistic_loss(X, y, theta)
        loss_valid[i] = logistic_loss(X_valid, y_valid, theta)
    return theta, loss_train, loss_valid

theta = np.zeros((X_train.shape[1],1))
alpha = 0.0001
num_iters = 200
uli_theta, loss_train, loss_test = logistic_descent(X_train, y_train, theta, alpha, num_iters, 64, x_test, y_test)
print(loss_train.max(), loss_train.min(), loss_test.max(), loss_test.min())

print(logistic_score(x_test,y_test,uli_theta))

iteration = np.arange(0, num_iters, step = 1)
fig, ax = plt.subplots(figsize = (12,8))
ax.set_title('Train vs Valid')
ax.set_xlabel('iteration')
ax.set_ylabel('loss')
plt.plot(iteration, loss_train, 'b', label='Training Set Loss')
plt.plot(iteration, loss_test, 'r', label='Validation Set Loss')
# plt.plot(iteration, scores, 'g', label='Score on Validation Set')
plt.legend()
plt.show()

def hinge_loss(X, y, theta, C):
    loss = np.maximum(0, 1 - np.multiply(y, X.dot(theta))).mean()
    reg = np.multiply(theta,theta).sum() / 2
    return C * loss + reg

theta = np.random.random((X_train.shape[1],1))
C = 0.4
hinge_loss(X_train, y_train, theta, C)

def hinge_gradient(X, y, theta, C):
    error = np.maximum(0, 1 - np.multiply(y, X.dot(theta)))
    index = np.where(error==0)
    x = X.copy()
    x[index,:] = 0
    grad = theta - C * x.T.dot(y) / len(y)
    grad[-1] = grad[-1] - theta[-1]
    return grad

def svm_descent(X, y, theta, alpha, num_iters, batch_size, X_valid, y_valid, C):
    loss_train = np.zeros((num_iters,1))
    loss_valid = np.zeros((num_iters,1))
    data = np.concatenate((y, X), axis=1)
    for i in range(num_iters):
        sample = np.matrix(random.sample(data.tolist(), batch_size))
        grad = hinge_gradient(sample[:,1:125], sample[:,0], theta, C)
        theta = theta - alpha * grad
        loss_train[i] = hinge_loss(X, y, theta, C)
        loss_valid[i] = hinge_loss(X_valid, y_valid, theta, C)
    return theta, loss_train, loss_valid

def svm_score(X, y, theta):
    hx = X.dot(theta)
    hx[hx>=5] = 1
    hx[hx<5] = -1
    hx = (hx==y)
    return np.mean(hx)

theta = np.random.random((X_train.shape[1],1))
alpha = 0.01
num_iters = 500
uli_theta, loss_train, loss_valid = svm_descent(X_train, y_train, theta, alpha, num_iters, 64, x_test, y_test, C)
print(loss_train.max(), loss_train.min(), loss_valid.max(), loss_valid.min())

print(svm_score(x_test,y_test,uli_theta))

iteration = np.arange(0, num_iters, step = 1)
fig, ax = plt.subplots(figsize = (12,8))
ax.set_title('Train vs Valid')
ax.set_xlabel('iteration')
ax.set_ylabel('loss')
plt.plot(iteration, loss_train, 'b', label='Training Set Loss')
plt.plot(iteration, loss_valid, 'r', label='Validation Set Loss')
plt.legend()
plt.show()

