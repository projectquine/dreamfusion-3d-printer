import pymeshlab
import sys


def smoothen(mesh_filepath):

    # Load the mesh
    mesh = pymeshlab.MeshSet()
    mesh.load_new_mesh(mesh_filepath)

    # Apply filter
    mesh.apply_coord_laplacian_smoothing(stepsmoothnum=6)
    # mesh.compact_faces()  # TODO: Was removed in latest pymeshlab but is still in meshlab. Find out if this feature still exists under a new function name.
    # mesh.compact_vertices()

    # Save the mesh
    mesh.save_current_mesh(mesh_filepath)


def main(mesh_filepath):
    smoothen(mesh_filepath)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python smoothen.py /path/to/mesh.obj')
        sys.exit(1)
    main(sys.argv[1])
