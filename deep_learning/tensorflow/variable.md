**Tensorflow api：r1.4v**

两种创建变量的方式：
- tf.Variable()：永远是创建一个新的变量，如果和已经存在的变量重名，tensorflow 会自动加上后缀
- tf.get_variable()：可以通过在 variable_scope 上设置 `reuse=tf.AUTO_REUSE` 来获得一个之前已经创建的变量

两种 scope：
- tf.name_scope：对 tf.get_variable() 不起作用，不会给他加上前缀
- tf.variable_scope：可以 reuse 变量

```python
import tensorflow as tf

with tf.name_scope("name_scope"):
    initializer = tf.constant_initializer(value=1)
    var1 = tf.get_variable(name='var1', shape=[1], dtype=tf.float32, initializer=initializer)
    var2 = tf.Variable(name='var2', initial_value=[2], dtype=tf.float32)
    var21 = tf.Variable(name='var2', initial_value=[2.1], dtype=tf.float32)
    var22 = tf.Variable(name='var2', initial_value=[2.2], dtype=tf.float32)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(var1.name)  # var1:0 get_variable() 不受 name_scope 影响
    print(var2.name)  # a_name_scope/var2:0
    print(var21.name)  # a_name_scope/var2_1:0
    print(var22.name)  # a_name_scope/var2_2:0  tf.Variable 无法获得已经定义的变量，tf 会自动加上后缀

with tf.variable_scope("variable_scope", reuse=tf.AUTO_REUSE) as scope:
    initializer = tf.constant_initializer(value=3)
    var3 = tf.get_variable(name='var3', shape=[1], dtype=tf.float32, initializer=initializer)
    var3_reuse = tf.get_variable(name='var3')
    var4 = tf.Variable(name='var4', initial_value=[4], dtype=tf.float32)
    var4_reuse = tf.Variable(name='var4', initial_value=[4], dtype=tf.float32)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(var3.name)  # a_variable_scope/var3:0
    print(var3_reuse.name)  # a_variable_scope/var3:0
    # Variable 无法 reuse 变量，依然会创建新的变量
    print(var4.name)  # a_variable_scope/var4:0
    print(var4_reuse.name)  # a_variable_scope/var4_1:0
```
