- 进入 pdb 环境：
```python
import pdb
....
pdb.set_tract()
```
- `l`：查看前后 11 行源代码
- `ll`：查看当前函数所有的源代码
- `p expression`：打印变量值
- `s`：单步调试，能进入函数体
- `n`：单步调试，不进入函数体
- `r`：直接执行到函数返回处
- `unt lineno`：执行到指定的行
- `j lineno`：调到指定地行，不会执行中间的代码
- `a`：在函数中时打印函数的参数和参数的值
- `whatis expression`：打印表达式的类型
- `interact`：使用当前的 context 进入交互解释器
- `q`：退出
