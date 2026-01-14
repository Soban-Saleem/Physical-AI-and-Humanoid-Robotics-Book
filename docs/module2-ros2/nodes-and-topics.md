---
sidebar_position: 2
title: "ROS 2 Nodes and Topics"
description: "Learn how ROS 2 nodes communicate through topics using the publish-subscribe pattern. Create publishers and subscribers in Python (rclpy) and understand message types."
keywords: ["ROS 2", "Nodes", "Topics", "Publisher", "Subscriber", "rclpy", "Publish-Subscribe"]
chapter: 2
lesson: 2
duration_minutes: 90

requirements:
  hardware: "Any computer with ROS 2 Humble installed"
  software: "ROS 2 Humble, Python 3 (rclpy), colcon build system"

skills:
  - name: "ROS 2 Node Architecture"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Understand"
    digcomp_area: "1.2 Interacting with digital devices and systems"
    measurable_at_this_level: "Student can explain how nodes work as independent processes that communicate"

  - name: "Topic-Based Communication"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "1.3 Managing information and data"
    measurable_at_this_level: "Student can implement publish-subscribe pattern with working code"

  - name: "ROS 2 Message Types"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "1.2 Interacting with digital devices and systems"
    measurable_at_this_level: "Student can select appropriate message types for different data"

learning_objectives:
  - objective: "Explain the publish-subscribe communication pattern and how it enables decoupled robot software architecture"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Written explanation comparing pub-sub to direct function calls"

  - objective: "Create a working ROS 2 publisher node using rclpy that sends messages on a topic"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code execution - publisher successfully sends messages visible via ros2 topic echo"

  - objective: "Create a working ROS 2 subscriber node using rclpy that receives and processes messages from a topic"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code execution - subscriber successfully receives and displays messages"

  - objective: "Select appropriate message types from std_msgs, geometry_msgs, and sensor_msgs for common robotics data"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Matching exercise or code selection task"

cognitive_load:
  new_concepts: 8
  assessment: "Students will write and execute working publisher and subscriber nodes, verifying communication with ros2 CLI tools"

differentiation:
  extension_for_advanced: "Create a node that is both a publisher AND subscriber, passing data through (e.g., receiving sensor data, processing it, publishing commands)"
  remedial_for_struggling: "Start with pre-written publisher/subscriber code and focus on understanding the communication flow using ros2 topic list, echo, and hz commands"
  hardware_alternatives: "All exercises work on any computer with ROS 2 installed. No physical robot required. Students without local ROS 2 can use online environments like The Construct's ROS 2 Basics in 5 Days cloud workspace"

safety_notes: "No physical hardware required for this lesson. Always source your ROS 2 setup script in new terminals: source /opt/ros/humble/setup.bash"

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# ROS 2 Nodes and Topics

Imagine a busy restaurant kitchen during dinner rush. The head chef doesn't personally cook every dish—they call out orders to specialized stations: "Two steaks medium-rare!" "Salad for table five!" Each station hears the orders relevant to them and acts independently. The chef doesn't need to know how the grill station works internally, and the grill station doesn't need to know who placed the order. They communicate through announcements, and anyone can listen or respond.

This is exactly how ROS 2 robots work. Instead of one massive program controlling everything, a robot is composed of many small, independent programs called **nodes** that communicate through **topics**. This architecture makes robotic software more flexible, easier to debug, and enables true parallel processing—critical when your robot needs to process camera data, update motor commands, and check battery levels all at the same time.

## The Publish-Subscribe Pattern

Before writing code, you need to understand the communication pattern that makes ROS 2 work. The **publish-subscribe** (pub-sub) pattern is different from the direct function calls you might be used to in traditional programming.

### Traditional Programming vs Pub-Sub

**Traditional Programming** (Direct Function Call):

```python
# Direct call: caller knows exactly who receives data
def process_sensor_data(data):
    return analyze(data)

result = process_sensor_data(sensor_value)  # Tightly coupled
```

**Pub-Sub Pattern** (Decoupled):

```python
# Publisher: Sends data without knowing who receives
publisher.publish(sensor_value)

# Subscriber: Receives data without knowing who sent
def callback(message):
    process(message.data)
subscriber.listen(callback)  # Many subscribers can listen
```

