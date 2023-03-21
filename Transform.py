import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
os.system('cls' if os.name == 'nt' else 'clear')


source_path = ''
options = ''
while source_path == "":
    source_path = input("Input the source image file path (drag to this terminal)")
    source_path = source_path.replace("'", "")
    source_path = source_path.replace('"', "")

while options == "":
    print("What do you want to transform your image?\n(For multiple image transformations, type the options separated by commas. eg. 1, 2, 3)")
    print("Input as sequential order of the transformations")
    print("Options: \n 1. Translation \n 2. Rotation \n 3. Dilatation")
    options = input("Type yout input here: ")
    if len(options) == 1:
        options = int(options)
        options = [options]
    elif len(options) > 1:
        options = options.split(",")
        # options = np.array(options).astype(int)


# print(f'options = {options}')

options_args = ['How many pixels do you want to translate your image? (X and Y are separated by commas)', 
                'How much do you want to rotate your image? (in degrees and CCW)', 
                'How much do you want to dilate your image? (X and Y factor are separated by commas)']

def rotation_matrix(theta):
    theta = float(theta)*np.pi/180
    return np.array([[np.cos(theta), -1*np.sin(theta), 0], 
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]])
def translate_matrix(x,y):
    return np.array([[1, 0, x], 
                     [0, 1, y],
                     [0, 0, 1]])

def dilate_matrix(sx,sy):
    return np.array([[sx, 0, 0], 
                     [0, sy, 0],
                     [0, 0, 1]])
tmp_opt = ''
options_inp = []
for opt in options:
    opt = int(opt)
    while tmp_opt == '':
        tmp_opt = input(options_args[opt-1])
        if opt != 2:
           tmp_opt = tmp_opt.split(',')
           tmp_opt = np.array(tmp_opt).astype(float)
        else:
            try: 
                tmp_opt = tmp_opt.astype(float)
            except:
                print('Error, please input using a float and separated by commas for options 1 and 3')
            else:
                tmp_opt = tmp_opt.astype(float)
        if opt == 1:
            matrix = translate_matrix(tmp_opt[0], tmp_opt[1])
        elif opt == 2:
            print(tmp_opt)
            matrix = rotation_matrix(tmp_opt)
        elif opt == 3:
            matrix = dilate_matrix(tmp_opt[0], tmp_opt[1])
        options_inp.append(matrix)
    tmp_opt = ''

image = cv2.imread(source_path)

transform_matrix = np.array([[1, 0, 0], 
                             [0, 1, 0],
                             [0, 0, 1]])
for mat in reversed(options_inp):
    tmp_mat = np.matmul(transform_matrix.astype(np.float32), mat.astype(np.float32))
    transform_matrix = tmp_mat
cols,rows, ch = image.shape
img_tr = cv2.warpPerspective(image, transform_matrix, (rows,cols))
ax1 = plt.subplot(1, 2, 1)
ax1.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
ax1.set_title("Original Image")
ax2 = plt.subplot(1, 2, 2)
ax2.imshow(cv2.cvtColor(img_tr, cv2.COLOR_BGR2RGB))
ax2.set_title("Transfromed Image")
plt.show()