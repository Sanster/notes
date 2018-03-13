This is a example of using opencv's `warpPerspective()` function to do perspective transform on a image.

The code below will make sure the warped image will all include in the result.


```python
import math
import random
import cv2
import numpy as np

def euler_to_mat(yaw, pitch, roll):
    # Rotate clockwise about the Y-axis
    c, s = math.cos(yaw), math.sin(yaw)
    M_y = np.matrix([[c, 0., s],
                     [0., 1., 0.],
                     [-s, 0., c]])

    # Rotate clockwise about the X-axis
    c, s = math.cos(pitch), math.sin(pitch)
    M_x = np.matrix([[1., 0., 0.],
                     [0., c, -s],
                     [0., s, c]])

    # Rotate clockwise about the Z-axis
    c, s = math.cos(roll), math.sin(roll)
    M_z = np.matrix([[c, -s, 0.],
                     [s, c, 0.],
                     [0., 0., 1.]])

    # rotate order: xyz
    return M_z * M_y * M_x
    
def get_perspective_transform(x=0.001, y=0.0001, z=0.015):
    pitch = random.uniform(0 - x, x)
    yaw = random.uniform(0 - y, y)
    roll = random.uniform(0 - z, z)

    M = euler_to_mat(yaw, pitch, roll)

    return M
    
if __name__ == '__main__':
  img_path = './output/val_10/00000001.jpg'
  img = cv2.imread(img_path, 0)
  height = img.shape[0]
  width = img.shape[1]

  # T1 is used to move image center to (0,0)
  T1 = np.matrix([[1., 0., 0. - width / 2],
                  [0., 1., 0. - height / 2],
                  [0., 0., 1.]])

  M = get_perspective_transform(x=0.001, y=0.001, z=0.15)

  pnts = np.asarray([
      [0, 0],
      [width, 0],
      [width, height],
      [0, height]
  ], dtype=np.float32)
  
  # check: http://answers.opencv.org/question/252/cv2perspectivetransform-with-python/
  pnts = np.array([pnts])

  dst_pnts = cv2.perspectiveTransform(pnts, M * T1)[0]
  dst_pnts = np.asarray(dst_pnts, dtype=np.float32)

  bbox = cv2.boundingRect(dst_pnts)

  width_after_perspective = bbox[2]
  height_after_perspective = bbox[3]

  # T2 is used to move left-top corner of bbox to (0,0)
  T2 = np.matrix([[1., 0., 0 - bbox[0]],
                [0., 1., 0 - bbox[1]],
                  [0., 0., 1.]])

  print("origin: width {} height {}".format(width, height))
  print("after perspective: width {} height {}".format(width_after_perspective, height_after_perspective))

  print(T1)
  print(T2)
  print(T2 * M * T1)

  ret = cv2.warpPerspective(img, T2 * M * T1,
                            (width_after_perspective, height_after_perspective))

  cv2.imshow("ori", img)
  cv2.imshow("result", ret)
  cv2.waitKey() 
```
