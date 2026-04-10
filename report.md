# LiDAR Fake Point Location Optimization Project
---
## Introduction

---
## Step 1: Environment Setup
- IDE: PyCharm  
- Programming Language: Python  
- Libraries: NumPy, Open3D, Matplotlib  

This environment was configured to support LiDAR point cloud processing, visualization, and numerical computation.

---

## Step 2: Dataset Selection and Understanding
- Dataset used: KITTI LiDAR Object Detection Dataset.  
- Input format: `.bin` (binary file format).  
- Each data point contains: (x, y, z, intensity).  
- Current implementation uses only spatial coordinates (x, y, z).

The KITTI dataset is widely used in autonomous driving research and provides real-world LiDAR scans suitable for evaluating point cloud-based algorithms.

---

## Step 3: Baseline LiDAR Loading and Visualization
- Successfully loaded a KITTI LiDAR frame using NumPy.  
- Converted binary data into structured point cloud format.  
- Verified shape of the point cloud (approximately 115k points per frame).  
- Visualized the 3D point cloud using Open3D.  

This step confirms that the LiDAR data pipeline is correctly implemented and that the spatial distribution of points represents a real-world driving environment.

---

## Step 4: Baseline Fake Point Injection
- Defined a target 3D region in front of the LiDAR sensor.  
- Generated synthetic (fake) LiDAR points within this region using uniform random sampling.  
- Injected fake points into the original point cloud.  
- Constructed a modified (attacked) point cloud.  

Example:
- Original point cloud: ~115,384 points.  
- Fake points added: 300 points.  
- Attacked point cloud: ~115,684 points.  

---

### Observations
- The injected fake points are numerically present in the attacked point cloud but are not visually distinguishable due to the large number of original points.  
- The current injection method is random and does not yet follow any optimization strategy.  
- This implementation serves as a baseline attack for further improvement.  

---

### Interpretation
This step simulates a basic LiDAR spoofing attack where artificial points are introduced into the sensor data. Although the attack is currently random, it demonstrates how the point cloud can be manipulated without modifying the physical environment.

This baseline setup will be extended in later steps to:
- Strategically place fake points using optimization techniques.  
- Analyze how these points affect object detection models.  
- Improve attack effectiveness through controlled placement.  

---

## Step 5: Visualization of fake points
- Enhanced visualization by assigning different colors to points types.
- Original LiDAR points are shown in gray.
- Injected fake points are highlighted in red.
- This allows clear identification of the attack region.
### Observation
- Fake points are visible as a cluster in a defined target region.
- Current distribution is random and does not resemble structure objects.
- Visualization confirms successful injection of adversarial points.

---

## Step 6: Structured Fake Point Injection
- Replaced random point generation with clustered distribution.
- Generated fake points around a defined center using a gaussian distribution.
- This helps to create a dense, object-like cluster.
### Observation
- Fake points now form a compact structure.
- The cluster resembles a potential object rather than random noise.
- This improves the realism of the attack.
### Interpretation
- Structured fake points are more likely to influence object detection models.
- This step is closer to an optimized adversarial attack.

---

## Step 7: Choosing Best Location Automatically & Optimization
- Implemented simple search-based optimization to automatically select a fake-point location.
- Evaluated multiple candidate centers within a realistic region in front of the LiDAR.
- Used a compactness-based scoring function to prefer tighter fake clusters.
### Observation
- Manual attacking location is no longer needed.
- Fake point cluster is now generated at an automatically selected position.
- This establishes the first optimization-based version of the attack.
### Interpretation
- This optimization is currently based on proxy objective rather than detector outputs.
- It serves as a baseline for upcoming/future detector-aware optimization.

---

## Step 8: Attack-Aware Optimization (Smart Optimization)

- Improved the optimization strategy to consider interaction with the real LiDAR scene instead of only cluster compactness.
- For each candidate location, generated a clustered set of fake points.
- Computed the distance from each fake point to the nearest real point.
- Selected the location that minimizes this distance as the optimal attack position.

### Observation
- The optimized fake cluster is positioned close to existing scene structures.
- Fake points are no longer isolated and instead overlap meaningful regions of the point cloud.

### Interpretation
- Placing fake points near real structures increases the likelihood of interfering with LiDAR-based perception.
- This approach is more realistic and effective compared to random or compact-only placement.

---

## Step 8.1: Export of Attacked Point Cloud

- Converted the attacked point cloud into KITTI-compatible binary format.
- Added an intensity column with zero values to match KITTI structure (x, y, z, intensity).
- Saved the modified scene as a new `.bin` file for detector-based evaluation.

---

## Step 9: Local Region Impact Analysis (This is done in Jupyter Notebook)

To evaluate the effectiveness of the optimized fake point injection, a local region analysis was performed around the attack center.

### Method
- Selected a spherical region centered at the optimized attack location.
- Compared point density between original and attacked point clouds.
- Visualized cropped regions using Open3D.
- Measured spatial statistics including bounding box and point count.

### Observation

- Point density increased significantly in the attack region:
  - At radius 2.0:
    - Original: 1188 points
    - Attacked: 1677 points
    - Increase: +489 points

- The increase closely matches the number of injected fake points (500)

- Visualization shows:
  - Original region contains structured LiDAR scan patterns.
  - Attacked region contains a dense artificial cluster overlapping real structure.

- Spatial extent changed:
  - Height (z-axis) increased noticeably.
  - Region became denser and more volumetric.

### Interpretation

- The fake points were successfully concentrated in a meaningful region of the scene.
- Instead of forming a separate object, the attack alters an existing structure.
- This distortion changes the geometric representation of the scene.

### Conclusion

- The optimized attack effectively modifies the local LiDAR geometry.
- The attack is spatially targeted and not random.
- This demonstrates the ability to mislead LiDAR-based perception by altering benign regions.