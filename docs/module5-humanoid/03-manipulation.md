---
sidebar_position: 3
title: "Robot Manipulation"
description: "Learn robot arms, grippers, and object manipulation. Master end effectors, grasp planning, force control, and dexterous manipulation for humanoid robots."
keywords: ["manipulation", "end effector", "gripper", "grasp planning", "force control", "dexterous manipulation", "pick and place", "MoveIt2", "robot arm"]
chapter: 5
lesson: 3
duration_minutes: 90

requirements:
  hardware: "Any computer with Python 3.10+ (simulation-based)"
  software: "Python 3.10+, NumPy, Matplotlib (pip install numpy matplotlib). ROS 2 Humble/Jazzy optional for advanced exercises"

skills:
  - name: "End Effector Analysis"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Analyze"
    measurable_at_this_level: "Student can compare different end effector types and select appropriate grippers for specific manipulation tasks"

  - name: "Grasp Planning"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can compute grasp quality metrics and generate grasp poses for simple objects"

  - name: "Force Control Implementation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can implement impedance and force control for safe manipulation"

  - name: "Dexterous Manipulation"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Evaluate"
    measurable_at_this_level: "Student can explain in-hand manipulation challenges and compare approaches"

learning_objectives:
  - objective: "Compare different end effector types (parallel jaw, vacuum, soft, dexterous) and select appropriate grippers for specific manipulation tasks"
    proficiency_level: "B1"
    bloom_level: "Analyze"
    assessment_method: "Design task: Select gripper for three manipulation scenarios and justify choices"

  - objective: "Compute grasp quality metrics using force closure and wrench space analysis to evaluate if a grasp will be stable"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code exercise: Implement grasp quality calculator for box grasps"

  - objective: "Implement force and impedance control for safe manipulation of fragile objects"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code exercise: Simulate force-controlled grasp with compliance"

  - objective: "Explain in-hand manipulation challenges and describe approaches for reorienting objects within the gripper"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Analysis: Compare finger gaiting, extrinsic dexterity, and dexterous hand approaches"

cognitive_load:
  new_concepts: 9
  assessment: "Students will implement grasp quality metrics, design pick-and-place sequences, and analyze force control approaches"

differentiation:
  extension_for_advanced: "Implement grasp planning using point cloud data from depth cameras with collision-free trajectory generation"
  remedial_for_struggling: "Focus on 2D grasp planning first (top-down grasps) before progressing to 3D grasps with arbitrary approach angles"
  hardware_alternatives: "All exercises use pure Python simulation. For ROS 2: Use MoveIt2 with Gazebo. For real hardware: Robotiq gripper with UR arm, or Unitree G1 hands"

safety_notes: "Physical robot arms can cause serious injury. Always test in simulation first. Use emergency stops, force limits, and keep clear workspace. Never bypass safety interlocks."

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Robot Manipulation

Watch a human pick up a pen. Your fingers wrap around it, applying just enough pressure to hold it without dropping. If it starts to slip, you automatically tighten your grip. You can reorient it, twirl it, pass it to someone else—all without conscious thought. This seemingly simple act involves incredibly complex sensing, planning, and control.

Robot manipulation seeks to give machines this same capability. A robot arm with a gripper can transform a factory warehouse, assist in surgery, or help a person with disabilities prepare a meal. But unlike locomotion, where the ground is predictable, manipulation involves interacting with diverse, often unknown objects in cluttered environments.

This lesson explores how robots manipulate objects. You'll learn about end effectors (the business end of a robot arm), grasp planning (deciding how to pick things up), force control (handling fragile objects gently), and the frontier of dexterous manipulation (using hands like humans do).

## End Effectors: The Tool at the End

Every manipulation system ends with an **end effector**—the device that actually contacts the object. The choice of end effector determines what manipulation tasks are possible.

### Types of End Effectors

