---
sidebar_position: 1
title: "Introduction to ROS 2"
description: "Learn the fundamentals of ROS 2 (Robot Operating System 2) - the standard framework for robotics development. Understand nodes, topics, services, and actions that enable robot software communication."
keywords: ["ROS 2", "Robot Operating System", "Nodes", "Topics", "Services", "Actions", "rclpy", "Ubuntu 22.04"]
chapter: 2
lesson: 1
duration_minutes: 90

requirements:
  hardware: "Any computer with Ubuntu 22.04 LTS (native or dual-boot), Windows with WSL2, or macOS with VM"
  software: "ROS 2 Humble Hawksbill, Python 3.10+, Ubuntu 22.04 LTS"

skills:
  - name: "ROS 2 Architecture Understanding"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can explain the publish-subscribe communication pattern and how ROS 2 nodes interact"

  - name: "ROS 2 Environment Setup"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can install ROS 2 Humble and configure the environment variables"

  - name: "Basic ROS 2 Node Development"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can write and run a simple publisher-subscriber system in Python"

  - name: "ROS 2 Communication Patterns"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Analyze"
    measurable_at_this_level: "Student can distinguish when to use topics, services, or actions for different robotics tasks"

learning_objectives:
  - objective: "Explain what ROS 2 is and why it has become the de facto standard for robotics software development"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Short written explanation comparing ROS 2 to traditional monolithic robot code"

  - objective: "Install ROS 2 Humble on Ubuntu 22.04 and verify the installation using ros2 command-line tools"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Installation checklist with screenshot of successful ros2 doctor output"

  - objective: "Identify and describe the four main communication patterns in ROS 2: topics, services, actions, and parameters"
    proficiency_level: "B1"
    bloom_level: "Remember"
    assessment_method: "Matching exercise or table completion"

  - objective: "Write a simple Python ROS 2 node that publishes messages and create a subscriber node that receives them"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code submission with demonstrated output from running nodes"

cognitive_load:
  new_concepts: 8
  assessment: "Students will complete installation verification, write a publisher-subscriber pair, and explain the communication flow"

differentiation:
  extension_for_advanced: "Create a multi-node system where one node controls another using services, implementing a simple robot state machine"
  remedial_for_struggling: "Focus on understanding concepts through visualization tools like rqt_graph before writing code. Use provided code templates and modify only the message content"
  hardware_alternatives: "ROS 2 can run entirely in simulation using Docker containers on any OS. Cloud options: GitHub Codespaces with ROS 2 pre-configured, or AWS RoboMaker for simulation workloads"

safety_notes: "No physical hardware required for this lesson. All exercises run in software simulation."

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Introduction to ROS 2

Imagine you're building a robot from scratch. You need to read camera data, process it with a neural network, plan a path to a goal, control motors to follow that path, and monitor battery levels—all simultaneously. Without a framework, you'd end up with thousands of lines of spaghetti code where everything is tightly coupled. Change one thing, and everything breaks.

This is exactly the problem robotics faced before **ROS 2** (Robot Operating System 2). ROS 2 isn't an operating system—it's a **middleware framework** that provides the standard plumbing for robotics software. Just as internet protocols let different computers communicate, ROS 2 lets different robot software components talk to each other. It's become the de facto standard: from research labs to industrial robots to autonomous vehicles, ROS 2 powers the machines that are shaping our future.

## What is ROS 2?

**ROS 2** is an open-source framework for writing robot software. It provides tools, libraries, and conventions that help you create complex, reliable robot behavior without reinventing communication infrastructure.

### Why ROS 2 Became the Standard

Before ROS, every robotics team built their own custom communication layer. If you wanted to use Team A's lidar processing with Team B's path planning, you had to rewrite code to make them compatible. ROS changed this by providing:

- **Standardized communication**: Nodes talk to each other using common patterns (topics, services, actions)
- **Hardware abstraction**: Write code that works regardless of underlying sensors and actuators
- **Package ecosystem**: Thousands of pre-built packages for navigation, perception, manipulation
- **Language independence**: Write components in Python, C++, Java, or others—they all work together
- **Tools and visualization**: Rviz (3D visualization), rqt (debugging interface), Gazebo (simulation)