### Key Differences

| Aspect | Direct Function Call | Pub-Sub Pattern |
|--------|---------------------|-----------------|
| **Coupling** | Tightly coupled (caller knows callee) | Loosely coupled (sender doesn't know receivers) |
| **Recipients** | Single recipient | Multiple recipients possible |
| **Timing** | Immediate, synchronous | Decoupled, asynchronous |
| **Knowledge** | Caller must know function exists | Publisher doesn't need to know subscribers exist |
| **Flexibility** | Hard to add new listeners | Easy to add new subscribers |

### Why Pub-Sub Matters for Robots

In robotics, the pub-sub pattern solves real problems:

1. **Sensor fusion**: Multiple nodes might need the same camera data (object detection, navigation, recording). With pub-sub, the camera publishes once, and all interested nodes subscribe.

2. **Hot-swappable components**: Want to try a new navigation algorithm? Replace the navigation node without touching the sensor nodes—they just keep publishing to the same topics.

3. **Parallel processing**: Each node runs as a separate process, utilizing all CPU cores. A blocking computation in one node doesn't stop others from running.

4. **Language independence**: A C++ node can publish to a topic that a Python node subscribes to. ROS 2 handles the translation.

## ROS 2 Nodes: The Building Blocks

A **node** is a standalone executable that uses ROS 2 to communicate with other nodes. Think of each node as one specific job in your robot's software—reading a camera, processing images, controlling motors, or managing battery power.

### Node Properties

Every ROS 2 node has these characteristics:

| Property | Description | Example |
|----------|-------------|---------|
| **Name** | Unique identifier within the ROS 2 system | `camera_node`, `wheel_controller` |
| **Publishers** | Sends data to specific topics | Camera publishes to `/camera/image_raw` |
| **Subscribers** | Receives data from specific topics | Wheel controller subscribes to `/cmd_vel` |
| **Parameters** | Configuration values | `frame_rate: 30`, `resolution: "1920x1080"` |
| **Lifecycle** | Can be started, stopped, and restarted independently | Restart camera node without stopping navigation |

### Visualizing Node Communication

Here's how nodes communicate in a typical robot:

```
+----------------+                    +------------------+
|  Camera Node   |                    |  Display Node    |
|  (Publisher)   |                    |  (Subscriber)    |
|                |                    |                  |
|  Publishes:    |   /camera/image    |  Subscribes to:  |
|  camera data   +------------------->  /camera/image    |
+----------------+                    +------------------+
       |                                       ^
       |                                       |
       v                                       |
+----------------+                    +------------------+
|  Object Detect |                    |  Recording Node  |
|  (Subscriber)  |                    |  (Subscriber)    |
|                |                    |                  |
|  Subscribes to: |   /camera/image   |  Subscribes to:  |
|  /camera/image  <-------------------+  /camera/image   |
+----------------+                    +------------------+

         ONE publisher (camera), THREE subscribers (detect, display, record)
```

**Key insight**: The camera node doesn't know or care who's listening. It just publishes images. New nodes can subscribe to `/camera/image` without any changes to the camera node.

### The Node Lifecycle

Understanding how nodes start, run, and stop is essential for ROS 2 development:

```python
# 1. Initialize ROS 2 communications
rclpy.init()

# 2. Create the node (instantiates your node class)
node = MyNode()

# 3. Spin (process incoming messages and callbacks)
rclpy.spin(node)  # Blocks until shutdown

# 4. Clean shutdown
node.destroy_node()
rclpy.shutdown()
```

**Spinning** is the process where ROS 2 handles incoming messages and executes your callback functions. Without spinning, your node would never receive messages from topics it subscribes to.

## Topics: Named Communication Buses

If nodes are the workers in your robot, **topics** are the communication channels they use. A topic is a named bus over which nodes exchange messages.

### Topic Naming Conventions

Topic names follow hierarchical conventions:

| Topic | Purpose | Naming Pattern |
|-------|---------|----------------|
| `/cmd_vel` | Velocity commands (standard) | Forward slash = global namespace |
| `/camera/image_raw` | Camera images | `/<sensor>/<data_type>` |
| `/robot/joint_states` | Robot joint positions | `/<robot>/<data_type>` |
| `/scan` | LIDAR scan data | Short name for common sensors |
| `~/local_data` | Node-private topic | Tilde = node's private namespace |

**Standard topic names**: ROS 2 defines standard topic names that robots should use. For example, `/cmd_vel` (command velocity) is the universal topic for sending movement commands to mobile robots. Using standard names makes your code compatible with other robots.

### Strong Typing

Unlike generic messaging systems, ROS 2 topics are **strongly typed**. When you create a publisher or subscriber, you must specify the message type:

```python
# Publisher that sends String messages
from std_msgs.msg import String
publisher = node.create_publisher(String, 'chatter', 10)

# Subscriber that receives Image messages
from sensor_msgs.msg import Image
subscriber = node.create_subscription(Image, 'camera/image_raw', callback, 10)
```

If a `String` publisher tries to send to a topic where a subscriber expects `Image` messages, ROS 2 will warn you about the type mismatch. This catches errors at runtime before they cause subtle bugs.

## Common Message Types

ROS 2 provides dozens of standard message types. You'll use these three packages most frequently:

### std_msgs (Basic Types)

| Message Type | Contains | Common Use |
|--------------|----------|------------|
| `String` | `string data` | Text messages, logs |
| `Int32`, `Float32` | `int32 data`, `float32 data` | Single numeric values |
| `Bool` | `bool data` | True/false flags |
| `Header` | `stamp`, `frame_id` | Timestamps and coordinate frames |

### geometry_msgs (Robot Motion)

| Message Type | Contains | Common Use |
|--------------|----------|------------|
| `Twist` | Linear (x,y,z) and angular (x,y,z) velocity | Movement commands (`/cmd_vel`) |
| `Pose` | Position (x,y,z) and orientation (quaternion) | Robot location and facing direction |
| `Vector3` | x, y, z values | 3D coordinates, forces |
| `Transform` | Translation, rotation | Coordinate frame transforms |

### sensor_msgs (Sensor Data)

| Message Type | Contains | Common Use |
|--------------|----------|------------|
| `Image` | Image data, encoding, dimensions | Camera images |
| `LaserScan` | Angle ranges, distance measurements | LIDAR scans (`/scan`) |
| `Imu` | Orientation, angular velocity, linear acceleration | IMU data (gyroscope, accelerometer) |
| `JointState` | Position, velocity, effort for each joint | Robot arm/leg joint feedback |

**Finding message types**: Use the `ros2 interface show` command to see what fields a message type contains:

```bash
ros2 interface show geometry_msgs/msg/Twist
```

**Output:**
```
# This expresses velocity in free space broken into its linear and angular parts.
Vector3  linear
Vector3  angular
```

## Creating Your First Publisher

Now let's create a working ROS 2 publisher node. This node will publish string messages to a topic called `/chatter`.

### Step 1: Set Up Your Workspace

First, ensure your ROS 2 workspace is properly set up:

```bash
# Source ROS 2 (do this in every new terminal)
source /opt/ros/humble/setup.bash

# Navigate to your workspace
cd ~/ros2_ws/src

# Create a new package
ros2 pkg create --build-type ament_python my_robot_package --dependencies rclpy std_msgs
```

### Step 2: Write the Publisher Code

Create a file `my_robot_package/my_robot_package/talker.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TalkerNode(Node):
    """A simple ROS 2 publisher that sends messages periodically."""

    def __init__(self):
        # Initialize the node with a unique name
        super().__init__('talker_node')

        # Create a publisher
        # Arguments: message type, topic name, queue size (QoS depth)
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        # Create a timer that triggers the callback every 0.5 seconds
        self.timer = self.create_timer(0.5, self.timer_callback)

        # Counter to increment messages
        self.count = 0

        self.get_logger().info('Talker node started, publishing to /chatter')

    def timer_callback(self):
        """Called every 0.5 seconds by the timer."""
        msg = String()

        # Set the message data
        msg.data = f'Hello, ROS 2! Count: {self.count}'

        # Publish the message
        self.publisher_.publish(msg)

        # Log what we published (useful for debugging)
        self.get_logger().info(f'Publishing: "{msg.data}"')

        self.count += 1

def main(args=None):
    # Initialize ROS 2 communications
    rclpy.init(args=args)

    # Create and spin the node
    talker = TalkerNode()

    try:
        rclpy.spin(talker)  # Keeps node alive, processing callbacks
    except KeyboardInterrupt:
        pass
    finally:
        # Clean shutdown
        talker.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Step 3: Register the Node

Edit `my_robot_package/setup.py` to register your node as an executable:

```python
entry_points={
    'console_scripts': [
        'talker = my_robot_package.talker:main',
    ],
},
```

### Step 4: Build and Run

```bash
# Build your package
cd ~/ros2_ws
colcon build --packages-select my_robot_package

# Source the workspace (required after building)
source install/setup.bash

# Run your publisher node
ros2 run my_robot_package talker
```

**Output:**
```
[INFO] [talker_node]: Talker node started, publishing to /chatter
[INFO] [talker_node]: Publishing: "Hello, ROS 2! Count: 0"
[INFO] [talker_node]: Publishing: "Hello, ROS 2! Count: 1"
[INFO] [talker_node]: Publishing: "Hello, ROS 2! Count: 2"
...
```

### Step 5: Verify with ros2 echo

Open a **new terminal** (keep the publisher running) and verify messages are being sent:

```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /chatter
```

**Output:**
```
data: 'Hello, ROS 2! Count: 0'
---
data: 'Hello, ROS 2! Count: 1'
---
data: 'Hello, ROS 2! Count: 2'
---
```

You now have a working ROS 2 publisher! The messages flow from your `talker` node to any subscriber listening on `/chatter`.

## Creating Your First Subscriber

Now let's create a subscriber that receives and processes the messages from your publisher.

### Write the Subscriber Code

Create `my_robot_package/my_robot_package/listener.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ListenerNode(Node):
    """A simple ROS 2 subscriber that receives and prints messages."""

    def __init__(self):
        # Initialize the node
        super().__init__('listener_node')

        # Create a subscription
        # Arguments: message type, topic name, callback function, queue size
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )

        self.get_logger().info('Listener node started, waiting for messages...')

    def listener_callback(self, msg):
        """Called whenever a new message arrives on /chatter."""
        # Process the received message
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    listener = ListenerNode()

    try:
        rclpy.spin(listener)  # Keeps node alive, processing callbacks
    except KeyboardInterrupt:
        pass
    finally:
        listener.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Register the listener in `setup.py`:

