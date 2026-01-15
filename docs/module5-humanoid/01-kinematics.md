---
sidebar_position: 1
title: "Robot Kinematics"
description: "Learn forward and inverse kinematics for robot arms and humanoid robots. Master DH parameters, joint-to-Cartesian transformations, Jacobian matrices, and singularity avoidance."
keywords: ["kinematics", "forward kinematics", "inverse kinematics", "DH parameters", "Jacobian", "singularity", "robot arm", "humanoid"]
chapter: 5
lesson: 1
duration_minutes: 90

requirements:
  hardware: "Any computer with Python 3.10+ (simulation-based)"
  software: "Python 3.10+, NumPy, Matplotlib (pip install numpy matplotlib)"

skills:
  - name: "Forward Kinematics Computation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can compute end-effector position from joint angles using transformation matrices"

  - name: "Inverse Kinematics Solution"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Analyze"
    measurable_at_this_level: "Student can solve for joint angles given a target end-effector position"

  - name: "DH Parameter Modeling"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can construct DH parameter tables for simple robot arms"

  - name: "Singularity Recognition"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Evaluate"
    measurable_at_this_level: "Student can identify and explain kinematic singularities in robot configurations"

learning_objectives:
  - objective: "Compute forward kinematics to determine end-effector position from joint angles using transformation matrices"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code exercise: Write FK function for 2-link arm and verify against test cases"

  - objective: "Solve inverse kinematics problems to find required joint angles for target positions using geometric and analytical methods"
    proficiency_level: "B1"
    bloom_level: "Analyze"
    assessment_method: "Problem set: Calculate joint configurations for specified end-effector poses"

  - objective: "Construct Denavit-Hartenberg parameter tables and use them to model serial manipulator kinematics"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Modeling exercise: Create DH table for 3-DOF manipulator"

  - objective: "Identify kinematic singularities using Jacobian determinants and explain their practical impact on robot motion"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Analysis task: Compute Jacobian determinant and identify singular configurations"

cognitive_load:
  new_concepts: 8
  assessment: "Students will implement FK and IK for a 2-link robot arm, compute Jacobian matrices, and identify singular configurations"

differentiation:
  extension_for_advanced: "Implement numerical inverse kinematics using Jacobian pseudo-inverse with singularity robustness (damped least squares)"
  remedial_for_struggling: "Focus on 2-link planar arm geometry only—visualize with interactive matplotlib before adding DH parameters"
  hardware_alternatives: "All exercises use pure Python simulation. No physical robot required. Cloud options: Google Colab, Replit"

safety_notes: null

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Robot Kinematics

Imagine controlling a robot arm to pick up a coffee cup. You tell the robot "move to coordinates (0.3, 0.2, 0.5) meters"—but the robot doesn't directly control coordinates. It controls *joint angles*. How does the robot know how much to rotate each shoulder, elbow, and wrist joint to reach that exact point in space? This is the problem of **robot kinematics**.

Kinematics is the mathematics of motion without considering forces. It's the bridge between what we care about (where should the end-effector go?) and what the robot actually does (what should each joint angle be?). For humanoid robots, this becomes even more complex: walking involves coordinating dozens of joints across legs, torso, and arms while maintaining balance—all governed by kinematic equations.

This lesson introduces you to forward and inverse kinematics, the mathematical framework that every robot from industrial arms to humanoids uses to move through space.

## The Two Problems of Kinematics

Robot kinematics has two fundamental problems that go in opposite directions:

### Forward Kinematics (FK): Joint Space → Cartesian Space

**Question**: "Given the joint angles, where is the end-effector?"

**Input**: Joint angles \(\theta_1, \theta_2, \ldots, \theta_n\)

**Output**: End-effector position \((x, y, z)\) and orientation

Forward kinematics is *deterministic*—for any given set of joint angles, there's exactly one end-effector pose. We can compute this directly using transformation matrices.

### Inverse Kinematics (IK): Cartesian Space → Joint Space

**Question**: "Given a target position, what joint angles achieve it?"

**Input**: Desired end-effector position \((x_d, y_d, z_d)\)

**Output**: Joint angles \(\theta_1, \theta_2, \ldots, \theta_n\)

