import open3d as o3d
import numpy as np

from load_kitti import load_kitti_bin
from inject_fake_points import inject_fake_points
from src.optimize_location import find_best_location


def visualize_with_colors(original_points, fake_points, title="Optimized Fake Point Injection"):
    """
    Visualize original and fake points using different color.
    """
    # Combine points
    all_points = np.vstack((original_points, fake_points))

    # Creating colors
    original_colors = np.tile([0.6, 0.6, 0.6], (original_points.shape[0], 1))  # gray color
    fake_colors = np.tile([1.0, 0.0, 0.0], (fake_points.shape[0], 1))  # red color
    all_colors = np.vstack((original_colors, fake_colors))

    # Creating Open3D object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(all_points)
    pcd.colors = o3d.utility.Vector3dVector(all_colors)

    o3d.visualization.draw_geometries(
        [pcd],
        window_name=title,
        width=900,
        height=700
    )


if __name__ == "__main__":
    # Loading original KITTI point cloud.
    file_path = "../data/000000.bin"
    original_points = load_kitti_bin(file_path)

    print("Original point cloud shape:", original_points.shape)

    best_center, best_score, fake_points = find_best_location(
        x_range=(4, 10),
        y_range=(-3, 3),
        z_range=(-1, 1),
        trials=30,
        size=0.3,
        num_points=500
    )

    # Defining a simple target region in front of the sensor.
    # target_box = {
    #     "x_min": 5.0,
    #     "x_max": 8.0,
    #     "y_min": -1.0,
    #     "y_max": 1.0,
    #     "z_min": -1.0,
    #     "z_max": 1.0
    # }

    # Center of fake object
    center = [6, 0, 0]

    # Inject fake points
    attacked_points = inject_fake_points(original_points, fake_points)
    print("Best center found:", best_center)
    print("Best score:", best_score)
    print("Fake points shape:", fake_points.shape)
    print("Attacked point cloud shape:", attacked_points.shape)

    # Visualize original and fake points with colors
    visualize_with_colors(original_points, fake_points, title="Optimized Fake Point Injection")

    # Visualize original scene
    # visualize_points(original_points, title="Original Point Cloud")
    # Visualize attacked scene
    # visualize_points(attacked_points, title="Attacked Point Cloud")
