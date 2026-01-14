---
sidebar_position: 4
title: "URDF and Robot Models"
description: "Learn how to describe robots using URDF (Unified Robot Description Format). Create robot models with links, joints, visual and collision elements, and visualize them in RViz."
keywords: ["URDF", "Robot Modeling", "ROS 2", "RViz", "Links", "Joints", "XML", "Robot Description"]
chapter: 2
lesson: 4
duration_minutes: 90

requirements:
  hardware: "Any computer with ROS 2 Humble installed"
  software: "ROS 2 Humble, Python 3, RViz2, colcon build system"

skills:
  - name: "URDF Robot Description"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "1.2 Interacting with digital devices and systems"
    measurable_at_this_level: "Student can create a valid URDF file describing a simple robot with links and joints"

  - name: "Robot Visualization in RViz"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "1.2 Interacting with digital devices and systems"
    measurable_at_this_level: "Student can load and display a URDF model in RViz2"

  - name: "Joint Type Selection"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Analyze"
    digcomp_area: "3.3 Digital content creation"
    measurable_at_this_level: "Student can select appropriate joint types (revolute, prismatic, fixed) for robot mechanisms"

learning_objectives:
  - objective: "Explain the purpose of URDF and how it represents robots as tree structures of links and joints"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Written explanation or diagram of robot tree structure"

  - objective: "Create a complete URDF file defining a simple robot with multiple links and joints"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code submission - URDF file that loads without errors in ROS 2"

  - objective: "Add visual, collision, and inertial properties to robot links for realistic simulation"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "URDF with complete link properties verified in RViz2"

  - objective: "Visualize a URDF robot model in RViz2 and verify joint transformations work correctly"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Screenshot of robot displayed in RViz with joint positions manipulated"

cognitive_load:
  new_concepts: 9
  assessment: "Students will create a URDF file from scratch, load it in ROS 2, and visualize it in RViz2. Success is measured by a correctly displayed robot model with movable joints"

differentiation:
  extension_for_advanced: "Add continuous and revolute joints with position limits, create a multi-degree-of-freedom robotic arm with 3+ joints"
  remedial_for_struggling: "Start with a pre-written 2-link URDF template and focus on understanding the link-joint relationship before adding complexity"
  hardware_alternatives: "All exercises work in RViz2 simulation. No physical robot required. Students can use online ROS 2 environments like The Construct if local installation unavailable"

safety_notes: "No physical hardware required. Always verify URDF syntax before loading to prevent XML parsing errors in ROS 2"

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# URDF and Robot Models

Imagine you're building a digital twin of a humanoid robot. You need to describe every part: the torso, head, arms, legs, and how they connect. How do you tell ROS 2 what your robot looks like? How does the navigation system know where the wheels are? How does the arm controller know which joint connects the upper arm to the forearm?

You need a language for describing robots—a format that specifies geometry, joints, sensors, and how everything connects. This is **URDF** (Unified Robot Description Format), the XML-based language that ROS 2 uses to represent robot models. Every robot in ROS 2, from simple wheeled platforms to complex humanoids, has a URDF file that tells the system exactly what the robot is made of.

## What is URDF?

**URDF** (Unified Robot Description Format) is an XML file format that describes your robot's physical properties. Think of it as a blueprint that ROS 2 tools like RViz (visualization), Gazebo (simulation), and MoveIt (motion planning) all read to understand your robot.

### Why URDF Matters

Without URDF, every ROS 2 tool would need its own way to represent robots. You'd describe your robot three times: once for visualization, once for simulation, and once for motion planning. URDF provides a single source of truth.

**Key benefits**:
- **Visualization**: See your robot in RViz before building it
- **Simulation**: Test controllers in Gazebo without risking hardware
- **Motion Planning**: MoveIt uses URDF to calculate valid robot poses
- **Code generation**: Generate robot-specific code automatically from the model

### URDF as a Tree Structure

URDF represents robots as a **tree** of links connected by joints:

```
        [base_link]
             |
        [joint_1]
             |
             v
      [link_1] ----- [joint_2] -----> [link_2]
             |
        [joint_3]
             |
             v
      [link_3] (end effector)
```

**Tree rules**:
- Every robot has exactly one **root link** (usually called `base_link`)
- Links connect through **joints**
- Each joint has exactly one **parent link** and one **child link**
- The structure is acyclic (no loops—a joint cannot connect back to an ancestor)

