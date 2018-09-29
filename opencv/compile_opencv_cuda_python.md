```
git clone https://github.com/opencv/opencv
cd opencv
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D WITH_CUDA=ON \
      -D ENABLE_FAST_MATH=1 \
      -D CUDA_FAST_MATH=1 \
      -D WITH_CUBLAS=1 \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D BUILD_EXAMPLES=OFF \
      -D INSTALL_C_EXAMPLES=OFF \
      -D BUILD_opencv_python2=OFF \
      -D BUILD_opencv_python3=ON \
      -D PYTHON3_EXECUTABLE=/usr/bin/python3 \
      -D PYTHON3_INCLUDE_DIR=/usr/include/python3.5m \
      -D PYTHON3_LIBRARY=/usr/lib/python3.5 ..
      
make -j4
make install
```
