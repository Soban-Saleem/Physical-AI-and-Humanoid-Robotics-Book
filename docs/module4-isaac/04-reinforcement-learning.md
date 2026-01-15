---
sidebar_position: 4
title: "Reinforcement Learning for Robotics"
description: "Learn reinforcement learning (RL) for robotics using Isaac Lab and Isaac Sim. Covers MDPs, PPO algorithm, reward shaping, observables, actions, and training policies through trial and error."
keywords: ["Reinforcement Learning", "PPO", "Isaac Lab", "MDP", "Reward Shaping", "Robot Learning", "Policy Gradient"]
chapter: 4
lesson: 4
duration_minutes: 120

requirements:
  hardware: "NVIDIA RTX 4080 (16GB VRAM) minimum; RTX 4090 recommended for multi-robot training"
  software: "Isaac Sim 5.1+, Isaac Lab, Python 3.10, Stable-Baselines3 or RSL-RL"

skills:
  - name: "RL Fundamentals for Robotics"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can explain the MDP framework and how RL enables robots to learn through trial and error"

  - name: "Isaac Lab RL Framework"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can configure Isaac Lab RL environments with observables, actions, and rewards"

  - name: "Policy Training with PPO"
    proficiency_level: "B2"
    category: "Applied"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can implement and train a PPO policy for a robotics task using Isaac Lab"

learning_objectives:
  - objective: "Explain the Markov Decision Process (MDP) framework and how it models sequential decision-making for robots"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Short answer explaining states, actions, rewards, and transition probabilities in robotics context"

  - objective: "Implement observables (observations), actions, and reward functions for an Isaac Lab RL task"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Coding exercise: Create custom MDP configuration for a robot task"

  - objective: "Train a policy using PPO (Proximal Policy Optimization) in Isaac Lab and evaluate its performance"
    proficiency_level: "B2"
    bloom_level: "Apply"
    assessment_method: "Lab exercise: Train a policy for a locomotion or manipulation task"

cognitive_load:
  new_concepts: 9
  assessment: "Students will implement a complete RL training pipeline in Isaac Lab, including MDP configuration, reward shaping, and policy training"

differentiation:
  extension_for_advanced: "Implement custom reward shaping with curriculum learning—start with easy tasks and progressively increase difficulty as the policy improves"
  remedial_for_struggling: "Focus on understanding the MDP components first—use the pre-built Isaac Lab examples (e.g., Isaac-Lift-Cube-Franka-IK-AB) before attempting custom tasks"
  hardware_alternatives: "Use Google Colab with Isaac Lab for cloud-based training, or reduce environment complexity (fewer robots, simpler tasks) for lower-end GPUs"

safety_notes: "No physical hardware risks—RL training occurs entirely in simulation. However, trained policies transferred to physical robots require extensive safety validation before deployment."

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Reinforcement Learning for Robotics

Imagine teaching a robot to walk by programming explicit rules: "Lift left leg 30 degrees, lean forward 5 degrees, engage balance algorithm..." Now imagine the robot learns to walk on its own, through thousands of trials, figuring out what works through trial and error—much like a human child learns. This is **reinforcement learning** (RL): instead of programming the solution, you define the goal, and the robot discovers the strategy through experience.

RL has revolutionized robotics in the past few years. Robots have learned to walk, run, manipulate objects, and even play soccer—not through hand-coded controllers, but by learning from experience in simulation. This lesson teaches you how to use **Isaac Lab**—NVIDIA's GPU-accelerated RL framework for robotics—to train intelligent robot policies.

## What is Reinforcement Learning?

Reinforcement learning is a machine learning paradigm where an **agent** learns to make decisions by interacting with an **environment**. Unlike supervised learning (learning from labeled examples) or unsupervised learning (finding patterns in data), RL learns through **trial and error** guided by rewards.

### The Learning Loop

```
+---------------------------------------------------------------+
|                                                               |
|    AGENT (Robot Brain)                ENVIRONMENT (World)      |
|                                                               |
|    +--------------+     action      +----------------------+  |
|    |   Policy     | -------------> |  Physics Simulation |  |
|    |  (Neural Net)|                |   + Robot State      |  |
|    +--------------+                 +----------------------+  |
|         ^      |                                    |         |
|         |      |                                    |         |
|         |      +--------------- reward, state ------+         |
|         |                                                           |
|    +--------------+                                              |
|    |   Update    | <--- Learn from experience                    |
|    +--------------+                                              |
|                                                               |
+---------------------------------------------------------------+
```

**The flow**:
1. Agent observes environment state
2. Agent selects action based on policy
3. Environment executes action, returns new state + reward
4. Agent updates policy based on reward
5. Repeat millions of times

### Why RL for Robotics?

Traditional robot control requires hand-crafted controllers for every behavior. RL offers an alternative:

| Approach | How It Works | Pros | Cons |
|----------|--------------|------|------|
| **Hand-Crafted Control** | Engineer writes explicit rules | Predictable, interpretable | Limited to simple tasks, brittle |
| **Reinforcement Learning** | Robot learns through trial | Handles complex, unstructured problems | Requires simulation, less interpretable |