```python
entry_points={
    'console_scripts': [
        'talker = my_robot_package.talker:main',
        'listener = my_robot_package.listener:main',
    ],
},
```

Rebuild and run both nodes:

```bash
# Terminal 1: Publisher
source ~/ros2_ws/install/setup.bash
ros2 run my_robot_package talker

# Terminal 2: Subscriber
source ~/ros2_ws/install/setup.bash
ros2 run my_robot_package listener
```

**Output (listener terminal):**
```
[INFO] [listener_node]: Listener node started, waiting for messages...
[INFO] [listener_node]: I heard: "Hello, ROS 2! Count: 0"
[INFO] [listener_node]: I heard: "Hello, ROS 2! Count: 1"
[INFO] [listener_node]: I heard: "Hello, ROS 2! Count: 2"
...
```

**What's happening**: Your `talker` node publishes messages to `/chatter`. Your `listener` node has a subscription to `/chatter`. ROS 2's middleware (DDS) delivers the messages from publisher to subscriber, and your `listener_callback` function processes each message.

## Test Publisher and Subscriber Together

ROS 2 provides useful command-line tools for debugging topics:

### List Active Topics

```bash
ros2 topic list
```

**Output:**
```
/chatter
/clock
/parameter_events
/rosout
```

### Get Topic Information

