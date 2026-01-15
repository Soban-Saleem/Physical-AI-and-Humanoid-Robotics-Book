---
sidebar_position: 1
title: "Introduction to NVIDIA Isaac Sim"
description: "Learn NVIDIA Isaac Sim, the physics simulation platform for robotics built on NVIDIA Omniverse. Covers installation, UI basics, physics simulation, and GPU-accelerated robot control."
keywords: ["Isaac Sim", "NVIDIA Omniverse", "Robot Simulation", "GPU Acceleration", "Physics Engine"]
chapter: 4
lesson: 1
duration_minutes: 90

requirements:
  hardware: "NVIDIA RTX 4080 (16GB VRAM) minimum; RTX 4090/5080 recommended"
  software: "Ubuntu 22.04 LTS or Windows 11, Python 3.10, NVIDIA Driver 535+"

skills:
  - name: "Isaac Sim Navigation"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Remember"
    measurable_at_this_level: "Student can identify Isaac Sim UI components and navigate the interface"

  - name: "Physics Simulation Control"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can explain how physics simulation works in Isaac Sim and the role of GPU acceleration"

  - name: "Python API for Robot Control"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can write Python scripts to spawn and control robots in simulation"

learning_objectives:
  - objective: "Explain what Isaac Sim is, its relationship to NVIDIA Omniverse, and why GPU acceleration matters for robotics simulation"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Short answer describing Isaac Sim architecture and GPU benefits"

  - objective: "Navigate the Isaac Sim interface and identify key components (Viewport, Stage, Property Panel, Timeline)"
    proficiency_level: "A2"
    bloom_level: "Remember"
    assessment_method: "UI component identification exercise"

  - objective: "Write Python scripts using the Isaac Sim Core API to spawn a robot and control its joints"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Coding exercise: Create a script that moves a robot arm"

cognitive_load:
  new_concepts: 7
  assessment: "Students will complete a coding exercise to control a robot arm using the Isaac Sim Python API"

differentiation:
  extension_for_advanced: "Explore the Articulation API to implement inverse kinematics for a robot arm to reach target positions"
  remedial_for_struggling: "Focus on UI navigation first—complete the guided tour of Isaac Sim interface before attempting Python scripting"
  hardware_alternatives: "Use NVIDIA Omniverse Cloud (free tier available) or Google Colab with Isaac Lab for cloud-based simulation without local GPU"

safety_notes: null

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Introduction to NVIDIA Isaac Sim

Imagine testing a humanoid robot's balance system by pushing it thousands of times in different ways, measuring how it recovers each time. Doing this with a physical robot would take months, cost thousands in repairs, and risk damaging the hardware. Now imagine running those same thousands of tests in a few hours with zero risk to any physical device. This is the power of **Isaac Sim**—NVIDIA's physics simulation platform built specifically for robotics.

Isaac Sim allows you to create "digital twins" of robots and environments, test algorithms virtually, and deploy to real hardware with confidence. It's built on **NVIDIA Omniverse**, a platform for 3D simulation and collaboration, and leverages NVIDIA GPUs for physics calculations that would be impossibly slow on traditional CPUs. This lesson introduces you to Isaac Sim's architecture, interface, and Python API—setting the foundation for simulation-based robotics development.

## What is Isaac Sim?

**Isaac Sim** is a robotics simulator built on NVIDIA Omniverse that combines realistic physics, accurate sensor simulation, and GPU-accelerated rendering. It's designed specifically for developing and testing robot software before deploying to physical hardware.

### Isaac Sim vs. Other Simulators

| Feature | Gazebo | Isaac Sim | Key Difference |
|---------|--------|-----------|----------------|
| **Physics Engine** | ODE/Bullet | PhysX (GPU-accelerated) | Isaac Sim uses GPU for faster physics |
| **Rendering** | Basic Ogre | RTX-powered path tracing | Photorealistic visuals for camera simulation |
| **Sensor Simulation** | Basic models | Ray-traced LiDAR, camera depth | More accurate sensor data |
| **Scalability** | Single robot | 1000+ robots simultaneously | Fleet-scale simulation |
| **ROS Integration** | Native | Isaac ROS bridge | GPU-accelerated ROS 2 packages |

