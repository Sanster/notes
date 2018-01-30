- 抛弃 os.path.join
```python
from pathlib import Path

dir_name = "lib"
root_path = Path("/home/usr")

lib_path = root_path / dir_name

print(lib_path) # /home/usr/lib
```
