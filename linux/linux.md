- 查看是否一个 library 已经安装：`ldconfig -p | grep library_name`
- 从命令行查看图片：`eog filename`
- samba 服务安装：https://draapho.github.io/2017/07/06/1718-linux-samba/
- 统计目录中包含的文件个数：`ls -l | grep "^-" | wc -l`
- 统计目录中包含的目录个数：`ls -l | grep "^d" | wc -l`
- 递归统计当前文件夹中的文件数量：`ls -lR |grep "^-"|wc -l`
- 命令行的输出直接拷贝到 clipboard：
Linux 有两种 clipboard： PRIMARY (Ctrl-X/C/V) 和 SELECTION (mouse selected text, inserted with Shift-Insert or clicking the mouse middle button），通过下面的命令可以把命令行的输出同时拷贝到两种 clipboard 上：
`echo "Hello world" | xclip -i selection primary | xclip -i selection clipboard`
- 查看当前文件夹大小：`du -h --max-depth=1`
- 查看显卡：`lspci  | grep -i vga`
- 压缩文件夹：`zip -r myfile.zip ./test_dir`
- 压缩文件：`zip myfile.zip ./test.txt`
- 命令行查看 json：
  - `apt-get install yajl-tools`. 
  - `echo '{"b":2, "a":1}' | json_reformat`
- 查看多个进程的内存总量：`top -b -n1 | grep chrome | awk '{ SUM += $9} END { print SUM }'`，`$6` 代表第6列(RES)的
- 如何把服务器上的字符串拷贝到本机的剪贴板： 
  - 参考 https://gist.github.com/dergachev/8259104
  - 本机启动：while (true); do nc -l 5556 | tr -d '\n' | pbcopy; done
  - .zshrc 里面设置：nc -q0 xxx.xx.xx.xx 5556
- 删除当前目录下所有的文件夹：`rm -R -- */` https://unix.stackexchange.com/questions/68846/how-do-i-remove-all-sub-directories-from-within-a-directory/68847
