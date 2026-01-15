---
sidebar_position: 4
title: "Creating Simulation Worlds with SDF"
description: "Learn to build custom Gazebo worlds using SDF (Simulation Description Format). Create environments with models, lights, physics settings, and spawn robots for testing."
keywords: ["SDF", "Gazebo", "World Files", "Simulation", "ROS 2", "Fuel Models"]
chapter: 3
lesson: 4
duration_minutes: 90

requirements:
  hardware: "Any computer with integrated GPU (minimum) or NVIDIA RTX GPU (recommended)"
  software: "Ubuntu 22.04 LTS, Gazebo Fortress, ROS 2 Humble"

skills:
  - name: "SDF World Structure"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can identify the basic structure of an SDF world file and explain the purpose of main sections"

  - name: "World Customization"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can create a custom world file with lighting, models, and physics settings"

  - name: "Model Spawning"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can include models from Gazebo Fuel and position them in a world"

learning_objectives:
  - objective: "Identify and explain the purpose of the main SDF world file sections (physics, lights, models, plugins)"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Labeling exercise matching SDF tags to their functions"

  - objective: "Create a custom SDF world file with a sun light source, ground plane, and at least three positioned models"
    proficiency_level: "A2"
    bloom_level: "Apply"
    assessment_method: "Hands-on exercise with verified world file execution"

  - objective: "Use ROS 2 spawn commands to add a robot to a running Gazebo world at a specified position"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Terminal exercise demonstrating robot spawning"

cognitive_load:
  new_concepts: 7
  assessment: "Students will create a custom world file and demonstrate spawning a robot via ROS 2 commands"

differentiation:
  extension_for_advanced: "Create a multi-room environment with doors, furniture, and dynamic lighting. Add a custom physics profile for different surface materials"
  remedial_for_struggling: "Focus on modifying an existing world file template rather than starting from scratch. Use the GUI initially to understand positions, then translate to SDF"
  hardware_alternatives: "Students without adequate GPU can use simplified worlds with fewer models and reduced physics fidelity, or use cloud-based Gazebo instances"

safety_notes: null

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Creating Simulation Worlds with SDF

Imagine you're building a virtual warehouse to test a delivery robot. You need shelves, boxes, doorways, and lighting conditions that match reality. You could manually drag each object into Gazebo every time you test, but that's tedious and error-prone. Instead, you define your entire world once in a text file—the **SDF world file**—and recreate it perfectly every time.

**SDF** (Simulation Description Format) is Gazebo's XML-based language for describing worlds. It's like HTML for robot simulations: you write text that defines everything in your virtual environment—lights, physics, models, and their positions. When you launch the world file, Gazebo builds your simulation exactly as specified.

This lesson teaches you to write SDF world files, giving you the power to create reproducible test environments for your robots.

## The SDF World File Structure

Every Gazebo world file follows the same basic structure. Understanding this anatomy helps you read and modify any world file, or create your own from scratch.

### Minimal World Template

All SDF world files start with these required tags:

```xml
<?xml version="1.0" ?>
<sdf version="1.8">
    <world name="my_world">
        <!-- Everything goes here -->
    </world>
</sdf>
```

**What each part means**:
- `<?xml version="1.0" ?>`: Declares this as XML (required first line)
- `<sdf version="1.8">`: Specifies SDF format version
- `<world name="my_world">`: The world container where you define all elements
- `</world>` and `</sdf>`: Closing tags (every opening tag must close)

### Essential World Sections

A functional world needs at least these four sections:

```
+-----------------------------------------------------------+
|                     <world>                               |
|  +-----------------------------------------------------+  |
|  |  <physics>    - Dynamics engine settings            |  |
|  +-----------------------------------------------------+  |
|  +-----------------------------------------------------+  |
|  |  <light>      - Sun, lamps, ambient illumination     |  |
|  +-----------------------------------------------------+  |
|  +-----------------------------------------------------+  |
|  |  <model>      - Objects, robots, obstacles           |  |
|  +-----------------------------------------------------+  |
|  +-----------------------------------------------------+  |
|  |  <plugin>     - System behaviors (physics, GUI)      |  |
|  +-----------------------------------------------------+  |
|                     </world>                                |
+-----------------------------------------------------------+
```

Let's build each section progressively, starting with a complete working example.

## A Complete Simple World