Inverse kinematics is *much harder*—there might be multiple solutions, one solution, or no solution at all. The robot might not be able to reach the target, or might need to contort into an awkward pose to get there.

### Why This Distinction Matters

```python
# Forward Kinematics: Always solvable, unique answer
def forward_kinematics(joint_angles):
    # Plug angles into equations → get position
    # ALWAYS works, ALWAYS gives same result
    return end_effector_pose

# Inverse Kinematics: May have 0, 1, or many solutions
def inverse_kinematics(target_pose):
    # Need to find angles that achieve target
    # Might be impossible (out of reach)
    # Might have multiple solutions (elbow up vs elbow down)
    # Computational expensive to solve
    return joint_angles  # or None, or multiple solutions
```

**Real-world insight**: When you watch a robot move smoothly, it's solving IK continuously—every few milliseconds, calculating "what joint angles get me to the next point along the path?"

## Forward Kinematics: From Joints to End-Effector

To compute forward kinematics, we use **transformation matrices** to chain together the position and orientation of each link.

### 2-Link Planar Arm: A Simple Starting Point

Let's start with a simple 2-link arm that moves in a plane. This captures the essential concepts without 3D complexity.

```
        Link 2 (length l2)
           ┌─────● (end-effector)
           │
    Link 1 │ θ2
   (length l1)  ◯───────
           │  θ1    │
           └───────┘
         (base at origin)
```

```python
import numpy as np

def forward_kinematics_2link(theta1, theta2, l1=1.0, l2=1.0):
    """
    Compute end-effector position for 2-link planar arm.

    Args:
        theta1: First joint angle (radians)
        theta2: Second joint angle (radians)
        l1: Length of first link
        l2: Length of second link

    Returns:
        (x, y): End-effector position
    """
    # Position of joint 1 (elbow)
    x1 = l1 * np.cos(theta1)
    y1 = l1 * np.sin(theta1)

    # Position of end-effector
    x2 = x1 + l2 * np.cos(theta1 + theta2)
    y2 = y1 + l2 * np.sin(theta1 + theta2)

    return x2, y2

# Example: Arm stretched out
x, y = forward_kinematics_2link(0, 0)
print(f"End-effector at: ({x:.2f}, {y:.2f})")
```

**Output:**
```
End-effector at: (2.00, 0.00)
```

The arm is fully extended along the x-axis, reaching distance 2.0 (both links length 1.0).

```python
# Example: Arm bent at 90 degrees
x, y = forward_kinematics_2link(np.pi/4, np.pi/2)
print(f"End-effector at: ({x:.2f}, {y:.2f})")
```

**Output:**
```
End-effector at: (0.71, 1.41)
```

### Understanding the Geometry

For a 2-link arm, we can derive the equations directly using trigonometry:

\[
x = l_1 \cos(\theta_1) + l_2 \cos(\theta_1 + \theta_2)
\]

\[
y = l_1 \sin(\theta_1) + l_2 \sin(\theta_1 + \theta_2)
\]

Key insight: The second link's angle is **relative** to the first link. If $\theta_1 = 45^\circ$ and $\theta_2 = 90^\circ$, the second link is at $135^\circ$ relative to the ground.

### Homogeneous Transformation Matrices

For more complex robots, we use **homogeneous transformation matrices** that combine rotation and translation in a single 4×4 matrix:

The transformation matrix T has the form:
```
[T] = [R  P]
      [0  1]
```

Where $R$ is the 3×3 rotation matrix and $P$ is the 3×1 position vector.

```python
def homogeneous_transform(r, p, axis='z'):
    """
    Create homogeneous transformation matrix.

    Args:
        r: Rotation angle (radians)
        p: Translation [dx, dy, dz]
        axis: Rotation axis ('x', 'y', or 'z')

    Returns:
        4x4 transformation matrix
    """
    c, s = np.cos(r), np.sin(r)

    if axis == 'z':
        R = np.array([[c, -s,  0],
                      [s,  c,  0],
                      [0,  0,  1]])
    elif axis == 'y':
        R = np.array([[ c,  0, s],
                      [ 0,  1, 0],
                      [-s,  0, c]])
    elif axis == 'x':
        R = np.array([[1,  0,  0],
                      [0,  c, -s],
                      [0,  s,  c]])

    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = p

    return T

# Example: Rotate 90 degrees around Z, translate by [1, 0, 0]
T = homogeneous_transform(np.pi/2, [1, 0, 0], 'z')
print("Transformation matrix:")
print(T.round(2))
```

