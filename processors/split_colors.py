import pymeshlab
from PIL import Image
import os
import sys


def get_unique_pixel_rgb_values(image_filename):
    # Open the image
    image = Image.open(image_filename)
    # Convert the image to a list of tuples (R, G, B)
    pixel_rgb_values = list(image.getdata())
    # Get the unique pixel RGB values
    unique_pixel_rgb_values = set(pixel_rgb_values)
    return unique_pixel_rgb_values


def split_colors(mesh_filepath, output_dir):

    albedo_filepath = os.path.join(os.path.dirname(mesh_filepath), 'albedo.png')
    # print(albedo_filepath)


    # # Get the unique pixel RGB values
    unique_pixel_rgb_values = get_unique_pixel_rgb_values(albedo_filepath)
    if 1 > len(unique_pixel_rgb_values) > 32:
        raise NotImplementedError(f'File contains {len(unique_pixel_rgb_values)} unique colors, which is currently unsupported. Downsample the image to a range of colors supported by prusaslicer.')

    for pixel in unique_pixel_rgb_values:
        r, g, b = pixel

        # Create output directory for this RGB value
        output_subdir = os.path.join(os.path.dirname(output_dir), f'{r}_{g}_{b}/')
        os.makedirs(output_subdir, exist_ok=True)

        # Load the mesh
        mesh = pymeshlab.MeshSet()
        mesh.load_new_mesh(mesh_filepath)
        mesh.transfer_texture_to_color_per_vertex()  # TODO: Should only be done once.

        # Apply the selection
        mesh.compute_selection_by_color_per_face(color=pymeshlab.Color(r, g, b), colorspace='RGB')
        # Invert selection
        mesh.apply_selection_inverse(invfaces=True, invverts=True)

        # Delete all selected
        mesh.meshing_remove_selected_vertices_and_faces()

        # Save the mesh
        output_file = os.path.join(output_subdir, 'mesh.obj')
        mesh.save_current_mesh(output_file)


def main(mesh_filepath):
    # Make sure the directories in the output path exist
    output_dir = os.path.join(os.path.dirname(mesh_filepath), 'split_colors_output/')
    os.makedirs(output_dir, exist_ok=True)

    split_colors(mesh_filepath, output_dir)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python split_colors.py /path/to/mesh.obj')
        sys.exit(1)
    main(sys.argv[1])
