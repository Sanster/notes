import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # 初始化梯度矩阵，每一列代表一个类别的向量
  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  delta = 1
    
  for i in range(num_train):
    # scores shape (10, )
    scores = X[i].dot(W)
    correct_class_score = scores[y[i]]
    
    for j in range(num_classes):
      # 忽略当前样本正确的分类结果
      if j == y[i]:
        continue
        
      # 计算其它所有类别的分数到正确类别的分数差 margin，其他类别的分数不应该大于当前正确类别的分数
      # delta 代表想要正确的 class score 与其他类的 score 有一定的间距
      margin = scores[j] - correct_class_score + delta
      if margin > 0:
        loss += margin
        
        # 梯度的公式见：svm_gradient.ipynb
        # correct class gradient part
        dW[:, y[i]] += -X[i]
        # incorrect class gradient part
        dW[:, j] += X[i]
      else:
        # margin < 0 从梯度的公式上可以看出，梯度都是 0，所以不需要任何操作
        pass
    
  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW /= num_train

  # Add regularization to the loss.
  loss += reg * np.sum(W * W)
  # Add regularization to the gradient
  dW += reg * W

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################


  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  # X shape (500, 3073)
  print('X.shape', X.shape)
  num_train = X.shape[0]
  num_classes = W.shape[1]
  delta = 1
  scores = X.dot(W) 
  print('scores shape:', scores.shape) # (500, 10)
  print('y shape:', y.shape) # (500, )
  
  correct_class_scores = scores[range(num_train), list(y)].reshape(-1,1) #(N, 1)
  print('correct_class_scores.shape', correct_class_scores.shape)
  
  margins = np.maximum(0, scores - correct_class_scores + delta)
  print('margins.shape', margins.shape)
  # 因为有 delta 的存在，所以这里要赋值 0，消除正确类的影响
  margins[range(num_train), list(y)] = 0
  loss = np.sum(margins) / num_train + reg * np.sum(W * W)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  # (500， 10)
  coeff_mat = np.zeros((num_train, num_classes))
  # 所有需要参与 loss 计算的位置记为 1，对应于梯度公式中对  w_j 求导
  coeff_mat[margins > 0] = 1
  
  # 对应梯度公式中对 w_{y_i} 求导
  coeff_mat[range(num_train), list(y)] = 0
  # 这一步比较难懂，对于 w_{y_i} 来说，要看 j!=y_i 时 margins > 0 j 的个数，所以这里要 sum
  coeff_mat[range(num_train), list(y)] = -np.sum(coeff_mat, axis=1)
  
  # X.T shape (3073, 500)
  # coeff_mat shape (500, 10)
  dW = (X.T).dot(coeff_mat)
  dW = dW/num_train + reg*W
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
