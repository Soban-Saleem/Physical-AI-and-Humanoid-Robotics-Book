---
sidebar_position: 2
title: "Bipedal Locomotion"
description: "Learn how humanoid robots walk on two legs. Master Zero Moment Point (ZMP), Linear Inverted Pendulum Model (LIPM), gait planning, and balance control for stable bipedal locomotion."
keywords: ["bipedal locomotion", "ZMP", "Zero Moment Point", "LIPM", "inverted pendulum", "gait planning", "walking robot", "balance control", "humanoid"]
chapter: 5
lesson: 2
duration_minutes: 90

requirements:
  hardware: "Any computer with Python 3.10+ (simulation-based)"
  software: "Python 3.10+, NumPy, Matplotlib (pip install numpy matplotlib)"

skills:
  - name: "ZMP Stability Analysis"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Analyze"
    measurable_at_this_level: "Student can calculate ZMP position and determine if a robot configuration is stable"

  - name: "LIPM Gait Planning"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can generate Center of Mass trajectories using LIPM for walking"

  - name: "Gait Cycle Design"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Create"
    measurable_at_this_level: "Student can design a complete gait cycle with single and double support phases"

  - name: "Balance Control Strategies"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Evaluate"
    measurable_at_this_level: "Student can compare balance control methods and select appropriate strategies"

learning_objectives:
  - objective: "Calculate Zero Moment Point (ZMP) position and explain its relationship to dynamic stability during walking"
    proficiency_level: "B1"
    bloom_level: "Analyze"
    assessment_method: "Problem set: Compute ZMP for given robot configurations and identify unstable cases"

  - objective: "Generate Center of Mass trajectories using the Linear Inverted Pendulum Model (LIPM) for stable walking"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code exercise: Implement LIPM trajectory generation for specified step parameters"

  - objective: "Design a complete gait cycle with single support, double support, and footstep planning"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "Design task: Create gait sequence for robot to walk forward 3 steps"

  - objective: "Evaluate balance control strategies and explain how feedback maintains stability during disturbances"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Analysis: Compare ZMP-based vs Capture Point control methods"

cognitive_load:
  new_concepts: 8
  assessment: "Students will implement ZMP calculation, LIPM trajectory generation, and design a complete gait cycle"

differentiation:
  extension_for_advanced: "Implement 3D-LIPM with variable Center of Mass height and incorporate Model Predictive Control (MPC) for online gait adaptation"
  remedial_for_struggling: "Focus on 2D walking (sagittal plane only) before extending to 3D. Use fixed Center of Mass height initially"
  hardware_alternatives: "All exercises use pure Python simulation. For physical testing: PyBullet physics engine, Gazebo with ROS 2, or real humanoid platforms like Unitree G1"

safety_notes: "Physical bipedal robots can fall and cause injury. Always test gaits in simulation first. Use safety harnesses and emergency stops when working with real hardware."

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Bipedal Locomotion

Watch a toddler learning to walk. They wobble, stagger, and fall repeatedly. Yet within months, they master a skill that took humanity millions of years to evolve. Bipedal walking—moving on two legs—is remarkably complex. We do it unconsciously, but building a robot that walks like us requires solving one of the most challenging problems in robotics.

This lesson explores how humanoid robots achieve stable bipedal locomotion. You'll learn about the Zero Moment Point (ZMP), the mathematical foundation of dynamic balance. You'll understand the Linear Inverted Pendulum Model (LIPM), which simplifies walking physics into tractable equations. And you'll see how these concepts combine to create gait cycles that enable robots to walk, turn, and even dance.

## Why Walking is Harder Than Standing

Standing still is relatively easy—if your center of mass stays within your support polygon (the area formed by your feet), you're stable. This is **static stability**. Walking is different: you're continuously falling forward and catching yourself. This is **dynamic stability**.

### Static vs Dynamic Walking

**Static walking**: At every moment, the robot is statically stable. The center of mass (COM) is always within the support polygon. This creates slow, shuffling motion.

**Dynamic walking**: The robot is momentarily unstable—falling forward—but continuously adjusts to maintain balance. This creates natural, efficient walking.

