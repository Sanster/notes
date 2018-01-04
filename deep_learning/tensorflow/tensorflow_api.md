## tf.nn.in_top_k()

A 为预测结果，B 为 label 集合

k 表示： A[0][B[0]]（A[1][B[1]]）的值是否属于 A[0](A[1]) 中的 Top k 值

```python
import tensorflow as tf;
  
A = [[0.8,0.6,0.3], [0.1,0.6,0.4]]  
B = [1, 1]  
out = tf.nn.in_top_k(A, B, 1)  
out2 = tf.nn.in_top_k(A, B, 2) 
with tf.Session() as sess:  
    sess.run(tf.initialize_all_variables())  
    print(sess.run(out))  # [False, True]
    print(sess.run(out2))  # [True, True]
```