**Why this matters**: Traditional simulators like Gazebo run physics on CPUs, limiting simulation speed and complexity. Isaac Sim offloads physics calculations to NVIDIA GPUs, enabling faster-than-real-time simulation and complex multi-robot scenarios.

### The Omniverse Foundation

Isaac Sim is built on **NVIDIA Omniverse**, a computing platform for 3D simulation and collaboration. Omniverse provides:

- **Universal Scene Description (USD)**: A format for describing 3D scenes that can be shared across applications
- **PhysX 5**: NVIDIA's physics engine with GPU acceleration
- **RTX Renderer**: Path-traced rendering for photorealistic visuals
- **MDL Material Definition Language**: Physically accurate material properties

This foundation means Isaac Sim inherits professional-grade simulation capabilities while adding robotics-specific features like articulation systems, sensor simulation, and ROS integration.

## System Requirements and Installation

Isaac Sim has demanding hardware requirements due to its GPU-accelerated physics and rendering.

### Hardware Requirements (Isaac Sim 5.1+)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU** | GeForce RTX 4080 | GeForce RTX 4090 / RTX 5080 |
| **VRAM** | 16 GB | 24 GB |
| **RAM** | 32 GB | 64 GB |
| **Storage** | 50 GB SSD | 500 GB NVMe SSD |
| **CPU** | 8 cores | 16+ cores |

**Important**: 8GB VRAM is insufficient for complex scenes. Rendering more than 16 megapixels per frame requires additional VRAM beyond 16GB.

### Installation Options

**Option 1: Local Installation**

Download Isaac Sim from NVIDIA and install on your local machine:

```bash
# Download Isaac Sim (requires NVIDIA account)
# https://developer.nvidia.com/isaac-sim

# Extract and run installer
./Isaac-Sim_5.1.0.run

# Or use Python package
pip install isaac-sim
```

**Option 2: Cloud Simulation**

If you don't have a powerful GPU, use cloud-based options:

- **NVIDIA Omniverse Cloud**: Run Isaac Sim in the browser with cloud GPUs
- **Google Colab**: Use Isaac Lab notebooks with free GPU access
- **AWS/Google Cloud**: Rent GPU instances on-demand

**What you gain with cloud**: No local hardware requirements, pay only for what you use, access to powerful GPUs without upfront cost.

**What you lose**: Latency in interaction, data transfer costs, requires internet connection.

## Isaac Sim Interface Tour

When you first launch Isaac Sim, you'll see a comprehensive interface designed for 3D content creation and robotics simulation.

### Main Interface Components

```
+---------------------------------------------------------------+
|  Menu Bar: File, Edit, Window, Physics, Robotics              |
+---------------------------------------------------------------+
|  Toolbar: Save, Play, Stop, Step, Select, Translate, Rotate   |
+---------------------------------------------------------------+
|  |                    |                        |             |
|  |   Viewport         |    Property Panel      |   Content   |
|  |   (3D Scene)       |    (Object properties)  |   Browser   |
|  |                    |                        |             |
|  |                    |                        |             |
+---------------------------------------------------------------+
|  Timeline: |====|====|====| 0:00:00 / 0:10:00                |
+---------------------------------------------------------------+
|  Console: Output and error messages                           |
+---------------------------------------------------------------+
```

**Key Components**:

1. **Viewport**: Main 3D view of your simulation scene
   - Left-click + drag: Rotate camera
   - Right-click + drag: Pan camera
   - Scroll: Zoom in/out

2. **Stage Panel** (left): Hierarchical view of all objects in the scene
   - Shows robots, sensors, lights, and environment objects
   - Drag to reorder parent-child relationships

3. **Property Panel** (right): Edit properties of selected objects
   - Transform (position, rotation, scale)
   - Physics properties (mass, friction)
   - Material properties

4. **Content Browser**: Library of pre-built assets
   - Robots: Franka, UR5, Quadrotors, Humanoids
   - Environments: Warehouses, offices, outdoor scenes
   - Objects: Tables, boxes, tools

5. **Timeline**: Control simulation playback
   - Play/Pause/Stop buttons
   - Time display and simulation speed control

6. **Console**: Python output and error messages

### First Steps: Loading a Scene

Let's load a pre-built scene with a robot:

1. Open Isaac Sim
2. Go to **Content Browser** → **Isaac** → **Environments** → **Simple Room**
3. Drag the room into the Viewport
4. Go to **Content Browser** → **Isaac** → **Robots** → **FRANCA** (cobot arm)
5. Drag the robot into the scene