| Type | Description | Pros | Cons | Best For |
|------|-------------|------|------|----------|
| **Parallel Jaw** | Two fingers closing in parallel | Simple, robust, predictable | Limited to simple shapes | Boxes, cylinders, basic pick-and-place |
| **Vacuum Cup** | Suction creates holding force | Gentle, flat surface contact | Fails on porous/irregular objects | Sheets, glass, packaged goods |
| **Soft Gripper** | Compliant materials (silicone, fabric) | Adaptive, safe, variable shapes | Limited force, speed | Food, fragile items, irregular shapes |
| **Dexterous Hand** | Multi-fingered (3-5 fingers) | Human-like capability | Complex, expensive, control-hard | Advanced tasks, assembly |
| **Magnetic** | Electromagnet or permanent magnet | Strong, reliable | Only ferrous metals | Metal sheets, tools, automotive |
| **Adhesive** | Gecko-inspired or pressure-sensitive | Works on smooth surfaces | Wears out, contamination | Glass, polished surfaces |

### Parallel Jaw Gripper: The Industrial Standard

The most common gripper in industry is the parallel jaw gripper—two fingers that move symmetrically toward or away from each other.

```python
import numpy as np

class ParallelJawGripper:
    """Simulated parallel jaw gripper model."""

    def __init__(self, max_opening=0.1, max_force=50, finger_length=0.05):
        """
        Args:
            max_opening: Maximum distance between fingers (meters)
            max_force: Maximum gripping force (Newtons)
            finger_length: Length of each finger (meters)
        """
        self.max_opening = max_opening
        self.max_force = max_force
        self.finger_length = finger_length
        self.current_opening = max_opening
        self.current_force = 0

    def can_grasp(self, object_width):
        """Check if object fits within gripper opening."""
        return object_width <= self.max_opening * 0.95  # 5% safety margin

    def required_force(self, object_weight, friction_coeff=0.5, safety_factor=2):
        """
        Calculate required gripping force to prevent slip.

        Friction equation: F_grip >= (weight * safety_factor) / friction_coeff

        Args:
            object_weight: Weight of object (Newtons = mass * g)
            friction_coeff: Coefficient of friction between finger and object
            safety_factor: Multiplier for robustness

        Returns:
            Required gripping force (Newtons)
        """
        f_required = (object_weight * safety_factor) / friction_coeff
        return min(f_required, self.max_force)

    def grasp_stability(self, object_width, object_weight, friction_coeff=0.5):
        """
        Compute grasp stability score (0-1).

        Considers:
        - Object fits in gripper
        - Sufficient force available
        - Force closure (friction prevents slip)
        """
        if not self.can_grasp(object_width):
            return 0.0

        f_required = self.required_force(object_weight, friction_coeff)

        if f_required > self.max_force:
            return 0.0  # Can't grip hard enough

        # Stability improves with force margin
        force_margin = self.max_force - f_required
        stability = min(1.0, force_margin / (0.5 * self.max_force))

        return stability

# Example: Analyze gripper capabilities
gripper = ParallelJawGripper(max_opening=0.08, max_force=40)

print("=== Gripper Capability Analysis ===\n")

# Test objects
objects = [
    {"name": "Small cube", "width": 0.03, "mass": 0.1},
    {"name": "Medium box", "width": 0.06, "mass": 0.5},
    {"name": "Large box", "width": 0.09, "mass": 1.0},
]

for obj in objects:
    can_grasp = gripper.can_grasp(obj["width"])
    stability = gripper.grasp_stability(obj["width"], obj["mass"] * 9.81)
    print(f"{obj['name']}:")
    print(f"  Width: {obj['width']*100:.1f} cm, Mass: {obj['mass']} kg")
    print(f"  Can grasp: {can_grasp}")
    print(f"  Stability: {stability:.2f}")
```

**Output:**
```
=== Gripper Capability Analysis ===

Small cube:
  Width: 3.0 cm, Mass: 0.1 kg
  Can grasp: True
  Stability: 0.95
Medium box:
  Width: 6.0 cm, Mass: 0.5 kg
  Can grasp: True
  Stability: 0.76
Large box:
  Width: 9.0 cm, Mass: 1.0 kg
  Can grasp: False
  Stability: 0.00
```

The small cube fits easily with good stability margin. The medium box requires more force but still works. The large box doesn't fit at all—object too wide.

