"""
  使用 Dataset api 并行读取图片数据
  参考：https://kratzert.github.io/2017/06/15/example-of-tensorflows-new-input-pipeline.html
"""

import tensorflow as tf
import os

import time
from tensorflow.python.framework import dtypes

NUM_CLASSES = 2
BATCH_SIZE = 64


def input_parser(img_path, label):
    # convert the label to one-hot encoding
    # one_hot = tf.one_hot(label, NUM_CLASSES)

    # read the img from file
    img_file = tf.read_file(img_path)
    img_decoded = tf.image.decode_image(img_file, channels=3)
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


if __name__ == '__main__':
    img_paths, labels = get_img_paths_and_labels('./data/train_10')
    train_imgs = tf.convert_to_tensor(img_paths, dtype=dtypes.string)
    train_labels = tf.convert_to_tensor(labels, dtype=dtypes.string)

    # Create Dataset
    train_data = tf.data.Dataset.from_tensor_slices((train_imgs, train_labels))
    train_data = train_data.map(input_parser, num_parallel_calls=4)
    train_data = train_data.shuffle(buffer_size=10)
    train_data = train_data.batch(BATCH_SIZE)

    # Create an uninitialized Iterator
    iterator = tf.data.Iterator.from_structure(train_data.output_types,
                                               train_data.output_shapes)

    next_batch = iterator.get_next()

    training_init_op = iterator.make_initializer(train_data)

    with tf.Session() as sess:
        # initialize the iterator on the training data

        # get each element of the training dataset until the end is reached
        start_time = time.time()

        epochs = 50
        count = 0
        for e in range(epochs):
            sess.run(training_init_op)
            index = 0
            while True:
                try:
                    imgs, labels = sess.run(next_batch)
                    if index == 0:
                        print(labels)

                    index += 1
                    count += 1
                except tf.errors.OutOfRangeError:
                    print("epoch {} finish...".format(e))
                    break

        print("Total batches: {}".format(count))
        print("Total time: {:.02f}s".format(time.time() - start_time))