**RL shines for**:
- Locomotion: Walking, running, climbing
- Manipulation: Grasping diverse objects
- Navigation: Complex, dynamic environments
- Multi-agent: Coordinating robot teams

**Hand-crafted control shines for**:
- Simple, well-defined tasks
- Safety-critical systems (where interpretability matters)
- Situations with abundant domain knowledge

In practice, modern robotics combines both: RL for complex behaviors, hand-crafted safeguards for safety.

## The MDP Framework

RL problems are formalized as **Markov Decision Processes (MDPs)**. An MDP is a mathematical framework for modeling sequential decision-making under uncertainty.

### MDP Components

An MDP is defined by five elements:

```python
# MDP Formal Definition
MDP = {
    "S": "State space (all possible environment states)",
    "A": "Action space (all possible agent actions)",
    "P": "Transition probabilities (P(s'|s,a) = probability of reaching s' from s with action a)",
    "R": "Reward function (R(s,a) = immediate reward for taking action a in state s)",
    "gamma": "Discount factor (0 <= gamma <= 1, how much to value future rewards)"
}
```

**For robotics**, each component maps to physical reality:

| MDP Component | Robotics Interpretation | Example |
|---------------|------------------------|---------|
| **State (S)** | What robot observes | Joint angles, velocities, sensor readings, object positions |
| **Action (A)** | What robot can do | Joint torques, gripper commands, velocity targets |
| **Transition (P)** | Physics dynamics | How robot moves given motor commands (determined by physics engine) |
| **Reward (R)** | Goal feedback | +10 for picking up object, -1 per timestep, -100 for falling |
| **Discount (gamma)** | Future importance | 0.99 means robot cares about future rewards |

### The RL Objective

The agent's goal is to find a **policy** (pi*) that maximizes the **expected cumulative reward**:

```python
# The RL objective
# G_t = expected sum of discounted future rewards

G_t = R_t + gamma * R_t+1 + gamma^2 * R_t+2 + gamma^3 * R_t+3 + ...

# Optimal policy: maximizes expected G_t from any starting state
pi* = argmax_pi E[G_t | pi]
```

**Intuition**: The robot learns to choose actions that lead to high long-term reward, not just immediate reward.

### Example: MDP for Robot Reaching

```python
# Robot Arm Reaching Task as MDP

class ReachingMDP:
    """MDP for robot arm reaching a target"""

    def __init__(self):
        # STATE SPACE: Robot and target configuration
        self.state_space = {
            "end_effector_pos": "x, y, z of gripper (3D)",
            "end_effector_vel": "velocity of gripper (3D)",
            "target_pos": "x, y, z of target (3D)",
            "joint_positions": "7 joint angles for robot arm",
            "joint_velocities": "7 joint velocities"
        }  # Total: 20-dimensional state

        # ACTION SPACE: Commands to robot
        self.action_space = {
            "type": "continuous",
            "dimension": 7,  # One per joint
            "range": [-1.0, 1.0],  # Normalized torques
            "meaning": "Joint torque commands scaled to robot limits"
        }

        # REWARD FUNCTION: What we want robot to learn
        self.reward_function = self.compute_reward

        # DISCOUNT FACTOR: How much to care about future
        self.gamma = 0.99  # Standard for robotics

    def compute_reward(self, state, action, next_state):
        """Calculate reward for reaching task"""

        # Distance from gripper to target
        gripper_pos = next_state["end_effector_pos"]
        target_pos = next_state["target_pos"]
        distance = np.linalg.norm(gripper_pos - target_pos)

        # Reward components
        reward = 0.0

        # Shaped reward: reward for getting closer
        reward -= distance * 1.0  # Negative distance (smaller = better)

        # Bonus for success
        if distance < 0.05:  # Within 5cm
            reward += 10.0  # Big success reward

        # Penalty for action magnitude (encourage efficiency)
        reward -= np.sum(np.abs(action)) * 0.01

        return reward

    def is_terminal(self, state):
        """Check if episode is done"""
        distance = np.linalg.norm(state["end_effector_pos"] - state["target_pos"])
        return distance < 0.05  # Success: reached target
```

**What this MDP captures**:
- The robot sees its joint states and target position (observation)
- The robot applies joint torques (action)
- Physics simulation determines resulting motion (transition)
- The robot gets rewarded for getting closer to target (reward)
- The robot repeats until reaching target (terminal state)

## Isaac Lab RL Framework

**Isaac Lab** is NVIDIA's open-source framework for robot learning, built on Isaac Sim. It provides GPU-accelerated simulation, pre-built RL environments, and integration with popular RL libraries.

### Isaac Lab Architecture