This tree structure matches how most robots are built: a base, with attachments branching out, ending in end-effectors (grippers, cameras, tools).

## URDF File Structure

A URDF file is XML with a specific structure. Here's the skeleton:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
    <!-- Links define physical parts -->
    <link name="base_link">
        <!-- link properties -->
    </link>

    <!-- Joints define connections between links -->
    <joint name="joint1" type="revolute">
        <!-- joint properties -->
    </joint>
</robot>
```

### Essential Elements

| Element | Purpose | Required |
|---------|---------|----------|
| `<robot>` | Root element, contains entire model | Yes |
| `<link>` | Defines a physical part of the robot | At least 1 |
| `<joint>` | Defines connection between two links | For movement |
| `<link>` visual | How the link looks (for display) | Recommended |
| `<link>` collision | Physical shape (for physics) | Recommended |
| `<link>` inertial | Mass and inertia (for dynamics) | Required for simulation |

## Links: Robot Parts

A **link** represents a rigid body—something that doesn't deform. A robot arm segment, a wheel, a camera housing, or a gripper finger could all be links.

### Link Structure

```xml
<link name="link_name">
    <!-- Visual: how it looks -->
    <visual>
        <geometry>
            <!-- shape definition -->
        </geometry>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <material name="blue">
            <color rgba="0 0 1 1"/>
        </material>
    </visual>

    <!-- Collision: physics shape -->
    <collision>
        <geometry>
            <!-- shape definition -->
        </geometry>
        <origin xyz="0 0 0" rpy="0 0 0"/>
    </collision>

    <!-- Inertial: mass properties -->
    <inertial>
        <mass value="1.0"/>
        <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
</link>
```

### Geometry Types

URDF supports several geometric primitives:

| Shape | XML Tag | Parameters | Use Case |
|-------|---------|------------|----------|
| **Box** | `<box size="x y z"/>` | Length in each axis | Limb segments, robot body |
| **Cylinder** | `<cylinder length="L" radius="r"/>` | Length, radius | Arms, legs, wheels |
| **Sphere** | `<sphere radius="r"/>` | Radius | Joint housings, end-effectors |
| **Mesh** | `<mesh filename="package://path/file.stl"/>` | 3D model file | Complex shapes (hands, torso) |

### Visual vs Collision Geometry

**Important distinction**: Visual and collision geometry can be different.

```xml
<link name="arm_segment">
    <!-- Visual: detailed mesh for appearance -->
    <visual>
        <geometry>
            <mesh filename="package://my_robot/meshes/arm.dae"/>
        </geometry>
    </visual>

    <!-- Collision: simple box for physics (faster) -->
    <collision>
        <geometry>
            <box size="0.1 0.1 0.5"/>
        </geometry>
    </collision>
</link>
```

**Why separate them?**
- Visual can be complex (hundreds of polygons) for realism
- Collision should be simple (box, cylinder, sphere) for physics performance
- Simulation uses collision geometry, not visual

### Origin and Coordinate Frames

The `<origin>` tag defines the link's reference frame relative to its parent:

```xml
<origin xyz="x y z" rpy="r p y"/>
```

- **xyz**: Position offset (meters)
- **rpy**: Rotation in Roll-Pitch-Yaw angles (radians)

**Example**: A joint positioned 0.5m above the parent, rotated 90 degrees around the Z-axis:

```xml
<origin xyz="0 0 0.5" rpy="0 0 1.571"/>
```

## Joints: Robot Connections

A **joint** defines how two links connect and move relative to each other.

### Joint Structure

```xml
<joint name="joint_name" type="joint_type">
    <parent link="parent_link_name"/>
    <child link="child_link_name"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
</joint>
```

### Joint Types

| Type | Motion | Example | Axis? | Limits? |
|------|--------|---------|-------|---------|
| **revolute** | Rotates around axis | Door hinge, robot arm joint | Yes | Yes |
| **continuous** | Rotates infinitely | Wheels, spinning gears | Yes | No |
| **prismatic** | Slides along axis | Linear actuator, drawer slide | Yes | Yes |
| **fixed** | No motion | Rigid attachment | No | No |
| **floating** | 6 DOF (rare) | Free-floating object | No | No |
| **planar** | Motion in plane | Hovering drone (2D) | No | No |

### Revolute Joint Example

A typical robot arm joint:

```xml
<joint name="shoulder_pan_joint" type="revolute">
    <parent link="torso"/>
    <child link="upper_arm"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1.0"/>
