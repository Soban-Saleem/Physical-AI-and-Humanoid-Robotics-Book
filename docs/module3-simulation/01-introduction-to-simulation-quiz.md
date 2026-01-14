---
sidebar_position: 2
title: "Lesson 1.1: Simulation Quiz"
description: "Assessment for Introduction to Robot Simulation lesson"
keywords: ["Quiz", "Assessment", "Simulation", "Gazebo"]
chapter: 3
lesson: 1
assessment_type: "quiz"
duration_minutes: 20
total_points: 50
passing_score: 35
---

# Lesson 1.1: Introduction to Robot Simulation - Quiz

**Instructions**: Answer all questions below. This quiz tests your understanding of robot simulation concepts, physics engine components, and basic Gazebo usage.

---

## Learning Objectives Assessed

- **LO-SIM-001**: Explain the role of simulation in robotics development and list at least three benefits over physical testing
- **LO-SIM-002**: Identify the core components of a physics simulation engine (collision detection, dynamics, sensors)
- **LO-SIM-003**: Launch Gazebo simulator, navigate the 3D environment, and insert a simple model

---

## Cognitive Distribution

- **Remember/Understand**: 40% (20 points) - Conceptual understanding
- **Apply**: 60% (30 points) - Practical application

---

## Part 1: Multiple Choice Questions (20 points)

### Question 1 (4 points) [Type: MCQ] [Bloom: Understand]

**What is a "digital twin" in robotics?**

A) A physical robot that looks exactly like another robot

B) A virtual replica of a physical system used for testing code before deployment

C) A backup copy of robot software stored in the cloud

D) A second physical robot used for redundancy

**Correct Answer**: B

**Explanation**:
- **B is correct**: A digital twin is a virtual replica that matches your real robot's dimensions, sensors, and capabilities. You develop and test against the twin, then deploy working code to the real robot.
- **A is incorrect**: This describes a physical duplicate, not a simulation. A digital twin exists in software, not hardware.
- **C is incorrect**: This describes software backup/storage, not a simulation environment for testing.
- **D is incorrect**: This describes hardware redundancy for reliability, not a simulation for development.

**Distractor Analysis**:
- A tests: Understanding of "digital" vs. physical concepts
- C tests: Confusion between backup storage and simulation
- D tests: Confusion between redundancy and testing environments

**Source**: Lesson 1: The Digital Twin Approach

---

### Question 2 (4 points) [Type: MCQ] [Bloom: Understand]

**Which benefit of simulation is described: "Tests run exactly the same way every time, with no variations in weather, lighting, or surface conditions"?**

A) Cost

B) Reproducibility

C) Safety

D) Speed

**Correct Answer**: B

**Explanation**:
- **B is correct**: Reproducibility means exact same conditions every time. In simulation, you can repeat tests identically, which is impossible in the real world where conditions always vary.
- **A is incorrect**: Cost refers to virtual testing being free compared to hardware testing costs.
- **C is incorrect**: Safety refers to simulated robots being unable to cause damage or injury.
- **D is incorrect**: Speed refers to running tests in parallel and accelerating time faster than reality.

**Distractor Analysis**:
- A tests: Recognizing cost benefits vs. consistency benefits
- C tests: Distinguishing safety from repeatability
- D tests: Distinguishing performance from consistency

**Source**: Lesson 1: Benefits of Simulation

---

### Question 3 (4 points) [Type: MCQ] [Bloom: Remember]

**In the physics simulation pipeline, what component is responsible for detecting when objects overlap and calculating where they touched?**

A) Dynamics Simulation

B) Joint Simulation

C) Collision Detection

D) Sensor Simulation

**Correct Answer**: C

**Explanation**:
- **C is correct**: Collision detection tracks every object's shape and position. When objects overlap, it detects the collision and calculates contact point and angle.
- **A is incorrect**: Dynamics calculates forces (mass, friction, acceleration) AFTER collision is detected.
- **B is incorrect**: Joint simulation handles robot joint limits and motors, not object-object contact.
- **D is incorrect**: Sensor simulation generates virtual sensor data (camera images, LIDAR readings), not collision information.

**Distractor Analysis**:
- A tests: Confusion between detecting collision and calculating forces from collision
- B tests: Confusion between joint mechanics and object contact
- D tests: Confusion between sensing and collision detection

**Source**: Lesson 1: Core Components - Collision Detection

---

### Question 4 (4 points) [Type: MCQ] [Bloom: Understand]

**A robot gripper applies 5N of force to hold a 200g cup with a friction coefficient of 0.5. The physics engine calculates whether the cup slips or is held. Which component performs this calculation?**

A) Collision Detection

B) Dynamics Simulation

C) Sensor Simulation

D) Joint Simulation

**Correct Answer**: B

