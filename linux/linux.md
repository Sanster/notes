- 查看是否一个 library 已经安装：`ldconfig -p | grep library_name`
- 从命令行查看图片：`eog filename`
- samba 服务安装：https://draapho.github.io/2017/07/06/1718-linux-samba/
- 统计目录中包含的文件个数：`ls -l | grep "^-" | wc -l`
- 统计目录中包含的目录个数：`ls -l | grep "^d" | wc -l`
- 命令行的输出直接拷贝到 clipboard：
Linux 有两种 clipboard： PRIMARY (Ctrl-X/C/V) 和 SELECTION (mouse selected text, inserted with Shift-Insert or clicking the mouse middle button），通过下面的命令可以把命令行的输出同时拷贝到两种 clipboard 上：
`echo "Hello world" | xclip -i selection primary | xclip -i selection clipboard`