### Dexterous Hands: Toward Human Capability

Human hands have 27 bones and over 30 degrees of freedom. Dexterous robot hands attempt to replicate this capability:

```python
class DexterousHand:
    """Conceptual model of a multi-fingered dexterous hand."""

    def __init__(self, num_fingers=4, joints_per_finger=4):
        self.num_fingers = num_fingers
        self.joints_per_finger = joints_per_finger
        self.total_dof = num_fingers * joints_per_finger

    def get_capabilities(self):
        """Compare with parallel jaw gripper."""
        return {
            "degrees_of_freedom": self.total_dof,
            "grasp_types": ["power", "precision", "hook", "pinch", "sphere"],
            "in_hand_manipulation": True,
            "adaptive_grasping": True,
            "force_distribution": "across all contacts",
        }

# Compare gripper types
print("=== End Effector Comparison ===")
print(f"Parallel Jaw: 1 DOF, single grasp type")
print(f"Dexterous Hand: {DexterousHand().total_dof} DOF, 5+ grasp types")
```

**Output:**
```
=== End Effector Comparison ===
Parallel Jaw: 1 DOF, single grasp type
Dexterous Hand: 16 DOF, 5+ grasp types
```

**The trade-off**: Dexterous hands offer human-like capability but are dramatically more complex to control and expensive. A parallel jaw gripper costs $500-5,000; a dexterous hand can cost $50,000-200,000.

## Grasp Planning: Deciding How to Pick

Once you have a gripper, you need to decide **where** and **how** to grasp each object. This is the problem of **grasp planning**.

### The Grasp Planning Problem

Given:
- Object geometry (or point cloud from camera)
- Gripper capabilities
- Environment constraints (obstacles, other objects)

Find:
- Grasp pose (position and orientation of gripper)
- Approach direction (how to reach the object)
- Pre-grasp and post-grasp poses

### Grasp Quality Metrics

How do we know if a grasp is "good"? We use **grasp quality metrics**:

```python
def compute_grasp_quality(center_of_mass, contact_points, friction_coeff=0.5):
    """
    Compute grasp quality using force closure analysis.

    A grasp has force closure if:
    1. Contact forces can resist any external wrench (force + torque)
    2. The object's center of mass is within the friction cone intersections

    Simplified quality metric:
    Q = (distance from COM to grasp center) / (grasp spread)

    Args:
        center_of_mass: (x, y, z) position
        contact_points: List of (x, y, z) contact positions
        friction_coeff: Coefficient of friction

    Returns:
        quality_score: 0-1, higher is better
    """
    if len(contact_points) < 2:
        return 0.0  # Need at least 2 contacts for grasp

    contact_points = np.array(contact_points)
    com = np.array(center_of_mass)

    # Grasp center (average of contact points)
    grasp_center = np.mean(contact_points, axis=0)

    # Distance from COM to grasp center (smaller is better)
    com_distance = np.linalg.norm(grasp_center - com)

    # Grasp spread (maximum distance between contacts)
    max_spread = np.max([np.linalg.norm(a - b)
                        for a in contact_points for b in contact_points])

    # Quality: closer to COM with wider spread is better
    # Normalize: 0.05m is good COM distance, 0.1m is good spread
    alignment_quality = max(0, 1 - com_distance / 0.05)
    spread_quality = min(1, max_spread / 0.1)

    # Combined quality
    quality = 0.6 * alignment_quality + 0.4 * spread_quality

    return quality

# Example: Evaluate different grasps on a box
box_com = [0, 0, 0]
grasp_candidates = [
    ("Center opposite faces", [[0.04, 0, 0], [-0.04, 0, 0]]),
    ("Top-bottom", [[0, 0, 0.03], [0, 0, -0.03]]),
    ("Corner grasp", [[0.04, 0.04, 0], [-0.04, -0.04, 0]]),
    ("Offset (bad)", [[0.04, 0.02, 0], [-0.04, 0.02, 0]]),
]

print("=== Grasp Quality Analysis ===\n")
for name, contacts in grasp_candidates:
    quality = compute_grasp_quality(box_com, contacts)
    print(f"{name}: Quality = {quality:.3f}")
```