**ROS 2 vs ROS 1**: ROS 2 added real-time capabilities, better security, and support for multiple robots. It uses DDS (Data Distribution Service) for communication instead of the custom ROS 1 middleware, making it more reliable for industrial applications.

## ROS 2 Architecture: The Big Picture

ROS 2 is built around **nodes**—independent processes that communicate with each other. Think of nodes as mini-programs, each doing one job well:

```
+------------------+                    +------------------+
|  Camera Node     |   publishes image  |  Vision Node     |
|  (reads camera)  |------------------> |  (detects objects)|
+------------------+   topic: /camera   +------------------+
                                                    |
                                                    v
                                          +------------------+
                                          |  Planner Node    |
                                          |  (plans path)    |
                                          +------------------+
                                                    |
                                                    v
                                          +------------------+
                                          |  Motor Node      |
                                          |  (controls wheels)|
                                          +------------------+
```

**Key insight**: Nodes don't know WHERE other nodes are. They publish to "topics" and subscribe to topics. The underlying ROS 2 middleware handles routing. This means you can replace your camera node without touching your vision node—the vision node just keeps subscribing to `/camera`.

### The Four Communication Patterns

ROS 2 provides four ways for nodes to communicate, each suited for different use cases:

| Pattern | Best For | Analogy | Data Flow |
|---------|----------|---------|-----------|
| **Topics** | Streaming data (sensor readings, motor commands) | Radio broadcast | One-way, many-to-many |
| **Services** | Request-response tasks (take photo, get status) | Phone call | Request, reply, done |
| **Actions** | Long-running tasks with feedback (navigation, grasping) | Pizza delivery tracker | Request, ongoing feedback, result |
| **Parameters** | Configuration values (robot radius, update rates) | Settings menu | Read/write static data |

**Why four patterns?** Different robot tasks need different communication styles. You don't want to wait for a response when streaming camera data (use topics). You DO want feedback when a robot navigates across a room (use actions).

## Installing ROS 2 Humble on Ubuntu 22.04

This lesson uses **ROS 2 Humble Hawksbill**, the Long Term Support (LTS) release officially supported on Ubuntu 22.04 (Jammy Jellyfish).

### Prerequisites

Before installing, ensure you have:

- Ubuntu 22.04 LTS (native installation recommended)
- At least 20 GB free disk space
- Internet connection for downloading packages

**Important**: ROS 2 Humble is specifically designed for Ubuntu 22.04. If you're on Windows or macOS, use WSL2 (Windows) or a virtual machine running Ubuntu.

### Step-by-Step Installation

**1. Set Locale** (ensures UTF-8 encoding):

```bash
locale  # Check if UTF-8 is supported
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

**2. Add ROS 2 Apt Repository**:

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

**3. Install ROS 2 Humble Desktop**:

```bash
sudo apt update
sudo apt install ros-humble-desktop -y
```

**This may take 15-30 minutes** depending on your internet connection. The `ros-humble-desktop` package includes ROS 2, libraries, and visualization tools.

**4. Set Up Your Environment**:

```bash
# Source the ROS 2 setup script (add to ~/.bashrc for persistence)
source /opt/ros/humble/setup.bash