```bash
ros2 topic info /chatter
```

**Output:**
```
Subscription count: 2
Node count: 1
  - /talker_node
```

### Monitor Message Rate

```bash
ros2 topic hz /chatter
```

**Output:**
```
average rate: 2.000
    min: 0.500s max: 0.501s std dev: 0.00031s window: 10
average rate: 2.000
    min: 0.500s max: 0.501s std dev: 0.00031s window: 10
...
```

This shows your publisher is sending messages at 2 Hz (every 0.5 seconds), as configured.

## A Practical Example: Robot Velocity Commands

Let's build something more practical: a node that sends movement commands to a robot. We'll use the standard `/cmd_vel` topic with `geometry_msgs/Twist` messages.

### Understanding Twist Messages

The `Twist` message type expresses velocity in 3D space:

```python
from geometry_msgs.msg import Twist

msg = Twist()

# Linear velocity (forward/backward, left/right, up/down)
msg.linear.x = 0.5   # Forward at 0.5 m/s
msg.linear.y = 0.0   # No sideways motion
msg.linear.z = 0.0   # No vertical motion

# Angular velocity (rotation around each axis)
msg.angular.x = 0.0  # No roll
msg.angular.y = 0.0  # No pitch
msg.angular.z = 0.3  # Turn left at 0.3 rad/s
```