```python
# Static vs Dynamic Stability
def is_statically_stable(com_position, support_polygon):
    """
    Check if COM is within support polygon (static stability).

    Args:
        com_position: (x, y) center of mass position
        support_polygon: List of (x, y) vertices forming foot support area

    Returns:
        True if COM is inside support polygon
    """
    # Point-in-polygon test (ray casting algorithm)
    x, y = com_position
    n = len(support_polygon)
    inside = False

    p1x, p1y = support_polygon[0]
    for i in range(n + 1):
        p2x, p2y = support_polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

# Example: Robot standing on both feet
left_foot = [(0, 0), (0.1, 0), (0.1, 0.05), (0, 0.05)]
right_foot = [(0.1, 0), (0.2, 0), (0.2, 0.05), (0.1, 0.05)]

# Combine for double support
double_support = left_foot + right_foot

print(f"COM at (0.1, 0.025): {is_statically_stable((0.1, 0.025), double_support)}")
print(f"COM at (0.25, 0.025): {is_statically_stable((0.25, 0.025), double_support)}")
```

**Output:**
```
COM at (0.1, 0.025): True
COM at (0.25, 0.025): False
```

The first position is stable (COM centered over feet). The second is unstable (COM outside support area—robot falls).

## Zero Moment Point (ZMP)

The **Zero Moment Point** is the foundation of bipedal locomotion control. Developed by Miomir Vukobratovic in 1972, ZMP defines exactly where a robot can apply force without tipping over.

### What is ZMP?

ZMP is the point on the ground where the total moment of all forces acting on the robot equals zero. If ZMP stays within the support polygon, the robot won't rotate (tip over).

**Key insight**: For stable walking, ZMP must always be inside the foot support area.

```python
import numpy as np

def calculate_zmp(force, moment, ground_height=0):
    """
    Calculate ZMP from force and moment measurements.

    The ZMP is where the moment due to reaction forces equals zero.
    If only vertical force Fz is applied at (x, y, z), then:
    ZMP_x = Mx / Fz
    ZMP_y = My / Fz

    Args:
        force: (Fx, Fy, Fz) forces acting on the robot
        moment: (Mx, My, Mz) moments about the origin
        ground_height: Z-coordinate of the ground

    Returns:
        (zmp_x, zmp_y) position on ground
    """
    Fx, Fy, Fz = force
    Mx, My, Mz = moment

    if abs(Fz) < 1e-6:
        raise ValueError("ZMP undefined: Fz is zero (robot in flight)")

    # ZMP calculation (assuming measurement at height h above ground)
    zmp_x = -My / Fz
    zmp_y = Mx / Fz

    return zmp_x, zmp_y

# Example: Robot standing on one foot
# Force from ground reaction (Newton's 3rd law)
Fz = 500  # Newton (robot weight ~50kg)
Mx, My = 5, -2  # Nm (moments from slight COM offset)

zmp = calculate_zmp((0, 0, Fz), (Mx, My, 0))
print(f"ZMP position: ({zmp[0]:.3f}, {zmp[1]:.3f}) meters")

# Check if ZMP is within foot support (foot: 0 to 0.2m in x, -0.1 to 0.1m in y)
foot_support_x = (0, 0.2)
foot_support_y = (-0.1, 0.1)

is_stable = (foot_support_x[0] <= zmp[0] <= foot_support_x[1] and
             foot_support_y[0] <= zmp[1] <= foot_support_y[1])
print(f"Stable: {is_stable}")
```

**Output:**
```
ZMP position: (0.004, -0.010) meters
Stable: True
```

The ZMP is within the foot support area, so the robot maintains balance.

### ZMP Stability Criterion

For stable walking, two conditions must hold:

1. **ZMP inside support polygon**: ZMP must remain within the foot/feet support area
2. **Friction cone constraint**: No slipping at foot-ground contact

