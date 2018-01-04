**不运行 sess.run()，向 summary 中直接添加 python 变量值**

```python
writer = tf.summary.FileWriter(...)
val = 10
summary = tf.Summary(value=[
    tf.Summary.Value(tag="tab_name", simple_value=val),
])
writer.add_summary(summary, global_step)
```

**同一个 plot 中画多条线**
- 用处：用在比较 test 和 val 数据集的精度和误差
- 方法：定义两个 writer，向不同的文件中写入 summary，写入的 tag 一样

```python
import tensorflow as tf
from numpy import random

writer_1 = tf.summary.FileWriter("./logs/plot_1")
writer_2 = tf.summary.FileWriter("./logs/plot_2")

log_var = tf.Variable(0.0)
tf.summary.scalar("loss", log_var)

write_op = tf.summary.merge_all()

session = tf.InteractiveSession()
session.run(tf.global_variables_initializer())

for i in range(100):
    # for writer 1
    summary = session.run(write_op, {log_var: random.rand()})
    writer_1.add_summary(summary, i)
    writer_1.flush()

    # for writer 2
    summary = session.run(write_op, {log_var: random.rand()})
    writer_2.add_summary(summary, i)
    writer_2.flush()
```

