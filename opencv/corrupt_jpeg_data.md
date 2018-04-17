ubuntu 下用 OpenCV 读 usb 相机的时候一直打印下面的错误，但测试下来，图像实际上是好的，没有损坏。
```bash
Corrupt JPEG data: 2 extraneous bytes before marker 0xd1
Corrupt JPEG data: 2 extraneous bytes before marker 0xd3
Corrupt JPEG data: 1 extraneous bytes before marker 0xd2
Corrupt JPEG data: 2 extraneous bytes before marker 0xd7
Corrupt JPEG data: 1 extraneous bytes before marker 0xd4
Corrupt JPEG data: 3 extraneous bytes before marker 0xd3
Corrupt JPEG data: 1 extraneous bytes before marker 0xd7
Corrupt JPEG data: 1 extraneous bytes before marker 0xd4
```

这个[Issue](https://github.com/opencv/opencv/issues/9477) 里面提到，这是 OpenCV 自带的 libjpeg 里的 bug，
如果使用系统自带 libjpeg 可能可以解决这个问题，具体的方法是在 CMake 里设置 `WITH_JPEG=OFF`，然后重新编译。
在我的环境下 bug 修复了，如果还有问题，可以再参考这个 [Pull Request](https://github.com/opencv/opencv/pull/9479)。