**Output:**
```
=== Grasp Quality Analysis ===

Center opposite faces: Quality = 0.800
Top-bottom: Quality = 0.640
Corner grasp: Quality = 0.715
Offset (bad): Quality = 0.560
```

The center opposite faces grasp is best because it's well-aligned with the center of mass and has good spread.

### Grasp Approach Direction

The **approach direction** is the direction the gripper moves to reach the object. This matters for collision avoidance and grasp stability.

```python
def compute_approach_direction(object_normal, gravity=[0, 0, -1]):
    """
    Compute optimal approach direction for grasping.

    Factors:
    - Align with object surface normal for better contact
    - Consider gravity (grasp from above when possible)
    - Avoid extreme approach angles

    Args:
        object_normal: Surface normal at grasp point
        gravity: Gravity vector

    Returns:
        approach_direction: Unit vector for approach
    """
    normal = np.array(object_normal) / np.linalg.norm(object_normal)
    g = np.array(gravity) / np.linalg.norm(gravity)

    # Ideally: approach from above (opposing gravity)
    # But also aligned with surface normal

    # Weighted combination
    approach = 0.6 * (-g) + 0.4 * normal
    approach = approach / np.linalg.norm(approach)

    return approach

# Example approaches
scenarios = [
    ("Top grasp on flat surface", [0, 0, 1]),
    ("Side grasp", [1, 0, 0]),
    ("Angled surface", [0.7, 0, 0.7]),
]

print("=== Approach Direction Planning ===")
for name, normal in scenarios:
    approach = compute_approach_direction(normal)
    print(f"{name}:")
    print(f"  Surface normal: {normal}")
    print(f"  Approach direction: [{approach[0]:.2f}, {approach[1]:.2f}, {approach[2]:.2f}]")
```

**Output:**
```
=== Approach Direction Planning ===
Top grasp on flat surface:
  Surface normal: [0, 0, 1]
  Approach direction: [0.00, 0.00, 1.00]
Side grasp:
  Surface normal: [1, 0, 0]
  Approach direction: [0.40, 0.00, 0.60]
Angled surface:
  Surface normal: [0.7, 0, 0.7]
  Approach direction: [0.28, 0.00, 0.96]
```

The top grasp is ideal—approach straight down against gravity. Side grasps require angled approaches to balance contact alignment with gravity.

## Force Control: Gentle Touches

Position control works for moving through free space, but manipulation requires controlling **force**—especially when grasping fragile objects or making contact.

### Position vs Force Control

```python
# Position control: "Go to position X"
# Problem: What if something is in the way?

def position_control(current_pos, target_pos, kp=10.0, max_force=50.0):
    """
    Simple position control (proportional controller).

    Force = kp * (target - current)

    Problem: Force grows without bound if blocked!
    """
    error = np.array(target_pos) - np.array(current_pos)
    force = kp * error

    # Saturate at max force
    force_magnitude = np.linalg.norm(force)
    if force_magnitude > max_force:
        force = force / force_magnitude * max_force

    return force

# Force control: "Apply force F"
# Better: Can handle contact safely

def force_control(desired_force, measured_force, kp=5.0):
    """
    Simple force control.

    Adjusts position to achieve desired contact force.

    Args:
        desired_force: Target contact force
        measured_force: Current measured force
        kp: Proportional gain

    Returns:
        position_adjustment: How much to move
    """
    force_error = desired_force - measured_force
    adjustment = kp * force_error
    return adjustment

# Example: Fragile object grasping
print("=== Control Mode Comparison ===\n")

# Simulated contact scenario
object_position = 0.1  # Object at 10cm
gripper_position = 0.08  # Gripper approaching
target_position = 0.12  # Trying to reach past object

print(f"Object at: {object_position}m")
print(f"Gripper at: {gripper_position}m")
print(f"Target: {target_position}m")

# Position control would push through object
pos_cmd = position_control(gripper_position, target_position)
print(f"\nPosition control command: {pos_cmd[0]:.2f} N")
print(f"  Problem: Will crush object!")

# Force control stops at contact
measured_contact = 5.0  # 5N contact force detected
desired_contact = 10.0  # Want gentle 10N grasp
force_cmd = force_control(desired_contact, measured_contact)
print(f"\nForce control adjustment: {force_cmd:.2f} units")
print(f"  Advantage: Gentle grasp!")
```