```
+---------------------------------------------------------------+
|                    Isaac Lab RL Framework                     |
+---------------------------------------------------------------+
|                                                               |
|  +-------------------+        +---------------------------+   |
|  |  RL Manager       | <----> |  MDP Managers             |   |
|  |  (Training Loop)  |        |  - Observation Manager    |   |
|  +-------------------+        |  - Action Manager         |   |
|         |                     |  - Reward Manager         |   |
|         v                     +---------------------------+   |
|  +-------------------+                        ^              |
|  |  RL Algorithm     |                        |              |
|  |  (PPO, SAC, etc.) |                        |              |
|  +-------------------+                        |              |
|         |                                     |              |
|         v                     +---------------------------+   |
|  +-------------------+        |  Environment              |   |
|  |  Policy Network   | <----> |  - Robot Assets           |   |
|  |  (Neural Net)     |        |  - Physics Simulation     |   |
|  +-------------------+        |  - Renderer               |   |
|                               +---------------------------+   |
|                                                               |
+---------------------------------------------------------------+
```

### Supported RL Algorithms

Isaac Lab integrates with multiple RL libraries:

| Library | Algorithms | Strength | Use Case |
|---------|------------|----------|----------|
| **Stable-Baselines3** | PPO, SAC, TD3 | Well-documented, easy to use | Learning, prototyping |
| **RSL-RL** | PPO (optimized) | GPU-optimized, fast | Production training |
| **SKRL** | PPO, SAC, droQ | Modern, flexible | Research |
| **RL-Games** | PPO | Efficient for large-scale | Multi-robot training |

For this lesson, we'll use **Stable-Baselines3**—it's beginner-friendly and excellent for learning RL fundamentals.

### Isaac Lab Installation

```bash
# Clone Isaac Lab repository
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# Install Isaac Lab (follow interactive prompts)
./isaaclab.sh --install

# Install Stable-Baselines3 for RL algorithms
pip install stable-baselines3

# Verify installation
./isaaclab.sh --prebuilt --task Isaac-Lift-Cube-Franka-IK-AB
```

**Output** (first run):
```
Isaac Lab installed successfully!
Assets downloaded: Franka robot, cube assets, environments
Running pre-built task: Isaac-Lift-Cube-Franka-IK-AB
```

## Observables: What the Robot Sees

**Observables** (observations) are the data the robot receives from the environment. Designing good observables is critical—the robot can only learn from what it can perceive.

### Observation Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Proprioceptive** | Robot's internal state | Joint positions, velocities, end-effector pose |
| **Exteroceptive** | Environment information | Camera images, depth maps, object positions |
| **Task-relevant** | Goal-specific information | Target position, distance to goal, object type |

### Isaac Lab Observation Manager

```python
from isaaclab.envs import ManagerBasedEnv, ManagerBasedRLEnv
from isaaclab.envs.mdp import obs_cfg

# Observation configuration
observation_cfg = obs_cfg.ObservationCfg()

# Add proprioceptive observations (robot state)
observation_cfg.policy = obs_cfg.PolicyObsCfg(
    [
        # Joint positions
        obs_cfg.SensorCfg(
            func="joint_pos_rel",  # Relative to default position
            params={"asset_name": "robot"},
            size=7,  # 7 joints
            noise={"type": "gaussian", "std": 0.01}  # Add sensor noise
        ),
        # Joint velocities
        obs_cfg.SensorCfg(
            func="joint_vel_rel",
            params={"asset_name": "robot"},
            size=7,
            noise={"type": "gaussian", "std": 0.01}
        ),
        # End-effector position
        obs_cfg.SensorCfg(
            func="body_pos_w",
            params={"asset_name": "robot", "body_name": "panda_hand"},
            size=3,
            noise={"type": "gaussian", "std": 0.005}
        ),
        # End-effector orientation (quaternion)
        obs_cfg.SensorCfg(
            func="body_quat_w",
            params={"asset_name": "robot", "body_name": "panda_hand"},
            size=4
        ),
        # Actions (last action taken)
        obs_cfg.SensorCfg(
            func="last_action",
            params={},
            size=7
        )
    ]
)

# Add task-specific observations (goal, target)
observation_cfg.critic = obs_cfg.CriticObsCfg(
    observation_cfg.policy.observations + [
        # Target position (critic sees goal, policy doesn't)
        obs_cfg.SensorCfg(
            func="target_pos_w",
            params={"asset_name": "target"},
            size=3
        )
    ]
)
```

### Observation Design Principles

**Principle 1: Include Necessary Information**
```python
# BAD: Missing critical information
observations = ["joint_positions"]  # Can't learn dynamics without velocities

# GOOD: Complete state representation
observations = ["joint_positions", "joint_velocities", "end_effector_pose"]
```

**Principle 2: Normalize Observations**
```python
# BAD: Raw values with different scales
joint_pos = [0.0, 1.57, 0.0, -1.2, 0.0, 0.78, 0.0]  # Radians, wide range
end_eff_pos = [0.5, 0.3, 0.2]  # Meters, different scale

# GOOD: Normalized to [-1, 1]
joint_pos_norm = [0.0, 0.99, 0.0, -0.76, 0.0, 0.49, 0.0]  # Normalized by limits
end_eff_pos_norm = [0.0, -0.2, -0.3]  # Relative to workspace center
```