Here's a fully functional world file with all essential elements:

```xml
<?xml version="1.0" ?>
<sdf version="1.8">
    <world name="simple_demo">

        <!-- 1. Physics Engine Settings -->
        <physics name="1ms" type="ode">
            <max_step_size>0.001</max_step_size>
            <real_time_factor>1.0</real_time_factor>
            <gravity>0 0 -9.80665</gravity>
        </physics>

        <!-- 2. Scene (background, ambient light, shadows) -->
        <scene>
            <ambient>0.4 0.4 0.4 1</ambient>
            <background>0.7 0.7 0.7 1</background>
            <shadows>true</shadows>
        </scene>

        <!-- 3. Sun Light -->
        <light type="directional" name="sun">
            <cast_shadows>true</cast_shadows>
            <pose>0 0 10 0 0 0</pose>
            <diffuse>0.8 0.8 0.8 1</diffuse>
            <specular>0.2 0.2 0.2 1</specular>
            <direction>-0.5 0.1 -0.9</direction>
        </light>

        <!-- 4. Ground Plane -->
        <model name="ground_plane">
            <static>true</static>
            <link name="link">
                <collision name="collision">
                    <geometry>
                        <plane>
                            <normal>0 0 1</normal>
                            <size>100 100</size>
                        </plane>
                    </geometry>
                    <surface>
                        <friction>
                            <ode>
                                <mu>100</mu>
                                <mu2>50</mu2>
                            </ode>
                        </friction>
                    </surface>
                </collision>
                <visual name="visual">
                    <cast_shadows>false</cast_shadows>
                    <geometry>
                        <plane>
                            <normal>0 0 1</normal>
                            <size>100 100</size>
                        </plane>
                    </geometry>
                    <material>
                        <script>
                            <uri>file://media/materials/scripts/gazebo.material</uri>
                            <name>Gazebo/Grey</name>
                        </script>
                    </material>
                </visual>
            </link>
        </model>

        <!-- 5. Essential Plugins -->
        <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics">
        </plugin>
        <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands">
        </plugin>
        <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster">
        </plugin>

    </world>
</sdf>
```

Save this file as `simple_world.sdf` and launch it:

```bash
gz sim simple_world.sdf
```

**Output**: Gazebo opens showing a grey ground plane with shadows enabled and realistic lighting from the sun.

Now let's break down each section so you understand what's happening and can customize it.

## Physics Configuration

The physics section controls how the simulation engine calculates motion, collisions, and forces.

```xml
<physics name="1ms" type="ode">
    <max_step_size>0.001</max_step_size>
    <real_time_factor>1.0</real_time_factor>
    <gravity>0 0 -9.80665</gravity>
</physics>
```

**Parameters explained**:

| Parameter | Meaning | Typical Values |
|-----------|---------|----------------|
| `name` | Identifier for this physics config | "1ms", "default", "accurate" |
| `type` | Physics engine to use | `ode`, `bullet`, `simbody`, `dart` |
| `max_step_size` | Time between physics calculations (seconds) | 0.001 (accurate) to 0.01 (faster) |
| `real_time_factor` | Target ratio of sim time to real time | 1.0 = real-time, 2.0 = 2x speed |
| `gravity` | Gravitational acceleration (x, y, z) | "0 0 -9.8" = Earth gravity downward |

**Why this matters**: Smaller `max_step_size` values give more accurate physics but require more computation. For testing basic navigation, 0.01 is fine. For grasping delicate objects, use 0.001.

## Lighting Setup

Lighting determines how your world looks and affects camera-based sensors. The sun is your primary light source.

### Directional Light (Sun)

```xml
<light type="directional" name="sun">
    <cast_shadows>true</cast_shadows>
    <pose>0 0 10 0 0 0</pose>
    <diffuse>0.8 0.8 0.8 1</diffuse>
    <specular>0.2 0.2 0.2 1</specular>
    <direction>-0.5 0.1 -0.9</direction>
</light>
```

**Parameters**:

- `type="directional"`: Light rays are parallel (like the sun)
- `cast_shadows`: Enable/disable shadow rendering
- `pose`: Position (x, y, z, roll, pitch, yaw)
- `diffuse`: Main light color (red, green, blue, alpha), values 0-1
- `specular`: Reflective highlight color
- `direction`: Which way light points (for directional/spot lights)