**Key values for mobile robots**:
- `linear.x > 0`: Move forward
- `linear.x < 0`: Move backward
- `angular.z > 0`: Rotate left (counter-clockwise)
- `angular.z < 0`: Rotate right (clockwise)

### Velocity Command Publisher

Create a node that sends velocity commands:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class VelocityPublisher(Node):
    """Publishes velocity commands to make a robot drive in a circle."""

    def __init__(self):
        super().__init__('velocity_publisher')

        # Create publisher for velocity commands
        self.vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Timer for sending commands at 10 Hz
        self.timer = self.create_timer(0.1, self.publish_velocity)

        self.start_time = self.get_clock().now()
        self.get_logger().info('Velocity publisher started')

    def publish_velocity(self):
        """Send velocity commands to drive in a circle."""
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        msg = Twist()

        # Drive forward at 0.2 m/s
        msg.linear.x = 0.2
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        # Turn slowly to create a circle
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.5  # Turn at 0.5 rad/s

        # Publish the command
        self.vel_publisher.publish(msg)

        self.get_logger().info(
            f'Sending: linear.x={msg.linear.x} m/s, '
            f'angular.z={msg.angular.z} rad/s'
        )

def main(args=None):
    rclpy.init(args=args)
    velocity_pub = VelocityPublisher()

    try:
        rclpy.spin(velocity_pub)
    except KeyboardInterrupt:
        # Send stop command before exiting
        stop_msg = Twist()
        velocity_pub.vel_publisher.publish(stop_msg)
        velocity_pub.get_logger().info('Sent stop command')
    finally:
        velocity_pub.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [velocity_publisher]: Velocity publisher started
[INFO] [velocity_publisher]: Sending: linear.x=0.2 m/s, angular.z=0.5 rad/s
[INFO] [velocity_publisher]: Sending: linear.x=0.2 m/s, angular.z=0.5 rad/s
...
```

If you had a real robot (or a simulator like Gazebo) running, this code would make the robot drive in a circle: forward motion + continuous turning = circular path.

## Debugging ROS 2 Communication

When working with topics, you'll encounter situations where messages don't arrive as expected. Here's a systematic debugging approach:

### Debug Checklist

1. **Check if the topic exists**: `ros2 topic list`
   - If your topic isn't listed, the publisher isn't running or has an error

2. **Check topic info**: `ros2 topic info /your_topic`
   - Shows how many publishers and subscribers are connected

3. **Verify message type**: `ros2 topic info /your_topic -v`
   - Shows the exact message type required

4. **Monitor messages**: `ros2 topic echo /your_topic`
   - See actual messages being published

5. **Check node logs**: `ros2 node list` then `ros2 node info /your_node`
   - Shows what topics the node publishes/subscribes

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| No messages received | Publisher not running | Start publisher, check with `ros2 node list` |
| Type mismatch error | Publisher/subscriber have different message types | Ensure both use same type (e.g., `String` vs `Int32`) |
| Messages arrive but are garbled | Serialization issue | Check that both nodes use same ROS 2 distribution |
| High CPU usage | No spinning or wrong timer rate | Ensure `rclpy.spin()` is called |

## Multiple Subscribers: The Power of Pub-Sub

The real power of the publish-subscribe pattern becomes apparent when you have multiple subscribers. Let's modify our example to have three different nodes all listening to `/chatter`.

### Subscriber 1: Message Counter

```python
class CounterNode(Node):
    """Counts how many messages it receives."""
    def __init__(self):
        super().__init__('counter_node')
        self.count = 0
        self.subscription = self.create_subscription(
            String, 'chatter', self.count_callback, 10
        )

    def count_callback(self, msg):
        self.count += 1
        self.get_logger().info(f'Received {self.count} messages total')
