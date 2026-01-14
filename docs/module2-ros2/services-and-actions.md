---
sidebar_position: 3
title: "ROS 2 Services and Actions"
description: "Learn ROS 2 Services for synchronous request-response communication and Actions for long-running tasks with feedback. Master when to use each communication pattern."
keywords: ["ROS 2", "Services", "Actions", "Request-Response", "Synchronous", "Asynchronous", "rclpy"]
chapter: 2
lesson: 3
duration_minutes: 90

requirements:
  hardware: "Any computer with ROS 2 Humble installed"
  software: "ROS 2 Humble, Python 3 (rclpy)"

skills:
  - name: "ROS 2 Service Communication"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Programming"
    measurable_at_this_level: "Student can implement a service server and client from specification"

  - name: "ROS 2 Action Communication"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Programming"
    measurable_at_this_level: "Student can implement an action server and client with feedback handling"

  - name: "Communication Pattern Selection"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Analyze"
    digcomp_area: "Problem Solving"
    measurable_at_this_level: "Student can choose appropriate communication pattern (topic/service/action) for given requirements"

learning_objectives:
  - objective: "Implement a ROS 2 service server that responds to synchronous requests and a client that sends requests and receives responses"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code exercise: Create add_two_ints server and client with verified output"

  - objective: "Explain the differences between topics, services, and actions, and select the appropriate communication pattern for specific robot control scenarios"
    proficiency_level: "B1"
    bloom_level: "Analyze"
    assessment_method: "Scenario analysis: Match communication pattern to use case with justification"

  - objective: "Implement a ROS 2 action server that provides feedback during long-running tasks and a client that monitors progress"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code exercise: Create navigation action server with periodic feedback updates"

cognitive_load:
  new_concepts: 9
  assessment: "Students will implement a service server/client pair and an action server/client pair, plus analyze scenarios to select appropriate communication patterns"

differentiation:
  extension_for_advanced: "Implement a service that uses custom data types with multiple fields, or create an action server with preemption (canceling running tasks)"
  remedial_for_struggling: "Start with the provided template code and modify only the callback logic. Focus on understanding the request-response flow before adding complexity"
  hardware_alternatives: "All exercises run in simulation. Use ROS 2 Humble on Ubuntu 22.04 (native, WSL2, or Docker). No physical robot required"

safety_notes: "No physical hardware required. When working with real robots later, ensure emergency stop is accessible before testing motion commands"

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# ROS 2 Services and Actions

Imagine you're controlling a robot arm to pick up an object. With topics (the publish-subscribe pattern you learned about), the robot arm node would continuously broadcast its position, and your control node would send motor commands. But what if you need to ask the robot arm a specific question and get a specific answer? "What's your current joint angle?" or "Move to position X and tell me when you're done."

Topics aren't designed for this question-answer pattern. They're great for streaming data, but not for request-response communication. That's where ROS 2 **Services** and **Actions** come in.

**Services** provide synchronous request-response communication: you ask a question, you wait for an answer. **Actions** handle long-running tasks with progress feedback: you start a task, get updates while it runs, and receive the final result. Together with topics, these three communication patterns form the foundation of ROS 2 robotics programming.

## Communication Patterns: When to Use What

Before diving into implementation, let's understand when each pattern makes sense. Choosing the wrong communication pattern is a common source of bugs in robotic systems.

### Comparison: Topics vs Services vs Actions

| Aspect | Topics | Services | Actions |
|--------|--------|----------|---------|
| **Communication** | One-way (stream) | Request-Response | Request-Feedback-Result |
| **Synchronous** | No (asynchronous) | Yes (blocking) | No (async with feedback) |
| **Use When** | Streaming data | Quick queries | Long-running tasks |
| **Examples** | Camera images, LIDAR scans | Get robot state, take snapshot | Navigation, grasping |
| **Response** | May never come | Guaranteed (or error) | Guaranteed with progress |
| **Cancellation** | Not applicable | Not applicable | Yes (preempt) |