</joint>
```

**What this means**:
- Parent: `torso`, Child: `upper_arm`
- Joint origin: 0.3m above torso
- Rotation axis: Z-axis (vertical)
- Limits: -90 to +90 degrees (-1.57 to 1.57 radians)
- Max effort: 50 Nm, Max velocity: 1 rad/s

### Fixed Joint Example

A camera rigidly attached to a robot head:

```xml
<joint name="camera_mount_joint" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.1 0 0.05" rpy="0 0.3 0"/>
</joint>
```

No axis or limits needed—this joint never moves.

### Continuous Joint Example

A drive wheel:

```xml
<joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.15 0" rpy="-1.57 0 0"/>
    <axis xyz="0 0 1"/>
    <limit effort="10" velocity="10"/>
</joint>
```

**Note**: Continuous joints have effort/velocity limits but no position limits (they spin infinitely).

## Creating Your First URDF

Let's build a simple robot: a mobile base with a single arm segment. This will demonstrate the complete URDF workflow.

### Step 1: Create the Package

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Navigate to workspace
cd ~/ros2_ws/src

# Create package
ros2 pkg create --build-type ament_python my_robot_description --dependencies rclpy
```

### Step 2: Create the URDF Directory

```bash
cd my_robot_description
mkdir urdf
mkdir launch
mkdir meshes
```

### Step 3: Write the URDF File

Create `urdf/my_first_robot.urdf`:

```xml
<?xml version="1.0"?>
<robot name="my_first_robot">
    <!-- ============================================ -->
    <!-- BASE LINK (root of the robot tree)           -->
    <!-- ============================================ -->
    <link name="base_link">
        <visual>
            <geometry>
                <cylinder length="0.1" radius="0.2"/>
            </geometry>
            <origin xyz="0 0 0" rpy="0 0 0"/>
            <material name="gray">
                <color rgba="0.5 0.5 0.5 1"/>
            </material>
        </visual>
        <collision>
            <geometry>
                <cylinder length="0.1" radius="0.2"/>
            </geometry>
            <origin xyz="0 0 0" rpy="0 0 0"/>
        </collision>
        <inertial>
            <mass value="1.0"/>
            <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
        </inertial>
    </link>

    <!-- ============================================ -->
    <!-- WHEELS (4 fixed joints, 1 continuous wheel)  -->
    <!-- ============================================ -->
    <link name="left_wheel">
        <visual>
            <geometry>
                <cylinder length="0.05" radius="0.05"/>
            </geometry>
            <origin xyz="0 0 0" rpy="1.57 0 0"/>
            <material name="black">
                <color rgba="0.1 0.1 0.1 1"/>
            </material>
        </visual>
        <collision>
            <geometry>
                <cylinder length="0.05" radius="0.05"/>
            </geometry>
            <origin xyz="0 0 0" rpy="1.57 0 0"/>
        </collision>
        <inertial>
            <mass value="0.1"/>
            <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
        </inertial>
    </link>

    <joint name="left_wheel_joint" type="continuous">
        <parent link="base_link"/>
        <child link="left_wheel"/>
        <origin xyz="0 0.2 0" rpy="0 0 0"/>
        <axis xyz="0 1 0"/>
        <limit effort="1.0" velocity="10.0"/>
    </joint>

    <!-- Right wheel (similar structure) -->
    <link name="right_wheel">
        <visual>
            <geometry>
                <cylinder length="0.05" radius="0.05"/>
            </geometry>
            <origin xyz="0 0 0" rpy="1.57 0 0"/>
            <material name="black">
                <color rgba="0.1 0.1 0.1 1"/>
            </material>
        </visual>
        <collision>
            <geometry>
                <cylinder length="0.05" radius="0.05"/>
            </geometry>
            <origin xyz="0 0 0" rpy="1.57 0 0"/>
        </collision>
        <inertial>
            <mass value="0.1"/>
            <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
        </inertial>
    </link>

    <joint name="right_wheel_joint" type="continuous">
        <parent link="base_link"/>
        <child link="right_wheel"/>
        <origin xyz="0 -0.2 0" rpy="0 0 0"/>
        <axis xyz="0 1 0"/>
        <limit effort="1.0" velocity="10.0"/>
    </joint>

    <!-- ============================================ -->
    <!-- ARM: Base segment                            -->
    <!-- ============================================ -->
    <link name="arm_base_link">
        <visual>
            <geometry>
                <box size="0.1 0.1 0.2"/>
            </geometry>
            <origin xyz="0 0 0.1" rpy="0 0 0"/>
            <material name="blue">
                <color rgba="0 0 1 1"/>
            </material>
        </visual>
        <collision>
            <geometry>
                <box size="0.1 0.1 0.2"/>
            </geometry>
            <origin xyz="0 0 0.1" rpy="0 0 0"/>
        </collision>
        <inertial>
            <mass value="0.5"/>
            <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.005"/>
        </inertial>
    </link>

    <joint name="arm_base_joint" type="revolute">
        <parent link="base_link"/>
        <child link="arm_base_link"/>
        <origin xyz="0 0 0.05" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
    </joint>

    <!-- ============================================ -->
    <!-- ARM: Upper segment                            -->
    <!-- ============================================ -->
    <link name="arm_upper_link">
        <visual>
            <geometry>
                <box size="0.08 0.08 0.3"/>
            </geometry>
            <origin xyz="0 0 0.15" rpy="0 0 0"/>
            <material name="red">
                <color rgba="1 0 0 1"/>
            </material>
        </visual>
        <collision>
            <geometry>
                <box size="0.08 0.08 0.3"/>
            </geometry>
            <origin xyz="0 0 0.15" rpy="0 0 0"/>
        </collision>
        <inertial>
            <mass value="0.3"/>
            <inertia ixx="0.003" ixy="0" ixz="0" iyy="0.003" iyz="0" izz="0.003"/>
        </inertial>
    </link>

    <joint name="elbow_joint" type="revolute">
        <parent link="arm_base_link"/>
        <child link="arm_upper_link"/>
        <origin xyz="0 0 0.2" rpy="0 0 0"/>
        <axis xyz="1 0 0"/>
        <limit lower="-1.57" upper="1.57" effort="5" velocity="1.0"/>
    </joint>
</robot>
```