You should now see a robotic arm in a simple room environment. Press the **Play** button in the toolbar to start physics simulation. The robot should respond to gravity and settle into a stable position.

## Physics Simulation in Isaac Sim

Isaac Sim uses **PhysX 5**, NVIDIA's physics engine, to simulate realistic physical interactions. Unlike traditional physics engines that run on CPUs, PhysX in Isaac Sim leverages GPU acceleration for massive parallelism.

### Physics Settings

To access physics settings, go to **Window** → **Physics** → **Settings**:

```python
# Key physics parameters (configurable via UI or Python)
physics_settings = {
    "gravity": [-0.0, -0.0, -9.81],      # m/s^2 (z-axis down)
    "dt": 1.0 / 60.0,                     # Time step (60 Hz)
    "num_threads": 4,                      # CPU threads for fallback
    "use_gpu": True,                       # Enable GPU acceleration
    "solver_type": "TGS",                  # Temporal Gauss-Seidel solver
    "num_position_iterations": 8,          # Solver accuracy
    "num_velocity_iterations": 8           # Velocity accuracy
}
```

**Why GPU matters**: Physics simulation requires calculating forces, collisions, and constraints for every object in the scene. GPUs excel at parallel computation, enabling Isaac Sim to simulate complex scenes (1000+ robots) that would overwhelm CPU-based simulators.

### Physics Types

Isaac Sim supports different physics types for different use cases:

| Physics Type | Use Case | Examples |
|--------------|----------|----------|
| **Rigid Body** | Solid objects that don't deform | Robots, boxes, tables |
| **Deformable** | Soft objects that change shape | Cloth, rubber, soft materials |
| **Particle System** | Fluids and granular materials | Water, sand, powder |
| **Cloth** | Fabric simulation | Clothing, curtains |
| **Hair** | Hair and fur simulation | Character hair |

For most robotics applications, you'll work with **rigid body physics**—robots, objects, and environmental elements that maintain their shape.

## Python API for Robot Control

Isaac Sim provides a comprehensive Python API for creating and controlling simulations programmatically. This is how you'll build automated tests, train reinforcement learning models, and develop robot control algorithms.

### Core API Concepts

The Isaac Sim Python API is organized around key objects:

```python
# Core Isaac Sim API structure
from omni.isaac.kit import SimulationApp

# Initialize simulation (required first step)
simulation_app = SimulationApp({"headless": False})  # Set True for cloud

# Key API modules
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.rotations import euler_angles_to_quat
from omni.isaac.nucleus import get_assets_root_path
```

### Example 1: Spawning and Controlling a Robot Arm

Let's create a complete Python script that spawns a Franka robot arm and controls its joints:

```python
#!/usr/bin/env python
"""
Isaac Sim Python API Example: Spawn and Control Robot Arm
This script demonstrates basic robot control using the Articulation API
"""

from omni.isaac.kit import SimulationApp

# Initialize simulation (must be first line)
simulation_app = SimulationApp({"headless": False})

import omni.isaac.core.utils.prims as prim_utils
from omni.isaac.core.articulations import Articulation
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.rotations import euler_angles_to_quat
from omni.isaac.core.objects import DynamicCuboid
import numpy as np

# Get Isaac Sim assets path
from omni.isaac.nucleus import get_assets_root_path
assets_root_path = get_assets_root_path()

class RobotController:
    """Simple controller for a robot arm"""

    def __init__(self):
        # Get the current world
        from omni.isaac.core import World
        self.world = World(stage_units_in_meters=1.0)
        self.world.scene.add_default_ground_plane()

        # Spawn Franka robot
        robot_usd_path = assets_root_path + "/Isaac/Robots/Franka/franka.usd"
        add_reference_to_stage(usd_path=robot_usd_path, prim_path="/World/Franka")

        # Create Articulation object for control
        self.franka = Articulation(
            prim_path="/World/Franka",
            name="franka_robot"
        )
        self.world.scene.add(self.franka)

        # Reset the simulation
        self.world.reset()

        print("Robot initialized successfully")
        print(f"Number of joints: {self.franka.num_joints}")
        print(f"Joint names: {self.franka.dof_names}")

    def move_to_position(self, joint_positions):
        """Move robot to specified joint positions"""
        # Set joint positions (target)
        self.franka.set_joint_positions(joint_positions)
        # Apply actions
        self.world.step(render=True)

    def get_joint_states(self):
        """Get current joint positions and velocities"""
        positions = self.franka.get_joint_positions()
        velocities = self.franka.get_joint_velocities()
        return positions, velocities

    def run_demo(self):
        """Run a simple demonstration"""
        print("\n=== Starting Robot Demo ===\n")

        # Get initial joint positions (home position)
        home_positions = self.franka.get_joint_positions()
        print(f"Home position: {np.round(home_positions, 3)}")

        # Move to a different position
        print("\nMoving to position 1...")
        target_1 = np.array([0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.0])

        for i in range(100):  # Smooth motion over 100 steps
            # Interpolate from current to target
            current = self.franka.get_joint_positions()
            interpolated = current + (target_1 - current) * 0.05
            self.franka.set_joint_positions(interpolated)
            self.world.step(render=True)

        print(f"Position 1 reached: {np.round(self.franka.get_joint_positions(), 3)}")

        # Pause for observation
        for _ in range(50):
            self.world.step(render=True)

        # Move to second position
        print("\nMoving to position 2...")
        target_2 = np.array([0.0, -0.2, 0.0, -1.5, 0.0, 1.0, 0.0])

        for i in range(100):
            current = self.franka.get_joint_positions()
            interpolated = current + (target_2 - current) * 0.05
            self.franka.set_joint_positions(interpolated)
            self.world.step(render=True)

        print(f"Position 2 reached: {np.round(self.franka.get_joint_positions(), 3)}")

        # Return to home
        print("\nReturning to home position...")
        for i in range(100):
            current = self.franka.get_joint_positions()
            interpolated = current + (home_positions - current) * 0.05
            self.franka.set_joint_positions(interpolated)
            self.world.step(render=True)

        print(f"Home position reached: {np.round(self.franka.get_joint_positions(), 3)}")
        print("\n=== Demo Complete ===")

# Run the demo
if __name__ == "__main__":
    controller = RobotController()
    controller.run_demo()

    # Keep simulation running for observation
    while simulation_app.is_running():
        controller.world.step(render=True)

    simulation_app.close()
```

**Output:**
```
Robot initialized successfully
Number of joints: 7
Joint names: ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']
Home position: [0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]

=== Starting Robot Demo ===

Moving to position 1...
Position 1 reached: [0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.0]

Moving to position 2...
Position 2 reached: [0.0, -0.2, 0.0, -1.5, 0.0, 1.0, 0.0]

Returning to home position...
Home position reached: [0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]

=== Demo Complete ===
```

### Example 2: Adding and Interacting with Objects

Robots exist to manipulate objects. Here's how to add objects to the scene and interact with them:

```python
from omni.isaac.core.objects import DynamicCuboid
from omni.isaac.core.utils.prims import define_prim
import numpy as np

def add_pickable_objects(world):
    """Add objects that the robot can manipulate"""

    # Create a red cube on the table
    red_cube = DynamicCuboid(
        prim_path="/World/RedCube",
        name="red_cube",
        position=np.array([0.5, 0.0, 0.5]),  # x, y, z in meters
        size=np.array([0.05, 0.05, 0.05]),   # 5cm cube
        color=np.array([1.0, 0.0, 0.0]),      # RGB color
        mass=0.1  # 100 grams
    )
    world.scene.add(red_cube)

    # Create a blue sphere
    from omni.isaac.core.objects import DynamicSphere
    blue_sphere = DynamicSphere(
        prim_path="/World/BlueSphere",
        name="blue_sphere",
        position=np.array([0.6, 0.1, 0.5]),
        radius=0.03,
        color=np.array([0.0, 0.0, 1.0]),
        mass=0.05
    )
    world.scene.add(blue_sphere)

    print("Objects added to scene")

    return red_cube, blue_sphere
```

### Running Scripts in Isaac Sim

There are three ways to run Python scripts in Isaac Sim:

**Method 1: Script Editor (Built-in)**
1. Open Isaac Sim
2. Go to **Window** → **Script Editor**
3. Paste your code and click **Run**

**Method 2: Command Line**
```bash
# Run script with Isaac Sim
./python.sh path/to/your_script.py

# On Windows
python.bat path/to/your_script.py
```