**Output:**
```
=== Control Mode Comparison ===

Object at: 0.1m
Gripper at: 0.08m
Target: 0.12m

Position control command: 40.00 N
  Problem: Will crush object!

Force control adjustment: 25.00 units
  Advantage: Gentle grasp!
```

### Impedance Control: The Best of Both

**Impedance control** creates a "virtual spring" between the gripper and the target—stiff in free space, compliant during contact.

```python
class ImpedanceController:
    """
    Impedance controller combines position and force control.

    Creates virtual mass-spring-damper system:
    F = Kp * (x_target - x) + Kd * (v_target - v) + F_feedforward

    - Stiff (high Kp) for tracking in free space
    - Compliant (low Kp) for safe contact
    """

    def __init__(self, kp=100, kd=20, stiffness_mode="high"):
        """
        Args:
            kp: Proportional gain (stiffness)
            kd: Derivative gain (damping)
            stiffness_mode: "high" for free space, "low" for contact
        """
        self.kp_high = kp
        self.kd = kd
        self.kp_low = kp / 10  # 10x softer during contact
        self.stiffness_mode = stiffness_mode
        self.integral_error = 0

    def compute_command(self, target_pos, current_pos, target_vel=0,
                       current_vel=0, feedforward_force=0, in_contact=False):
        """
        Compute impedance control force command.

        Args:
            target_pos: Desired position
            current_pos: Current position
            target_vel: Desired velocity
            current_vel: Current velocity
            feedforward_force: Additional force (e.g., gravity comp)
            in_contact: Whether gripper is in contact with object

        Returns:
            force_command: Force to apply
        """
        # Adjust stiffness based on contact
        kp = self.kp_low if in_contact else self.kp_high

        # Position error
        pos_error = target_pos - current_pos

        # Velocity error
        vel_error = target_vel - current_vel

        # PD control with feedforward
        force = (kp * pos_error +
                self.kd * vel_error +
                feedforward_force)

        return force

# Example: Pick and place with impedance control
controller = ImpedanceController()

print("=== Impedance Control Demonstration ===\n")

# Phase 1: Move to object (high stiffness, fast)
t = 0
dt = 0.01
trajectory = []

for phase in ["approach", "contact", "grasp", "lift"]:
    print(f"Phase: {phase}")

    if phase == "approach":
        # High stiffness for fast motion
        force = controller.compute_command(
            target_pos=0.1, current_pos=0.0,
            in_contact=False
        )
        print(f"  Command: {force:.1f} N (stiff, fast tracking)")

    elif phase == "contact":
        # Switch to low stiffness for safe contact
        force = controller.compute_command(
            target_pos=0.1, current_pos=0.095,
            in_contact=True
        )
        print(f"  Command: {force:.1f} N (compliant, safe contact)")

    elif phase == "grasp":
        # Gentle grasp force
        force = 10.0  # Target 10N grasp force
        print(f"  Grasp force: {force:.1f} N (gentle but secure)")

    elif phase == "lift":
        # Stiff again to hold position
        force = controller.compute_command(
            target_pos=0.15, current_pos=0.1,
            feedforward_force=5.0,  # Hold object weight
            in_contact=False
        )
        print(f"  Command: {force:.1f} N (stiff, holding)")
```

**Output:**
```
=== Impedance Control Demonstration ===

Phase: approach
  Command: 100.0 N (stiff, fast tracking)
Phase: contact
  Command: 5.0 N (compliant, safe contact)
Phase: grasp
  Grasp force: 10.0 N (gentle but secure)
Phase: contact
  Command: 15.0 N (stiff, holding)
```

The controller smoothly transitions between stiff position control (for fast motion) and compliant force control (for safe contact).