## Visualizing in RViz2

Now let's see your robot in RViz2, the ROS 2 visualization tool.

### Step 1: Create a Launch File

Create `launch/display_robot.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the path to your URDF file
    urdf_file = os.path.join(
        get_package_share_directory('my_robot_description'),
        'urdf',
        'my_first_robot.urdf'
    )

    # Read the URDF file
    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([
        # Robot State Publisher - publishes TF transforms from URDF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}]
        ),
        # Joint State Publisher - allows manual joint control
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        # RViz2 - visualization
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        ),
    ])
```

### Step 2: Build and Launch

```bash
# Build the package
cd ~/ros2_ws
colcon build --packages-select my_robot_description

# Source the workspace
source install/setup.bash

# Launch the visualization
ros2 launch my_robot_description display_robot.launch.py
```

**Output:**
- RViz2 window opens showing your robot
- Joint State Publisher GUI window appears with sliders
- Moving sliders controls robot joints in real-time

### Step 3: Configure RViz Display

If the robot doesn't appear immediately:

1. In RViz, click **Add** → **RobotModel**
2. Set **Fixed Frame** to `base_link`
3. Your robot should now be visible

### Step 4: Test Joint Movement

Use the Joint State Publisher GUI sliders to move:

- `arm_base_joint`: Rotates the arm base
- `elbow_joint`: Bends the elbow
- `left_wheel_joint` / `right_wheel_joint`: Spin the wheels

**What's happening**:
1. You move a slider in the GUI
2. `joint_state_publisher_gui` publishes joint state messages
3. `robot_state_publisher` reads your URDF and calculates transforms
4. RViz2 receives transforms and updates the robot display

## Verifying Your URDF

ROS 2 provides tools to check your URDF for errors.

### Check URDF Syntax

```bash
# Check the URDF file for XML syntax errors
xacro ~/ros2_ws/src/my_robot_description/urdf/my_first_robot.urdf
```

**Output (if valid):**
```
No errors found.
```

**Output (if errors):**
```
Error: XML parsing error
```

### View URDF Structure

```bash
# Print the robot structure
urdf_to_graphiz ~/ros2_ws/src/my_robot_description/urdf/my_first_robot.urdf
```

This generates a PDF showing your robot's tree structure.

### Check with check_urdf

```bash
check_urdf ~/ros2_ws/src/my_robot_description/urdf/my_first_robot.urdf
```