# Verify installation
ros2 --version
```

**Output:**
```
ros2 is a command-line tool for ROS 2.
```

**5. Install Development Tools** (for building your own packages):

```bash
sudo apt install python3-rosdep python3-colcon-common-extensions -y
```

### Verifying Your Installation

Run the ROS 2 diagnostic tool to check everything is working:

```bash
source /opt/ros/humble/setup.bash
ros2 doctor --report
```

**Expected output**: A report showing your ROS 2 version, Python version, and available RMW (middleware) implementations.

### Making ROS 2 Persistent

Add the ROS 2 environment setup to your `.bashrc` so it loads automatically:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Understanding Topics: Publish-Subscribe Communication

Topics are the foundation of ROS 2 communication. They follow the **publish-subscribe pattern**: publishers send messages to a topic, subscribers receive messages from topics.

**Real-world analogy**: Think of topics like radio stations. Publishers broadcast on specific frequencies (topics), and anyone tuned in (subscribed) receives the signal. Multiple publishers can broadcast to the same topic, and multiple subscribers can listen.

### Example: A Simple Publisher

Let's create a node that publishes "Hello, ROS 2!" messages to a topic called `/chat`.

Create a file named `publisher.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')

        # Create a publisher on the 'chat' topic
        self.publisher_ = self.create_publisher(String, 'chat', 10)

        # Timer: publish every 0.5 seconds
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello, ROS 2! Count: {self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Make it executable:

```bash
chmod +x publisher.py
```

### Example: A Simple Subscriber

Now create a subscriber that listens to the `/chat` topic. Create `subscriber.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')

        # Create a subscription on the 'chat' topic
        self.subscription = self.create_subscription(
            String,
            'chat',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Make it executable:

```bash
chmod +x subscriber.py
```

### Running the Publisher-Subscriber System

Open **two terminal windows**:

**Terminal 1** (run the publisher):
```bash
source /opt/ros/humble/setup.bash
python3 publisher.py
```

**Terminal 2** (run the subscriber):
```bash
source /opt/ros/humble/setup.bash
python3 subscriber.py
```

**Publisher output:**
```
[INFO] [minimal_publisher]: Publishing: "Hello, ROS 2! Count: 0"
[INFO] [minimal_publisher]: Publishing: "Hello, ROS 2! Count: 1"
[INFO] [minimal_publisher]: Publishing: "Hello, ROS 2! Count: 2"
...
```

**Subscriber output:**
```
[INFO] [minimal_subscriber]: I heard: "Hello, ROS 2! Count: 0"
[INFO] [minimal_subscriber]: I heard: "Hello, ROS 2! Count: 1"
[INFO] [minimal_subscriber]: I heard: "Hello, ROS 2! Count: 2"
...
```

**What's happening**: The publisher sends messages to the `/chat` topic every 0.5 seconds. The subscriber receives these messages and logs them. The nodes don't know about each other—they only know the topic name.

### Inspecting Topics with ros2 Command

ROS 2 provides powerful command-line tools for inspecting your system:

**List all active topics**:
```bash
ros2 topic list
```

**Output:**
```
/chat
/parameter_events
/rosout
```

**See topic details** (message type, publishers, subscribers):
```bash
ros2 topic info /chat
```

**Output:**
```
Subscription count: 1
Publisher count: 1
  Node name: minimal_publisher
```

**Listen to a topic** (without writing a subscriber):
```bash
ros2 topic echo /chat
```

**Output:**
```
data: 'Hello, ROS 2! Count: 42'
---
data: 'Hello, ROS 2! Count: 43'
---
```

## Understanding Services: Request-Response

Topics work great for streaming data, but sometimes you need a specific answer to a specific request. That's where **services** come in.

**Topic vs Service**:
- **Topic**: Fire and forget. Publisher sends, doesn't care who receives.
- **Service**: Call and response. Client requests, server replies.

### Example: A Simple Add Two Ints Service

ROS 2 provides a built-in example service. Let's try it:

**Terminal 1** (run the service server):
```bash
ros2 run examples_rclpy_minimal_service service
```

**Terminal 2** (call the service):
```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 3}"
```

**Output:**
```
sum: 8
```

**What's happening**: The client sends a request (a=5, b=3) to the `/add_two_ints` service. The server computes the sum and returns the result (8).

## Understanding Actions: Long-Running Tasks

**Actions** are for tasks that take time and provide ongoing feedback. Think of a robot navigating to a goal—you want progress updates, not just a final result.

**Key difference from services**:
- **Service**: Request → (wait) → Result (binary: succeeded/failed)
- **Action**: Request → (feedback, feedback, feedback...) → Result (continuous progress)

Example actions in robotics:
- **Navigation**: "Go to location X" → feedback: "moving, 50% complete" → result: "arrived"
- **Grasping**: "Pick up object" → feedback: "approaching, gripper closing" → result: "grasped" or "failed"

We'll cover actions in detail in a later lesson when we build navigation systems.

## ROS 2 Tools for Visualization and Debugging

ROS 2 includes powerful tools that make development easier:

### Rviz2: 3D Visualization

**Rviz2** is the standard ROS 2 visualization tool. It displays:
- Robot models (from URDF files)
- Sensor data (point clouds, camera images, laser scans)
- Coordinate frames (robot pose, object positions)
- Paths and trajectories

```bash
rviz2
```

### RQT: GUI Debugging

**rqt** is a Qt-based GUI framework for ROS 2. It includes plugins for:
- Viewing topic graphs (which nodes publish to which topics)
- Plotting data over time
- Monitoring parameters
- Dynamic reconfigure

```bash
# View the communication graph
rqt_graph
```

### Ros2 Doctor

We already used `ros2 doctor` to check installation. It also diagnoses runtime issues:

```bash
ros2 doctor --report | less
```

## Hardware and Simulation Options

**No physical robot required** for this lesson or the next several. All ROS 2 concepts work identically with:
- **Simulation**: Gazebo (coming in Module 3)
- **Virtual machines**: Ubuntu 22.04 VM on any host OS
- **Docker**: Pre-configured ROS 2 containers
- **Cloud**: GitHub Codespaces with ROS 2, AWS RoboMaker

When we do add physical hardware (Module 4, weeks 11-13), ROS 2 makes the transition seamless—your code designed for simulation works with real robots, only the hardware interface layer changes.

## Common ROS 2 Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `ros2 node list` | List all running nodes | See active nodes |
| `ros2 topic list` | List all active topics | See data streams |
| `ros2 topic echo <name>` | Print topic messages | Debug sensor data |
| `ros2 topic info <name>` | Show topic details | See message type |
| `ros2 service list` | List available services | See available commands |
| `ros2 service call <name> <type> <data>` | Call a service | Trigger robot action |
| `ros2 action list` | List available actions | See long-running tasks |
| `ros2 bag record <topics>` | Record topic data | Save sensor logs |
| `ros2 bag play <file>` | Replay recorded data | Test with saved data |

## Try With AI

### Exercise 1: Explore ROS 2 Applications

```text
I'm learning ROS 2, the Robot Operating System 2—a middleware framework that lets robot software components communicate. ROS 2 uses nodes (independent programs), topics (for streaming data), services (for request-response), and actions (for long-running tasks with feedback).

