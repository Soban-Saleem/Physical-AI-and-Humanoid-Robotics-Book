---
sidebar_position: 3
title: "Sensor Simulation in Robotics"
description: "Learn how to simulate robot sensors in Gazebo including cameras, LIDAR, IMU, and contact sensors. Understand sensor plugins, noise models, and reading sensor data with ROS 2."
keywords: ["sensor simulation", "Gazebo plugins", "camera simulation", "LIDAR simulation", "IMU simulation", "ROS 2", "point clouds"]
chapter: 3
lesson: 3
duration_minutes: 90

requirements:
  hardware: "Any computer with integrated GPU (minimum) or NVIDIA RTX GPU (recommended)"
  software: "Ubuntu 22.04 LTS, Gazebo Fortress or Gazebo Sim, ROS 2 Humble"

skills:
  - name: "Sensor Plugin Configuration"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can configure sensor plugins in Gazebo SDF files"

  - name: "Sensor Data Interpretation"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can explain different sensor data formats (images, point clouds, IMU readings)"

  - name: "ROS 2 Sensor Integration"
    proficiency_level: "A2"
    category: "Applied"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can write ROS 2 nodes that subscribe to sensor topics"

  - name: "Sensor Noise Modeling"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can explain why sensor noise simulation matters for sim-to-real transfer"

learning_objectives:
  - objective: "Configure Gazebo sensor plugins for cameras, LIDAR, and IMU sensors in SDF world files"
    proficiency_level: "A2"
    bloom_level: "Apply"
    assessment_method: "Hands-on exercise creating a robot model with multiple sensors"

  - objective: "Explain how simulated sensors publish data to ROS 2 topics and identify the standard topic naming conventions"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Short answer describing sensor topic naming and message types"

  - objective: "Write a ROS 2 node that subscribes to sensor topics and processes camera images, LIDAR point clouds, or IMU data"
    proficiency_level: "A2"
    bloom_level: "Apply"
    assessment_method: "Code exercise implementing a sensor processing node"

  - objective: "Describe the role of sensor noise models in simulation and how they improve sim-to-real transfer"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Written explanation with examples of noise parameters"

cognitive_load:
  new_concepts: 7
  assessment: "Students will create a robot model with sensors, write a ROS 2 node to process sensor data, and explain sensor noise concepts"

differentiation:
  extension_for_advanced: "Experiment with different sensor noise parameters and compare how they affect obstacle detection performance. Create a visualization showing noise impact on point cloud data."
  remedial_for_struggling: "Focus on a single sensor type (camera) first. Master the camera plugin and ROS 2 image subscription before adding LIDAR or IMU sensors."
  hardware_alternatives: "All exercises use Gazebo simulation. Students without GPUs can reduce camera resolution or use cloud-based NVIDIA Omniverse Cloud for heavy sensor simulations."

safety_notes: null

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Sensor Simulation in Robotics

A self-driving car approaches an intersection. Its cameras detect traffic lights, its LIDAR maps parked cars, and its IMU tracks acceleration and turn rate. All these sensors work together to build a complete picture of the environment. But before this car ever saw a real street, it drove through thousands of virtual intersections in simulation, testing how its sensors perform in every conceivable scenario.

Sensor simulation is the bridge between robot code and the physical world. Without it, you'd need expensive hardware to test even simple algorithms. With it, you can test perception systems overnight, reproduce exact conditions for debugging, and train AI on millions of simulated scenarios. This lesson teaches you how to simulate the most common robot sensors in Gazebo and read their data with ROS 2.

## Why Simulate Sensors?

Before diving into configuration, let's understand why sensor simulation matters and what makes it challenging.

### Benefits of Sensor Simulation