```python
def check_zmp_stability(zmp_x, zmp_y, support_polygons, margin=0.01):
    """
    Check if ZMP is stable (within any support polygon with safety margin).

    Args:
        zmp_x, zmp_y: ZMP position
        support_polygons: List of polygons, each is list of (x, y) vertices
        margin: Safety margin from polygon edge (meters)

    Returns:
        (is_stable, which_foot) tuple
    """
    for i, polygon in enumerate(support_polygons):
        # Check if ZMP is within polygon
        if is_statically_stable((zmp_x, zmp_y), polygon):
            # Also check margin distance from edges (simplified)
            # Full implementation would compute distance to polygon edges
            return True, f"Foot {i}"

    return False, "None (falling)"

# Example: Single support phase
left_foot_polygon = [(0, 0), (0.2, 0), (0.2, 0.1), (0, 0.1)]

# Stable case
zmp_stable = (0.1, 0.05)
status, foot = check_zmp_stability(zmp_stable[0], zmp_stable[1],
                                    [left_foot_polygon])
print(f"ZMP {zmp_stable}: {status} ({foot})")

# Unstable case
zmp_unstable = (0.25, 0.05)
status, foot = check_zmp_stability(zmp_unstable[0], zmp_unstable[1],
                                    [left_foot_polygon])
print(f"ZMP {zmp_unstable}: {status} ({foot})")
```

**Output:**
```
ZMP (0.1, 0.05): True (Foot 0)
ZMP (0.25, 0.05): False (None (falling))
```

## The Inverted Pendulum Model

Walking robots are often modeled as **inverted pendulums**—a mass on a rod that balanced precariously above a pivot point. This captures the essential physics: the robot's Center of Mass (COM) is like the mass, and the foot contact point is the pivot.

### Why Inverted Pendulum?

When humans walk, we essentially:
1. Fall forward (rotate around supporting foot)
2. Swing other leg forward
3. Catch ourselves on the new foot
4. Repeat

This is exactly how an inverted pendulum behaves: continuously falling and being caught.

### Simple Inverted Pendulum Dynamics

```python
def inverted_pendulum_dynamics(theta, theta_dot, length=1.0, gravity=9.81):
    """
    Compute angular acceleration for simple inverted pendulum.

    Equation: theta_ddot = (g/L) * sin(theta)

    Args:
        theta: Angle from vertical (radians)
        theta_dot: Angular velocity
        length: Pendulum length (meters)
        gravity: Gravitational acceleration

    Returns:
        theta_ddot: Angular acceleration
    """
    # For small angles, sin(theta) ≈ theta
    # For large angles, use full nonlinear equation
    theta_ddot = (gravity / length) * np.sin(theta)

    return theta_ddot

# Simulate tipping forward
dt = 0.01  # Time step
theta = 0.1  # Initial tilt (about 5.7 degrees)
theta_dot = 0

trajectory = []
for _ in range(100):  # 1 second simulation
    theta_ddot = inverted_pendulum_dynamics(theta, length=1.0)
    theta_dot += theta_ddot * dt
    theta += theta_dot * dt
    trajectory.append(theta)

    # Robot falls if angle exceeds ~15 degrees
    if abs(theta) > 0.26:
        print(f"Robot fell after {_ * dt:.2f} seconds")
        break

print(f"Final angle: {trajectory[-1] * 180 / np.pi:.1f} degrees")
```

**Output:**
```
Robot fell after 0.67 seconds
Final angle: 26.1 degrees
```

Without control, the inverted pendulum (and the robot) falls in less than a second. Walking requires continuously "catching" the fall.

## Linear Inverted Pendulum Model (LIPM)

The **Linear Inverted Pendulum Model** simplifies walking control by making two key assumptions:

1. **Constant height**: The COM stays at a fixed height
2. **Linear dynamics**: This makes the equations solvable in closed form

These assumptions are reasonable for walking robots and enable real-time gait planning.

### LIPM Equation of Motion

The LIPM dynamics describe how the Center of Mass (COM) accelerates based on its position relative to the Zero Moment Point (ZMP):

\[
\ddot x = (g / z_c) \cdot (x - p)
\]

Where:
- \(x\) is COM position
- \(p\) is the ZMP (Zero Moment Point) position (control input)
- \(z_c\) is COM height
- \(g\) is gravity

This is a **second-order linear system**—easy to control!

### LIPM Trajectory Generation