**Method 3: Jupyter Notebook**
```bash
# Launch Isaac Sim with Jupyter
./isaac_python.sh -m jupyter notebook

# Access at http://localhost:8888
```

## GPU Acceleration: Why It Matters

The key advantage of Isaac Sim over traditional simulators is GPU acceleration. Let's understand what this means practically.

### CPU vs GPU Physics Simulation

```python
# Traditional CPU-based simulation (e.g., Gazebo)
# Each physics step processes objects sequentially
for object in scene.objects:
    calculate_forces(object)
    check_collisions(object)
    update_position(object)
# Total time: O(n) where n = number of objects

# GPU-based simulation (Isaac Sim with PhysX)
# All objects processed in parallel on GPU
calculate_forces_batch(scene.objects)  # Parallel on GPU
check_collisions_batch(scene.objects)  # Parallel on GPU
update_positions_batch(scene.objects)  # Parallel on GPU
# Total time: O(1) for fixed batch size
```

**Real-world impact**: Simulating 100 robots with CPU-based physics might run at 5% real-time (20 seconds of simulation time takes 400 seconds). With GPU acceleration, the same scene might run at 200% real-time (20 seconds of simulation takes 10 seconds).

### When GPU Matters Most

GPU acceleration provides the biggest benefits for:

1. **Multi-robot scenarios**: Warehouse with 100+ robots
2. **Complex environments**: Thousands of objects, detailed geometry
3. **Sensor simulation**: Ray-traced camera and LiDAR
4. **Reinforcement learning**: Training requires millions of simulation steps
5. **Photorealistic rendering**: Training vision models

If you're simulating a single robot in a simple environment, GPU acceleration won't show dramatic benefits. But as your simulations grow in complexity, GPU becomes essential.

## Common Challenges and Solutions

### Challenge 1: Simulation Runs Slowly

**Symptoms**: Simulation framerate drops below 30 FPS, robot movement is choppy

**Solutions**:
- Reduce physics complexity: Decrease `num_position_iterations` and `num_velocity_iterations`
- Simplify geometry: Use lower-polygon meshes
- Reduce rendering quality: Disable ray tracing, lower resolution
- Fewer objects: Remove unnecessary items from scene

```python
# Optimize physics settings
from omni.isaac.core.utils.stage import set_simulation_rate
set_simulation_rate(60)  # Lower from 240 to 60 Hz
```

### Challenge 2: Robot Falls Over Immediately

**Symptoms**: Robot collapses when simulation starts

**Solutions**:
- Check robot is positioned above ground: `position=[0, 0, 0.1]` (not 0,0,0)
- Verify ground plane exists: Add default ground plane
- Check robot mass properties: Unrealistic mass can cause instability
- Enable fixed base for stationary robots

```python
# Fix robot falling issues
articulation.set_fixed_base(True)  # For base that shouldn't move
```

### Challenge 3: Joints Don't Move

**Symptoms**: Setting joint positions has no effect

**Solutions**:
- Check joint limits: Target position within valid range
- Verify articulation is awake: Call `wake_up()` if sleeping
- Check control mode: May need to switch to position control

```python
# Troubleshooting joint control
print(f"Joint limits: {robot.joint_limits}")
robot.wake_up()  # Wake if sleeping
robot.set_joint_positions(target, drive_type="position")  # Explicit position control
```

## Hardware Alternatives and Cloud Options

Not everyone has an RTX 4080 or better. Here are alternatives for running Isaac Sim without powerful local hardware.

### Option 1: NVIDIA Omniverse Cloud

NVIDIA offers cloud-based access to Isaac Sim through Omniverse Cloud:

- **Free tier**: Limited hours per month for learning
- **Paid tiers**: On-demand GPU access
- **Advantage**: No local hardware requirements
- **Disadvantage**: Requires internet, data transfer costs