| Benefit | Explanation |
|---------|-------------|
| **Cost** | Test perception without buying sensors (LIDAR costs $500-$75,000+) |
| **Reproducibility** | Exact same conditions every time (lighting, objects, positions) |
| **Ground Truth** | Know the "correct" answer for evaluating algorithms |
| **Edge Cases** | Test rare scenarios safely (sensor failures, extreme lighting) |
| **Parallel Testing** | Run multiple perception tests simultaneously |

### The Sim-to-Real Challenge

Simulated sensors are perfect. Real sensors are not. This difference causes the **sim-to-real gap**: algorithms that work perfectly in simulation often fail on real hardware.

**Real sensor imperfections that simulation must model:**
- **Noise**: Random variations in measurements
- **Bias**: Systematic offset from true values
- **Delay**: Time lag between reality and sensor reading
- **Occlusion**: Objects blocking sensor view
- **Interference**: Sensors affecting each other
- **Environmental effects**: Rain, fog, dust, lighting changes

**Good news**: Gazebo includes noise models for most sensors, letting you simulate realistic imperfections.

## Gazebo Sensor Plugins

Gazebo uses a **plugin system** for sensors. Instead of writing sensor simulation code yourself, you attach pre-built plugins to your robot model. Each plugin:
- Simulates a specific sensor type
- Publishes data to ROS 2 topics
- Configurable through SDF parameters

### Sensor Plugin Types

| Sensor | Plugin Name | ROS 2 Message Type |
|--------|-------------|-------------------|
| **Camera** | `libgazebo_ros_camera.so` | `sensor_msgs/msg/Image` |
| **Depth Camera** | `libgazebo_ros_depth_camera.so` | `sensor_msgs/msg/Image` + `PointCloud2` |
| **LIDAR** | `libgazebo_ros_laser.so` | `sensor_msgs/msg/LaserScan` |
| **3D LIDAR** | `libgazebo_ros_velodyne.so` | `sensor_msgs/msg/PointCloud2` |
| **IMU** | `libgazebo_ros_imu.so` | `sensor_msgs/msg/Imu` |
| **Contact** | `libgazebo_ros_contact.so` | `std_msgs/msg/Bool` |
| **GPS** | `libgazebo_ros_gps.so` | `sensor_msgs/msg/NavSatFix` |

## Camera Simulation

Let's start with the most common sensor: cameras. A simulated camera renders the 3D world to 2D images, just like a real camera.

### Camera Plugin Configuration

```xml
<!-- Camera sensor on a robot link -->
<model name="my_robot">
  <link name="chassis">
    <!-- ... other link content ... -->

    <!-- Camera sensor -->
    <sensor name="camera" type="camera">
      <pose>0.2 0 0.1 0 0 0</pose>  <!-- Position relative to link -->
      <visualize>true</visualize>    <!-- Show camera frustum in Gazebo -->
      <update_rate>30</update_rate>  <!-- Hz (frames per second) -->

      <!-- Camera parameters -->
      <camera>
        <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees in radians -->
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>  <!-- RGB color -->
        </image>
        <clip>
          <near>0.1</near>   <!-- Near clipping plane (meters) -->
          <far>100</far>     <!-- Far clipping plane (meters) -->
        </clip>
        <noise>
          <type>gaussian</type>
          <mean>0</mean>
          <stddev>0.007</stddev>  <!-- Noise level -->
        </noise>
      </camera>

      <!-- ROS 2 plugin -->
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <!-- ROS 2 namespace -->
          <namespace></namespace>
          <remapping>image_raw:=/camera/image_raw</remapping>
          <remapping>camera_info:=/camera/camera_info</remapping>
        </ros>
        <camera_name>camera</camera_name>
        <frame_name>camera_link</frame_name>
        <hack_baseline>0.07</hack_baseline>
        <min_depth>0.1</min_depth>
        <max_depth>100</max_depth>
      </plugin>
    </sensor>
  </link>
</model>
```

### Understanding Camera Parameters