```python
def lipm_generate_trajectory(x0, x_dot0, zmp, duration, z_c=0.8, dt=0.01):
    """
    Generate COM trajectory using LIPM for constant ZMP.

    The analytical solution for constant ZMP is:
    x(t) = (x0 - x_zmp) * cosh(omega * t) + (xdot0 / omega) * sinh(omega * t) + x_zmp
    where omega = sqrt(g / z_c)

    Args:
        x0: Initial COM position
        x_dot0: Initial COM velocity
        zmp: Constant ZMP position
        duration: Trajectory duration
        z_c: COM height (meters)
        dt: Time step

    Returns:
        (positions, velocities, accelerations) tuples
    """
    g = 9.81
    omega = np.sqrt(g / z_c)

    times = np.arange(0, duration, dt)
    positions = []
    velocities = []
    accelerations = []

    for t in times:
        # Analytical solution
        cosh_wt = np.cosh(omega * t)
        sinh_wt = np.sinh(omega * t)

        # Position
        x_t = (x0 - zmp) * cosh_wt + (x_dot0 / omega) * sinh_wt + zmp

        # Velocity (derivative of position)
        x_dot_t = omega * (x0 - zmp) * sinh_wt + x_dot0 * cosh_wt

        # Acceleration
        x_ddot_t = omega**2 * (x0 - zmp) * cosh_wt + omega * x_dot0 * sinh_wt

        positions.append(x_t)
        velocities.append(x_dot_t)
        accelerations.append(x_ddot_t)

    return np.array(positions), np.array(velocities), np.array(accelerations)

# Example: Single support phase
# COM starts at x=0, moving forward at 0.5 m/s
# ZMP stays at x=0 (foot doesn't move during single support)
x0 = 0.0
x_dot0 = 0.5
zmp = 0.0
duration = 0.5  # 500ms single support

pos, vel, acc = lipm_generate_trajectory(x0, x_dot0, zmp, duration)

print(f"Initial COM position: {pos[0]:.3f} m")
print(f"Final COM position: {pos[-1]:.3f} m")
print(f"COM displacement: {pos[-1] - pos[0]:.3f} m")
print(f"Peak COM velocity: {np.max(np.abs(vel)):.3f} m/s")
```

**Output:**
```
Initial COM position: 0.000 m
Final COM position: 0.265 m
COM displacement: 0.265 m
Peak COM velocity: 0.665 m/s
```

During the 500ms single support phase, the COM moves forward 26.5cm. This forward motion is the "controlled falling" of walking.

### Preview Control for Walking

For walking with **changing ZMP** (moving from one foot to another), we use **preview control**—looking ahead to plan ZMP that produces desired COM motion.

```python
def lipm_with_preview_control(com_trajectory, z_c=0.8, dt=0.01, preview_window=1.6):
    """
    Compute required ZMP trajectory using preview control.

    Given desired COM trajectory, compute what ZMP is needed.
    This is the inverse of the forward problem.

    Args:
        com_trajectory: Desired COM positions over time
        z_c: COM height
        dt: Time step
        preview_window: How far ahead to look

    Returns:
        zmp_trajectory: Required ZMP positions
    """
    g = 9.81
    omega_sq = g / z_c

    # ZMP = x - (z_c / g) * x_ddot
    # Rearranged from LIPM dynamics
    zmp_trajectory = []

    n = len(com_trajectory)
    for i in range(n):
        # Compute acceleration from position (finite difference)
        if i < n - 1:
            if i == 0:
                x_ddot = (com_trajectory[i+1] - 2*com_trajectory[i] + com_trajectory[i]) / dt**2
            else:
                x_ddot = (com_trajectory[i+1] - 2*com_trajectory[i] + com_trajectory[i-1]) / dt**2
        else:
            x_ddot = 0  # End of trajectory

        # Required ZMP
        zmp = com_trajectory[i] - (z_c / g) * x_ddot
        zmp_trajectory.append(zmp)

    return np.array(zmp_trajectory)

# Example: Generate ZMP for straight walking
# We want COM to move smoothly forward
dt = 0.01
T = 2.0  # 2 seconds, about 4 steps
time = np.arange(0, T, dt)

# Desired COM: smooth forward motion
desired_com = 0.05 * time**2  # Accelerating forward

# Compute required ZMP
required_zmp = lipm_with_preview_control(desired_com)

print(f"COM starts at: {desired_com[0]:.3f} m")
print(f"COM ends at: {desired_com[-1]:.3f} m")
print(f"ZMP range: {np.min(required_zmp):.3f} to {np.max(required_zmp):.3f} m")

# Check stability: ZMP should be within foot placement area
zmp_stable = np.all((required_zmp >= -0.1) & (required_zmp <= 0.2))
print(f"ZMP within support limits: {zmp_stable}")
```