**Output:**
```
robot name is: my_first_robot
---------- Successfully Parsed XML ---------------
root link: base_link has 3 children
    child(1): left_wheel
    child(2): right_wheel
    child(3): arm_base_link
...
```

## Adding Sensors to Your Robot

Robots need sensors to perceive the world. Here's how to add a camera and LIDAR.

### Camera Sensor

```xml
<!-- Camera link -->
<link name="camera_link">
    <visual>
        <geometry>
            <box size="0.05 0.1 0.05"/>
        </geometry>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <material name="black">
            <color rgba="0 0 0 1"/>
        </material>
    </visual>
    <collision>
        <geometry>
            <box size="0.05 0.1 0.05"/>
        </geometry>
    </collision>
    <inertial>
        <mass value="0.05"/>
        <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
</link>

<!-- Camera joint (fixed to arm) -->
<joint name="camera_joint" type="fixed">
    <parent link="arm_upper_link"/>
    <child link="camera_link"/>
    <origin xyz="0 0 0.3" rpy="0 0.3 0"/>
</joint>
```

### LIDAR Sensor

```xml
<!-- LIDAR link -->
<link name="laser_link">
    <visual>
        <geometry>
            <cylinder length="0.1" radius="0.05"/>
        </geometry>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <material name="dark_gray">
            <color rgba="0.3 0.3 0.3 1"/>
        </material>
    </visual>
    <collision>
        <geometry>
            <cylinder length="0.1" radius="0.05"/>
        </geometry>
    </collision>
    <inertial>
        <mass value="0.2"/>
        <inertia ixx="0.0005" ixy="0" ixz="0" iyy="0.0005" iyz="0" izz="0.0005"/>
    </inertial>
</link>

<!-- LIDAR joint (on top of base) -->
<joint name="laser_joint" type="revolute">
    <parent link="base_link"/>
    <child link="laser_link"/>
    <origin xyz="0 0 0.15" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="1" velocity="10"/>
</joint>
```

## Inertia Calculations

Inertia tensors describe how mass is distributed. They're required for physics simulation but can be complex to calculate.

### Simplified Inertia Formulas

For basic shapes, use these approximations:

```xml
<!-- Solid box: size = (x, y, z), mass = m -->
<inertial>
    <mass value="m"/>
    <inertia ixx="m/12*(y^2+z^2)" ixy="0" ixz="0"
              iyy="m/12*(x^2+z^2)" iyz="0"
              izz="m/12*(x^2+y^2)"/>
</inertial>

<!-- Solid cylinder: radius = r, length = h, mass = m -->
<inertial>
    <mass value="m"/>
    <inertia ixx="m/12*(3r^2+h^2)" ixy="0" ixz="0"
              iyy="m/12*(3r^2+h^2)" iyz="0"
              izz="m/2*r^2"/>
</inertial>

<!-- Solid sphere: radius = r, mass = m -->
<inertial>
    <mass value="m"/>
    <inertia ixx="2*m/5*r^2" ixy="0" ixz="0"
              iyy="2*m/5*r^2" iyz="0"
              izz="2*m/5*r^2"/>
</inertial>
```

### Quick Calculation Tool