**Field of View (FOV)**: How wide the camera sees
- Wide FOV (90-120 degrees): See more, but objects appear smaller
- Narrow FOV (30-60 degrees): See less, but more detail per pixel
- `horizontal_fov` is specified in **radians** (1.047 rad = 60 degrees)

**Resolution**: Image dimensions in pixels
- Higher resolution = more detail but more processing
- Common: 640x480 (VGA), 1920x1080 (Full HD), 3840x2160 (4K)
- Trade-off: Resolution vs. frame rate vs. processing power

**Clip Planes**: Near and far rendering distances
- `near`: Closest visible distance (objects closer are clipped)
- `far`: Farthest visible distance (objects beyond are not rendered)
- Too small range: Z-fighting (flickering) or missing objects
- Too large range: Depth precision issues

**Noise Model**: Simulates realistic camera noise
- Gaussian noise adds random variation to each pixel
- `stddev` (standard deviation) controls noise amount
- Higher values = more grainy images (like low-light conditions)

### Reading Camera Data in ROS 2

Once your camera plugin is running, images are published to ROS 2 topics:

```bash
# See available topics
ros2 topic list | grep camera

# Output:
# /camera/camera_info
# /camera/image_raw

# View camera info (contains calibration data)
ros2 topic echo /camera/camera_info --once

# View image statistics
ros2 topic hz /camera/image_raw
```

**ROS 2 Node to Process Camera Images**:

```python
#!/usr/bin/env python3
"""
ROS 2 node that subscribes to camera images and detects objects.
This is a simplified example using color blob detection.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraProcessor(Node):
    """Process camera images to detect red objects"""

    def __init__(self):
        super().__init__('camera_processor')

        # Subscribe to camera images
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10  # QoS profile depth
        )

        # Bridge between ROS Image and OpenCV
        self.cv_bridge = CvBridge()

        self.get_logger().info('Camera Processor Started - Waiting for images...')

    def image_callback(self, msg):
        """Called when new image arrives"""
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Detect red objects (simple color threshold)
            # Convert to HSV color space
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

            # Red color range (two ranges in HSV)
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])

            # Create masks
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = mask1 + mask2

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw bounding boxes around detected objects
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # Filter small noise
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(cv_image, 'Red Object', (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display image (in development; use ROS topics for production)
            cv2.imshow('Camera View', cv_image)
            cv2.waitKey(1)

            # Log detection
            if len(contours) > 0:
                self.get_logger().info(f'Detected {len(contours)} red object(s)')

        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

def main():
    rclpy.init()
    processor = CameraProcessor()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [camera_processor]: Camera Processor Started - Waiting for images...
[INFO] [camera_processor]: Detected 1 red object(s)
[INFO] [camera_processor]: Detected 2 red object(s)
```

## LIDAR Simulation

LIDAR (Light Detection and Ranging) measures distance by casting laser rays and measuring return time. In simulation, we use ray-casting to calculate distances.

### 2D LIDAR (Laser Scan)

The most common LIDAR for ground robots is a 2D planar scanner:

```xml
<!-- 2D LIDAR sensor -->
<sensor name="laser" type="ray">
  <pose>0 0 0.1 0 0 0</pose>
  <visualize>true</visualize>
  <update_rate>10</update_rate>  <!-- 10 Hz scan rate -->

  <ray>
    <scan>
      <horizontal>
        <samples>360</samples>       <!-- Number of rays -->
        <resolution>1</resolution>   <!-- 1 = all samples, 0.5 = half resolution -->
        <min_angle>-3.14159</min_angle>  <!-- -180 degrees -->
        <max_angle>3.14159</max_angle>   <!-- +180 degrees -->
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>     <!-- Minimum range (meters) -->
      <max>10.0</max>    <!-- Maximum range (meters) -->
      <resolution>0.01</resolution>  <!-- Distance resolution -->
    </range>
    <noise>
      <type>gaussian</type>
      <mean>0</mean>
      <stddev>0.01</stddev>  <!-- 1cm noise -->
    </noise>
  </ray>

  <!-- ROS 2 plugin -->
  <plugin name="laser_controller" filename="libgazebo_ros_laser.so">
    <ros>
      <namespace></namespace>
      <remapping>scan:=/scan</remapping>
    </ros>
    <output_type>sensor_msgs/LaserScan</output_type>
    <frame_name>laser_link</frame_name>
  </plugin>
</sensor>
```