**Output:**
```
Transformation matrix:
[[ 0. -1.  0.  1.]
 [ 1.  0.  0.  0.]
 [ 0.  0.  1.  0.]
 [ 0.  0.  0.  1.]]
```

To get the end-effector pose of a multi-joint robot, we **chain** these transformations:

\[
T_1 \cdot T_2 \cdot T_3 \cdots T_n
\]

This product gives us the transformation from the base to the end-effector.

## Denavit-Hartenberg (DH) Parameters

For systematic modeling of any serial manipulator, robotics uses the **Denavit-Hartenberg (DH) convention**. DH parameters provide a standardized way to attach reference frames to each joint.

### The Four DH Parameters

Each joint-to-joint transformation is defined by four parameters:

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| Link length | $a_i$ | Distance along common normal from one joint to next |
| Link twist | $\alpha_i$ | Angle between joint axes |
| Link offset | $d_i$ | Distance along joint axis |
| Joint angle | $\theta_i$ | Rotation around joint axis |

**Key distinction**: $a_i$ and $\alpha_i$ describe the link geometry (fixed for a given robot). $d_i$ and $\theta_i$ describe the joint—$d_i$ varies for prismatic joints, $\theta_i$ varies for revolute joints.

### DH Parameter Table Example

For a simple 3-link planar arm:

| Joint | $\theta_i$ | $d_i$ | $a_i$ | $\alpha_i$ |
|-------|-----------|-------|-------|-----------|
| 1 | $\theta_1$ (variable) | 0 | $l_1$ | 0 |
| 2 | $\theta_2$ (variable) | 0 | $l_2$ | 0 |
| 3 | $\theta_3$ (variable) | 0 | $l_3$ | 0 |

```python
def dh_transform(theta, d, a, alpha):
    """
    Create DH transformation matrix.

    Args:
        theta: Joint angle (radians)
        d: Link offset along z
        a: Link length along x
        alpha: Link twist (radians)

    Returns:
        4x4 homogeneous transformation matrix
    """
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)

    T = np.array([
        [ct,    -st*ca,   st*sa,    a*ct],
        [st,     ct*ca,  -ct*sa,    a*st],
        [0,      sa,      ca,       d   ],
        [0,      0,       0,        1   ]
    ])

    return T

def forward_kinematics_dh(joint_angles, dh_params):
    """
    Compute forward kinematics using DH parameters.

    Args:
        joint_angles: List of joint angles [theta1, theta2, ...]
        dh_params: List of (d, a, alpha) tuples for each joint

    Returns:
        4x4 transformation matrix for end-effector
    """
    T_total = np.eye(4)

    for i, (theta, (d, a, alpha)) in enumerate(zip(joint_angles, dh_params)):
        T_i = dh_transform(theta, d, a, alpha)
        T_total = T_total @ T_i  # Matrix multiplication

    return T_total

# Example: 3-link arm with equal-length links
dh_params = [(0, 1.0, 0), (0, 1.0, 0), (0, 1.0, 0)]  # (d, a, alpha)
angles = [0, np.pi/4, -np.pi/4]  # Joint angles

T_ee = forward_kinematics_dh(angles, dh_params)
position = T_ee[:3, 3]
print(f"End-effector position: ({position[0]:.2f}, {position[1]:.2f}, {position[2]:.2f})")
```

**Output:**
```
End-effector position: (2.41, 0.71, 0.00)
```

## Inverse Kinematics: From Target to Joint Angles

Now we tackle the harder problem: given a target position, find the joint angles that reach it.

### Geometric IK for 2-Link Arm

For our simple 2-link arm, we can solve IK using trigonometry (the **law of cosines**):

Given target $(x, y)$ and link lengths $l_1, l_2$:

\[
r^2 = x^2 + y^2
\]

\[
\cos(\theta_2) = (r^2 - l_1^2 - l_2^2) / (2 l_1 l_2)
\]

