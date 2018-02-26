"""
    使用 Dataset api 并行读取图片数据
    参考：
        - 关于 TF Dataset api 的改进讨论：https://github.com/tensorflow/tensorflow/issues/7951
        - https://kratzert.github.io/2017/06/15/example-of-tensorflows-new-input-pipeline.html
        - https://stackoverflow.com/questions/47064693/tensorflow-data-api-prefetch
        - https://stackoverflow.com/questions/46444018/meaning-of-buffer-size-in-dataset-map-dataset-prefetch-and-dataset-shuffle

    TL;DR
        Dataset.shuffle() 的 buffer_size 参数影响数据的随机性， TF 会先取 buffer_size 个数据放入 catch 中，再从里面选取
        batch_size 个数据，所以使用 shuffle 有两种方法：
            1. 每次调用 Dataset api 前手动 shuffle 一下 filepaths 和 labels
            2. Dataset.shuffle() 的 buffer_size 直接设为 len(filepaths)。这种做法要保证 shuffle() 函数在 map、batch 前调用

        Dataset.prefetch() 的 buffer_size 参数可以提高数据预加载性能，但是它比 tf.FIFOQueue 简单很多。
        tf.FIFOQueue supports multiple concurrent producers and consumers
"""

import tensorflow as tf
import numpy as np
import cv2
import os

import time
from tensorflow.python.framework import dtypes

NUM_CLASSES = 2
BATCH_SIZE = 64
NUM_EPOCHS = 50


def input_parser(img_path, label):
    # convert the label to one-hot encoding
    # one_hot = tf.one_hot(label, NUM_CLASSES)

    # read the img from file
    img_file = tf.read_file(img_path)
    img_decoded = tf.image.decode_image(img_file, channels=3)
    # img_decoded = (img_decoded - 128.) / 128.
    img_decoded = tf.subtract(img_decoded, 128)
    img_decoded = tf.divide(img_decoded, 128)
    return img_decoded, label


def get_img_paths_and_labels(img_dir):
    img_paths = []
    labels = []

    for root, sub_folder, file_list in os.walk(img_dir):
        for idx, file_name in enumerate(sorted(file_list)):
            image_path = os.path.join(root, file_name)
            img_paths.append(image_path)

            # 00000_abcd.png
            label = file_name[:-4].split('_')[0]
            labels.append(label)

    return img_paths, labels


def cv_load_img(img_path):
    img = (cv2.imread(img_path).astype(np.float32) - 128.) / 128.
    img = np.reshape(img, [32, 180, 3])

    # 00000_abcd.png
    label = img_path[:-4].split('/')[-1].split('_')[0]
    return img, label


def test_tf_dataset(img_paths, labels):
    train_imgs = tf.convert_to_tensor(img_paths, dtype=dtypes.string)
    train_labels = tf.convert_to_tensor(labels, dtype=dtypes.string)

    # Create Dataset
    train_data = tf.data.Dataset.from_tensor_slices((train_imgs, train_labels))

    # Make sure to call tf.data.Dataset.shuffle() before applying the heavy
    # transformations (like reading the images, processing them, batching...).
    train_data = train_data.shuffle(buffer_size=len(img_paths))

    train_data = train_data.map(input_parser, num_parallel_calls=4)
    train_data = train_data.batch(BATCH_SIZE)
    train_data = train_data.repeat(NUM_EPOCHS)

    # Typically it is most useful to add a small prefetch buffer (with perhaps
    # just a single element) at the very end of the pipeline
    train_data = train_data.prefetch(buffer_size=BATCH_SIZE * 2)

    # Create an uninitialized Iterator
    iterator = tf.data.Iterator.from_structure(train_data.output_types,
                                               train_data.output_shapes)

    next_batch = iterator.get_next()

    training_init_op = iterator.make_initializer(train_data)

    with tf.Session() as sess:
        # initialize the iterator on the training data

        # get each element of the training dataset until the end is reached
        start_time = time.time()

        count = 0
        sess.run(training_init_op)
        while True:
            try:
                batch_data = sess.run(next_batch)
                count += len(batch_data[0])
            except tf.errors.OutOfRangeError:
                break

        print("Total images: {}".format(count))
        print("Total time: {:.02f}s".format(time.time() - start_time))


def test_cv_load(img_paths, labels):
    num_train = len(img_paths)
    batchs = int(num_train / BATCH_SIZE)

    cv_start_time = time.time()
    count = 0
    for e in range(NUM_EPOCHS):
        for cur_batch in range(batchs):
            shuffle_idx = np.random.permutation(num_train)
            indexs = [shuffle_idx[i % num_train] for i in range(BATCH_SIZE)]

            for i in range(BATCH_SIZE):
                cv_load_img(img_paths[indexs[i]])
                count += 1

    print("cv Total images: {}".format(count))
    print("cv Total time: {:.02f}s".format(time.time() - cv_start_time))


if __name__ == '__main__':
    img_paths, labels = get_img_paths_and_labels('/home/cwq/data/train_10')
    test_tf_dataset(img_paths, labels)
    test_cv_load(img_paths, labels)