### Understanding LIDAR Parameters

**Samples vs Resolution**:
- `samples`: Total number of laser rays (360 = one per degree)
- `resolution`: Fraction of samples to use (1.0 = all, 0.5 = half)
- More samples = better angular resolution but more processing

**Angle Range**:
- `min_angle` and `max_angle`: Scan coverage in radians
- -3.14 to +3.14 = full 360-degree coverage
- Smaller range = faster scans but less coverage

**Range**:
- `min`: Closest measurable distance (laser blind spot)
- `max`: Farthest measurable distance
- Objects closer than `min` or farther than `max` are not detected

### Reading LIDAR Data in ROS 2

```python
#!/usr/bin/env python3
"""
ROS 2 node that reads LIDAR scans and detects obstacles.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class LidarProcessor(Node):
    """Process LIDAR scans for obstacle detection"""

    def __init__(self):
        super().__init__('lidar_processor')

        # Subscribe to LIDAR
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Publisher for obstacle warnings
        self.warning_pub = self.create_publisher(
            str,
            '/obstacle_warning',
            10
        )

        self.get_logger().info('LIDAR Processor Started')

    def scan_callback(self, msg):
        """Process each LIDAR scan"""
        # Find minimum distance in front quadrant (-45 to +45 degrees)
        front_start = len(msg.ranges) // 4  # -45 degrees
        front_end = 3 * len(msg.ranges) // 4  # +45 degrees

        front_ranges = msg.ranges[front_start:front_end]

        # Filter out inf and nan values
        valid_ranges = [r for r in front_ranges
                       if not math.isinf(r) and not math.isnan(r)]

        if valid_ranges:
            min_distance = min(valid_ranges)

            # Obstacle detection logic
            if min_distance < 0.5:
                self.get_logger().warn(f'OBSTACLE TOO CLOSE: {min_distance:.2f}m')
                self.warning_pub.publish('STOP')
            elif min_distance < 1.0:
                self.get_logger().info(f'Obstacle detected: {min_distance:.2f}m')
                self.warning_pub.publish('SLOW')
            else:
                # Clear path
                pass

            # Log full scan summary every 10 iterations
            if hasattr(self, '_counter'):
                self._counter += 1
            else:
                self._counter = 0

            if self._counter % 10 == 0:
                self.get_logger().info(
                    f'Scan: min={min(valid_ranges):.2f}m, '
                    f'max={max(valid_ranges):.2f}m, '
                    f'avg={sum(valid_ranges)/len(valid_ranges):.2f}m'
                )

def main():
    rclpy.init()
    processor = LidarProcessor()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [lidar_processor]: LIDAR Processor Started
[INFO] [lidar_processor]: Scan: min=0.45m, max=9.82m, avg=4.12m
[WARN] [lidar_processor]: OBSTACLE TOO CLOSE: 0.42m
[INFO] [lidar_processor]: Obstacle detected: 0.78m
[INFO] [lidar_processor]: Scan: min=0.78m, max=9.45m, avg=3.89m
```

## IMU Simulation

An IMU (Inertial Measurement Unit) measures acceleration and rotation—essential for robot balance and navigation.

### IMU Plugin Configuration