**Light types**:

| Type | Use Case | Example |
|------|----------|---------|
| `directional` | Sun/outdoor lighting | Simulating daylight |
| `point` | Light bulbs, indoor lighting | Lamps, overhead lights |
| `spot` | Flashlights, focused beams | Robot headlights |

### Adding Indoor Lighting

For an indoor environment, add point lights:

```xml
<light type="point" name="ceiling_light">
    <pose>0 0 3 0 0 0</pose>
    <diffuse>1 1 0.9 1</diffuse>  <!-- Warm white -->
    <attenuation>
        <range>10</range>
        <constant>0.5</constant>
        <linear>0.1</linear>
        <quadratic>0.01</quadratic>
    </attenuation>
    <cast_shadows>false</cast_shadows>
</light>
```

## Including Models from Gazebo Fuel

Rather than building models from scratch, you can use the **Gazebo Fuel** model repository—a library of hundreds of pre-built robots, objects, and environments.

### Method 1: Direct URL Include

Include a model directly from Fuel using its URL:

```xml
<include>
    <name>table1</name>
    <pose>1 0 0 0 0 0</pose>
    <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Table</uri>
</include>
```

**What happens**: When you launch the world, Gazebo downloads the model automatically and places it at the specified position.

### Method 2: Local Model Include

Download the model once and reference it locally (faster world loading):

```xml
<include>
    <name>table1</name>
    <pose>1 0 0 0 0 0</pose>
    <uri>model://table</uri>
</include>
```

For local models, set the resource path:

```bash
export GZ_SIM_RESOURCE_PATH=/path/to/your/models
gz sim my_world.sdf
```

### Position Format

The `<pose>` tag uses 6 values: `x y z roll pitch yaw`

```
     Z (up)
      |
      |___ Y (forward)
     /
   X (right)
```

**Example poses**:

```xml
<pose>0 0 0 0 0 0</pose>     <!-- Origin, no rotation -->
<pose>1 2 0.5 0 0 1.57</pose>  <!-- X=1m, Y=2m, Z=0.5m, rotated 90 degrees around Z -->
<pose>0 0 1 0 0.785 0</pose>  <!-- Z=1m, tilted forward 45 degrees -->
```

## Building a Simple Scene

Let's create a simple indoor scene with a table, chair, and some objects:

```xml
<?xml version="1.0" ?>
<sdf version="1.8">
    <world name="simple_room">

        <!-- Physics and scene from earlier -->
        <physics name="1ms" type="ode">
            <max_step_size>0.001</max_step_size>
            <real_time_factor>1.0</real_time_factor>
        </physics>

        <scene>
            <ambient>0.4 0.4 0.4 1</ambient>
            <background>0.7 0.7 0.7 1</background>
            <shadows>true</shadows>
        </scene>

        <!-- Indoor lighting -->
        <light type="point" name="ceiling_light">
            <pose>0 0 2.5 0 0 0</pose>
            <diffuse>1 1 0.9 1</diffuse>
            <attenuation>
                <range>8</range>
                <constant>0.5</constant>
                <linear>0.2</linear>
            </attenuation>
        </light>

        <!-- Ground -->
        <model name="ground_plane">
            <static>true</static>
            <link name="link">
                <collision name="collision">
                    <geometry>
                        <plane><normal>0 0 1</normal><size>10 10</size></plane>
                    </geometry>
                </collision>
                <visual name="visual">
                    <cast_shadows>false</cast_shadows>
                    <geometry>
                        <plane><normal>0 0 1</normal><size>10 10</size></plane>
                    </geometry>
                    <material>
                        <script>
                            <uri>file://media/materials/scripts/gazebo.material</uri>
                            <name>Gazebo/Grey</name>
                        </script>
                    </material>
                </visual>
            </link>
        </model>

        <!-- Table -->
        <include>
            <name>dining_table</name>
            <pose>0 0 0 0 0 0</pose>
            <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Table</uri>
        </include>

        <!-- Chair -->
        <include>
            <name>chair1</name>
            <pose>0 -0.8 0 0 0 0</pose>
            <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Chair</uri>
        </include>

        <!-- Objects on table -->
        <include>
            <name>coke_can</name>
            <pose>0.2 0 0.75 0 0 0</pose>
            <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Coke</uri>
        </include>

        <!-- Essential plugins -->
        <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"></plugin>
        <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"></plugin>
        <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"></plugin>

    </world>
</sdf>
```