### Decision Guide

**Use TOPICS when:**
- Data flows continuously (sensor readings, motor commands)
- Multiple nodes need the same data
- Timing matters more than reliability (losing some frames is okay)
- One-to-many communication (publisher to multiple subscribers)

**Use SERVICES when:**
- You need a specific answer to a specific question
- The operation completes quickly (milliseconds to seconds)
- You need to know if the request succeeded or failed
- One-to-one communication (client to server)

**Use ACTIONS when:**
- The task takes time (seconds to minutes)
- You need progress updates during execution
- You might want to cancel the task mid-execution
- The task has a clear goal and final result

### Real-World Example: Robot Navigation

A robot navigating to a goal location uses all three patterns:

```python
# 1. TOPIC: Continuous sensor data
/camera/image_raw    # Camera publishes images continuously
/lidar/scan          # LIDAR publishes distance measurements

# 2. SERVICE: Quick queries
/get_robot_state     # Ask: "Are you moving?" → Answer: "Yes/No"
/get_map_metadata    # Ask: "What's the map resolution?" → Answer: "0.05 m/pixel"

# 3. ACTION: Long-running navigation
/navigate_to_goal    # Start: "Go to (5, 3)"
                     # Feedback: "Progress: 60%, distance remaining: 2.1m"
                     # Result: "Reached successfully"
```

The navigation action might take 30 seconds to complete. During that time, you receive continuous feedback about progress. If the goal becomes irrelevant (user changed their mind), you can cancel the action mid-execution—something topics and services can't do.

## ROS 2 Services: Synchronous Request-Response

A **Service** in ROS 2 is like a function call across different nodes (or even different computers). The service server provides a capability, and service clients request that capability.

### Service Architecture

```
Client Node                  Server Node
    |                            |
    | ----- Request --------->   |
    |   "What's the time?"       |
    |                            |
    |                            | [Process request]
    |                            |
    | <---- Response ---------   |
    |   "12:34:56"               |
    |                            |
```

**Key characteristics:**
- **Blocking**: The client waits for the response (cannot do other work)
- **One-to-one**: One request gets one response from one server
- **Reliable**: You get a response or an error, no "maybe"
- **Stateful**: The server can maintain state between requests

### Creating a Service Definition

Services use `.srv` files to define the request and response data structures. These live in a `srv/` folder in your ROS 2 package:

```bash
# File: my_robot_package/srv/GetBatteryStatus.srv
# Request (empty—we're just asking for status)
---
# Response
float32 percentage
bool charging
int32 minutes_remaining
string status_message
```

The `---` separates the request (top) from the response (bottom). This service takes no request data and returns battery information.

### Implementing a Service Server

Let's create a service server that reports a robot's battery status:

```python
# battery_service_server.py
import rclpy
from rclpy.node import Node
from my_robot_package.srv import GetBatteryStatus

class BatteryServiceServer(Node):
    """Service server that provides robot battery status."""

    def __init__(self):
        super().__init__('battery_service_server')

        # Create the service
        # 'get_battery_status' is the service name
        # GetBatteryStatus is the service type
        self.srv = self.create_service(
            GetBatteryStatus,
            'get_battery_status',
            self.get_battery_status_callback
        )

        # Simulate battery state
        self.battery_percentage = 78.5
        self.is_charging = False

        self.get_logger().info('Battery Service Server ready')

    def get_battery_status_callback(self, request, response):
        """
        Called when a client requests battery status.

        Args:
            request: The service request (empty in this case)
            response: The service response object to fill in

        Returns:
            The completed response
        """
        self.get_logger().info('Incoming battery status request')

        # Fill in the response
        response.percentage = self.battery_percentage
        response.charging = self.is_charging
        response.minutes_remaining = int(self.battery_percentage * 2.5)

        # Set status message based on battery level
        if self.battery_percentage > 50:
            response.status_message = "Battery healthy"
        elif self.battery_percentage > 20:
            response.status_message = "Battery low - consider charging"
        else:
            response.status_message = "Battery critical - charge immediately"

        return response

def main(args=None):
    rclpy.init(args=args)
    battery_server = BatteryServiceServer()

    try:
        rclpy.spin(battery_server)
    except KeyboardInterrupt:
        pass
    finally:
        battery_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [battery_service_server]: Battery Service Server ready
[INFO] [battery_service_server]: Incoming battery status request
[INFO] [battery_service_server]: Incoming battery status request
```