```xml
<!-- IMU sensor -->
<sensor name="imu_sensor" type="imu">
  <pose>0 0 0.05 0 0 0</pose>
  <visualize>true</visualize>
  <update_rate>100</update_rate>  <!-- 100 Hz for accurate integration -->

  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0</mean>
          <stddev>0.001</stddev>  <!-- Gyro noise (rad/s) -->
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0</mean>
          <stddev>0.001</stdev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0</mean>
          <stddev>0.001</stddev>
        </noise>
      </z>
    </angular_velocity>

    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0</mean>
          <stddev>0.015</stddev>  <!-- Accelerometer noise (m/s^2) -->
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0</mean>
          <stddev>0.015</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0</mean>
          <stddev>0.015</stddev>
        </noise>
      </z>
    </linear_acceleration>
  </imu>

  <!-- ROS 2 plugin -->
  <plugin name="imu_controller" filename="libgazebo_ros_imu.so">
    <ros>
      <namespace></namespace>
      <remapping>~/out:=/imu</remapping>
    </ros>
    <initial_orientation_as_reference>false</initial_orientation_as_reference>
    <frame_name>imu_link</frame_name>
  </plugin>
</sensor>
```

### Reading IMU Data in ROS 2

```python
#!/usr/bin/env python3
"""
ROS 2 node that reads IMU data and detects robot orientation/motion.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import math

class ImuProcessor(Node):
    """Process IMU data for orientation and motion detection"""

    def __init__(self):
        super().__init__('imu_processor')

        # Subscribe to IMU
        self.subscription = self.create_subscription(
            Imu,
            '/imu',
            self.imu_callback,
            10
        )

        self.get_logger().info('IMU Processor Started')

    def imu_callback(self, msg):
        """Process IMU measurements"""
        # Extract angular velocity (rad/s)
        wx = msg.angular_velocity.x
        wy = msg.angular_velocity.y
        wz = msg.angular_velocity.z

        # Extract linear acceleration (m/s^2)
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z

        # Calculate total rotation rate
        rotation_rate = math.sqrt(wx**2 + wy**2 + wz**2)

        # Calculate total acceleration magnitude
        acceleration = math.sqrt(ax**2 + ay**2 + az**2)

        # Detect motion states
        if rotation_rate > 0.1:
            self.get_logger().info(f'Rotating: {rotation_rate:.3f} rad/s')

        # Detect tilt (deviation from gravity)
        # If flat on ground, az should be ~9.81 m/s^2 (gravity)
        gravity_deviation = abs(az - 9.81)
        if gravity_deviation > 1.0:
            tilt_angle = math.degrees(math.asin(min(1.0, gravity_deviation / 9.81)))
            self.get_logger().warn(f'Tilted: ~{tilt_angle:.1f} degrees')

        # Detect collision (sudden acceleration)
        if acceleration > 12.0:
            self.get_logger().error(f'Collision detected! Acceleration: {acceleration:.2f} m/s^2')

def main():
    rclpy.init()
    processor = ImuProcessor()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [imu_processor]: IMU Processor Started
[INFO] [imu_processor]: Rotating: 0.234 rad/s
[WARN] [imu_processor]: Tilted: ~12.3 degrees
[ERROR] [imu_processor]: Collision detected! Acceleration: 14.23 m/s^2
```

## Complete Robot Example: Multiple Sensors

Let's put it all together with a robot that has camera, LIDAR, and IMU sensors:

```xml
<?xml version="1.0"?>
<sdf version="1.7">
  <model name="sensor_robot">
    <pose>0 0 0.5 0 0 0</pose>

    <!-- Static base -->
    <link name="chassis">
      <pose>0 0 0 0 0 0</pose>
      <inertial>
        <mass>5.0</mass>
        <inertia>
          <ixx>0.1</ixx><iyy>0.1</iyy><izz>0.1</izz>
        </inertia>
      </inertial>

      <collision name="collision">
        <geometry>
          <box><size>0.3 0.3 0.2</size></box>
        </geometry>
      </collision>

      <visual name="visual">
        <geometry>
          <box><size>0.3 0.3 0.2</size></box>
        </geometry>
        <material>
          <ambient>0 0.5 1 1</ambient>
          <diffuse>0 0.5 1 1</diffuse>
        </material>
      </visual>
    </link>

    <!-- Camera sensor -->
    <link name="camera_link">
      <pose>0.15 0 0.05 0 0 0</pose>
      <sensor name="camera" type="camera">
        <update_rate>30</update_rate>
        <camera>
          <horizontal_fov>1.047</horizontal_fov>
          <image>
            <width>640</width>
            <height>480</height>
          </image>
          <clip><near>0.1</near><far>10</far></clip>
        </camera>
        <plugin name="camera_plugin" filename="libgazebo_ros_camera.so">
          <ros>
            <remapping>image_raw:=/camera/image_raw</remapping>
          </ros>
          <frame_name>camera_link</frame_name>
        </plugin>
      </sensor>
    </link>

    <!-- LIDAR sensor -->
    <link name="laser_link">
      <pose>0 0 0.15 0 0 0</pose>
      <sensor name="laser" type="ray">
        <visualize>true</visualize>
        <update_rate>10</update_rate>
        <ray>
          <scan>
            <horizontal>
              <samples>360</samples>
              <min_angle>-3.14159</min_angle>
              <max_angle>3.14159</max_angle>
            </horizontal>
          </scan>
          <range><min>0.1</min><max>10.0</max></range>
        </ray>
        <plugin name="laser_plugin" filename="libgazebo_ros_laser.so">
          <ros><remapping>scan:=/scan</remapping></ros>
          <frame_name>laser_link</frame_name>
        </plugin>
      </sensor>
    </link>

    <!-- IMU sensor -->
    <link name="imu_link">
      <pose>0 0 0.1 0 0 0</pose>
      <sensor name="imu" type="imu">
        <update_rate>100</update_rate>
        <imu>
          <angular_velocity>
            <x><noise><mean>0</mean><stddev>0.001</stddev></noise></x>
            <y><noise><mean>0</mean><stddev>0.001</stddev></noise></y>
            <z><noise><mean>0</mean><stddev>0.001</stddev></noise></z>
          </angular_velocity>
          <linear_acceleration>
            <x><noise><mean>0</mean><stddev>0.015</stddev></noise></x>
            <y><noise><mean>0</mean><stddev>0.015</stddev></noise></y>
            <z><noise><mean>0</mean><stddev>0.015</stddev></noise></z>
          </linear_acceleration>
        </imu>
        <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
          <ros><remapping>~/out:=/imu</remapping></ros>
          <frame_name>imu_link</frame_name>
        </plugin>
      </sensor>
    </link>

    <!-- Joints to attach sensor links -->
    <joint name="camera_joint" type="fixed">
      <parent>chassis</parent>
      <child>camera_link</child>
    </joint>
    <joint name="laser_joint" type="fixed">
      <parent>chassis</parent>
      <child>laser_link</child>
    </joint>
    <joint name="imu_joint" type="fixed">
      <parent>chassis</parent>
      <child>imu_link</child>
    </joint>
  </model>
</sdf>
```

## Sensor Fusion: Combining Multiple Sensors

Real robots combine data from multiple sensors—a process called **sensor fusion**. Each sensor has strengths and weaknesses:

| Sensor | Strengths | Weaknesses |
|--------|-----------|------------|
| **Camera** | Rich semantic info (objects, colors, text) | Affected by lighting, no direct depth |
| **LIDAR** | Accurate distance, works in dark | Low resolution, no color/texture |
| **IMU** | Fast motion detection, orientation | Drifts over time, no position |

**Example**: A robot navigating a hallway might use:
- Camera: Recognize door numbers and signs
- LIDAR: Detect walls and obstacles in 3D
- IMU: Detect when robot is stuck (wheels spinning but not moving)

## Hardware Requirements and Alternatives

