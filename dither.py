from math import *
import numpy as np

def apply_threshold(value):
    return 255 * floor(value/128)

def floyd_steinberg_dither(image_file):
        new_img = image_file
        new_img = new_img.convert('RGB')
        pixel = new_img.load()

        x_lim, y_lim = new_img.size

        for y in range(1, y_lim):
            for x in range(1, x_lim):
                red_oldpixel, green_oldpixel, blue_oldpixel = pixel[x, y]

                red_newpixel = apply_threshold(red_oldpixel)
                green_newpixel = apply_threshold(green_oldpixel)
                blue_newpixel = apply_threshold(blue_oldpixel)

                pixel[x, y] = red_newpixel, green_newpixel, blue_newpixel

                red_error = red_oldpixel - red_newpixel
                blue_error = blue_oldpixel - blue_newpixel
                green_error = green_oldpixel - green_newpixel

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