Access at: [https://omniverse.nvidia.com/](https://omniverse.nvidia.com/)

### Option 2: Isaac Lab (Lighter Alternative)

Isaac Lab is a lightweight framework built on Isaac Sim, designed for robotics research:

```bash
# Install Isaac Lab (lighter than full Isaac Sim)
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab
./isaaclab.sh --install

# Run Isaac Lab examples
./isaaclab.sh --prebuilt --task Isaac-Lift-Cube-Franka-IK-AB
```

Isaac Lab can run with less powerful GPUs (8GB VRAM minimum) and provides pre-built examples for common robotics tasks.

### Option 3: Google Colab with Isaac

For learning and experimentation, Google Colab offers free GPU access:

```python
# Install Isaac Sim in Colab
!pip install isaac-sim

# Run Isaac Sim headless (no display)
from omni.isaac.kit import SimulationApp
simulation_app = SimulationApp({"headless": True})
```

**Limitations**: Headless mode only (no visualization), time limits per session, not suitable for complex scenes.

## Key Takeaways

Isaac Sim is NVIDIA's physics simulation platform for robotics, built on Omniverse and powered by GPU acceleration. It provides:

- **Realistic physics**: PhysX 5 engine with GPU acceleration
- **Accurate sensors**: Ray-traced cameras, LiDAR, depth sensors
- **Python API**: Programmatic control for automation and learning
- **ROS integration**: Isaac ROS bridge for GPU-accelerated ROS 2 packages
- **Scalability**: Simulate 1000+ robots simultaneously

In this lesson, you learned the Isaac Sim interface, physics simulation basics, and Python API for robot control. In the next lessons, we'll dive deeper into Isaac ROS, reinforcement learning, and advanced robot control.

## Try With AI

### Exercise 1: Isaac Sim Architecture Exploration

```text
I'm learning about NVIDIA Isaac Sim, a robotics simulator built on Omniverse. Help me understand:

1. How Isaac Sim relates to NVIDIA Omniverse—what does Omniverse provide that Isaac Sim builds upon?

2. Why GPU acceleration matters specifically for robotics simulation (not just rendering). What physics calculations benefit from parallel processing?

3. The difference between Isaac Sim and traditional simulators like Gazebo—specifically for multi-robot scenarios and reinforcement learning.

Provide concrete examples where GPU acceleration would enable simulation scenarios that aren't practical with CPU-only simulation.
```

**What you're learning:** This exercise builds your understanding of Isaac Sim's architecture and advantages. By exploring the relationship between Omniverse and Isaac Sim, you'll understand how professional-grade 3D simulation tools combine with robotics-specific features. Understanding GPU benefits will help you choose the right simulation approach for different robotics problems.

### Exercise 2: Robot Control Debugging

```text
I have this Isaac Sim Python script that should make a Franka robot arm move, but the robot isn't responding when I run it. Here's my code:

```python
from omni.isaac.kit import SimulationApp
simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.core.articulations import Articulation
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.nucleus import get_assets_root_path
import numpy as np

world = World()
world.scene.add_default_ground_plane()

assets_root = get_assets_root_path()
robot_path = assets_root + "/Isaac/Robots/Franka/franka.usd"
add_reference_to_stage(usd_path=robot_path, prim_path="/World/Franka")

franka = Articulation(prim_path="/World/Franka", name="franka")
world.scene.add(franka)

# Try to move the robot
franka.set_joint_positions(np.array([0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.0]))

while simulation_app.is_running():
    world.step(render=True)
```

Help me debug: What's missing or incorrect? Explain the issues and show the corrected code.
```

**What you're learning:** This exercise teaches you to debug Isaac Sim Python code by identifying common mistakes like missing initialization, incorrect articulation setup, or simulation loop issues. Understanding these debugging patterns will help you develop your own robot control scripts more effectively.

### Exercise 3: Scenario Design Challenge

```text
I want to design an Isaac Sim simulation for training a warehouse robot to navigate through cluttered aisles and pick up packages. The robot needs to:

1. Navigate using a simulated LiDAR sensor
2. Detect packages (boxes of different sizes)
3. Plan paths around obstacles
4. Pick up packages with a gripper

Help me design this simulation by:

1. Listing the Isaac Sim components I need (robot type, sensors, environment setup)
2. Suggesting which assets from the Isaac Sim library I should use
3. Explaining how to set up the Python script structure for training
4. Identifying what I should simulate in Isaac Sim vs. what needs physical hardware testing

Be specific about Isaac Sim features and APIs to use.
```

**What you're learning:** This exercise develops your ability to design complete simulation scenarios for robotics applications. By planning the architecture, components, and training pipeline, you'll practice the same system design thinking used in real robotics development. You'll also learn to distinguish between what can/should be simulated versus what requires physical testing—a critical skill for efficient robotics development.