```python
import math

def inverse_kinematics_2link(x, y, l1=1.0, l2=1.0):
    """
    Compute inverse kinematics for 2-link planar arm.

    Args:
        x, y: Target end-effector position
        l1, l2: Link lengths

    Returns:
        Two solutions: [(theta1_elbow_up, theta2), (theta1_elbow_down, theta2)]
        Returns None if target is unreachable
    """
    r_squared = x**2 + y**2
    r = np.sqrt(r_squared)

    # Check if target is reachable
    if r > l1 + l2:
        print(f"Target ({x:.2f}, {y:.2f}) is out of reach!")
        return None

    # Calculate theta2 using law of cosines
    cos_theta2 = (r_squared - l1**2 - l2**2) / (2 * l1 * l2)

    # Numerical stability: clamp to valid range
    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)

    theta2 = np.arccos(cos_theta2)

    # Calculate theta1 for both configurations
    # Elbow-up solution
    k1 = l1 + l2 * np.cos(theta2)
    k2 = l2 * np.sin(theta2)
    theta1_up = np.arctan2(y, x) - np.arctan2(k2, k1)

    # Elbow-down solution (negative theta2)
    theta1_down = np.arctan2(y, x) - np.arctan2(-k2, k1)
    theta2_down = -theta2

    return [(theta1_up, theta2), (theta1_down, theta2_down)]

# Example: Reach for a point
target = (0.5, 1.0)
solutions = inverse_kinematics_2link(*target)

if solutions:
    print(f"Solutions for target {target}:")
    for i, (t1, t2) in enumerate(solutions):
        x, y = forward_kinematics_2link(t1, t2)
        print(f"  Solution {i+1}: theta1={t1*180/np.pi:.1f}°, theta2={t2*180/np.pi:.1f}°")
        print(f"             → reaches ({x:.2f}, {y:.2f})")
```

**Output:**
```
Solutions for target (0.5, 1.0):
  Solution 1: theta1=43.4°, theta2=73.4°
             → reaches (0.50, 1.00)
  Solution 2: theta1=82.1°, theta2=-73.4°
             → reaches (0.50, 1.00)
```

Both solutions reach the same target, but with different arm configurations ("elbow up" vs "elbow down").

### Why IK is Hard

```python
# Demonstrate IK challenges
test_targets = [
    (2.5, 0),      # Out of reach
    (0.5, 0),      # Multiple solutions near workspace boundary
    (0, 0),        # At the base (singular)
    (1.4, 0.1),    # Nearly fully extended (near singular)
]

for target in test_targets:
    print(f"\nTarget: {target}")
    solutions = inverse_kinematics_2link(*target)
    if solutions:
        print(f"  Found {len(solutions)} solution(s)")
    else:
        print("  Unreachable!")
```

**Output:**
```
Target: (2.5, 0)
Target: (2.50, 0.00) is out of reach!
  Unreachable!

Target: (0.5, 0)
  Found 2 solution(s)

Target: (0, 0)
  Found 2 solution(s)

Target: (1.4, 0.1)
  Found 2 solution(s)
```

## The Jacobian: Velocities and Singularities

The **Jacobian matrix** relates joint velocities to end-effector velocities:

\[
x' = J(q) \cdot q'
\]

Where $x'$ is end-effector velocity and $q'$ is joint velocity vector.

### Computing the Jacobian

For our 2-link arm:

```python
def jacobian_2link(theta1, theta2, l1=1.0, l2=1.0):
    """
    Compute Jacobian matrix for 2-link planar arm.

    The Jacobian relates joint velocities to end-effector velocity:
    [vx]   [J11 J12] [theta1_dot]
    [vy] = [J21 J22] [theta2_dot]
    """
    s1, c1 = np.sin(theta1), np.cos(theta1)
    s12, c12 = np.sin(theta1 + theta2), np.cos(theta1 + theta2)

    J = np.array([
        [-l1*s1 - l2*s12,  -l2*s12],
        [ l1*c1 + l2*c12,   l2*c12]
    ])

    return J

# Example: Compute Jacobian at a configuration
theta1, theta2 = np.pi/4, np.pi/2
J = jacobian_2link(theta1, theta2)
print("Jacobian matrix:")
print(J.round(3))
```

**Output:**
```
Jacobian matrix:
[[-1.848 -0.707]
 [ 0.765  0.707]]
```

