# This script takes the name of the ".png" file as a command-line argument, opens the file using the Python Imaging Library (PIL), downsamples the colors in the image to their nearest neighboring buckets (currently the minmax RGB values, AKA 0.0.255; 255.0.255; etc), and saves the source image to a new file called "original.png".

# TODO: Improve handling of certain colors that are perceived by the human eye as light/dark colors. These should be biased towards color but will currently get flipped to white or black. For example, if a pixel's RGB values are 10.120.10, the current implementation will downsample it to 0.0.0, but it makes much more sense to downsample it to 0.255.0, even though that's technically not the nearest "rounded" color.

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
            # Set the pixel value in the downsampled image
            downsampled_image.putpixel((x, y), (downsample(r), downsample(g), downsample(b)))
    return downsampled_image


def downsample(color):
    # Scale the value to the range [0, 1]
    color /= 255.0
    # Calculate the bucket index
    r_index = round(color)
    # Scale the index back to the range [0, 255]
    r_scaled = int(r_index * 255)
    return r_scaled


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
