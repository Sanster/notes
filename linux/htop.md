## 字段含义
- PRI：进程的优先级别
- NI：进程的优先级别数值
- VIRT：进程占用的虚拟内存值
- RES：进程占用的物理内存值
- SHR：进程使用的共享内存值
- S：进程的状态，其中S表示休眠，R表示正在运行，Z表示僵死状态，N表示该进程优先值是负数
- CPU%：该进程占用的CPU使用率
- MEM%：该进程占用的物理内存和总内存的百分比
- TIME+：该进程启动后占用的总的CPU时间
- Command：进程启动的启动命令名称

## 有多个同名进程
使用`H`只显示主进程
[why-are-there-many-processes-listed-under-the-same-title-in-htop](https://superuser.com/questions/118086/why-are-there-many-processes-listed-under-the-same-title-in-htop)