### Minimum Requirements (Simulation-Only)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 8 GB | 16 GB |
| **GPU** | Integrated graphics | NVIDIA RTX 4070 Ti (12GB VRAM) |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS native |

### Performance Tips for Sensor Simulation

1. **Reduce camera resolution**: 320x240 instead of 1920x1080
2. **Lower update rates**: 10 Hz instead of 30 Hz for testing
3. **Reduce LIDAR samples**: 180 instead of 360 rays
4. **Disable visualization**: Set `<visualize>false</visualize>` for sensors
5. **Use headless mode**: Run Gazebo without GUI for batch testing

### Cloud Alternatives

- **NVIDIA Omniverse Cloud**: Run heavy sensor simulations in browser
- **AWS RoboMaker**: Cloud-based robotics development
- **Google Colab**: Free GPU for basic image processing

## Try With AI

### Exercise 1: Design a Sensor Suite for a Delivery Robot

```text
I'm designing a delivery robot that navigates office buildings and delivers packages to specific rooms. The robot needs to:

1. Navigate hallways and avoid obstacles
2. Read room numbers and door signs
3. Detect when it's stuck or colliding
4. Know its rough location in the building

Help me design the sensor configuration by:
1. Specifying which sensors I need (camera, LIDAR, IMU, etc.) and why each is necessary
2. For each sensor, recommend key Gazebo parameters (resolution, FOV, range, update rate) with justification
3. Explain how these sensors complement each other's weaknesses
4. Describe a sensor fusion approach: how would the robot combine data from multiple sensors?

After we design the configuration, help me write the Gazebo SDF sensor plugin configuration for one sensor.
```

**What you're learning:** This exercise develops your ability to select and configure sensors for specific robotics applications. You'll practice matching sensor capabilities to task requirements, understanding trade-offs (cost vs. performance), and designing sensor fusion strategies. This systems-thinking skill is essential for robotics engineers—choosing the right sensors can make or break a robot's performance.

### Exercise 2: Debug Sensor Simulation Issues

```text
I have a Gazebo simulation with sensors, but I'm experiencing these issues:

1. Camera images are always black (no scene visible)
2. LIDAR shows infinity for all distances
3. IMU data never changes (always reads zero acceleration)

Help me debug by:
1. Identifying 2-3 possible causes for each symptom
2. Explaining how to diagnose each issue (what to check, what commands to run)
3. Providing specific fixes for common problems
4. Creating a diagnostic checklist I can use when sensors aren't working

For each solution, explain the underlying cause—why does this fix work?
```

**What you're learning:** This exercise builds your debugging intuition for sensor simulation. Rather than memorizing fixes, you'll understand the common failure modes and how to systematically diagnose them. This skill is invaluable when your simulated robot "goes blind"—you'll know exactly where to look and what to check.

### Exercise 3: Implement Sensor Fusion with ROS 2

```text
I want to create a ROS 2 node that fuses data from camera and LIDAR for better obstacle detection.

Requirements:
- Subscribe to both /camera/image_raw and /scan topics
- When LIDAR detects an object within 2 meters, check if camera sees a red object in that direction
- Only report obstacles that are BOTH close (LIDAR) AND red (camera)
- Publish warnings to a /obstacles topic

Help me by:
1. Explaining the coordinate system challenge: how to map LIDAR angles to camera pixels
2. Providing the Python code structure for this sensor fusion node
3. Suggesting how to synchronize messages from sensors with different update rates (10 Hz LIDAR vs 30 Hz camera)
4. Explaining how this fusion approach reduces false positives compared to using either sensor alone

Also discuss: what are the limitations of this simple fusion approach?
```

**What you're learning:** This exercise teaches you the fundamentals of sensor fusion—combining data from multiple sensors to produce better information than either sensor alone. You'll learn practical challenges like coordinate transformations, message synchronization, and timestamp handling. These skills are directly applicable to real robotics projects where sensor fusion is essential for robust perception.
