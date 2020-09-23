import glob as gl
import cv2
import random
import os
import numpy as np
class Data_aug(object):
    def __init__(self,aug_method_list,aug_number,data_path,save_dir):
        self.aug_method_list = aug_method_list
        self.aug_number = int(aug_number)
        self.data_path = data_path
        self.save_dir = save_dir
        self.expand_num=0
        self.per_imgpath=""
    def select_aug(self):
        glob = gl.glob(self.data_path+'/*.jpg')
        num = len(glob)
        per_image_aug = self.aug_number//num

        self.per_image_per_aug = per_image_aug//len(self.aug_method_list)
        print(per_image_aug)
        for i in self.aug_method_list:
            for path in glob:
                self.per_imgpath = path
                if i=='rotate':
                    self.rotate()
                if i=='shear':
                    self.shear()

                if i=='transform':
                    self.transform()

                if i=='warp':
                    self.warp()

                if i=='zoom':
                    self.zoom()

    def rotate(self):
        image = cv2.imread(self.per_imgpath)
        h, w, c = image.shape
        random_angle = random.randint(-90, 90)  # 随机角度
        matRotate = cv2.getRotationMatrix2D(
            (h * 0.5, w * 0.5), random_angle, 0.9)
        expand_image = cv2.warpAffine(image, matRotate, (h, w))
        cv2.imwrite(os.path.join(self.save_dir,str(self.expand_num)+'.jpg'), expand_image)
        self.expand_num+=1
    def shear(self):
        image = cv2.imread(self.per_imgpath)
        h, w = image.shape[:2]

        A = cv2.getPerspectiveTransform(

            np.array([[0, 0], [w, 0], [0, h], [w, h]], np.float32),

            np.array([[w / 2, 0], [w, 0], [0, h], [w, h / 2.0]], np.float32))

        expand_image = cv2.warpPerspective(image, A, (w, h))
        cv2.imwrite(os.path.join(self.save_dir, str(self.expand_num) + '.jpg'), expand_image)
        self.expand_num += 1
    def transform(self):
        img = cv2.imread(self.per_imgpath)

        imgInfo = img.shape
        height = imgInfo[0]
        width = imgInfo[1]
        # mode = imgInfo[2]
        expand_image = np.zeros(imgInfo, np.uint8)

        for i in range(height):
            for j in range(width - 100):
                expand_image[i, j + 100] = img[i, j]
        cv2.imwrite(os.path.join(self.save_dir, str(self.expand_num) + '.jpg'), expand_image)
        self.expand_num += 1
    def warp(self):
        img = cv2.imread(self.per_imgpath)
        imgInfo = img.shape
        height = imgInfo[0]
        width = imgInfo[1]
        deep = imgInfo[2]

        expand_image = np.zeros([height * 2, width, deep], np.uint8)

        for i in range(height):
            for j in range(width):
                expand_image[i, j] = img[i, j]
                expand_image[height * 2 - i - 1, j] = img[i, j]

        for i in range(width):
            expand_image[height, i] = (0, 0, 255)
        cv2.imwrite(os.path.join(self.save_dir, str(self.expand_num) + '.jpg'), expand_image)
        self.expand_num += 1
    def zoom(self):
        img = cv2.imread(self.per_imgpath)
        imgInfo = img.shape
        height = imgInfo[0]
        width = imgInfo[1]
        dstHeight = int(height * 0.5)
        dstWeight = int(width * 0.5)

        # 最近邻域插值 双线性插值 像素关系重采样 立方插值
        expand_image = cv2.resize(img, (dstWeight, dstHeight))
        cv2.imwrite(os.path.join(self.save_dir, str(self.expand_num) + '.jpg'), expand_image)
        self.expand_num += 1