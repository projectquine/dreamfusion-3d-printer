import pymeshlab
# from PIL import Image
# import os
import sys


def apply_meshing_remove_connected_component_by_diameter_filter(mesh_filepath):
    # Load the mesh
    mesh = pymeshlab.MeshSet()
    mesh.load_new_mesh(mesh_filepath)

    # Apply the filter
    mesh.meshing_remove_connected_component_by_diameter()
    # Save the mesh
    mesh.save_current_mesh(mesh_filepath)


def main(mesh_filepath):
    apply_meshing_remove_connected_component_by_diameter_filter(mesh_filepath)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python remove_artifacts.py /path/to/mesh.obj')
        sys.exit(1)
    main(sys.argv[1])