**Explanation**:
- **B is correct**: Dynamics simulation calculates forces after collision is detected. It considers object mass, friction coefficients, and applied forces to determine motion (including whether an object slips).
- **A is incorrect**: Collision detection only identifies that contact occurred, not forces involved.
- **C is incorrect**: Sensor simulation generates sensor readings, not force calculations.
- **D is incorrect**: Joint simulation handles robot joint mechanics, not object grip physics.

**Distractor Analysis**:
- A tests: Understanding the scope of collision detection vs. force calculation
- C tests: Confusion between sensing and physics
- D tests: Confusion about what joint simulation handles

**Source**: Lesson 1: Core Components - Dynamics Simulation

---

### Question 5 (4 points) [Type: MCQ] [Bloom: Understand]

**When comparing simulation to reality, which aspect does simulation typically handle LESS accurately?**

A) Kinematics (motion geometry)

B) Logic (code behavior)

C) Sensor noise

D) Algorithms (path planning)

**Correct Answer**: C

**Explanation**:
- **C is correct**: Simulation sensors are often too perfect. Real sensors have noise, drift, and variations that simulation may not fully capture.
- **A is incorrect**: Kinematics are perfect within numerical precision in simulation (motion geometry follows mathematical models exactly).
- **B is incorrect**: Logic is identical because the same code runs in both simulation and reality.
- **D is incorrect**: Algorithms behave the same way in both environments because they're deterministic computations.

**Distractor Analysis**:
- A tests: Understanding what simulation models perfectly
- B tests: Recognizing that code behavior is consistent across environments
- D tests: Understanding algorithmic determinism

**Source**: Lesson 1: Simulation vs Reality: The Gap

---

## Part 2: Matching Exercise (10 points)

### Question 6 (10 points) [Type: Matching] [Bloom: Remember]

**Match each physics engine component to its primary function.**

| Component | Letter | Function |
|-----------|--------|----------|
| Collision Detection | | A. Calculates forces, acceleration, momentum based on mass and friction |
| Dynamics Simulation | | B. Renders 3D scene to 2D images like a real camera |
| Joint Simulation | | C. Detects when objects overlap and calculates contact point/angle |
| Sensor Simulation (Camera) | | D. Respects joint angle limits and motor constraints |
| Sensor Simulation (LIDAR) | | E. Casts virtual laser rays and returns distance measurements |

**Correct Answer**:
- Collision Detection: C
- Dynamics Simulation: A
- Joint Simulation: D
- Sensor Simulation (Camera): B
- Sensor Simulation (LIDAR): E

**Scoring**: 2 points per correct match

**Distractor Analysis**:
- Students may confuse collision detection with dynamics (detecting vs. calculating forces)
- Students may confuse camera vs. LIDAR sensor functions (visual vs. distance)
- Students may not understand joint simulation is separate from dynamics

**Source**: Lesson 1: Core Components

---

## Part 3: Short Answer Questions (10 points)

### Question 7 (5 points) [Type: Short Answer] [Bloom: Understand]

**List three benefits of using robot simulation over physical testing. For each benefit, briefly explain why it matters for robotics development.**

**Rubric** (5 points total):

| Criteria | Excellent (5 pts) | Good (3-4 pts) | Fair (1-2 pts) | Poor (0 pts) |
|----------|-------------------|----------------|----------------|--------------|
| Completeness | Lists 3 distinct benefits with clear explanations | Lists 3 benefits with adequate explanations | Lists 1-2 benefits or incomplete explanations | No valid benefits listed |

**Example Excellent Answer**:
1. **Cost**: Virtual testing is free. Physical testing requires robot hardware, replacement parts, and energy.
2. **Safety**: Simulated robots can't damage property or injure people during testing failures.
3. **Speed**: Multiple tests can run in parallel and time can be accelerated faster than reality.

**Diagnostic Indicators**:
- IF lists fewer than 3 benefits → Recall gap → Review "Benefits of Simulation" table
- IF lists benefits without explanation → Understanding gap → Review lesson explanations of why each benefit matters
- IF confuses benefit categories (e.g., lists "accuracy" as benefit) → Concept gap → Review simulation limitations section

**Source**: Lesson 1: Benefits of Simulation

---

### Question 8 (5 points) [Type: Short Answer] [Bloom: Understand]

**Explain the perception-decision-action loop in robot simulation. Describe what happens at each stage.**

**Rubric** (5 points total):

| Criteria | Excellent (5 pts) | Good (3-4 pts) | Fair (1-2 pts) | Poor (0 pts) |
|----------|-------------------|----------------|----------------|--------------|
| Accuracy | Correctly describes all 3 stages with specific examples | Describes all 3 stages with some detail | Describes 1-2 stages or missing key details | Missing or incorrect |
| Clarity | Clear explanation with proper terminology | Generally clear with minor issues | Unclear or confusing | No coherent explanation |