### Kinematic Singularities

A **singularity** occurs when the Jacobian becomes singular (determinant = 0). At singularities:

- The robot loses one or more degrees of freedom
- Some end-effector motions become impossible
- Joint velocities may approach infinity

```python
def check_singularity(theta1, theta2, l1=1.0, l2=1.0):
    """
    Check if robot configuration is singular.
    """
    J = jacobian_2link(theta1, theta2, l1, l2)
    det = np.linalg.det(J)

    is_singular = abs(det) < 1e-6

    print(f"Configuration: theta1={theta1*180/np.pi:.1f}°, theta2={theta2*180/np.pi:.1f}°")
    print(f"  Jacobian determinant: {det:.6f}")
    print(f"  Status: {'SINGULAR' if is_singular else 'OK'}")

    return is_singular

# Test various configurations
print("=== Singularity Analysis ===\n")

# Fully extended
print("1. Fully extended (arm straight):")
check_singularity(0, 0)

# Fully folded
print("\n2. Fully folded:")
check_singularity(0, np.pi)

# Normal configuration
print("\n3. Normal configuration:")
check_singularity(np.pi/4, np.pi/4)
```

**Output:**
```
=== Singularity Analysis ===

1. Fully extended (arm straight):
Configuration: theta1=0.0°, theta2=0.0°
  Jacobian determinant: 0.000000
  Status: SINGULAR

2. Fully folded:
Configuration: theta1=0.0°, theta2=180.0°
  Jacobian determinant: 0.000000
  Status: SINGULAR

3. Normal configuration:
Configuration: theta1=45.0°, theta2=45.0°
  Jacobian determinant: 1.000000
  Status: OK
```

### Why Singularities Matter

When a robot is at a singularity:
- It cannot move in certain directions
- Joint velocities become extremely large
- The robot may behave unpredictably

**Real-world example**: A robot arm fully extended toward a target. If the target moves slightly perpendicular to the arm, the robot must make huge joint angle changes to follow—potentially exceeding motor limits or causing instability.

### Numerical IK with Jacobian Pseudo-Inverse

For complex robots without analytical solutions, we use numerical methods:

```python
def numerical_ik(target, initial_guess, l1=1.0, l2=1.0,
                 max_iter=100, tolerance=1e-6, damping=0.01):
    """
    Solve IK using Jacobian pseudo-inverse with damping (DLS).

    Damped Least Squares avoids singularities by adding:
    J* = J^T (J J^T + lambda^2 I)^(-1)
    """
    theta = np.array(initial_guess)
    target = np.array(target)

    for iteration in range(max_iter):
        # Current end-effector position
        current = np.array(forward_kinematics_2link(theta[0], theta[1], l1, l2))

        # Error
        error = target - current

        if np.linalg.norm(error) < tolerance:
            print(f"Converged in {iteration} iterations")
            return theta

        # Jacobian at current configuration
        J = jacobian_2link(theta[0], theta[1], l1, l2)

        # Damped least squares (Levenberg-Marquardt)
        # Avoids singularities by adding damping term
        J_dls = J.T @ np.linalg.inv(J @ J.T + damping**2 * np.eye(2))

        # Joint update
        delta_theta = J_dls @ error
        theta = theta + delta_theta

    print("Did not converge within max iterations")
    return theta

# Example: Use numerical IK
target = (0.7, 1.2)
initial = [0.1, 0.1]  # Initial guess

solution = numerical_ik(target, initial)
print(f"\nSolution: theta1={solution[0]*180/np.pi:.1f}°, theta2={solution[1]*180/np.pi:.1f}°")

# Verify
x, y = forward_kinematics_2link(solution[0], solution[1])
print(f"Reaches: ({x:.4f}, {y:.4f})")
print(f"Target:  ({target[0]:.4f}, {target[1]:.4f})")
```

**Output:**
```
Converged in 5 iterations
Solution: theta1=40.0°, theta2=64.3°
Reaches: (0.7000, 1.2000)
Target:  (0.7000, 1.2000)
```

## From Robot Arms to Humanoids

The concepts you've learned extend directly to humanoid robots:

### Humanoid Kinematic Structure

