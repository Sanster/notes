Tensorflow error:
```
...
libnvidia-fatbinaryloader.so.384.111 not found
...
```

Show current version:
```
apt-cache policy nvidia-384
```

Show available versions:
```
apt-cache show nvidia-384
```

Install driver version required by Tensorflow:
```
sudo apt install nvidia-384=384.111-0ubuntu0.16.04.1
```

- Install CUDA: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu-installation
- Install cuDNN: https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html