**Example Excellent Answer**:
The perception-decision-action loop is the continuous cycle that controls robot behavior:
1. **Perception (Sensors)**: Virtual sensors (cameras, LIDAR, IMU) read the simulated environment and provide data to the robot's control system.
2. **Decision (Your Code)**: ROS 2 nodes process the sensor data and plan what actions to take (e.g., path planning, obstacle avoidance).
3. **Action (Actuation)**: Motor commands are sent to the physics engine, which updates the robot's position and state based on forces and physics.
The loop then repeats continuously.

**Diagnostic Indicators**:
- IF missing perception stage → Concept gap in sensor simulation
- IF missing decision stage → Concept gap in control software role
- IF missing action stage → Concept gap in physics engine actuation
- IF describes stages but not the loop → Understanding gap in closed-loop control concept

**Source**: Lesson 1: The Physics Pipeline

---

## Part 4: Hands-On Exercise (10 points)

### Question 9 (10 points) [Type: Hands-On] [Bloom: Apply]

**Launch Gazebo simulator and complete the following tasks. Document your work with screenshots.**

**Tasks**:
1. Launch Gazebo with an empty world (2 points)
2. Demonstrate camera navigation: rotate, pan, and zoom (3 points)
3. Insert a simple model (e.g., a table or robot) into the world (3 points)
4. Take a screenshot showing your model in the 3D world (2 points)

**Rubric** (10 points total):

#### Task 1: Launch Gazebo (2 points)

| Criteria | Pass (2 pts) | Partial (1 pt) | Fail (0 pts) |
|----------|--------------|----------------|--------------|
| Gazebo launches successfully with empty world visible | Screenshot shows Gazebo interface with ground plane | Screenshot shows attempted launch but incomplete | No evidence or incorrect interface |

#### Task 2: Camera Navigation (3 points)

| Criteria | Pass (3 pts) | Partial (1-2 pts) | Fail (0 pts) |
|----------|--------------|-------------------|--------------|
| Demonstrates rotate, pan, and zoom | Evidence of all 3 navigation types (screenshots at different angles/positions) | Evidence of 1-2 navigation types | No navigation evidence |

#### Task 3: Insert Model (3 points)

| Criteria | Pass (3 pts) | Partial (1-2 pts) | Fail (0 pts) |
|----------|--------------|-------------------|--------------|
| Model successfully inserted and visible | Screenshot shows model correctly placed in 3D world | Model attempted but not properly placed | No model visible |

#### Task 4: Documentation (2 points)

| Criteria | Pass (2 pts) | Partial (1 pt) | Fail (0 pts) |
|----------|--------------|----------------|--------------|
| Screenshot quality and documentation | Clear screenshot showing completed task with annotation | Screenshot present but unclear or unlabeled | No screenshot provided |

**Hints** (for students who need support):

**Hint 1** (Gentle): Review the "Launching Gazebo" section for the terminal command to start Gazebo with an empty world.

**Hint 2** (Moderate): For camera controls, remember: left-click drag to rotate, middle-click drag (or scroll) to pan, scroll wheel to zoom.

**Hint 3** (Explicit): Use the Insert tab in the left panel to find models. Click and drag a model from the list into the 3D world.

**Diagnostic Indicators**:
- IF Gazebo won't launch → Installation/environment issue → Check ROS 2 and Gazebo installation
- IF can't navigate camera → UI familiarity gap → Practice navigation controls in empty world
- IF can't insert model → UI interaction gap → Review Insert tab usage
- IF model falls through ground → Physics engine issue → Report as environment problem

**Source**: Lesson 1: Launching Gazebo, Basic Navigation, Inserting a Model

---

## Part 5: Application Exercise (10 points)

### Question 10 (10 points) [Type: Scenario] [Bloom: Apply]

**You are developing a delivery robot for a warehouse. You have written code that makes the robot follow a path while avoiding obstacles.**

**Answer the following questions**:

1. **Describe how you would test this code in simulation before deploying to the physical robot.** (5 points)

2. **After the simulation tests pass, what specific things would you validate on the physical robot?** (5 points)

**Rubric** (10 points total):

#### Part 1: Simulation Testing (5 points)

| Criteria | Excellent (5 pts) | Good (3-4 pts) | Fair (1-2 pts) | Poor (0 pts) |
|----------|-------------------|----------------|----------------|--------------|
| Test design | Describes specific test scenarios (obstacles, paths) | General testing approach mentioned | Vague or incomplete testing plan | No valid testing approach |
| Simulation features | References relevant Gazebo features (world setup, sensors) | Some simulation concepts mentioned | No simulation-specific details | No simulation context |

