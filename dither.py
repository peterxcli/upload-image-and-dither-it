from math import *
import numpy as np

#二值化 [0, 255]
def apply_threshold(value):
    return 255 * floor(value/128)

def findClosestColour(pixel):
    # 定義顏色庫，此例中為黃色、紅色、白色、黑色
    colors = np.array([[255, 255, 0], [255, 0, 0], [255, 255, 255], [0, 0, 0]])
    
    # 計算每個顏色與輸入像素的距離
    distances = np.sum(np.abs(pixel[:, np.newaxis].T - colors), axis=1)
    
    # 取距離最短的顏色
    shortest = np.argmin(distances)
    closest_color = colors[shortest]
    
    # 回傳最接近的顏色
    return closest_color

def floyd_steinberg_dither(image_file):
        new_img = image_file
        # 轉換圖片格式為RGB
        new_img = new_img.convert('RGB')
        pixel = new_img.load()

        x_lim, y_lim = new_img.size

        # 遍歷圖片中的每個像素
        for y in range(1, y_lim):
            for x in range(1, x_lim):
                red_oldpixel, green_oldpixel, blue_oldpixel = pixel[x, y]

                # 計算新的像素值
                red_newpixel = apply_threshold(red_oldpixel)
                green_newpixel = apply_threshold(green_oldpixel)
                blue_newpixel = apply_threshold(blue_oldpixel)

                pixel[x, y] = red_newpixel, green_newpixel, blue_newpixel

                # 計算舊值與新值之間的誤差
                red_error = red_oldpixel - red_newpixel
                blue_error = blue_oldpixel - blue_newpixel
                green_error = green_oldpixel - green_newpixel

                # 計算並更新周圍像素的誤差值
                if (x < x_lim - 1):
                    red = pixel[x+1, y][0] + round(red_error * 7/16)
                    green = pixel[x+1, y][1] + round(green_error * 7/16)
                    blue = pixel[x+1, y][2] + round(blue_error * 7/16)

                    pixel[x+1, y] = (red, green, blue)

                if (x > 1 and y < y_lim - 1):
                    red = pixel[x-1, y+1][0] + round(red_error * 3/16)
                    green = pixel[x-1, y+1][1] + round(green_error * 3/16)
                    blue = pixel[x-1, y+1][2] + round(blue_error * 3/16)

                    pixel[x-1, y+1] = (red, green, blue)

                if (y < y_lim - 1):
                    red = pixel[x, y+1][0] + round(red_error * 5/16)
                    green = pixel[x, y+1][1] + round(green_error * 5/16)
                    blue = pixel[x, y+1][2] + round(blue_error * 5/16)

                    pixel[x, y+1] = (red, green, blue)

                if (x < x_lim - 1 and y < y_lim - 1):
                    red = pixel[x+1, y+1][0] + round(red_error * 1/16)
                    green = pixel[x+1, y+1][1] + round(green_error * 1/16)
                    blue = pixel[x+1, y+1][2] + round(blue_error * 1/16)

                    pixel[x+1, y+1] = (red, green, blue)

        return new_img

def findClosestColour(pixel):
    colors = np.array([[255, 255, 0], [255, 0, 0], [255, 255, 255], [0, 0, 0]])
    distances = np.sum(np.abs(pixel[:, np.newaxis].T - colors), axis=1)
    shortest = np.argmin(distances)
    closest_color = colors[shortest]
    return closest_color

def floydDither(img_array):
    img_array = np.array(img_array)
    height, width, _ = img_array.shape
    for y in range(0, height-1):
        for x in range(1, width-1):
            old_pixel = img_array[y, x, :]
            new_pixel = findClosestColour(old_pixel)
            img_array[y, x, :] = new_pixel
            quant_error = new_pixel - old_pixel
            img_array[y, x+1, :] =  img_array[y, x+1, :] + quant_error * 7/16
            img_array[y+1, x-1, :] =  img_array[y+1, x-1, :] + quant_error * 3/16
            img_array[y+1, x, :] =  img_array[y+1, x, :] + quant_error * 5/16
            img_array[y+1, x+1, :] =  img_array[y+1, x+1, :] + quant_error * 1/16
    return img_array