### Implementing a Service Client

Now let's create a client that requests battery status from the server:

```python
# battery_service_client.py
import rclpy
from rclpy.node import Node
from my_robot_package.srv import GetBatteryStatus

class BatteryServiceClient(Node):
    """Service client that requests robot battery status."""

    def __init__(self):
        super().__init__('battery_service_client')

        # Create the client
        # 'get_battery_status' must match the server's service name
        self.cli = self.create_client(GetBatteryStatus, 'get_battery_status')

        # Wait for the service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for battery service server...')

        self.get_logger().info('Battery Service Client connected')

    def send_request(self):
        """Send a request to get battery status."""
        # Create a request object
        request = GetBatteryStatus.Request()

        # Send request asynchronously
        # This returns a future that will contain the response
        self.future = self.cli.call_async(request)

        # Spin until we get the response
        rclpy.spin_until_future_complete(self, self.future)

        # Get the response
        response = self.future.result()

        # Display the results
        self.get_logger().info('Battery Status Received:')
        self.get_logger().info(f'  Percentage: {response.percentage}%')
        self.get_logger().info(f'  Charging: {response.charging}')
        self.get_logger().info(f'  Time Remaining: {response.minutes_remaining} minutes')
        self.get_logger().info(f'  Status: {response.status_message}')

        return response

def main(args=None):
    rclpy.init(args=args)
    client = BatteryServiceClient()

    try:
        # Send one request
        client.send_request()
    except KeyboardInterrupt:
        pass
    finally:
        client.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [battery_service_client]: Waiting for battery service server...
[INFO] [battery_service_client]: Battery Service Client connected
[INFO] [battery_service_client]: Battery Status Received:
[INFO] [battery_service_client]:   Percentage: 78.5%
[INFO] [battery_service_client]:   Charging: False
[INFO] [battery_service_client]:   Time Remaining: 196 minutes
[INFO] [battery_service_client]:   Status: Battery healthy
```

### Synchronous vs Asynchronous Service Calls

The example above uses `call_async()` with `spin_until_future_complete()`, which blocks until the response arrives. This is **asynchronous at the network level** (non-blocking I/O) but **synchronous for your code** (waits for response).

For truly asynchronous service calls (where your node can do other work while waiting):

```python
def send_request_async(self):
    """Send request and do other work while waiting."""
    request = GetBatteryStatus.Request()
    future = self.cli.call_async(request)

    # Register a callback when response arrives
    future.add_done_callback(self.response_callback)

    # Node continues spinning, can do other work
    self.get_logger().info('Request sent, continuing work...')

def response_callback(self, future):
    """Called when response arrives."""
    response = future.result()
    self.get_logger().info(f'Got response: {response.percentage}%')
```

This pattern is useful when your node needs to remain responsive while waiting for service calls.

### Common Service Use Cases in Robotics

| Use Case | Service Name | Description |
|----------|--------------|-------------|
| **Robot State** | `/get_robot_state` | Query if robot is moving, error states |
| **Map Services** | `/save_map`, `/load_map` | Save navigation map to disk |
| **Camera** | `/take_snapshot` | Capture single image (vs video stream on topic) |
| **Localization** | `/global_localization` | Ask robot: "Where are you?" |
| **Configuration** | `/set_parameters` | Change robot behavior parameters |

## ROS 2 Actions: Long-Running Tasks with Feedback

Services work well for quick operations, but they have limitations for long-running tasks:

