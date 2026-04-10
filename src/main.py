import numpy as np
import open3d as o3d

from load_kitti import load_kitti_bin
from inject_fake_points import inject_fake_points
from optimize_location import find_best_location

from save_attacked_bin import save_kitti_bin



def visualize_with_colors(original_points, fake_points, title="Attack-Aware Optimized Fake Point Injection"):
    """
    Visualize original points in gray and fake points in red.
    """
    all_points = np.vstack((original_points, fake_points))

    original_colors = np.tile([0.6, 0.6, 0.6], (original_points.shape[0], 1))  # gray
    fake_colors = np.tile([1.0, 0.0, 0.0], (fake_points.shape[0], 1))          # red

    all_colors = np.vstack((original_colors, fake_colors))

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(all_points)
    pcd.colors = o3d.utility.Vector3dVector(all_colors)

    o3d.visualization.draw_geometries(
        [pcd],
        window_name=title,
        width=1000,
        height=750
    )


if __name__ == "__main__":
    # Load original LiDAR frame
    file_path = "../data/original.bin"
    original_points = load_kitti_bin(file_path)

    print("Original point cloud shape:", original_points.shape)

    # Find attack-aware optimized location
    best_center, best_score, fake_points = find_best_location(
        original_points=original_points,
        x_range=(4, 10),
        y_range=(-3, 3),
        z_range=(-1, 1),
        trials=30,
        size=0.3,
        num_points=500
    )

    #  Inject fake points
    attacked_points = inject_fake_points(original_points, fake_points)

    #  Print results
    print("Best center found:", best_center)
    print("Best score:", best_score)
    print("Fake points shape:", fake_points.shape)
    print("Attacked point cloud shape:", attacked_points.shape)

    # Save attacked points cloud as KITTI-format .bin
    save_kitti_bin(attacked_points, "../data/attacked_000000.bin")

    # Verify saved file
    saved_check = np.fromfile("../data/attacked_000000.bin", dtype=np.float32).reshape(-1, 4)
    print("Reloaded saved attacked bin shape:", saved_check.shape)
    print("First 5 saved points:\n", saved_check[:5])

    #  Visualize
    visualize_with_colors(
        original_points=original_points,
        fake_points=fake_points,
        title="Attack-Aware Optimized Fake Point Injection"
    )


