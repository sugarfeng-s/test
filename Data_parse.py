import cv2
import glob as gl
# import pydicom
import numpy
import os
class Data_parse(object):
    def __init__(self,parse_method,data_path,save_dir):
        self.parse_method = parse_method
        self.data_path = data_path
        self.save_dir = save_dir
    def select_parse(self):
        if self.parse_method=='EM':
            self.EM_data_parse()
        if self.parse_method=='CT':
            self.CT_data_parse()
        if self.parse_method=='Norm':
            self.Norm_data_parse()
        if self.parse_method=='ISIC':
            self.ISIC_data_parse()
    def EM_data_parse(self):
        glob = gl.glob(self.data_path + '/*')  # 读取文件路径
        for image in glob:
            x = cv2.imread(image)
            h, w, c = x.shape
        for p_c in range(c):
            cv2.imwrite(os.path.join(self.save_dir,str(p_c)+'.jpg'),x[:,:,p_c])
    def Norm_data_parse(self):
        glob = gl.glob(self.data_path + '/*')  # 读取文件路径
        print(glob)
        print(self.save_dir)
        num=0
        for image in glob:
            x = cv2.imread(image)
            cv2.imwrite(os.path.join(self.save_dir, str(num)+'.jpg'), x)
            num+=1
    def ISIC_data_parse(self):
        glob = gl.glob(self.data_path + '/*')  # 读取文件路径
        for image in glob:
            x = cv2.imread(image)
            x = cv2.resize(x,(512,512))
            cv2.imwrite(os.path.join(self.save_dir, image + '.jpg'), x)
    # def CT_data_parse(self):
    #     lstFilesDCM = []
    #     RefDs = pydicom.read_file(lstFilesDCM[0])  # 读取第一张dicom图片
    #
    #     # 建立三维数组
    #     ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
    #
    #     # 得到spacing值 (mm为单位)
    #     ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
    #
    #     # 三维数据
    #     x = numpy.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0],
    #                      ConstPixelSpacing[0])  # 0到（第一个维数加一*像素间的间隔），步长为constpixelSpacing
    #     y = numpy.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])  #
    #     z = numpy.arange(0.0, (ConstPixelDims[2] + 1) * ConstPixelSpacing[2], ConstPixelSpacing[2])  #
    #
    #     # ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
    #
    #     # 遍历所有的dicom文件，读取图像数据，存放在numpy数组中
    #     for filenameDCM in lstFilesDCM:
    #         ds = pydicom.read_file(filenameDCM)
    #         cv2.imwrite(os.path.join(self.save_dir, filenameDCM + '.jpg'), ds.pixelArray)
