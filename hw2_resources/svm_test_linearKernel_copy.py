from numpy import *
from plotBoundary import *
import pylab as pl
import Problem2 as p2
import cvxopt as opt
import numpy as np

# parameters
def wrapper_linear(data, C):
    # print '======Training======'
    # load data from csv files
    # train = loadtxt('data/data'+name+'_train.csv')
    # use deep copy here to make cvxopt happy
    X_train = data["Xtrain"]
    Y_train = data["Ytrain"]

    print X_train.shape, Y_train.shape

    # Define parameters

    K = p2.linear_gram(X_train)
    
    def column_kernel(SVM_X,x):
        '''
        Given an array of X values and a new x to predict, 
        computes the  vector whose i^th entry is k(SVM_X[i],x)
        '''
        def k(y):
            #return np.dot(x,y) # returns the identity kernel
        
            return (1+np.dot(x,y)) # returns the linear basis kernel
            
        return np.apply_along_axis(k, 1, SVM_X ).reshape(-1,1)
    
    # Carry out training, primal and/or dual
    a, SVM_alpha, SVM_X, SVM_Y, support = p2.dual_SVM(X_train, Y_train, C, K)
    print "a", np.min(a), np.max(a)
    def get_prediction_constants():
        ay = SVM_alpha*SVM_Y
        # get gram matrix for only support X values
        SVM_K = K[support]
        SVM_K = SVM_K.T[support]
        SVM_K = SVM_K.T
    
        # compute bias
        bias = np.nansum([SVM_Y[i] - np.dot(ay.T, SVM_K[i]) for i in range(len(SVM_Y))]) / len(SVM_Y)
    
        return ay, bias
    
    # Define the predictSVM(x) function, which uses trained parameters
    # Define the predict_gaussianSVM(x) function, which uses trained parameters, alpha
    
    ay, bias = get_prediction_constants()
    print bias
    
    def predictSVM(x):
        '''
        The predicted value is given by h(x) = sign( sum_{support vectors} alpha_i y_i k(x_i,x) )
        '''
        debug = False
    
        x = x.reshape(1, -1)
        if debug: print 'Classify x: ',x
        
        # predict new Y output
        kernel = column_kernel(SVM_X, x)
        y = np.dot(ay.T, kernel)
        if debug:
            print 'New y ', y
        return y + bias
    
    def classification_error(X, Y):
        ''' Computes the error of the classifier on some training set'''
        n,d = X.shape
        incorrect = 0.0
        for i in range(n):
            if predictSVM(X[i]) * Y[i] < 0:
                incorrect += 1
        return incorrect/n
        
    train_err = classification_error(X_train, Y_train)
    # plot training results
    # plotDecisionBoundary(X, Y, predictSVM, [-1, 0, 1], title = 'MNIST SVM Train on dataset '+str(name)+' with C = '+str(C))
    # pl.savefig('MNIST_prob2linear_kernelSVMtrain_'+str(name)+'_with C='+str(C)+'.png')
    
    # print '======Validation======'
    # load data from csv files
    # validate = loadtxt('data/data'+name+'_validate.csv')
    X_validate = data["Xvalidate"]
    Y_validate = data["Yvalidate"]

    validation_err = classification_error(X_validate, Y_validate)
    print C, "validation", validation_err
    
    # plot validation results
    plotDecisionBoundary(X_train, Y_train, predictSVM, [-1, 0, 1], title = 'MNIST SVM Validate on dataset '+' with C = '+str(C))
    pl.savefig('MNIST_prob2linear_kernelSVMvalidate_'+'_with C='+str(C)+'.png')
    pl.show()

    # print '======Testing======'
    X_test = data["Xtest"]
    Y_test = data["Ytest"]
    
    testing_error = classification_error(X_test, Y_test)
    print C, "testing", testing_error

    # f = open('errors for linear kernel dataset '+str(name)+' with C = '+str(C)+'.txt', 'w')
    # f.write('Train err: ')
    # f.write(str(train_err))
    # f.write('\n')
    # f.write('Validate err: ')
    # f.write(str(validation_err))
    # f.write('Testing err: ')
    # f.write(str(testing_error))
    # f.write('\n')
    # f.write('Number of SVMs: ')
    # f.write(str(len(SVM_Y)))
    # f.close()

    return [C, validation_err, testing_error]
    
    # print 'Done plotting...'
    

# for C in [0.001, 0.01, 1, 10, 100]:
#     for name in ['1','2','3']:
#         wrapper_linear(name, C)
    
    