Save as `room.sdf` and launch:

```bash
gz sim room.sdf
```

**Output**: A simple room with a table, chair, and coke can lit by overhead lighting.

## Spawning Robots with ROS 2

Once your world is loaded, you'll want to add robots. ROS 2 provides the `spawn_entity.py` script to spawn robots into running Gazebo worlds.

### Basic Robot Spawning

```bash
# Spawn a robot from a URDF file
ros2 run gazebo_ros spawn_entity.py \
    -entity my_robot \
    -file /path/to/robot.urdf \
    -x 0 -y 0 -z 0.5
```

### Spawning from ROS 2 Package

For robots installed as ROS 2 packages:

```bash
# Spawn the TurtleBot3 robot (example)
ros2 run gazebo_ros spawn_entity.py \
    -entity turtlebot3 \
    -topic /robot_description \
    -x 1.0 -y 1.0 -z 0.0 \
    -Y 0.0
```

**Parameters**:

| Parameter | Meaning | Example |
|-----------|---------|--------|
| `-entity` | Unique name for spawned robot | `my_robot`, `robot1` |
| `-file` | Path to URDF/XACRO file | `/path/to/robot.urdf` |
| `-topic` | ROS 2 topic publishing robot description | `/robot_description` |
| `-x -y -z` | Position to spawn at | `-x 1 -y 2 -z 0.5` |
| `-Y` | Yaw rotation (radians) | `-Y 1.57` (90 degrees) |

### Launch File Integration

For convenience, create a ROS 2 launch file that starts Gazebo with your world AND spawns the robot:

```python
# launch_robot_in_world.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    # Path to your world file
    world_file = os.path.join(
        os.path.dirname(__file__),
        'worlds',
        'room.sdf'
    )

    return LaunchDescription([
        # Launch Gazebo with custom world
        ExecuteProcess(
            cmd=['gz', 'sim', world_file],
            output='screen'
        ),

        # Spawn robot
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'my_robot',
                      '-file', '/path/to/robot.urdf',
                      '-x', '1.0', '-y', '1.0', '-z', '0.5'],
            output='screen'
        ),
    ])
```

Launch your complete simulation:

```bash
ros2 launch my_package launch_robot_in_world.py
```

## Common World Patterns

### Empty World for Testing

```xml
<!-- Minimal world for algorithm testing -->
<world name="empty_test">
    <physics name="1ms" type="ode">
        <max_step_size>0.01</max_step_size>
    </physics>
    <scene>
        <ambient>1 1 1 1</ambient>
        <background>0 0 0 1</background>
    </scene>
    <light type="point" name="light">
        <pose>0 0 5 0 0 0</pose>
        <diffuse>1 1 1 1</diffuse>
    </light>
    <!-- Just ground plane, no obstacles -->
    <include>
        <uri>model://ground_plane</uri>
    </include>
</world>
```

### Maze Navigation World

```xml
<!-- Simple maze using wall models -->
<world name="maze">
    <!-- Physics, scene, light... -->

    <!-- Outer walls -->
    <include>
        <name>wall_north</name>
        <pose>0 5 0 0 0 0</pose>
        <uri>model://wall_block</uri>
    </include>
    <include>
        <name>wall_south</name>
        <pose>0 -5 0 0 0 0</pose>
        <uri>model://wall_block</uri>
    </include>
    <include>
        <name>wall_east</name>
        <pose>5 0 0 0 0 1.57</pose>
        <uri>model://wall_block</uri>
    </include>
    <include>
        <name>wall_west</name>
        <pose>-5 0 0 0 0 1.57</pose>
        <uri>model://wall_block</uri>
    </include>

    <!-- Internal walls forming maze -->
    <include>
        <name>wall1</name>
        <pose>2 2 0 0 0 1.57</pose>
        <uri>model://wall_block</uri>
    </include>
    <include>
        <name>wall2</name>
        <pose>-2 -2 0 0 0 0</pose>
        <uri>model://wall_block</uri>
    </include>
</world>
```

## Debugging World Files

When your world doesn't load correctly, check these common issues:

### Issue: Models Don't Appear

**Symptom**: Gazebo launches but no models visible