1. **No progress updates**: Client waits blindly until response arrives
2. **No cancellation**: Once requested, you must wait for completion
3. **Timeout issues**: Long-running services may exceed timeout limits

**Actions** solve these problems by providing:
- **Goal**: The task to accomplish
- **Feedback**: Periodic updates during execution
- **Result**: Final outcome when task completes
- **Cancel**: Ability to abort mid-execution

### Action Architecture

```
Client Node                  Action Server
    |                            |
    | ----- Goal ------------->  |
    |   "Navigate to (5, 3)"     |
    |                            |
    | <---- Feedback ------------| (repeated during execution)
    |   "Progress: 30%"          |
    | <---- Feedback ------------|
    |   "Progress: 60%"          |
    | <---- Feedback ------------|
    |   "Progress: 90%"          |
    |                            |
    | <---- Result ------------- |
    |   "Success: Reached goal"  |
```

### Creating an Action Definition

Actions use `.action` files with three sections separated by `---`:

```bash
# File: my_robot_package/action/NavigateToGoal.action
# Goal (what we want to accomplish)
float64 target_x
float64 target_y
float64 target_theta  # Orientation angle
---
# Result (final outcome)
bool success
string message
float64 final_x
float64 final_y
float64 final_theta
---
# Feedback (periodic updates during execution)
float32 percent_complete
float64 current_x
float64 current_y
float64 distance_remaining
```

### Implementing an Action Server

Let's create an action server that simulates robot navigation:

```python
# navigate_action_server.py
import time
import math
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from my_robot_package.action import NavigateToGoal

class NavigateActionServer(Node):
    """Action server for robot navigation with feedback."""

    def __init__(self):
        super().__init__('navigate_action_server')

        # Create the action server
        self._action_server = ActionServer(
            self,
            NavigateToGoal,
            'navigate_to_goal',
            self.execute_callback
        )

        # Simulate robot starting position
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        self.get_logger().info('Navigate Action Server ready')

    def execute_callback(self, goal_handle):
        """
        Called when a client sends a navigation goal.

        Args:
            goal_handle: Contains the goal and manages the action lifecycle
        """
        self.get_logger().info('Received navigation goal')

        # Extract goal parameters
        target_x = goal_handle.request.target_x
        target_y = goal_handle.request.target_y
        target_theta = goal_handle.request.target_theta

        self.get_logger().info(
            f'Navigating to: x={target_x}, y={target_y}, theta={target_theta}'
        )

        # Simulate navigation with periodic feedback
        feedback_msg = NavigateToGoal.Feedback()
        start_time = time.time()
        total_distance = math.sqrt(target_x**2 + target_y**2)

        # Simulation: 100 steps to reach goal
        for step in range(1, 101):
            # Check if client canceled the action
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result = NavigateToGoal.Result()
                result.success = False
                result.message = "Navigation canceled by user"
                return result

            # Update simulated position
            progress = step / 100.0
            self.current_x = target_x * progress
            self.current_y = target_y * progress
            self.current_theta = target_theta * progress

            # Calculate remaining distance
            distance_remaining = total_distance * (1 - progress)

            # Send feedback
            feedback_msg.percent_complete = int(progress * 100)
            feedback_msg.current_x = self.current_x
            feedback_msg.current_y = self.current_y
            feedback_msg.distance_remaining = distance_remaining

            goal_handle.publish_feedback(feedback_msg)

            self.get_logger().info(
                f'Feedback: {feedback_msg.percent_complete}% complete, '
                f'{distance_remaining:.2f}m remaining'
            )

            # Simulate work (sleep)
            time.sleep(0.05)  # 5 seconds total for 100 steps

        # Goal succeeded
        goal_handle.succeed()

        # Prepare result
        result = NavigateToGoal.Result()
        result.success = True
        result.message = "Navigation completed successfully"
        result.final_x = target_x
        result.final_y = target_y
        result.final_theta = target_theta

        self.get_logger().info(f'Goal succeeded: {result.message}')

        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = NavigateActionServer()

    try:
        rclpy.spin(action_server)
    except KeyboardInterrupt:
        pass
    finally:
        action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [navigate_action_server]: Navigate Action Server ready
[INFO] [navigate_action_server]: Received navigation goal
[INFO] [navigate_action_server]: Navigating to: x=5.0, y=3.0, theta=1.57
[INFO] [navigate_action_server]: Feedback: 1% complete, 5.83m remaining
[INFO] [navigate_action_server]: Feedback: 2% complete, 5.72m remaining
[INFO] [navigate_action_server]: Feedback: 3% complete, 5.60m remaining
...
[INFO] [navigate_action_server]: Feedback: 98% complete, 0.12m remaining
[INFO] [navigate_action_server]: Feedback: 99% complete, 0.06m remaining
[INFO] [navigate_action_server]: Feedback: 100% complete, 0.00m remaining
[INFO] [navigate_action_server]: Goal succeeded: Navigation completed successfully
```

