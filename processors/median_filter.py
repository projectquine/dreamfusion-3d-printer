# This script takes the name of the ".png" file as a command-line argument, opens the file using the Python Imaging Library (PIL), and applies a median filter to the image. The median filter works by iterating over each pixel in the image, calculating the median color of the surrounding pixels (including the pixel itself), and updating the pixel color to match the median color. The filtered image is then saved to a file called "filtered.png".

import itertools
import sys
from PIL import Image

PASSES = 2
SCAN_RANGE = 2

# TODO: Find better ways to cleanup small color regions. Currently it's doing it by looking at the 2D texture, which is an okay way to do it for small corrections, but produces noticeable mistakes at higher iterations because the 2D file is not aware of how it maps onto 3D voxels which causes it to generate false positives/negatives. There are some quick&dirty ways to fix this (defrag texture) but ultimately this'll require a rewrite to a purely 3D implementation if we want to do it right.
# TODO: OPTIONAL: Convert loops into vectorized operations to make the script run much faster.
# TODO: OPTIONAL: Parametrize "PASSES" and "SCAN_RANGE" logic.
# TODO: OPTIONAL: Refactor "PASSES" logic so it doesn't save->load over and over. Then again, this does allow for graceful interruption of the process... TBD
# TODO: OPTIONAL: Implement variations. Currently it just flips pixels to their median surrounding color. Alternatives are: Median (excluding diagonals); Median (excluding self); Supermajority; Stateful (takes preceding pixel results into account before waiting for full iteration); Chaotic (pick random neighboring color).
# TODO: OPTIONAL: Complex setups. f.e. "Run 10 passes at scan range 1, then 20 passes at scan range 2". This can be done easily using CLI, so it's low prio.


class MedianFilter:
    def __init__(self, image):
        self.image = image
        self.pixels = image.load()

    def apply(self):
        # Create a copy of the image to store the filtered pixels
        filtered_image = Image.new('RGB', self.image.size)
        filtered_pixels = filtered_image.load()

        # Iterate over the pixels in the image
        for x in range(self.image.width):
            for y in range(self.image.height):
                # Get the surrounding pixels
                surrounding_pixels = self.get_surrounding_pixels(x, y)
                # Calculate the median color of the surrounding pixels
                median_color = self.get_median_color(surrounding_pixels)
                # Update the pixel color to the median color
                filtered_pixels[x, y] = median_color

        # Save the filtered image
        filtered_image.save('albedo.png')

    def get_surrounding_pixels(self, x, y):
        return [
            self.pixels[i, j]
            for i, j in itertools.product(self.scan(x), self.scan(y))
            if i >= 0 and i < self.image.width and j >= 0 and j < self.image.height
        ]

    def scan(self, coord):
        return range(coord - SCAN_RANGE, coord + (SCAN_RANGE + 1))

    def get_median_color(self, pixels):
        # Sort the pixels by their red, green, and blue values
        sorted_pixels = sorted(pixels, key=lambda p: (p[0], p[1], p[2]))
        # Return the pixel at the middle of the list as the median color
        return sorted_pixels[len(sorted_pixels) // 2]


def main(filename):
    for i in range(PASSES):
        # Open the image file
        # image = Image.open(filename if i == 0 else 'filtered.png')
        image = Image.open(filename)
        # Create a MedianFilter object for the image
        median_filter = MedianFilter(image)
        # Apply the median filter to the image
        median_filter.apply()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python median_filter.py <filename>.png')
        sys.exit(1)
    main(sys.argv[1])
