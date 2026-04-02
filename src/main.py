import open3d as o3d
import numpy as np

from load_kitti import load_kitti_bin
from inject_fake_points import generate_fake_points, inject_fake_points


def visualize_points(points: np.ndarray, title: str = "Point Cloud"):
    """
    Visualize a point cloud in Open3D.
    """
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries(
        [point_cloud],
        window_name=title,
        width=900,
        height=700
    )


if __name__ == "__main__":
    # Loading original KITTI point cloud.
    file_path = "../data/000000.bin"
    original_points = load_kitti_bin(file_path)

    print("Original point cloud shape:", original_points.shape)

    # Defining a simple target region in front of the sensor.

    target_box = {
        "x_min": 5.0,
        "x_max": 8.0,
        "y_min": -1.0,
        "y_max": 1.0,
        "z_min": -1.0,
        "z_max": 1.0
    }

    # Fake points Generations
    fake_points = generate_fake_points(target_box, num_points=300)
    print("Fake points shape:", fake_points.shape)

    # Inject fake points
    attacked_points = inject_fake_points(original_points, fake_points)
    print("Attacked point cloud shape:", attacked_points.shape)

    # Visualize original scene
    visualize_points(original_points, title="Original Point Cloud")

    # Visualize attacked scene
    visualize_points(attacked_points, title="Attacked Point Cloud")
