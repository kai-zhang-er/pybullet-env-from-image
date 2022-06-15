# decompose a polygon to several rectangles to faciliate the building of environment in pybullet
import matplotlib.pyplot as plt
import numpy as np
import cv2
from adabox.proc import decompose
from adabox.plot_tools import plot_rectangles

# in_path="./sample_data/sample_1.csv"
# data_2d=np.loadtxt(in_path, delimiter=",")
# plt.scatter(data_2d[:,0], data_2d[:, 1])
# plt.show()

def filter_out_small_rectangles(rectangles):
    filtered_result=[]
    for rect in rectangles:
        length=abs(rect.x1-rect.x2)
        height=abs(rect.y1-rect.y2)
        if length<3 or height<3 or length*height<25:
            continue
        filtered_result.append(rect)
    return filtered_result

def save_to_txt(rectangles):
    f=open("rect.txt","w")
    for rect in rectangles:
        length=abs(rect.x1-rect.x2)
        height=abs(rect.y1-rect.y2)
        center_x=(rect.x1+rect.x2)/2
        center_y=(rect.y1+rect.y2)/2
        f.write("{},{},{},{}\r".format(center_x, center_y, length, height))
    f.close()

img=cv2.imread("floor_plan_simple.png", 0)//200
# remove small walls
kernel=np.ones((5,5), np.uint8)
img_dilate=cv2.dilate(img, kernel, iterations=1)
img=cv2.erode(img_dilate, kernel, iterations=1)


# cv2.imshow("img", img_dilate*255)
# cv2.imshow("img2", img_erosion*255)
# cv2.waitKey(0)

ind_black=np.where(img==0)
flag=np.zeros((1,ind_black[0].shape[0]))
data_2d=np.concatenate((ind_black, flag), axis=0).T
rectangles=[]
searches=2
(rectangles, sep_value)=decompose(data_2d, searches)
filtered_rectangles=filter_out_small_rectangles(rectangles)
print('number of rectangles found: {}'.format(len(filtered_rectangles)))
plot_rectangles(filtered_rectangles,2)
plt.show()
save_to_txt(rectangles)

