手头有个 Polycom 的摄像头，用 videocapture 读取视频流时摄像头报错：
```bash
VIDEOIO ERROR: V4L2: Pixel format of incoming image is unsupported by OpenCV
```

使用 v4l 查看摄像头的视频流格式，发现是 YU12 格式：
```bash
# sudo apt install v4l-util
v4l2-ctl -d /dev/video0 --list-formats

ioctl: VIDIOC_ENUM_FMT
	Index       : 0
	Type        : Video Capture
	Pixel Format: 'YU12'
	Name        : Planar YUV 4:2:0
```

要读取 YUV 格式的视频流，开启下面两个选项重新编译下 opencv：

- WITH_V4L=ON
- WITH_LIBV4L=ON

参考：
- https://github.com/opencv/opencv/issues/7974
