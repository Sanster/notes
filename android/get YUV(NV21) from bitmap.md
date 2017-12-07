`getNV21()` 输入图像的长宽都不能是奇数，先调用 cropBitmap 裁剪
```java
Bitmap croppedBitmap = cropBitmap(img);
byte[] data = getNV21(croppedBitmap);
```

```java
    Bitmap cropBitmap(Bitmap img) {
        if (img.getHeight() % 2 > 0 || img.getWidth() % 2 > 0) {
            return Bitmap.createBitmap(img, 0, 0, img.getWidth() / 2 * 2, img.getHeight() / 2 * 2);
        }
        return img;
    }
    
    byte[] getNV21(Bitmap img) {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] argb = new int[width * height];
        img.getPixels(argb, 0, width, 0, 0, width, height);
        
        // 如果 height 和 width 都为奇数，则 yuv 会比原图小
        byte[] yuv = new byte[width * height * 3 / 2];
        encodeYUV420SP(yuv, argb, width, height);

        return yuv;
    }

    void encodeYUV420SP(byte[] yuv420sp, int[] argb, int width, int height) {
        final int frameSize = width * height;

        int yIndex = 0;
        int uvIndex = frameSize;

        int a, R, G, B, Y, U, V;
        int index = 0;
        for (int j = 0; j < height; j++) {
            for (int i = 0; i < width; i++) {

                a = (argb[index] & 0xff000000) >> 24; // a is not used obviously
                R = (argb[index] & 0xff0000) >> 16;
                G = (argb[index] & 0xff00) >> 8;
                B = (argb[index] & 0xff) >> 0;

                // well known RGB to YUV algorithm
                Y = ((66 * R + 129 * G + 25 * B + 128) >> 8) + 16;
                U = ((-38 * R - 74 * G + 112 * B + 128) >> 8) + 128;
                V = ((112 * R - 94 * G - 18 * B + 128) >> 8) + 128;

                // NV21 has a plane of Y and interleaved planes of VU each sampled by a factor of 2
                //    meaning for every 4 Y pixels there are 1 V and 1 U.  Note the sampling is
                // every other
                //    pixel AND every other scanline.
                yuv420sp[yIndex++] = (byte) ((Y < 0) ? 0 : ((Y > 255) ? 255 : Y));
                if (j % 2 == 0 && index % 2 == 0) {
                    yuv420sp[uvIndex++] = (byte) ((V < 0) ? 0 : ((V > 255) ? 255 : V));
                    yuv420sp[uvIndex++] = (byte) ((U < 0) ? 0 : ((U > 255) ? 255 : U));
                }

                index++;
            }
        }
    }
```

参考：https://stackoverflow.com/questions/5960247/convert-bitmap-array-to-yuv-ycbcr-nv21