For simple robots, use [inertia calculators online](https://www.wolframalpha.com/input?i=moment+of+inertia+calculator) or use the `solid_primitives` inertia values as reasonable approximations.

## Common URDF Mistakes

### Mistake 1: Forgetting Root Link

**Wrong**: No links defined, or links form a cycle

```xml
<!-- WRONG: No root link specified -->
<robot name="bad_robot">
    <joint name="j1" type="fixed">
        <parent link="link1"/>
        <child link="link2"/>
    </joint>
    <!-- link1 and link2 never defined! -->
</robot>
```

**Correct**: Define base_link first

```xml
<robot name="good_robot">
    <link name="base_link">
        <!-- properties -->
    </link>
    <joint name="j1" type="fixed">
        <parent link="base_link"/>
        <child link="link1"/>
    </joint>
</robot>
```

### Mistake 2: Joint Reference Errors

**Wrong**: Referencing undefined links

```xml
<!-- WRONG: link doesn't exist -->
<joint name="bad_joint" type="fixed">
    <parent link="nonexistent_link"/>
    <child link="base_link"/>
</joint>
```

### Mistake 3: Missing Inertial Properties

**Problem**: Simulation fails because physics engine can't compute dynamics

```xml
<!-- WRONG: No inertial tag -->
<link name="arm_link">
    <visual>...</visual>
    <collision>...</collision>
    <!-- Missing inertial! -->
</link>
```

**Correct**: Always include inertial for simulation

```xml
<link name="arm_link">
    <visual>...</visual>
    <collision>...</collision>
    <inertial>
        <mass value="0.5"/>
        <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
</link>
```

## Using Xacro for Reusable URDF

As your robot gets complex, repeating code becomes tedious. **Xacro** (XML Macros) lets you create reusable URDF components.

### Simple Xacro Example

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="xacro_robot">

    <!-- Define a reusable wheel macro -->
    <xacro:macro name="wheel" params="prefix reflect">
        <link name="${prefix}_wheel">
            <visual>
                <geometry>
                    <cylinder length="0.05" radius="0.05"/>
                </geometry>
                <origin xyz="0 0 0" rpy="1.57 0 0"/>
            </visual>
            <inertial>
                <mass value="0.1"/>
                <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
            </inertial>
        </link>

        <joint name="${prefix}_wheel_joint" type="continuous">
            <parent link="base_link"/>
            <child link="${prefix}_wheel"/>
            <origin xyz="0 ${reflect * 0.2} 0" rpy="0 0 0"/>
            <axis xyz="0 1 0"/>
        </joint>
    </xacro:macro>

    <!-- Use the macro twice -->
    <xacro:wheel prefix="left" reflect="1"/>
    <xacro:wheel prefix="right" reflect="-1"/>

</robot>
```

**Xacro benefits**:
- Define components once, reuse multiple times
- Parameterized components (size, position, etc.)
- Mathematical expressions in values
- Conditional includes

## Try With AI

### Exercise 1: Design a Robot Arm

```text
I'm learning URDF for robot modeling. I need to design a simple 3-DOF (degree of freedom) robotic arm.

The arm should have:
1. A base link that connects to a table
2. A shoulder joint (revolute) connecting base to upper arm
3. An elbow joint (revolute) connecting upper arm to forearm
4. A wrist joint (revolute) connecting forearm to gripper

For each joint:
- Specify the joint type
- Define appropriate limits (in radians) for human-like motion
- Choose the rotation axis
- Specify origin offsets between links

Generate the complete URDF XML for this arm. Include visual and collision geometries (use boxes for arm segments).
```

**What you're learning:** This exercise solidifies your understanding of the URDF tree structure and joint properties. By designing a multi-joint arm, you'll practice defining parent-child relationships, choosing appropriate joint limits for realistic motion, and positioning links correctly relative to each other. This design skill is essential before building any robot—whether in simulation or reality.

### Exercise 2: Debug a Broken URDF

```text
I have this URDF file that won't load in RViz. Here's the content:

<?xml version="1.0"?>
<robot name="broken_robot">
    <link name="base_link">
        <visual>
            <geometry>
                <box size="0.5 0.5 0.2"/>
            </geometry>
        </visual>
    </link>

    <joint name="arm_joint" type="revolute">
        <parent link="base_link"/>
        <child link="arm_link"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57"/>
    </joint>

    <link name="arm_link">
        <visual>
            <geometry>
                <cylinder length="0.5" radius="0.1"/>
            </geometry>
        </visual>
    </link>
</robot>

RViz shows an error: "No transform from base_link to arm_link"

What are 3 problems with this URDF, and how would I fix each one?
```

**What you're learning:** Debugging URDF files is a critical robotics skill. This exercise teaches you to identify common errors like missing origin tags, incomplete link definitions (missing collision/inertial), and improper joint configurations. You'll learn systematic debugging: check the tree structure, verify all required tags are present, and ensure parent-child relationships are properly defined.

### Exercise 3: Compare URDF Approaches

```text
I want to model a robot gripper with two fingers that open and close.

Option 1: Use a single "gripper" link with a prismatic joint to a "fingers" link

Option 2: Use separate "left_finger" and "right_finger" links, each with their own prismatic joint to the "palm" link

Compare these two approaches:
1. Which is more realistic for simulation?
2. Which allows independent finger control?
3. Which is better for grasping objects of different sizes?
4. Generate the URDF code for the better approach
```

**What you're learning:** This exercise develops your ability to make design decisions when modeling robots. You'll learn that how you structure your URDF affects what behaviors are possible—independent finger control vs. synchronized motion, realistic collision detection, and grasp quality. This architectural thinking separates "code that works" from "well-designed robot models" suitable for real applications like manipulation and grasping.