### Implementing an Action Client

Now let's create a client that sends navigation goals and receives feedback:

```python
# navigate_action_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from my_robot_package.action import NavigateToGoal

class NavigateActionClient(Node):
    """Action client for robot navigation."""

    def __init__(self):
        super().__init__('navigate_action_client')

        # Create the action client
        self._action_client = ActionClient(
            self,
            NavigateToGoal,
            'navigate_to_goal'
        )

    def send_goal(self, x, y, theta):
        """Send a navigation goal and monitor progress."""
        self.get_logger().info('Waiting for action server...')

        # Wait for server to be available
        self._action_client.wait_for_server()

        # Create the goal
        goal_msg = NavigateToGoal.Goal()
        goal_msg.target_x = x
        goal_msg.target_y = y
        goal_msg.target_theta = theta

        self.get_logger().info(f'Sending goal: x={x}, y={y}, theta={theta}')

        # Send goal asynchronously
        # 'send_goal_async' returns a future for the goal handle
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        # Register callback for when goal is accepted/rejected
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Called when the action server accepts or rejects the goal."""
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        # Request the result
        # This returns a future that completes when the action finishes
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """Called periodically during action execution."""
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Feedback: {feedback.percent_complete}% complete, '
            f'Current position: ({feedback.current_x:.2f}, {feedback.current_y:.2f}), '
            f'{feedback.distance_remaining:.2f}m remaining'
        )

    def get_result_callback(self, future):
        """Called when the action completes."""
        result = future.result().result
        self.get_logger().info(f'Result: {result.message}')
        self.get_logger().info(
            f'Final position: ({result.final_x:.2f}, {result.final_y:.2f}, '
            f'theta={result.final_theta:.2f})'
        )

        # Shutdown after receiving result
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)

    client = NavigateActionClient()

    # Send a navigation goal
    client.send_goal(x=5.0, y=3.0, theta=1.57)

    # Spin until action completes (shutdown called in callback)
    rclpy.spin(client)

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [navigate_action_client]: Waiting for action server...
[INFO] [navigate_action_client]: Sending goal: x=5.0, y=3.0, theta=1.57
[INFO] [navigate_action_client]: Goal accepted :)
[INFO] [navigate_action_client]: Feedback: 1% complete, Current position: (0.05, 0.03), 5.83m remaining
[INFO] [navigate_action_client]: Feedback: 2% complete, Current position: (0.10, 0.06), 5.72m remaining
[INFO] [navigate_action_client]: Feedback: 3% complete, Current position: (0.15, 0.09), 5.60m remaining
...
[INFO] [navigate_action_client]: Feedback: 98% complete, Current position: (4.90, 2.94), 0.12m remaining
[INFO] [navigate_action_client]: Feedback: 99% complete, Current position: (4.95, 2.97), 0.06m remaining
[INFO] [navigate_action_client]: Result: Navigation completed successfully
[INFO] [navigate_action_client]: Final position: (5.00, 3.00, theta=1.57)
```