**Principle 3: Add Realistic Sensor Noise**
```python
# Real sensors aren't perfect
observation_noise = {
    "joint_positions": 0.01,  # 1% noise
    "joint_velocities": 0.02,  # 2% noise
    "camera_depth": 0.05,      # 5% noise
}
```

## Actions: What the Robot Does

The **action space** defines what the robot can control. In Isaac Lab, actions are typically joint-level commands: position targets, velocity targets, or torques.

### Action Types

| Action Type | Meaning | Use Case |
|-------------|---------|----------|
| **Joint Position** | Target joint angles | Precise control, easier learning |
| **Joint Velocity** | Target joint velocities | Velocity-based behaviors |
| **Joint Effort** | Motor torques/forces | Dynamic interactions, more realistic |

### Isaac Lab Action Manager

```python
from isaaclab.envs.mdp import action_cfg

# Action configuration
action_cfg = action_cfg.ActionCfg(
    asset_name="robot",
    action_type="joint_position",  # or "joint_velocity", "joint_effort"
    joints=["panda_joint1", "panda_joint2", "panda_joint3",
            "panda_joint4", "panda_joint5", "panda_joint6", "panda_joint7"],
    scale=0.5,  # Scale normalized action to joint limits
    clip={"min": -1.0, "max": 1.0}  # Clip actions to valid range
)
```

### Action Space Design

```python
# Example: Different action spaces for same robot

# SMALL ACTION SPACE: Coarse control
action_space = gym.spaces.Box(
    low=-1.0, high=1.0,
    shape=(3,),  # Only control x, y, z of end-effector
    dtype=np.float32
)

# MEDIUM ACTION SPACE: Joint-level control
action_space = gym.spaces.Box(
    low=-1.0, high=1.0,
    shape=(7,),  # All 7 robot joints
    dtype=np.float32
)

# LARGE ACTION SPACE: Full robot control
action_space = gym.spaces.Box(
    low=-1.0, high=1.0,
    shape=(9,),  # 7 joints + gripper open/close + base motion
    dtype=np.float32
)
```

**Trade-off**: Larger action spaces = more flexibility but harder learning. Start small, then increase complexity.

## Rewards: Shaping Robot Behavior

The **reward function** tells the robot what we want. Good reward design is more art than science—you're shaping behavior through mathematical feedback.

### Reward Shaping Principles

**Principle 1: Dense Rewards for Learning**
```python
# BAD: Sparse reward (hard to learn)
def reward_sparse(state):
    if task_complete(state):
        return 1.0  # Only reward at the very end
    return 0.0  # No feedback otherwise

# GOOD: Dense reward (guides learning)
def reward_dense(state):
    reward = 0.0

    # Progress reward: getting closer to goal
    distance = distance_to_goal(state)
    reward -= distance * 0.1  # Negative distance

    # Speed bonus: faster completion
    if distance < 0.1:
        reward += 1.0

    # Success reward
    if task_complete(state):
        reward += 10.0

    return reward
```

**Principle 2: Balance Rewards**
```python
# Multiple objectives need balanced weights
def compute_reward(state, action, next_state):
    reward = 0.0

    # Task completion (most important)
    reward += success_reward(state) * 10.0

    # Progress toward goal
    reward += progress_reward(state) * 1.0

    # Efficiency (penalize large actions)
    reward -= action_penalty(action) * 0.01

    # Safety (penalize dangerous states)
    reward -= safety_penalty(state) * 5.0

    return reward
```

### Isaac Lab Reward Manager

```python
from isaaclab.envs.mdp import reward_cfg

# Reward configuration
reward_cfg = reward_cfg.RewardCfg(
    # Primary reward: reach target
    reward_cfg.RewardTermCfg(
        func="reach_target",
        params={"asset_name": "robot", "target_name": "target"},
        weight=1.0
    ),
    # Secondary reward: minimize effort
    reward_cfg.RewardTermCfg(
        func="action_l2",
        params={"asset_name": "robot"},
        weight=-0.01  # Negative = penalty
    ),
    # Safety: limit joint velocities
    reward_cfg.RewardTermCfg(
        func="joint_vel_l2",
        params={"asset_name": "robot"},
        weight=-0.001
    ),
    # Termination bonus
    reward_cfg.RewardTermCfg(
        func="is_success",
        params={"threshold": 0.05},
        weight=10.0
    )
)
```

## PPO: Proximal Policy Optimization

**PPO** (Proximal Policy Optimization) is the most widely used RL algorithm for robotics. It balances ease of implementation with strong performance.

### Why PPO for Robotics?

| Algorithm | Sample Efficiency | Stability | Implementation |
|-----------|-------------------|-----------|----------------|
| **PPO** | Medium | High | Easy |
| **SAC** | High | Medium | Medium |
| **TD3** | Medium | Medium | Easy |
| **A2C/A3C** | Low | Low | Easy |