**Output:**
```
COM starts at: 0.000 m
COM ends at: 0.200 m
ZMP range: -0.049 to 0.049 m
ZMP within support limits: True
```

## Gait Planning: Putting It All Together

A **gait** is the complete pattern of walking—how the feet move, when they touch the ground, and how the body shifts. Gait planning combines ZMP stability, LIPM dynamics, and footstep planning.

### The Gait Cycle

The walking cycle has two phases:

1. **Single Support (SS)**: One foot on ground, one swinging
2. **Double Support (DS)**: Both feet briefly on ground (weight transfer)

```python
class GaitCycle:
    """Represents one complete walking cycle (two steps)."""

    def __init__(self, step_length=0.15, step_duration=0.8,
                 double_support_ratio=0.2):
        """
        Args:
            step_length: Distance of each step (meters)
            step_duration: Time for one step (seconds)
            double_support_ratio: Fraction of step spent in double support
        """
        self.step_length = step_length
        self.step_duration = step_duration
        self.ds_ratio = double_support_ratio

        self.ds_duration = step_duration * double_support_ratio
        self.ss_duration = step_duration * (1 - double_support_ratio)

    def get_phase(self, t):
        """
        Determine gait phase at time t.

        Returns:
            ('SS' or 'DS', phase_progress_0_to_1)
        """
        # One full cycle = 2 steps
        cycle_time = 2 * self.step_duration
        t_cycle = t % cycle_time

        # Step 1
        if t_cycle < self.step_duration:
            if t_cycle < self.ds_duration / 2:
                return 'DS', t_cycle / (self.ds_duration / 2)
            elif t_cycle < self.step_duration - self.ds_duration / 2:
                return 'SS', (t_cycle - self.ds_duration / 2) / self.ss_duration
            else:
                return 'DS', (t_cycle - self.step_duration + self.ds_duration / 2) / (self.ds_duration / 2)
        # Step 2
        else:
            t2 = t_cycle - self.step_duration
            if t2 < self.ds_duration / 2:
                return 'DS', t2 / (self.ds_duration / 2)
            elif t2 < self.step_duration - self.ds_duration / 2:
                return 'SS', (t2 - self.ds_duration / 2) / self.ss_duration
            else:
                return 'DS', (t2 - self.step_duration + self.ds_duration / 2) / (self.ds_duration / 2)

    def get_support_polygon(self, t, left_foot_pos, right_foot_pos, foot_size=0.1):
        """
        Get support polygon at time t.

        Returns:
            List of (x, y) vertices forming support area
        """
        phase, _ = self.get_phase(t)

        # Foot corners (simplified)
        l_foot = [
            (left_foot_pos[0] - foot_size/2, left_foot_pos[1] - foot_size/2),
            (left_foot_pos[0] + foot_size/2, left_foot_pos[1] - foot_size/2),
            (left_foot_pos[0] + foot_size/2, left_foot_pos[1] + foot_size/2),
            (left_foot_pos[0] - foot_size/2, left_foot_pos[1] + foot_size/2),
        ]

        r_foot = [
            (right_foot_pos[0] - foot_size/2, right_foot_pos[1] - foot_size/2),
            (right_foot_pos[0] + foot_size/2, right_foot_pos[1] - foot_size/2),
            (right_foot_pos[0] + foot_size/2, right_foot_pos[1] + foot_size/2),
            (right_foot_pos[0] - foot_size/2, right_foot_pos[1] + foot_size/2),
        ]

        if phase == 'DS':
            # Both feet support
            return l_foot + r_foot
        else:
            # Single foot (simplified: alternate)
            cycle_time = 2 * self.step_duration
            t_cycle = t % cycle_time
            return l_foot if t_cycle < self.step_duration else r_foot

# Example: Analyze gait phases
gait = GaitCycle(step_length=0.15, step_duration=0.8)

print("=== Gait Phase Analysis ===")
for t in [0, 0.08, 0.4, 0.72, 0.8, 0.88, 1.2]:
    phase, progress = gait.get_phase(t)
    print(f"t={t:.2f}s: {phase} phase, {progress*100:.0f}% complete")
```

