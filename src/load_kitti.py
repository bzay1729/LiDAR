import numpy as np


def load_kitti_bin(file_path: str) -> np.ndarray:
    """
    Load a KITTI LiDAR .bin file.
    Each point contains 4 values: x, y, z, intensity.
    This function returns only x, y, z.
    """
    point_cloud = np.fromfile(file_path, dtype=np.float32)

    if point_cloud.size % 4 != 0:
        raise ValueError("Invalid KITTI .bin file. Data size is not divisible by 4.")

    point_cloud = point_cloud.reshape(-1, 4)
    return point_cloud[:, :3]