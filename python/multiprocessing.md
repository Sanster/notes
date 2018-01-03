向目标函数传递多个参数：
```python
from itertools import repeat
from multiprocessing import Pool

def func(p1, p2):
    print(p1+p2)

if __name__ == '__main__':
    with Pool(processes=8) as pool:
        # [(1,0), (1,1), ..., (1, 9)]
        pool.starmap(func, zip(repeat(1), range(10)))
```
