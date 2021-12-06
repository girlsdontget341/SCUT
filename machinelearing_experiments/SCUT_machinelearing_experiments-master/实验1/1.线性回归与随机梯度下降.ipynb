import numpy as np
import sklearn.datasets as sd
import sklearn.model_selection as sms
import matplotlib.pyplot as plt

X, y = sd.load_svmlight_file('housing.txt',n_features = 13)
X_train, x_test, y_train, y_test = sms.train_test_split(X, y)

X_train = X_train.toarray()
x_test = x_test.toarray()
y_train = y_train.reshape(len(y_train),1)
y_test = y_test.reshape(len(y_test),1)

#闭式解
theta = np.zeros((14,1))

def compute_loss(x,y,theta):
    re = x.dot(theta)
    error = np.power((re-y),2).mean()/2
    return error

X_train = np.concatenate((np.ones((X_train.shape[0],1)), X_train), axis = 1)
x_test = np.concatenate((np.ones((x_test.shape[0],1)), x_test), axis = 1)

loss = compute_loss(X_train,y_train,theta)

def normal_equation(X, y):
    return (np.linalg.inv(X.T.dot(X))).dot(X.T).dot(y)

theta = normal_equation(X_train, y_train)
print(theta)

loss_train = compute_loss(X_train, y_train,theta)
print(loss_train)

loss_test = compute_loss(x_test, y_test, theta)
print(loss_test)

#梯度下降
def gradient(x,y,theta):
    return x.T.dot(x.dot(theta)-y)

def desc(x,y,theta, alpha, iters, x_test, y_test):
    loss_train = np.zeros((iters,1))
    loss_test = np.zeros((iters,1))
    for i in range(iters):
        grad = gradient(x,y,theta)
        theta = theta - alpha*grad
        loss_train[i] =compute_loss(x,y,theta)
        loss_test[i] = compute_loss(x,y,theta)
    return theta, loss_train,loss_test

theta = np.zeros((14,1))
alpha = 0.001
iters = 25
opt_theta, loss_train, loss_valid = desc(X_train, y_train, theta, alpha, iters, x_test, y_test)
print(loss_train.min(), loss_valid.min())

iteration = np.arange(0, iters, step = 1)
fig, ax = plt.subplots(figsize = (12,8))
ax.set_title('Train')
ax.set_xlabel('iteration')
ax.set_ylabel('loss')
plt.plot(iteration, loss_train, 'b', label='Train')
# plt.plot(iteration, loss_valid, 'r', label='Valid')
plt.legend()
plt.show()