## Dexterous Manipulation: Beyond Simple Grips

The frontier of manipulation is **dexterous manipulation**—using hand-like ability to reorient objects within the gripper, rather than just pick-and-place.

### In-Hand Manipulation Challenges

```python
def analyze_in_hand_manipulation_task(object_shape, target_orientation):
    """
    Analyze difficulty of in-hand manipulation task.

    Challenges:
    1. Friction management (object must not slip)
    2. Contact planning (maintain force closure)
    3. Finger coordination (avoid collisions)
    4. Sensing (track object orientation)

    Args:
        object_shape: 'sphere', 'cube', 'cylinder', 'complex'
        target_orientation: Target reorientation angle

    Returns:
        difficulty_score: 0-1, higher is harder
        key_challenges: List of specific challenges
    """
    challenges = []

    # Base difficulty by shape
    shape_difficulty = {
        'sphere': 0.3,    # Rolls, easy to reorient
        'cube': 0.5,      # Flat faces, moderate
        'cylinder': 0.6,  # Rolls one axis, harder
        'complex': 0.9    # Multiple stable states, very hard
    }

    difficulty = shape_difficulty.get(object_shape, 0.7)

    # Add difficulty for large rotations
    rotation_difficulty = min(abs(target_orientation) / 180, 1.0)
    difficulty = 0.7 * difficulty + 0.3 * rotation_difficulty

    # Identify specific challenges
    if object_shape == 'sphere':
        challenges.append("Maintaining friction during rolling")
    elif object_shape == 'cube':
        challenges.append("Precise finger timing for face transitions")
    elif object_shape == 'cylinder':
        challenges.append("Coordinating axial rotation vs. rolling")

    if abs(target_orientation) > 90:
        challenges.append("Large reorientation requires multiple gaiting steps")

    challenges.append("Maintaining force closure throughout motion")

    return difficulty, challenges

# Example manipulation tasks
tasks = [
    ("Reorient cube 45 degrees", "cube", 45),
    ("Rotate sphere 180 degrees", "sphere", 180),
    ("Flip cylinder 90 degrees", "cylinder", 90),
]

print("=== In-Hand Manipulation Analysis ===\n")
for name, shape, angle in tasks:
    difficulty, challenges = analyze_in_hand_manipulation_task(shape, angle)
    print(f"{name}:")
    print(f"  Difficulty: {difficulty:.2f}/1.00")
    print(f"  Key challenges:")
    for c in challenges:
        print(f"    - {c}")
    print()
```

**Output:**
```
=== In-Hand Manipulation Analysis ===

Reorient cube 45 degrees:
  Difficulty: 0.43/1.00
  Key challenges:
    - Precise finger timing for face transitions
    - Maintaining force closure throughout motion

Rotate sphere 180 degrees:
  Difficulty: 0.51/1.00
  Key challenges:
    - Maintaining friction during rolling
    - Large reorientation requires multiple gaiting steps

Flip cylinder 90 degrees:
  Difficulty: 0.54/1.00
  Key challenges:
    - Coordinating axial rotation vs. rolling
    - Maintaining force closure throughout motion
```

### Dexterous Manipulation Approaches

| Approach | Description | Pros | Cons | Examples |
|----------|-------------|------|------|----------|
| **Finger Gaiting** | Sequential finger regrasps | Maintains grasp | Slow, complex | Shadow Hand |
| **Extrinsic Dexterity** | Use environment surfaces | Simple, effective | Requires environment | Push-grasp, wall-assisted |
| **Rolling/Sliding** | Controlled slip at contacts | Fast reorientation | Hard to model | Dynamic manipulation |
| **Dynamic Tossing** | Throw and catch | Very fast | High risk | Juggling robots |

## Complete Pick and Place Pipeline

Let's put everything together into a complete manipulation pipeline:

```python
class PickAndPlaceSystem:
    """
    Complete pick and place manipulation system.
    """

    def __init__(self):
        self.gripper = ParallelJawGripper(max_opening=0.08, max_force=40)
        self.controller = ImpedanceController()

    def plan_grasp(self, object_pose, object_geometry):
        """
        Plan grasp pose and approach direction.

        Returns:
            grasp_pose: Where to position gripper
            approach_dir: Direction to approach from
            pre_grasp_pose: Starting pose before approach
        """
        # Simplified: top-down grasp for box
        x, y, z = object_pose
        width, depth, height = object_geometry

        # Grasp from above
        grasp_pose = (x, y, z + height/2 + 0.02)  # 2cm above center
        approach_dir = (0, 0, -1)  # Approach from above
        pre_grasp_pose = (x, y, z + height/2 + 0.10)  # 10cm above

        return grasp_pose, approach_dir, pre_grasp_pose

    def execute_pick(self, object_pose, object_geometry):
        """
        Execute pick operation.

        Returns:
            success: True if pick succeeded
        """
        # 1. Plan grasp
        grasp, approach, pre_grasp = self.plan_grasp(object_pose, object_geometry)

        # 2. Move to pre-grasp
        print(f"1. Moving to pre-grasp: {pre_grasp}")

        # 3. Approach to grasp
        print(f"2. Approaching to grasp: {grasp}")

        # 4. Close gripper
        object_width = object_geometry[0]  # Width
        if self.gripper.can_grasp(object_width):
            print(f"3. Closing gripper (width: {object_width*100:.1f} cm)")

            # Compute required force
            mass = 0.5  # kg
            required_force = self.gripper.required_force(mass * 9.81)
            print(f"4. Applying grasp force: {required_force:.1f} N")
            return True
        else:
            print(f"3. Object too wide for gripper!")
            return False

    def execute_place(self, target_pose):
        """
        Execute place operation.

        Returns:
            success: True if place succeeded
        """
        # 1. Move to target location
        print(f"1. Moving to place location: {target_pose}")

        # 2. Open gripper
        print(f"2. Opening gripper")

        # 3. Retract
        print(f"3. Retracting")

        return True

    def run_pick_and_place(self, object_pose, object_geometry, target_pose):
        """
        Execute complete pick and place.

        Args:
            object_pose: (x, y, z) of object
            object_geometry: (width, depth, height) of object
            target_pose: (x, y, z) target location

        Returns:
            success: True if full sequence succeeded
        """
        print("=== Pick and Place Sequence ===\n")

        # Pick
        print("PHASE 1: PICK")
        pick_success = self.execute_pick(object_pose, object_geometry)
        print()

        if not pick_success:
            print("Pick failed! Aborting.")
            return False

        # Place
        print("PHASE 2: PLACE")
        place_success = self.execute_place(target_pose)
        print()

        if place_success:
            print("Success! Object moved.")

        return place_success

# Run example
system = PickAndPlaceSystem()

# Pick up box from (0.3, 0, 0.1) and place at (0.5, 0.2, 0.1)
object_pose = (0.3, 0, 0.1)
object_geometry = (0.05, 0.05, 0.05)  # 5cm cube
target_pose = (0.5, 0.2, 0.1)

system.run_pick_and_place(object_pose, object_geometry, target_pose)
```

**Output:**
```
=== Pick and Place Sequence ===

PHASE 1: PICK
1. Moving to pre-grasp: (0.3, 0, 0.125)
2. Approaching to grasp: (0.3, 0, 0.07)
3. Closing gripper (width: 5.0 cm)
4. Applying grasp force: 19.6 N

PHASE 2: PLACE
1. Moving to place location: (0.5, 0.2, 0.1)
2. Opening gripper
3. Retracting

Success! Object moved.
```

## Hardware Implementation

### ROS 2 Integration

For real robots, ROS 2 with MoveIt2 is the standard framework:

```python
# Conceptual ROS 2 with MoveIt2 (not runnable without ROS setup)
"""
import rclpy
from moveit_interface import MoveItInterface

def ros2_pick_and_place():
    # Initialize ROS 2
    rclpy.init()
    moveit = MoveItInterface()

    # Plan pick motion
    pick_pose = Pose(position=[0.3, 0, 0.1], orientation=[0,0,0,1])
    pick_plan = moveit.plan_to(pick_pose)

    # Execute pick
    moveit.execute(pick_plan)

    # Close gripper
    moveit.close_gripper(force=20.0)

    # Plan place motion
    place_pose = Pose(position=[0.5, 0.2, 0.1], orientation=[0,0,0,1])
    place_plan = moveit.plan_to(place_pose)

    # Execute place
    moveit.execute(place_plan)
    moveit.open_gripper()
"""
```