### Canceling an Action

One of the key advantages of actions is the ability to cancel mid-execution:

```python
def cancel_goal(self):
    """Cancel the currently running goal."""
    if self._goal_handle is not None:
        self._goal_handle.cancel_goal_async()
        self.get_logger().info('Canceling goal...')
```

Use cases for cancellation:
- User presses emergency stop
- A new, higher-priority goal arrives
- Sensor data shows an obstacle
- Battery level drops critically low

### Common Action Use Cases in Robotics

| Use Case | Action Name | Description |
|----------|-------------|-------------|
| **Navigation** | `/navigate_to_pose` | Move robot to location with progress updates |
| **Grasping** | `/grasp_object` | Plan and execute grasp with feedback |
| **Mapping** | `/build_map` | Create environment map (long-running) |
| **Inspection** | `/perform_inspection` | Follow inspection waypoints |
| **Docking** | `/dock_robot` | Navigate to charging station |

## Debugging Services and Actions

ROS 2 provides command-line tools to inspect and test services and actions without writing code.

### Service CLI Tools

```bash
# List all available services
ros2 service list

# List services with types
ros2 service list -t

# Get service type details
ros2 service type /get_battery_status

# Show service interface (request and response structure)
ros2 interface show my_robot_package/srv/GetBatteryStatus

# Call a service from command line
ros2 service call /get_battery_status my_robot_package/srv/GetBatteryStatus '{}'
```

### Action CLI Tools

```bash
# List all available actions
ros2 action list

# List actions with types
ros2 action list -t

# Get action type details
ros2 action type /navigate_to_goal

# Show action interface (goal, result, feedback)
ros2 interface show my_robot_package/action/NavigateToGoal

# Send an action goal from command line
ros2 action send_goal /navigate_to_goal my_robot_package/action/NavigateToGoal \
  "{target_x: 5.0, target_y: 3.0, target_theta: 1.57}" \
  --feedback
```

## Common Mistakes to Avoid

### Mistake 1: Using Services for Long-Running Tasks

**Problem**: Service blocks while executing. A navigation task taking 30 seconds blocks the client.

```python
# WRONG: Navigation as a service
def navigate_callback(self, request, response):
    # This blocks for 30 seconds!
    self.navigate_to_goal(request.x, request.y)
    response.success = True
    return response
```

**Correct**: Use actions for long-running tasks with feedback.

### Mistake 2: Forgetting to Spin While Waiting for Services

**Problem**: Client creates service but never spins, so callbacks never execute.

```python
# WRONG: No spinning
self.cli = self.create_client(GetBatteryStatus, 'get_battery_status')
# Missing: rclpy.spin_some(self) or similar
response = self.cli.call_async(request)
```

**Correct**: Always spin the node while waiting for async operations.

### Mistake 3: Not Handling Service Availability

**Problem**: Client crashes if service doesn't exist.

```python
# WRONG: Assume service exists
self.cli.call_async(request)  # Crashes if server not running
```

**Correct**: Wait for service with timeout.

```python
# RIGHT: Wait with timeout
if not self.cli.wait_for_service(timeout_sec=5.0):
    self.get_logger().error('Service not available!')
    return
```

## Simulation Exercise: Robot Battery Monitor

Let's put it all together. We'll create a complete robotic system using topics, services, and actions together.

### System Architecture

```
+-------------------+     /battery_state     +---------------------+
|  Battery Monitor  | <====================  |   Robot Hardware    |
|   (Publisher)     |      (Topic)          |     (Simulation)    |
+-------------------+                       +---------------------+
        ^
        |
        | /get_battery_status
        | (Service)
        |
+-------------------+     /navigate_to_goal  +---------------------+
|  Control Panel    | ====================> |   Navigation        |
|    (Client)       |      (Action)         |   (Action Server)   |
+-------------------+                       +---------------------+
```

### Running the Complete System