**Causes**:
1. URL is incorrect (check Fuel website)
2. Network is down (can't download models)
3. Model name conflict (all models need unique names)

**Fix**: Try downloading model locally first

### Issue: Models Fall Through Ground

**Symptom**: Objects sink into ground plane

**Cause**: Physics engine not loaded or collision disabled

**Fix**: Ensure physics plugin is included:
```xml
<plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"></plugin>
```

### Issue: World Loads Slowly

**Symptom**: Long wait time before Gazebo appears

**Causes**:
1. Too many high-polygon models
2. Small `max_step_size` (overly accurate physics)
3. Shadows enabled on complex scenes

**Fixes**:
```xml
<physics>
    <max_step_size>0.01</max_step_size>  <!-- Increase for faster loading -->
</physics>
<scene>
    <shadows>false</shadows>  <!-- Disable for faster rendering -->
</scene>
```

## Hardware and Performance Considerations

**Minimum specs for world building**:
- CPU: 4 cores
- RAM: 8 GB
- GPU: Integrated graphics

**Recommended specs**:
- CPU: 8+ cores
- RAM: 16 GB
- GPU: NVIDIA RTX with 4+ GB VRAM

**Cloud alternatives**:
- NVIDIA Omniverse Cloud: Run Gazebo worlds in browser
- AWS/Azure GPU instances: For heavy simulations

## Try With AI

### Exercise 1: Create a Custom Navigation Environment

```text
I'm learning to create Gazebo world files using SDF for robot navigation testing.

Help me design a world file for a warehouse delivery robot that needs to:
- Navigate through a space with shelves and obstacles
- Pick up objects from tables
- Navigate through doorways

For my world, please:
1. Create an SDF world file with:
   - A floor area of at least 10x10 meters
   - At least 4 obstacles (could be boxes, shelves, or tables)
   - Two doorways (open spaces between obstacles)
   - Indoor lighting suitable for camera-based navigation

2. Explain the pose values you chose for each object
3. Suggest modifications if I wanted to test:
   - A narrow corridor scenario
   - A crowded room with many obstacles
   - An outdoor navigation scenario
```

**What you're learning:** This exercise teaches you to translate real-world environments into SDF specifications. You'll practice spatial reasoning—converting "a room with shelves" into precise pose coordinates. Understanding this translation is crucial: your robot can only navigate what you accurately simulate. You'll also learn to modify worlds for different testing scenarios, a key skill for comprehensive robot testing.

### Exercise 2: Diagnose and Fix a Broken World File

```text
I have this Gazebo world file that isn't working properly. When I run it, Gazebo opens but the ground plane doesn't have physics enabled and models fall through.

Here's my world file:
[Paste your problematic world file or have AI create one with intentional bugs]

Help me by:
1. Identifying what's wrong with the file
2. Explaining WHY each issue causes the observed problem
3. Providing the corrected version
4. Listing the warning signs I should look for in future world files

After fixing it, teach me how to add a simple obstacle at position (2, 2, 0) with proper physics enabled.
```

**What you're learning:** Debugging SDF files teaches you to understand XML structure and Gazebo's requirements. Rather than just memorizing correct syntax, you'll learn the underlying principles—why plugins are required, what enables physics, how tags nest. This diagnostic skill is invaluable: you'll inevitably make mistakes when building complex worlds, and knowing how to fix them yourself saves countless hours.

### Exercise 3: World Optimization for Performance

```text
I've created a Gazebo world with many models, but it runs slowly on my computer. The simulation stutters and real-time factor drops below 0.5.

Help me optimize my world by:
1. Analyzing my current world file settings
2. Suggesting specific changes to improve performance:
   - Physics settings (max_step_size, real_time_factor)
   - Rendering options (shadows, ambient lighting)
   - Model complexity (can I simplify some models?)
3. Creating a version with "fast" settings and explaining the trade-offs

I need to understand: what performance am I giving up with each optimization? Will my robot's behavior change significantly, or will it be approximately the same?
```

**What you're learning:** Performance optimization is a critical skill for simulation. You'll learn the trade-offs between accuracy and speed—when high-fidelity physics matter (grasping objects) versus when simpler physics suffice (navigation). This understanding helps you choose appropriate settings for each testing phase: fast iteration during development, accurate simulation for final validation. You'll also learn to diagnose performance bottlenecks, a skill applicable to all computational work.
