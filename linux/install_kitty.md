官方安装指导：https://sw.kovidgoyal.net/kitty/binary.html

安装完以后，运行 kitty 会报错： 
```
ImportError: /home/<my_user>/Desktop/kitty-0.12.0-x86_64/bin/../lib/libharfbuzz.so.0: undefined symbol: FT_Get_Var_Blend_Coordinates
```

原因是 freetype 版本太老了，ubuntu 16.04 默认是 2.6.1 的，参考这个[链接](http://ubuntuhandbook.org/index.php/2017/06/install-freetype-2-8-in-ubuntu-16-04-17-04/)中
安装新版本：
```bash
sudo add-apt-repository ppa:glasen/freetype2
sudo apt update && sudo apt install freetype2-demos
```