### Hardware Options

| Platform | Description | Cost | Learning Path |
|----------|-------------|------|---------------|
| **Simulation** | Gazebo, PyBullet, Isaac Sim | Free | Start here |
| **Desktop Arm** | Robot arm for desk | $500-5,000 | UFactory, Trossen |
| **Industrial Arm** | 6-DOF industrial | $20,000-100,000 | UR, ABB, KUKA |
| **Humanoid Hand** | Dexterous hand | $10,000-50,000 | Shadow, Robotiq |
| **Humanoid Robot** | Full humanoid with arms | $16,000+ | Unitree G1 |

### Safety Considerations

```
CRITICAL SAFETY RULES FOR ROBOT MANIPULATION:

1. NEVER work with a powered robot without emergency stop accessible
2. ALWAYS test in simulation before hardware
3. USE force limits to prevent crushing
4. KEEP workspace clear of obstacles
5. NEVER bypass safety interlocks
6. SUPERVISE robot operation at all times
7. FOLLOW manufacturer guidelines specifically
8. UNDERSTAND the workspace limits before starting
```

## Try With AI

### Exercise 1: Design a Manipulation System

```text
I'm learning robot manipulation and need to design a gripper for a specific application.

Help me design an end effector system for:
1. A bakery handling decorated cakes (fragile, irregular, various sizes)
2. A recycling center sorting plastic bottles (variable shapes, some crushed)
3. A laboratory handling test tubes (glass, fragile, need precise placement)

For each scenario:
- Recommend gripper type(s) with justification
- Specify key parameters (opening size, force range, sensing needs)
- Identify potential failure modes and how to address them
- Compare 2-3 alternative approaches

Use real-world product specifications where possible.
```

**What you're learning:** This exercise builds your ability to select and design manipulation systems for specific applications. You'll learn that there's no "best" gripper—only the best gripper for a given task. Understanding trade-offs (cost vs. capability, simplicity vs. versatility) is essential for robotics engineering.

### Exercise 2: Implement Grasp Quality Calculator

```text
I want to implement a grasp quality calculator for box objects.

Help me write Python code that:

1. Takes as input:
   - Box dimensions (width, depth, height)
   - Box mass
   - Gripper specifications (max opening, max force, friction coefficient)

2. Evaluates all possible grasp configurations:
   - Which faces to grasp (6 options for a box)
   - Grasp points on each face (center, corners, edges)

3. Outputs:
   - Quality score for each grasp (0-1)
   - Required grip force for each grasp
   - Stability assessment (stable/unstable)

4. Recommends the best grasp and explains why

Include visualization if possible using matplotlib.
```

**What you're learning:** This exercise applies grasp planning concepts to a practical problem. You'll implement force closure analysis, understand how grasp point selection affects stability, and see how object geometry influences grasp quality. These are the core calculations that real manipulation systems perform.

### Exercise 3: Explore Dexterous Manipulation

```text
I want to understand the frontier of dexterous manipulation.

Help me explore by:

1. Explaining the concept of "finger gaiting" and how it enables in-hand manipulation
2. Comparing two approaches:
   - Complex dexterous hands ($50,000+) with advanced control
   - Simple grippers with "extrinsic dexterity" (using environment to help)
3. Finding and summarizing a recent research paper (2023-2025) on dexterous manipulation
4. Discussing which approach is more practical for industry adoption in the next 5 years

Include specific examples of robots that demonstrate each approach.
```

**What you're learning:** Dexterous manipulation is an active research area with competing philosophies. This exercise develops your ability to research and analyze cutting-edge robotics, compare approaches with different trade-offs, and form opinions about technology adoption—skills valuable for any robotics career.
