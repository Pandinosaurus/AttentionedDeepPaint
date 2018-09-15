import os
import glob

import random
import numpy as np

from utils.image import load_data


class ImageTranslationDataLoader:
    """
    image translation dataset loader
    """

    def __init__(self, root, batch_size=1):
        train_root = os.path.join(root, "train")
        val_root = os.path.join(root, "val")

        self.train_files = glob.glob(os.path.join(train_root, "*.jpg"))
        self.val_files = glob.glob(os.path.join(val_root, "*.jpg"))

        random.shuffle(self.train_files)

        self.train_idx = self.val_idx = 0

        self.len_train = len(self.train_files)
        self.len_val = len(self.val_files)

        self.batch_size = batch_size

        self.train_step = int(
            np.ceil(len(self.train_files) / self.batch_size))
        self.val_step = int(np.ceil(len(self.val_files) / self.batch_size))

    def get_next_train_batch(self):
        if self.len_train - self.train_idx < self.batch_size:
            # cannot read exact batch size
            files = self.train_files[self.train_idx:]
            self.train_idx = 0
        else:
            files = self.train_files[self.train_idx:self.train_idx +
                                     self.batch_size]
            self.train_idx += self.batch_size
            if self.train_idx == self.len_train:
                self.train_idx = 0

        image_A, image_B = [], []
        for file in files:
            A, B = load_data(file)
            image_A.append(A)
            image_B.append(B)

        image_A = np.array(image_A, dtype=np.float32)
        image_B = np.array(image_B, dtype=np.float32)

        return image_A, image_B

    def get_next_val_batch(self):
        if self.len_val - self.val_idx < self.batch_size:
            # cannot read exact batch size
            files = self.val_files[self.val_idx:]
            self.val_idx = 0
        else:
            files = self.val_files[self.val_idx:self.val_idx +
                                   self.batch_size]
            self.val_idx += self.batch_size
            if self.val_idx == self.len_val:
                self.val_idx = 0

        image_A, image_B = [], []
        for file in files:
            A, B = load_data(file, is_test=True)
            image_A.append(A)
            image_B.append(B)

        image_A = np.array(image_A, dtype=np.float32)
        image_B = np.array(image_B, dtype=np.float32)

        return image_A, image_B