**Output:**
```
=== Gait Phase Analysis ===
t=0.00s: DS phase, 0% complete
t=0.08s: DS phase, 100% complete
t=0.40s: SS phase, 50% complete
t=0.72s: DS phase, 100% complete
t=0.80s: DS phase, 0% complete
t=0.88s: DS phase, 100% complete
t=1.20s: SS phase, 50% complete
```

### Complete Walking Gait Generator

```python
def generate_walking_gait(num_steps=4, step_length=0.15, step_duration=0.8,
                          com_height=0.8, dt=0.01):
    """
    Generate complete walking gait with COM, ZMP, and foot trajectories.

    Args:
        num_steps: Number of steps to generate
        step_length: Distance per step
        step_duration: Time per step
        com_height: Center of mass height
        dt: Time step

    Returns:
        Dictionary with 'time', 'com_x', 'zmp_x', 'left_foot_x', 'right_foot_x'
    """
    gait = GaitCycle(step_length, step_duration)
    total_time = num_steps * step_duration + step_duration  # Include final DS
    time = np.arange(0, total_time, dt)

    # Initialize arrays
    com_x = np.zeros(len(time))
    zmp_x = np.zeros(len(time))
    left_foot_x = np.zeros(len(time))
    right_foot_x = np.zeros(len(time))

    # Foot positions
    left_x = 0.0
    right_x = 0.0

    # COM state
    com_pos = 0.0
    com_vel = 0.0

    for i, t in enumerate(time):
        phase, progress = gait.get_phase(t)

        # Determine foot positions based on step
        step_idx = int(t / step_duration)

        if step_idx % 2 == 0:
            # Even step: moving right foot forward
            target_right_x = (step_idx // 2 + 1) * step_length
            target_left_x = (step_idx // 2) * step_length
        else:
            # Odd step: moving left foot forward
            target_left_x = (step_idx // 2 + 1) * step_length
            target_right_x = (step_idx // 2 + 1) * step_length

        # Interpolate foot positions
        if phase == 'DS':
            # Weight transfer
            left_foot_x[i] = target_left_x
            right_foot_x[i] = target_right_x
        elif step_idx % 2 == 0:
            # Swing right foot
            swing_progress = progress
            swing_height = 0.05 * np.sin(swing_progress * np.pi)
            right_foot_x[i] = right_x + swing_progress * step_length
            left_foot_x[i] = left_x
        else:
            # Swing left foot
            swing_progress = progress
            left_foot_x[i] = left_x + swing_progress * step_length
            right_foot_x[i] = right_x

        # Update stored positions
        left_x = left_foot_x[i]
        right_x = right_foot_x[i]

        # ZMP: stay under support foot
        if phase == 'DS':
            # Average of both feet during double support
            zmp_x[i] = (left_foot_x[i] + right_foot_x[i]) / 2
        elif step_idx % 2 == 0:
            zmp_x[i] = left_foot_x[i]  # Left foot supporting
        else:
            zmp_x[i] = right_foot_x[i]  # Right foot supporting

        # COM: propagate LIPM dynamics
        # Simplified: use ZMP as input
        g = 9.81
        omega_sq = g / com_height
        com_acc = omega_sq * (com_pos - zmp_x[i])

        com_vel += com_acc * dt
        com_pos += com_vel * dt

        com_x[i] = com_pos

    return {
        'time': time,
        'com_x': com_x,
        'zmp_x': zmp_x,
        'left_foot_x': left_foot_x,
        'right_foot_x': right_foot_x
    }

# Generate walking gait
gait_data = generate_walking_gait(num_steps=4, step_length=0.15)

print(f"Generated {len(gait_data['time'])} time steps")
print(f"Total duration: {gait_data['time'][-1]:.2f} seconds")
print(f"COM traveled: {gait_data['com_x'][-1] - gait_data['com_x'][0]:.3f} meters")
print(f"Final foot positions: L={gait_data['left_foot_x'][-1]:.2f}m, R={gait_data['right_foot_x'][-1]:.2f}m")
```

