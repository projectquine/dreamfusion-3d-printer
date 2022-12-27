# This script takes the name of the ".png" file as a command-line argument, opens the file using the Python Imaging Library (PIL), downsamples the colors in the image to their nearest neighboring buckets (currently the minmax RGB values, AKA 0.0.255; 255.0.255; etc), and saves the source image to a new file called "original.png".

# TODO: Add bias for extreme RGB values, so hues that are perceived by the human eye are biased towards color rather than towards pure black or pure white. For example, if a pixel's RGB values are 10.120.10, the current implementation will downscale it to 0.0.0, but it makes much more sense to downscale it to 0.255.0, even though that's technically not the nearest "rounded" color.

import sys
from PIL import Image


# Downsample the colors in the image
def downsample_colors(image):
    # Create a blank image with the same size as the original image
    downsampled_image = Image.new('RGB', image.size)
    # Iterate over the pixels in the image
    for x in range(image.width):
        for y in range(image.height):
            # Get the RGB values for the pixel
            r, g, b = image.getpixel((x, y))
            # Scale the values to the range [0, 1]
            r /= 255.0
            g /= 255.0
            b /= 255.0
            # Calculate the bucket indices for each value
            r_index = round(r)
            g_index = round(g)
            b_index = round(b)
            # Scale the indices back to the range [0, 255]
            r_scaled = int(r_index * 255)
            g_scaled = int(g_index * 255)
            b_scaled = int(b_index * 255)
            # Set the pixel value in the downsampled image
            downsampled_image.putpixel((x, y), (r_scaled, g_scaled, b_scaled))
    return downsampled_image


def main(filename):
    # Open the image file
    image = Image.open(filename)
    # Downsample the colors in the image
    downsampled_image = downsample_colors(image)
    # image.save('albedo_original.png')
    # Save the downsampled image to a new file
    downsampled_image.save(filename)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python downsample_colors.py /path/to/albedo.png')
        sys.exit(1)
    main(sys.argv[1])