Help me understand how ROS 2 is used in real robotics by:
1. Describing three real-world robots or robotics products that use ROS 2
2. For each example, explain which ROS 2 communication patterns (topics, services, actions) would be most important and why
3. Identify one job role in robotics that requires ROS 2 skills and what kind of ROS 2 work they do
```

**What you're learning:** This exercise connects ROS 2 concepts to actual robotics applications. By exploring real robots that use ROS 2, you'll understand why the framework's communication patterns matter in practice. You'll also discover career paths where ROS 2 skills are essential, giving you context for what you're learning.

### Exercise 2: Design a ROS 2 System

```text
I want to design a ROS 2 system for a simple delivery robot that moves around an office building and delivers packages to different rooms.

Help me design the ROS 2 architecture by:
1. Identifying at least 5 nodes this robot would need (e.g., camera node, navigation node, motor controller)
2. For each node, specify what topics it would publish to and/or subscribe from
3. Specify which operations would be better as services vs topics vs actions
4. Draw a simple text diagram showing how these nodes connect

After you provide the design, ask me questions to help refine it based on real-world constraints.
```

**What you're learning:** This exercise develops your ability to think in ROS 2 architecture patterns. By designing a multi-node system, you'll practice decomposing complex robot behavior into independent, communicating components. The refinement conversation helps you understand real-world trade-offs in robotics system design.

### Exercise 3: Debug and Extend Publisher-Subscriber Code

```text
I have this ROS 2 Python publisher node that's supposed to publish sensor readings, but something isn't working. Here's the code:

[PASTE YOUR PUBLISHER CODE WITH AN INTENTIONAL BUG]

Can you:
1. Identify what's wrong with the code and explain the issue
2. Show me the corrected version
3. Then help me extend it: add a second publisher that publishes a "status" message every 2 seconds to a different topic called /robot_status
4. Create a subscriber node that listens to both topics and logs both the sensor reading and status

Please explain your corrections so I understand what went wrong.
```

**What you're learning:** This exercise builds practical debugging skills and extends your understanding of ROS 2 node development. By working with intentional bugs, you'll learn common pitfalls in ROS 2 Python code. The extension work reinforces your understanding of topics and multi-node systems, preparing you for more complex robotics software.
