import cv2
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif']=['simhei']
plt.rcParams['figure.figsize'] = (12, 12)
plt.rcParams['axes.unicode_minus'] = False

def showRGB(img, name, size=None):
    plt.imshow(img)
    plt.title(name)
    if size:
        plt.figure(figsize=size)
    plt.show()

def showBGR(img, name, size=None):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    showRGB(img, size)
    
def showGray(img, name, size=None):
    plt.imshow(img, cmap='gray')
    plt.title(name)
    if size:
        plt.figure(figsize=size)
    plt.show()