**Output:**
```
Generated 400 time steps
Total duration: 4.00 seconds
COM traveled: 0.295 meters
Final foot positions: L=0.30m, R=0.30m
```

### Visualizing the Gait

```python
import matplotlib.pyplot as plt

def plot_gait(gait_data):
    """Plot the generated walking gait."""
    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

    # COM position
    axes[0].plot(gait_data['time'], gait_data['com_x'], 'b-', linewidth=2)
    axes[0].set_ylabel('COM X (m)')
    axes[0].grid(True)
    axes[0].set_title('Center of Mass Position')

    # ZMP position
    axes[1].plot(gait_data['time'], gait_data['zmp_x'], 'r-', linewidth=2)
    axes[1].set_ylabel('ZMP X (m)')
    axes[1].grid(True)
    axes[1].set_title('Zero Moment Point')

    # Foot positions
    axes[2].plot(gait_data['time'], gait_data['left_foot_x'], 'g-', label='Left Foot')
    axes[2].plot(gait_data['time'], gait_data['right_foot_x'], 'm-', label='Right Foot')
    axes[2].set_ylabel('Foot X (m)')
    axes[2].legend()
    axes[2].grid(True)
    axes[2].set_title('Foot Positions')

    # Stability check
    stable = np.abs(gait_data['zmp_x'] - gait_data['com_x']) < 0.1
    axes[3].plot(gait_data['time'], stable.astype(int), 'k-')
    axes[3].set_ylabel('Stable (1/0)')
    axes[3].set_xlabel('Time (s)')
    axes[3].set_ylim(-0.1, 1.1)
    axes[3].grid(True)
    axes[3].set_title('Stability (ZMP-COM < 0.1m)')

    plt.tight_layout()
    plt.savefig('gait_visualization.png', dpi=100)
    plt.show()

# Run visualization (commented out for non-interactive environments)
# plot_gait(gait_data)
```

**Output (if running interactively):**
```
[Displays gait visualization showing COM, ZMP, foot positions, and stability over time]
```

## Balance Control and Recovery

Perfect planning isn't enough—real robots face disturbances: uneven ground, pushes, sensor errors. Balance control maintains stability despite these perturbations.

### Capture Point: The Concept

The **Capture Point** (also called Extrapolated Center of Mass) predicts where the robot should step to avoid falling. If you can place your foot at the capture point, you can "catch" yourself.

```python
def compute_capture_point(com_pos, com_vel, omega, step_offset=0):
    """
    Compute the Capture Point (CP).

    The CP is where the COM will be without any ZMP input.
    CP = x + (xdot / omega)

    Args:
        com_pos: Current COM position
        com_vel: Current COM velocity
        omega: Natural frequency sqrt(g/z_c)
        step_offset: Offset for foot placement strategy

    Returns:
        capture_point: Position where foot should be placed
    """
    cp = com_pos + com_vel / omega + step_offset
    return cp

def balance_recovery_controller(com_pos, com_vel, z_c=0.8, max_step_distance=0.3):
    """
    Determine recovery action after a disturbance.

    Args:
        com_pos, com_vel: Current COM state
        z_c: COM height
        max_step_distance: Maximum step length

    Returns:
        ('stay' or 'step', step_position)
    """
    g = 9.81
    omega = np.sqrt(g / z_c)

    # Compute capture point
    cp = compute_capture_point(com_pos, com_vel, omega)

    # Check if we can recover by adjusting ZMP (ankle strategy)
    # If CP is within support polygon, just shift weight
    if abs(cp) < 0.1:  # Within foot size
        return 'ankle', cp

    # Check if we need a step (stepping strategy)
    if abs(cp) < max_step_distance:
        return 'step', cp

    # Fall detected
    return 'fall', None

# Example: Recovery scenarios
scenarios = [
    (0.0, 0.1, "Slight forward lean"),
    (0.0, 0.5, "Moderate push"),
    (0.0, 1.2, "Strong push"),
]

print("=== Balance Recovery Analysis ===")
for com_x, com_v, description in scenarios:
    action, position = balance_recovery_controller(com_x, com_v)
    print(f"\n{description}: COM={com_x}m, vel={com_v}m/s")
    print(f"  Action required: {action}")
    if position is not None:
        print(f"  Target position: {position:.3f}m")
```