```

### Subscriber 2: Message Logger

```python
class LoggerNode(Node):
    """Logs messages to a file."""
    def __init__(self):
        super().__init__('logger_node')
        self.subscription = self.create_subscription(
            String, 'chatter', self.log_callback, 10
        )
        self.file = open('messages.log', 'w')

    def log_callback(self, msg):
        timestamp = self.get_clock().now().to_msg()
        self.file.write(f'{timestamp.sec}.{timestamp.nanosec}: {msg.data}\n')
        self.file.flush()
```

### Subscriber 3: Message Transformer

```python
class TransformerNode(Node):
    """Transforms messages and publishes to a different topic."""
    def __init__(self):
        super().__init__('transformer_node')
        self.input_sub = self.create_subscription(
            String, 'chatter', self.transform_callback, 10
        )
        self.output_pub = self.create_publisher(String, 'chatter_uppercase', 10)

    def transform_callback(self, msg):
        # Transform: convert to uppercase
        transformed_msg = String()
        transformed_msg.data = msg.data.upper()
        self.output_pub.publish(transformed_msg)
```

**Key insight**: Each subscriber processes the same data independently. The publisher doesn't know or care that three different nodes are using its messages. Add a fourth subscriber? No changes needed to the publisher. This is the flexibility that makes ROS 2 scalable for complex robot systems.

## Try With AI

### Exercise 1: Design a Robot Node Architecture

```text
I'm learning ROS 2 topics and nodes. I need to design a robot's software architecture.

The robot has these components:
- Camera (provides images)
- LIDAR (provides distance scans)
- Object detection AI (processes images)
- Navigation system (plans paths)
- Motor controller (drives wheels)
- Battery monitor (reports power level)

Design a node architecture using ROS 2 topics. For each component, specify:
1. What topics it publishes to
2. What topics it subscribes to
3. What message types it uses (std_msgs, geometry_msgs, sensor_msgs)

Show the data flow from sensors to motors.
```

**What you're learning:** This exercise reinforces your understanding of how nodes and topics connect in a real robot system. By designing an architecture, you'll practice selecting appropriate message types and structuring communication flows. This design thinking is essential before writing any ROS 2 code—you need to plan how your nodes will interact.

### Exercise 2: Debug a Broken ROS 2 System

```text
I have a ROS 2 system where a camera node publishes to /camera/image and a display node subscribes to /camera/image.

The camera node starts without errors and says "Publishing to /camera/image".
The display node starts but never shows any images.

When I run:
- ros2 topic list: I see /camera/image listed
- ros2 topic info /camera/image: Shows 1 publisher and 1 subscriber
- ros2 topic echo /camera/image: I see NO output (empty)

What are 3-4 possible causes for this problem, and how would I debug each one?
```

**What you're learning:** Debugging is a critical skill in robotics development. This exercise teaches you systematic troubleshooting: when something doesn't work, you need to generate hypotheses, test each one, and isolate the root cause. You'll learn about common ROS 2 issues like QoS mismatches, message type errors, and node lifecycle problems.

### Exercise 3: Create a Bidirectional Node

```text
I want to create a ROS 2 node that is BOTH a publisher AND a subscriber (called a "transform" node).

This node should:
1. Subscribe to /cmd_vel (geometry_msgs/Twist)
2. Double the linear and angular velocity values
3. Publish the transformed values to /cmd_vel_doubled

Write the complete Python code for this node using rclpy. Include:
- Proper node initialization
- Publisher setup with correct message type
- Subscriber setup with callback function
- The transformation logic in the callback
- Proper cleanup on shutdown

Also explain: Does this node need to spin? Why or why not?
```

**What you're learning:** This exercise teaches you about bidirectional nodes that consume data, process it, and produce output—a pattern used throughout robotics (sensor processing, command filtering, data transformation). You'll also reinforce your understanding of the spinning mechanism and when it's required. This is a stepping stone to more complex robot behaviors where nodes chain together to form processing pipelines.