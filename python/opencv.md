- 两张图片平成一张图片，numpy 数据类型应为 int
```python
# 竖直方向，上下拼
result = np.concatenate((img1, img2), axis=0)

# 水平方向，左右拼
result = np.concatenate((img1, img2), axis=1)
```