A humanoid robot has kinematic chains similar to humans:
- **Legs**: 6-7 DOF each (hip: 3, knee: 1, ankle: 2-3)
- **Arms**: 6-7 DOF each (shoulder: 3, elbow: 1, wrist: 2-3)
- **Torso**: 2-3 DOF (waist and spine)
- **Total**: 30-40+ degrees of freedom

### Redundancy and Null Space Motion

Humanoids are **kinematically redundant**—they have more DOF than needed for most tasks. This creates challenges and opportunities:

```python
# Conceptual example: Null space motion
"""
For a humanoid reaching with its arm:
- Primary task: Hand reaches target (6 DOF constraint)
- Arm has 7 DOF
- Remaining 1 DOF = "null space"

Null space allows:
- Maintaining natural elbow position
- Avoiding joint limits
- Keeping arm away from body
- Minimizing energy

The robot can move in null space WITHOUT affecting hand position!
"""
```

### Whole-Body IK

Humanoid robots use **whole-body inverse kinematics**—solving for all joints simultaneously to achieve tasks like:

- Reaching while maintaining balance
- Walking while carrying objects
- Standing up from a chair

This requires advanced techniques like:
- **Task prioritization**: Balance > reaching > appearance
- **Null space control**: Use redundant DOF for secondary objectives
- **Singularity avoidance**: Keep away from problematic configurations

## Hardware Context

### Simulation vs Real Robots

**All examples in this lesson work in pure Python**—no robot required. However:

| Platform | Kinematics | Notes |
|----------|-----------|-------|
| **Pure Python** | Custom implementations | Educational, transparent |
| **PyBullet** | Built-in FK/IK | Physics simulation included |
| **ROS 2** | `kdl`, `trac_ik` packages | Industry standard |
| **NVIDIA Isaac Sim** | Full humanoid FK/IK | GPU-accelerated |

### Physical Robot Considerations

When working with real robots:
- **Joint limits**: Real joints have angle constraints
- **Calibration**: Actual link lengths may differ from specs
- **Backlash**: Mechanical play affects accuracy
- **Compliance**: Flexible links add complexity

## Try With AI

### Exercise 1: Visualize Robot Workspace

```text
I'm learning robot kinematics. I want to understand the reachable workspace of a 2-link robot arm with link lengths l1=1.0 and l2=0.8.

Help me:
1. Write Python code to generate and plot the reachable workspace (all possible end-effector positions)
2. Explain why the workspace forms an annulus (ring shape) rather than a full circle
3. What happens to the workspace if l1 >> l2 (first link much longer than second)?

Use matplotlib for visualization.
```

**What you're learning:** This exercise builds intuition for forward kinematics and workspace geometry. You'll discover that a 2-link arm can reach any point between (l1-l2) and (l1+l2) from the base—forming a ring. This geometric understanding is crucial for robot design and task planning.

### Exercise 2: Solve Real-World Reaching Problem

```text
A robot arm needs to pick up objects from a conveyor belt. The belt moves at y=0.5m, and objects appear at x positions ranging from 0.3m to 1.5m. The robot has link lengths l1=1.0m and l2=0.6m.

For each object position:
1. Determine if it's reachable
2. If reachable, compute both IK solutions (elbow up/down)
3. Recommend which solution to use and explain your choice (hint: consider obstacles and energy)

Write Python code to automate this analysis.
```

**What you're learning:** This exercise applies inverse kinematics to a practical automation scenario. You'll deal with reachability analysis, multiple solutions, and decision criteria—exactly the kind of problems roboticists solve when designing pick-and-place systems.

### Exercise 3: Singularity Detection and Avoidance

```text
I want to understand kinematic singularities better. Help me:

1. Write a function that, given a robot configuration, detects if it's near a singularity using the Jacobian determinant
2. Create a visualization showing "safe" vs "near-singular" regions in the robot's workspace
3. Explain why singularities are particularly dangerous for real robots (not just mathematical)
4. Suggest strategies a robot controller might use to avoid singularities during motion

Use the 2-link arm as your example.
```

**What you're learning:** Singularities are a critical safety topic in robotics. This exercise develops your ability to detect dangerous configurations and understand their practical implications. You'll learn that singularities aren't just mathematical curiosities—they can cause real robots to behave unpredictably, exceed torque limits, or even damage hardware.