PPO dominates robotics because:
- Stable learning (doesn't collapse easily)
- Works with continuous action spaces (robot joints)
- Relatively sample efficient (important for simulation)
- Easy to tune and debug

### PPO Algorithm Overview

```python
# Simplified PPO pseudocode

def train_ppo(env, policy, value_network, num_iterations=1000):
    """Train policy using PPO algorithm"""

    for iteration in range(num_iterations):

        # 1. COLLECT TRAJECTORIES
        # Run current policy to collect experience
        states, actions, rewards, log_probs = [], [], [], []
        for _ in range(rollout_steps):
            state = env.reset()
            action, log_prob = policy.act(state)
            next_state, reward, done = env.step(action)

            states.append(state)
            actions.append(action)
            rewards.append(reward)
            log_probs.append(log_prob)

        # 2. COMPUTE ADVANTAGES
        # Estimate how much better each action was
        advantages = compute_advantages(rewards, value_network, gamma=0.99)

        # 3. UPDATE POLICY
        # Multiple epochs over collected data
        for _ in range(num_epochs):
            # PPO clipped objective: prevent large policy updates
            ratio = new_policy_prob / old_policy_prob
            clipped_ratio = torch.clamp(ratio, 1 - epsilon, 1 + epsilon)

            # Policy loss: maximize clipped advantage
            policy_loss = -torch.min(
                ratio * advantages,
                clipped_ratio * advantages
            ).mean()

            # Value loss: fit value function
            value_loss = F.mse_loss(value_network(states), returns)

            # Entropy bonus: encourage exploration
            entropy = policy.entropy().mean()

            # Total loss
            loss = policy_loss + value_loss - 0.01 * entropy

            # Update networks
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Log progress
        print(f"Iteration {iteration}: Average reward = {np.mean(rewards):.2f}")
```

### Key PPO Concepts

**Clipped Objective**: PPO limits how much the policy can change each update, preventing collapse.

```python
# The PPO clipped objective (simplified)
epsilon = 0.2  # Clip parameter

ratio = pi_new(action | state) / pi_old(action | state)
clipped_ratio = torch.clamp(ratio, 1 - epsilon, 1 + epsilon)

# Use minimum of unclipped and clipped
objective = torch.min(ratio * advantage, clipped_ratio * advantage)
```

**Advantage Estimation**: How much better was this action than average?

```python
# Generalized Advantage Estimation (GAE)
# Balances bias vs variance in advantage estimates

def compute_gae(rewards, values, gamma=0.99, lambda_gae=0.95):
    advantages = []
    gae = 0

    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * values[t + 1] - values[t]
        gae = delta + gamma * lambda_gae * gae
        advantages.insert(0, gae)

    return advantages
```

## Complete Example: Training a Reaching Policy

Let's put it all together: a complete Isaac Lab RL training example for a robot arm reaching task.

### Environment Configuration

```python
"""
Isaac Lab RL Training Example: Robot Arm Reaching
Trains a Franka robot to reach random target positions using PPO
"""

from isaaclab.envs import ManagerBasedRLEnv
from isaaclab.envs.mdp import (
    obs_cfg, action_cfg, reward_cfg, termination_cfg, curriculum_cfg
)
from isaaclab.devices import SeedReader
from isaaclab.utils import configclass

@configclass
class ReachingEnvCfg:
    """Configuration for reaching task"""

    # Environment
    num_envs = 4096  # Number of parallel environments (GPU-accelerated)
    env_spacing = 2.0  # Distance between environments
    episode_length_s = 8.0  # Max episode duration

    # Observation space
    observations = obs_cfg.ObservationCfg(
        policy=obs_cfg.PolicyObsCfg([
            # Robot joint positions
            obs_cfg.SensorCfg(
                func="joint_pos_rel",
                params={"asset_name": "robot"},
                size=7,
                noise={"type": "gaussian", "std": 0.01}
            ),
            # Robot joint velocities
            obs_cfg.SensorCfg(
                func="joint_vel_rel",
                params={"asset_name": "robot"},
                size=7,
                noise={"type": "gaussian", "std": 0.01}
            ),
            # End-effector position
            obs_cfg.SensorCfg(
                func="body_pos_w",
                params={"asset_name": "robot", "body_name": "panda_hand"},
                size=3
            ),
            # Target position (relative to end-effector)
            obs_cfg.SensorCfg(
                func="target_pos_rel",
                params={"asset_name": "target"},
                size=3
            ),
            # Previous action
            obs_cfg.SensorCfg(
                func="last_action",
                size=7
            )
        ])
    )

    # Action space
    actions = action_cfg.ActionCfg(
        asset_name="robot",
        action_type="joint_position",
        joints=[
            "panda_joint1", "panda_joint2", "panda_joint3",
            "panda_joint4", "panda_joint5", "panda_joint6", "panda_joint7"
        ],
        scale=0.1,  # Action scaling
        clip={"min": -1.0, "max": 1.0}
    )

    # Reward function
    rewards = reward_cfg.RewardCfg(
        # Primary: reach target
        reward_cfg.RewardTermCfg(
            func="reach_target_smooth",
            params={
                "asset_name": "robot",
                "target_name": "target",
                "dist_threshold": 0.05
            },
            weight=1.0
        ),
        # Penalty: large actions (efficiency)
        reward_cfg.RewardTermCfg(
            func="action_l2",
            params={"asset_name": "robot"},
            weight=-0.01
        ),
        # Penalty: joint velocity limits
        reward_cfg.RewardTermCfg(
            func="joint_vel_l2",
            params={"asset_name": "robot"},
            weight=-0.001
        ),
        # Bonus: success
        reward_cfg.RewardTermCfg(
            func="is_success",
            params={"threshold": 0.05},
            weight=10.0
        )
    )

    # Termination conditions
    terminations = termination_cfg.TerminationCfg(
        # Success: reached target
        termination_cfg.TerminationTermCfg(
            func="reach_target",
            params={"threshold": 0.05},
            time_out=True
        ),
        # Failure: robot falls
        termination_cfg.TerminationTermCfg(
            func="robot_base_height",
            params={"threshold": 0.05}
        )
    )

    # Curriculum: start easy, get harder
    curriculum = curriculum_cfg.CurriculumCfg(
        curriculum_cfg.CurriculumTermCfg(
            func="target_position_randomization",
            params={
                "num_stages": 5,
                "difficulty": [0.1, 0.2, 0.3, 0.4, 0.5]  # Target distance
            }
        )
    )
```

### Training Script with PPO

```python
"""
Training script using Stable-Baselines3 PPO
"""

import gymnasium as gym
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from isaaclab.envs import ManagerBasedRLEnv

# Create Isaac Lab environment
env = ManagerBasedRLEnv(cfg=ReachingEnvCfg())

# Wrap for SB3 compatibility
env = gym.make("Isaac-Reaching-v0", **env.cfg)

# Configure PPO algorithm
ppo_config = {
    "learning_rate": 3e-4,      # Step size for policy updates
    "n_steps": 2048,             # Steps per update
    "batch_size": 512,           # Batch size for training
    "n_epochs": 10,              # Training epochs per update
    "gamma": 0.99,               # Discount factor
    "gae_lambda": 0.95,          # GAE parameter
    "clip_range": 0.2,           # PPO clipping parameter
    "ent_coef": 0.01,            # Entropy coefficient (exploration)
    "vf_coef": 0.5,              # Value function coefficient
    "max_grad_norm": 1.0,        # Gradient clipping
    "policy": "MultiInputPolicy", # For dict observations
    "activation_fn": torch.nn.Tanh,
    "net_arch": {"pi": [256, 256], "vf": [256, 256]},  # Network size
}

# Create PPO model
model = PPO(
    **ppo_config,
    env=env,
    verbose=1,
    tensorboard_log="./logs/reaching_ppo/",
    device="cuda"  # GPU acceleration
)

# Checkpoint callback (save model every 100k steps)
checkpoint_callback = CheckpointCallback(
    save_freq=100000,
    save_path="./checkpoints/",
    name_prefix="reaching_ppo"
)

# Train
print("Starting training...")
model.learn(
    total_timesteps=5_000_000,  # 5 million steps
    callback=checkpoint_callback,
    progress_bar=True
)

# Save final model
model.save("reaching_ppo_final")
print("Training complete! Model saved.")
```

**Output** (during training):
```
Starting training...
---------------------------------
| rollout/           |          |
|    ep_len_mean     | 186      |
|    ep_rew_mean     | -45.2    |
| time/iterations    | 1        |
| time/fps           | 8243     |
| time/time_elapsed  | 248      |
| time/total_timesteps | 2048    |
---------------------------------
...
---------------------------------
| rollout/           |          |
|    ep_len_mean     | 98       |
|    ep_rew_mean     | 8.7      |
| time/iterations    | 2444     |
| time/fps           | 8912     |
| time/time_elapsed  | 561      |
| time/total_timesteps | 5000000 |
---------------------------------
Training complete! Model saved.
```

### Evaluating the Trained Policy

```python
"""
Evaluation script: Test trained policy
"""

import numpy as np
from stable_baselines3 import PPO

# Load trained model
model = PPO.load("reaching_ppo_final")

# Create evaluation environment
eval_env = gym.make("Isaac-Reaching-v0", **env.cfg)

# Evaluate
num_episodes = 100
success_count = 0
episode_rewards = []

for episode in range(num_episodes):
    obs, _ = eval_env.reset()
    done = False
    total_reward = 0
    steps = 0

    while not done:
        # Get action from trained policy
        action, _ = model.predict(obs, deterministic=True)

        # Execute action
        obs, reward, done, truncated, info = eval_env.step(action)
        total_reward += reward
        steps += 1

        # Check success
        if "is_success" in info and info["is_success"]:
            success_count += 1

    episode_rewards.append(total_reward)

# Print results
print(f"Evaluation Results ({num_episodes} episodes):")
print(f"Success Rate: {success_count / num_episodes * 100:.1f}%")
print(f"Average Reward: {np.mean(episode_rewards):.2f} +/- {np.std(episode_rewards):.2f}")
print(f"Average Episode Length: {np.mean([len(r) for r in episode_rewards]):.1f} steps")
```

**Output**:
```
Evaluation Results (100 episodes):
Success Rate: 94.0%
Average Reward: 8.43 +/- 1.21
Average Episode Length: 87.3 steps
```

## Common RL Training Challenges

Training RL policies for robotics comes with common challenges. Here's how to diagnose and fix them.

### Challenge 1: Policy Doesn't Learn

**Symptoms**: Reward stays flat, no improvement over training

**Diagnosis**:
```python
# Check learning: monitor reward curve
# Flat line = not learning

# Common causes:
# 1. Reward function doesn't guide behavior
# 2. Observation space missing critical information
# 3. Action space too large or disconnected
# 4. Learning rate too high or too low
```

**Solutions**:
```python
# Solution 1: Add denser rewards
def reward_dense(state, action, next_state):
    # Before: sparse success reward only
    # After: progress reward
    old_dist = distance_to_goal(state)
    new_dist = distance_to_goal(next_state)
    reward = (old_dist - new_dist) * 10.0  # Reward for getting closer
    return reward

# Solution 2: Verify observations
print("Observation keys:", obs.keys())
print("Observation shapes:", {k: v.shape for k, v in obs.items()})

# Solution 3: Reduce action space
# Before: control all 9 DOF
# After: control only 4 critical joints
action_cfg = ActionCfg(joints=["joint1", "joint2", "joint3", "joint4"])

# Solution 4: Tune learning rate
# Try: 1e-5, 3e-5, 1e-4, 3e-4, 1e-3
model = PPO(..., learning_rate=3e-4)
```

### Challenge 2: Policy Learns but Collapses

**Symptoms**: Reward increases then suddenly drops to near-zero

**Diagnosis**:
```python
# Check learning curve: goes up then crashes
# This is policy collapse

# Common causes:
# 1. Learning rate too high (unstable updates)
# 2. Entropy coefficient too low (premature exploitation)
# 3: Gradient explosion (large updates)
```

**Solutions**:
```python
# Solution 1: Lower learning rate
model = PPO(..., learning_rate=1e-5)  # Was 3e-4

# Solution 2: Increase entropy (more exploration)
model = PPO(..., ent_coef=0.05)  # Was 0.01

# Solution 3: Add gradient clipping
model = PPO(..., max_grad_norm=0.5)  # Was 1.0

# Solution 4: Use more conservative PPO clipping
model = PPO(..., clip_range=0.1)  # Was 0.2
```

### Challenge 3: Reward Hacking

**Symptoms**: High reward but policy behaves incorrectly

**Diagnosis**:
```python
# Policy finds loophole in reward function
# Example: robot spins in circles to maximize "movement" reward

# Check: visualize policy behavior
# If reward is high but behavior wrong = reward hacking
```

**Solutions**:
```python
# Solution 1: Add counter-rewards
def reward_fixed(state, action, next_state):
    reward = 0.0

    # Original reward
    reward += movement_reward(state, next_state)

    # Counter-reward: penalize undesired behavior
    reward -= spinning_penalty(state, next_state)
    reward -= oscillation_penalty(action)

    return reward

# Solution 2: Constraint rewards
# Only give reward for goal-oriented behavior
def reward_constrained(state, action, next_state):
    if is_moving_toward_goal(state, next_state):
        return distance_reward
    else:
        return -penalty  # Penalize irrelevant movement
```

### Challenge 4: Simulation-to-Reality Gap

**Symptoms**: Policy works in simulation, fails on real robot

**Diagnosis**:
```python
# The "sim-to-real" gap
# Differences: sensor noise, actuator delays, physics inaccuracies

# Domain randomization: vary simulation during training
# to make policy robust to reality differences
```

**Solutions**:
```python
# Solution 1: Domain randomization
observation_cfg = obs_cfg.ObservationCfg(
    policy=obs_cfg.PolicyObsCfg([
        obs_cfg.SensorCfg(
            func="joint_pos_rel",
            noise={"type": "gaussian",
                   "std": {"range": [0.0, 0.05]}  # Random noise level
                  }
        ),
        # Randomize physics parameters
        obs_cfg.SensorCfg(
            func="randomize_mass",
            params={"range": [0.8, 1.2]}  # +/- 20% mass variation
        )
    ])
)

# Solution 2: System identification
# Measure real robot parameters, match in simulation
real_robot_params = {
    "joint_friction": measure_friction(),
    "actuator_delay": measure_delay(),
    "mass_distribution": measure_mass()
}

# Apply to simulation
sim.set_parameters(real_robot_params)
```

## Hardware Requirements and Alternatives

RL training is computationally intensive. Here's what you need and alternatives if you don't have powerful hardware.

### Recommended Hardware

| Component | Minimum | Recommended | For Multi-Robot |
|-----------|---------|-------------|-----------------|
| **GPU** | RTX 4080 (16GB) | RTX 4090 (24GB) | RTX 5090 or A6000 (48GB) |
| **RAM** | 32 GB | 64 GB | 128 GB |
| **Storage** | 100 GB SSD | 500 GB NVMe | 1 TB NVMe |

**Why**: GPU-accelerated simulation with thousands of parallel environments requires significant VRAM. More VRAM = more parallel environments = faster training.

### Performance Estimates

| Scenario | Environments | GPU | Training Time (5M steps) |
|----------|--------------|-----|--------------------------|
| Single arm reaching | 512 | RTX 4080 | ~8 hours |
| Quadruped locomotion | 2048 | RTX 4090 | ~4 hours |
| Multi-robot warehouse | 4096 | RTX 5090 | ~2 hours |

### Cloud Alternatives

If you don't have a powerful GPU:

**Option 1: NVIDIA Omniverse Cloud**
- On-demand Isaac Sim/Isaac Lab access
- Pay per hour
- No local hardware required

**Option 2: Cloud GPU Rentals**
- AWS: p4d instances (A100 GPUs)
- Google Cloud: A2 instances
- Lambda Labs: RTX 4090/5090 rentals

**Option 3: Reduced Complexity**
```python
# Reduce environment count for slower GPUs
env_cfg = ReachingEnvCfg(
    num_envs=512,  # Was 4096
    episode_length_s=4.0  # Shorter episodes
)

# Disable rendering for speed
simulation_app = SimulationApp({"headless": True})
```

## Try With AI

### Exercise 1: Design an MDP for a Robotics Task

```text
I'm learning reinforcement learning for robotics using Isaac Lab. I want to design an MDP (Markov Decision Process) for a robotics task.

Choose ONE of these tasks and help me design the MDP:

1. **Quadruped locomotion**: Robot dog learning to walk forward
2. **Cube stacking**: Robot arm stacking blocks into a tower
3. **Door opening**: Mobile robot navigating to and opening a door

For your chosen task, specify:

1. STATE SPACE (observations): What should the robot observe? (Proprioceptive, exteroceptive, task-specific)

2. ACTION SPACE: What can the robot control? (Joint positions, velocities, end-effector commands)

3. REWARD FUNCTION: How do we shape the desired behavior? Include both primary rewards and potential penalties

4. TERMINATION: When does an episode end? (Success condition, failure condition, timeout)

Be specific about the values (e.g., "joint positions (7D)", "reward = +10 for success, -0.01 per timestep").
```

**What you're learning:** This exercise develops your ability to translate a robotics task into an MDP formulation—the foundational step for any RL project. By specifying states, actions, and rewards, you'll practice the same design thinking used by RL researchers to create learning tasks. Understanding these components deeply will help you debug training issues and design better learning problems.

### Exercise 2: Debugging a Reward Function

```text
I'm training a robot arm to reach a target using reinforcement learning in Isaac Lab. The policy isn't learning—rewards stay around zero and never improve.

Here's my reward function:

```python
def compute_reward(self, state, action, next_state):
    reward = 0.0

    # Success reward
    distance = np.linalg.norm(
        next_state["end_effector_pos"] - next_state["target_pos"]
    )
    if distance < 0.01:  # Within 1cm
        reward += 1.0

    # Penalty for large actions
    reward -= np.sum(np.abs(action)) * 0.01

    return reward
```

And my observation space:
```python
observations = [
    "joint_positions",  # 7 joint angles
    "joint_velocities"  # 7 joint velocities
]
```

Help me debug:
1. Why isn't the policy learning? Identify specific issues with my reward function and observations.

2. What improvements would you make to the reward function to guide learning better?

3. Am I missing any critical observations that the robot needs to succeed?

Provide corrected code with explanations.
```

**What you're learning:** This exercise teaches you to diagnose and fix common RL training problems. Reward function design is one of the most challenging aspects of robotics RL—small changes can mean the difference between a policy that learns and one that fails. By debugging a broken reward function, you'll develop intuition for what makes rewards effective.

### Exercise 3: RL Training Strategy for Complex Task

```text
I want to train a humanoid robot to perform a backflip using reinforcement learning in Isaac Lab. This is a complex, high-DoF (degrees of freedom) task.

Help me design a training strategy by answering:

1. CURRICULUM LEARNING: How should I structure training? Start with easy subtasks and progressively increase difficulty. What are the intermediate milestones?

2. STATE REPRESENTATION: What observations are critical for a backflip? Consider body orientation, angular velocity, joint states, contact information.

3. REWARD SHAPING: What rewards encourage the right behavior? How do I balance forward rotation with landing safely and staying upright?

4. TRAINING CONFIGURATION: What PPO hyperparameters would you start with? Consider learning rate, network architecture, number of parallel environments.

5. FAILURE MODES: What common failures should I anticipate? (e.g., robot collapses, spins uncontrollably, learns to cheat by falling slowly)

Provide a progressive training plan from beginner to successful backflip.
```

**What you're learning:** This exercise develops your ability to design training strategies for complex robotics tasks. Complex behaviors like backflips can't be learned end-to-end directly—they require curriculum learning, careful reward design, and strategic hyperparameter choices. By planning a multi-stage training approach, you'll practice the same methodology used by researchers to achieve impressive robot behaviors.