```bash
# Terminal 1: Start battery monitor (topic publisher)
ros2 run my_robot_package battery_monitor_node

# Terminal 2: Start battery service server
ros2 run my_robot_package battery_service_server

# Terminal 3: Start navigation action server
ros2 run my_robot_package navigate_action_server

# Terminal 4: Run control panel (tests all three patterns)
ros2 run my_robot_package control_panel
```

## Try With AI

### Exercise 1: Design Robot Communication Architecture

```
I'm designing a warehouse robot that needs to:

1. Continuously report its position to a central system
2. Accept commands to pick up items from specific shelf locations
3. Provide progress updates during pickup tasks (driving, reaching, grasping)
4. Answer queries about its current battery level and load capacity
5. Allow cancellation of pickup tasks if a higher-priority order arrives

For each requirement, recommend whether to use Topics, Services, or Actions. Explain your reasoning with specific details about:
- Why that pattern fits the requirement
- What message types would be needed
- Any potential issues with the chosen approach

After your recommendations, identify any scenarios where my choices might be wrong or where a different pattern would be better.
```

**What you're learning:** This exercise develops your ability to analyze requirements and select appropriate communication patterns—the core architectural skill for ROS 2 systems. By explaining your reasoning, you'll deepen your understanding of when each pattern shines. The request to identify alternatives builds critical thinking: real-world engineering has trade-offs, and recognizing them prevents over-engineering.

### Exercise 2: Debug a Service Implementation

```
I wrote a ROS 2 service server for a robot arm, but it's not working. When I call the service, I get no response and eventually a timeout error.

Here's my code:

```python
import rclpy
from rclpy.node import Node
from robot_arm_pkg.srv import MoveJoint

class ArmServiceServer(Node):
    def __init__(self):
        super().__init__('arm_service_server')

        # I create the service here
        self.srv = self.create_service(
            MoveJoint,
            'move_joint',
            self.move_joint_callback
        )

    def move_joint_callback(self, request, response):
        self.get_logger().info('Moving joint...')

        # This takes a few seconds
        result = self physically_move_joint(request.joint_id, request.angle)

        response.success = result
        return response

def main():
    rclpy.init()
    server = ArmServiceServer()
    rclpy.spin(server)
```

Can you:
1. Identify what's wrong with this code?
2. Explain why it causes the timeout?
3. Show me the correct implementation?
4. Suggest a better communication pattern if the movement takes >5 seconds

Also, explain how I could test this service from the command line to debug the issue.
```

**What you're learning:** Debugging ROS 2 services is a critical skill. This exercise teaches you to recognize common mistakes (missing spinning, blocking operations, timeout issues) and understand the relationship between code behavior and network communication. The command-line testing portion introduces valuable debugging tools that work without writing additional code.

### Exercise 3: Extend Action Server with Preemption

```
I have a working navigation action server that provides feedback during execution. Now I want to add preemption (canceling) support when a new goal arrives.

Current implementation:
```python
def execute_callback(self, goal_handle):
    target_x = goal_handle.request.target_x
    target_y = goal_handle.request.target_y

    for step in range(100):
        # Navigation logic here
        goal_handle.publish_feedback(feedback_msg)
        time.sleep(0.05)

    goal_handle.succeed()
    return result
```

Help me modify this to:
1. Check for cancellation requests during execution
2. Gracefully handle preemption when a new goal arrives
3. Report the correct result status (canceled vs succeeded)
4. Clean up any resources when canceled

Show me the complete modified execute_callback function with detailed comments explaining each addition.

Also, discuss: What considerations should I make for the physical robot when canceling a navigation goal mid-execution?
```

**What you're learning:** Action preemption is a critical real-world capability. This exercise teaches you to implement cancellation correctly, including the lifecycle of goal states (accepted, executing, canceled, succeeded). The physical robot consideration connects software to hardware reality—canceling a navigation goal means the robot might be halfway through a turn or stuck in a doorway, and your software must account for this.