**Example Excellent Answer for Part 1**:
- Create a Gazebo world with warehouse-like environment: shelves, aisles, boxes
- Insert obstacles representing forklifts, people, or dropped items
- Place the robot model with camera and LIDAR sensors
- Run multiple test scenarios: straight paths, corner navigation, obstacle avoidance
- Test edge cases: narrow corridors, blocked paths, sensor failures

#### Part 2: Physical Validation (5 points)

| Criteria | Excellent (5 pts) | Good (3-4 pts) | Fair (1-2 pts) | Poor (0 pts) |
|----------|-------------------|----------------|----------------|--------------|
| Reality gap understanding | Identifies aspects simulation misses (sensor noise, surface variation) | General awareness of differences | Limited understanding | No valid validation points |
| Specific validations | Lists 3+ specific physical tests | Lists 1-2 physical tests | Vague suggestions | No relevant validations |

**Example Excellent Answer for Part 2**:
After simulation tests pass, I would validate on the physical robot:
1. **Sensor accuracy**: Test that real camera and LIDAR detect obstacles at expected distances (simulation sensors are perfect, real ones have noise)
2. **Surface variation**: Test on different floor types (tile vs. concrete vs. carpet) because simulation assumes perfectly flat surfaces
3. **Real-world disturbances**: Test with wind, doors opening, people walking—things simulation can't predict

**Diagnostic Indicators**:
- IF Part 1 lacks specific scenarios → Application gap → Practice designing test cases
- IF Part 1 doesn't mention simulation features → Tool familiarity gap → Review Gazebo capabilities
- IF Part 2 focuses only on "does it work" → Reality gap understanding needed → Review "Simulation vs Reality" section
- IF Part 2 overlaps with Part 1 → Concept confusion between simulation and reality

**Source**: Lesson 1: Benefits of Simulation, Simulation vs Reality: The Gap

---

## Answer Key

### Part 1: Multiple Choice

1. **B** - Digital twin is virtual replica for testing
2. **B** - Reproducibility provides consistent test conditions
3. **C** - Collision Detection detects object overlap
4. **B** - Dynamics Simulation calculates forces
5. **C** - Sensor noise is less accurate in simulation

### Part 2: Matching

6. Collision Detection: C, Dynamics Simulation: A, Joint Simulation: D, Sensor Simulation (Camera): B, Sensor Simulation (LIDAR): E

### Part 3: Short Answer

7. **Three benefits**: Any 3 from [Cost, Safety, Speed, Reproducibility, Debugging, Edge Cases] with explanations

8. **Perception-Decision-Action Loop**:
   - Perception: Sensors read environment
   - Decision: Code processes data and plans actions
   - Action: Motor commands sent to physics engine

### Part 4: Hands-On

9. **Task-based rubric scoring** - see detailed rubric above

### Part 5: Application

10. **Scenario-based evaluation** - see detailed rubric above

---

## Objective Coverage Matrix

| Question | Learning Objective | Bloom's Level | Points |
|----------|-------------------|---------------|--------|
| Q1 | LO-SIM-001 | Understand | 4 |
| Q2 | LO-SIM-001 | Understand | 4 |
| Q3 | LO-SIM-002 | Remember | 4 |
| Q4 | LO-SIM-002 | Understand | 4 |
| Q5 | LO-SIM-001, LO-SIM-002 | Understand | 4 |
| Q6 | LO-SIM-002 | Remember | 10 |
| Q7 | LO-SIM-001 | Understand | 5 |
| Q8 | LO-SIM-002 | Understand | 5 |
| Q9 | LO-SIM-003 | Apply | 10 |
| Q10 | LO-SIM-001, LO-SIM-002 | Apply | 10 |

**Total**: 50 points

---

## Assessment Validation

- [x] All questions align with learning objectives
- [x] Three-way alignment: CEFR A2 + Bloom's levels + Assessment types
- [x] Variety of question types (MCQ, Matching, Short Answer, Hands-On, Scenario)
- [x] 60% non-recall (30 points at Apply level)
- [x] Rubrics provided for all open-ended questions
- [x] Diagnostic indicators identify specific gaps
- [x] Distractor analysis for MCQs
- [x] Clear success criteria for each question

---

**Constitutional alignment**:
- Principle 1 (Validity): Assessments measure target cognitive operations
- Principle 2 (Alignment): CEFR A2 + Bloom's + Type three-way aligned
- Principle 3 (Scaffolding): Formative assessment with appropriate A2 scaffolding
- Principle 4 (Diagnostics): Rubrics provide actionable feedback
- Layer progression: L1 (Manual) - foundational simulation concepts

**Reviewed by**: assessment-architect v1.0.0
**Date**: 2025-01-14