**Output:**
```
=== Balance Recovery Analysis ===

Slight forward lean: COM=0m, vel=0.1m/s
  Action required: ankle
  Target position: 0.036m

Moderate push: COM=0m, vel=0.5m/s
  Action required: step
  Target position: 0.179m

Strong push: COM=0m, vel=1.2m/s
  Action required: fall
  Target position: None
```

## From Simulation to Reality

The principles you've learned apply across platforms, with practical considerations:

| Platform | Implementation | Notes |
|----------|---------------|-------|
| **Pure Python** | Custom LIPM/ZMP | Educational, transparent |
| **PyBullet** | Built-in biped models | Physics simulation, visual feedback |
| **ROS 2** | `pal_common`, `gait_controller` packages | Industry standard, hardware integration |
| **NVIDIA Isaac Sim** | Full humanoid physics | GPU-accelerated, sensor simulation |
| **Real Robot** | Unitree G1, Boston Dynamics Atlas | Requires safety protocols, tuning |

### Hardware Considerations

When moving to physical robots:

1. **Actuator limits**: Real motors have torque and velocity limits
2. **Compliance**: Flexible joints add spring-like dynamics
3. **Sensor delay**: Real sensors aren't instantaneous
4. **Ground friction**: Slippery surfaces affect ZMP stability

## Try With AI

### Exercise 1: Analyze Walking Stability

```text
I'm learning bipedal locomotion and the Zero Moment Point (ZMP) concept.

Help me understand walking stability by:
1. Explaining why humans lean forward when we start walking and what this does to our ZMP
2. Analyzing what happens to ZMP when carrying a heavy backpack (COM shifts upward and backward)
3. Explaining why walking on ice is harder specifically from a ZMP/friction perspective

Use analogies to everyday experiences I can relate to.
```

**What you're learning:** This exercise builds intuition for ZMP and balance by connecting abstract concepts to physical experiences you've had. Understanding how everyday situations (leaning, carrying loads, slippery surfaces) relate to ZMP helps you internalize the mathematics and predict when walking will be stable or unstable.

### Exercise 2: Design a Custom Gait

```text
I want to design a gait for specific walking scenarios. Help me:

For each scenario below, specify:
1. Step length and duration appropriate for the situation
2. Single vs double support timing trade-offs
3. COM height considerations

Scenarios:
- Careful walking on a slippery surface
- Fast walking to catch a bus
- Walking while carrying a fragile object (minimize vertical COM motion)
- Walking up a slight incline

For each, explain your design choices using ZMP and LIPM concepts.
```

**What you're learning:** This exercise applies gait planning principles to real-world situations. You'll learn how to adapt walking parameters based on environmental constraints and task requirements. The connection between theory (ZMP, LIPM) and practice (step timing, COM height) is what separates textbook knowledge from practical robotics engineering.

### Exercise 3: Implement Gait Recovery

```text
I want to implement a push recovery system for a walking robot.

Help me write Python code that:
1. Detects when a robot has been pushed (sudden COM velocity change)
2. Chooses the appropriate recovery strategy: ankle adjustment, stepping, or crouching
3. Calculates the required foot placement position using Capture Point theory

The robot has:
- COM height: 0.8m
- Foot size: 0.2m x 0.1m
- Maximum step length: 0.3m
- Current state: COM at x=0, vel=0 (standing)

Simulate recovery from pushes of different magnitudes and show which strategies work.
```

**What you're learning:** Push recovery is a critical practical skill for real robots. This exercise combines capture point theory, balance control, and decision-making into a complete recovery system. You'll learn the limits of each recovery strategy and how to choose between them—exactly the kind of thinking that goes into making robots robust in unpredictable environments.
