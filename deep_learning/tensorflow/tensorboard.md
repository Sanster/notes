- 不运行 sess.run()，向 summary 中直接添加 python 变量值
```python
writer = tf.summary.FileWriter(...)
val = 10
summary = tf.Summary(value=[
    tf.Summary.Value(tag="tab_name", simple_value=val),
])
writer.add_summary(summary, global_step)
```
