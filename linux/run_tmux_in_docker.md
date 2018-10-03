在 docker container 中安装 ssh 服务 和 tmux：
```
apt install openssh tmux
service start sshserver
```

将开发机器上的 `~/.ssh/id_rsa.pub` 内容，拷贝到 docker container 的 `~/.ssh/authorized_keys` 文件中


- https://stackoverflow.com/questions/51809181/how-to-run-tmux-inside-a-docker-container
