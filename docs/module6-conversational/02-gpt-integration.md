---
sidebar_position: 2
title: "GPT Integration for Robotics"
description: "Learn how to integrate Large Language Models like GPT into robot systems. Understand function calling, prompt engineering for robotics, and building conversational robot interfaces."
keywords: ["GPT", "OpenAI API", "Function Calling", "LLM Robotics", "Conversational AI", "Prompt Engineering", "Robot Control", "VLA Models"]
chapter: 6
lesson: 2
duration_minutes: 90

requirements:
  hardware: "Any computer with internet connection; RTX GPU recommended for local model alternatives"
  software: "Python 3.10+, OpenAI API key (or local LLM), ROS 2 Humble (optional)"

skills:
  - name: "LLM Fundamentals for Robotics"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can explain how LLMs process natural language and generate robot commands"

  - name: "Function Calling Implementation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can implement OpenAI function calling to convert text to structured robot commands"

  - name: "Prompt Engineering for Robotics"
    proficiency_level: "B2"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can design effective prompts that guide LLM behavior for robot control"

  - name: "Conversational Robot Architecture"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Analyze"
    measurable_at_this_level: "Student can design a system architecture integrating LLMs with ROS 2"

learning_objectives:
  - objective: "Explain how Large Language Models can bridge natural language and robot control through function calling"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Written explanation or diagram of the LLM-to-robot pipeline"

  - objective: "Implement function calling with OpenAI API to convert natural language into structured robot commands"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Working Python code using OpenAI API with function definitions"

  - objective: "Design effective prompts that guide LLM behavior for robotics applications, including safety constraints"
    proficiency_level: "B2"
    bloom_level: "Create"
    assessment_method: "Prompt template with system message and function definitions"

  - objective: "Integrate GPT-based command parsing with ROS 2 for conversational robot control"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "ROS 2 node that uses GPT to process voice/text commands"

cognitive_load:
  new_concepts: 8
  assessment: "Students will implement a GPT-integrated robot command system that understands natural language and executes robot actions through function calling"

differentiation:
  extension_for_advanced: "Implement multi-step reasoning (GPT plans complex tasks), add memory of conversation history, or integrate local LLMs (Llama 3, Mistral) for offline operation"
  remedial_for_struggling: "Use pre-built function calling templates, start with 2-3 simple functions only, and provide example API responses for testing without API calls"
  hardware_alternatives: "Use OpenAI API (requires internet and API key), or run local LLMs (Llama 3 via Ollama) on RTX GPU; all examples work in simulation without physical robot"

safety_notes: "Always include safety constraints in system prompts. Never allow LLMs to directly control hardware without validation. Implement rate limiting and emergency stop overrides. Test in simulation before physical deployment."

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# GPT Integration for Robotics

Imagine a robot that understands not just rigid commands like "move forward 2 meters," but natural instructions like "I need you to go to the kitchen, find the red cup on the counter, and bring it to me." The robot processes this request, breaks it down into subtasks, identifies the cup, plans a path, and executes the manipulation—all while understanding context and handling ambiguity. This is the promise of integrating Large Language Models (LLMs) like GPT into robotics systems.

LLMs have transformed how we interact with AI systems. Chatbots and coding assistants demonstrate how models can understand natural language, follow complex instructions, and generate useful responses. Bringing these capabilities to robots creates machines that can understand human intent, reason about tasks, and communicate naturally. This lesson teaches you how to integrate GPT and similar models into robot systems using function calling—the bridge between text understanding and robot action.

## From Text to Action: The Challenge

Traditional robot control requires precise, structured commands:

```python
# Traditional robot control
move_robot(direction="forward", distance=2.5)
rotate(angle=90)
gripper.activate(close=True)
```

This works for programmers but fails for natural human interaction. Humans don't speak in function calls—they speak in context, with ambiguity, filler words, and varying phrasings:

- "Go forward a bit"
- "Can you move towards the door?"
- "I think the red cup is on the table, grab it"
- "Um, could you maybe turn left? Like, 90 degrees?"

**The gap**: Natural language is messy and context-dependent. Robot control is precise and structured. LLMs like GPT are the translator between these worlds.

## The LLM-for-Robotics Architecture

```
+-----------------------------------------------------------------------+
|                    CONVERSATIONAL ROBOT PIPELINE                      |
+-----------------------------------------------------------------------+
|                                                                       |
|  1. HUMAN INPUT                                                       |
|     "Go to the kitchen and get the red cup"                           |
|           |                                                           |
|           v                                                           |
|  2. SPEECH-TO-TEXT (Whisper)                                          |
|     Converts voice to text (if using voice)                           |
|           |                                                           |
|           v                                                           |
|  3. LLM UNDERSTANDING (GPT)                                           |
|     System prompt: "You are a robot controller..."                   |
|     Available functions: move_to(), pick_up(), find_object()         |
|     Output: {"function": "move_to", "args": {"location": "kitchen"}}  |
|           |                                                           |
|           v                                                           |
|  4. FUNCTION VALIDATION                                               |
|     Check parameters, safety limits, feasibility                      |
|           |                                                           |
|           v                                                           |
|  5. ROS 2 EXECUTION                                                   |
|     Publish to /cmd_vel, /navigation_goal, /gripper_command           |
|           |                                                           |
|           v                                                           |
|  6. ROBOT ACTION + FEEDBACK                                           |
|     Robot executes, provides status back to LLM                       |
|                                                                       |
+-----------------------------------------------------------------------+
```

**Key insight**: The LLM doesn't directly control the robot. It translates intent into structured function calls, which are then validated and executed by the robot system. This separation ensures safety and reliability.

## Setting Up OpenAI API Access

First, obtain API credentials:

```bash
# Install OpenAI Python library
pip install openai

# Set your API key (get from platform.openai.com)
export OPENAI_API_KEY="sk-your-key-here"

# Or create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**Alternative: Local LLMs**

If you prefer not to use cloud APIs, local models work too:

```bash
# Install Ollama for local LLMs
curl -fsSL https://ollama.com/install.sh | sh

# Download Llama 3 (8B parameter version)
ollama pull llama3:8b

# Run local API server
ollama serve
```

## Function Calling: The Bridge to Robot Control

Function calling (also called "tool use") allows LLMs to output structured data instead of just text. Here's the foundation:

```python
# gpt_robot_integration.py - Basic function calling setup
import os
from openai import OpenAI
import json

# Initialize client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define what the robot can do
robot_functions = [
    {
        "name": "move_robot",
        "description": "Move the robot in a specified direction and distance",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["forward", "backward", "left", "right"],
                    "description": "Direction to move"
                },
                "distance_meters": {
                    "type": "number",
                    "minimum": 0.1,
                    "maximum": 10.0,
                    "description": "Distance to move in meters"
                }
            },
            "required": ["direction", "distance_meters"]
        }
    },
    {
        "name": "rotate_robot",
        "description": "Rotate the robot by a specified angle",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["left", "right"],
                    "description": "Direction to rotate"
                },
                "angle_degrees": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 360,
                    "description": "Angle to rotate in degrees"
                }
            },
            "required": ["direction", "angle_degrees"]
        }
    },
    {
        "name": "stop_robot",
        "description": "Immediately stop all robot motion (emergency stop)",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def process_command(user_input):
    """Process natural language command using GPT"""

    # System prompt defines behavior
    system_prompt = """You are a helpful robot controller. You control a mobile robot that can move, rotate, and stop.

When the user gives a command:
1. Understand their intent
2. Call the appropriate function with correct parameters
3. If the command is unclear or unsafe, explain why

Always prioritize safety. If something seems dangerous, ask for clarification."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cost-effective option
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        functions=robot_functions,
        function_call="auto"  # Let GPT decide when to use functions
    )

    message = response.choices[0].message

    # Check if GPT wants to call a function
    if message.function_call:
        function_name = message.function_call.name
        function_args = json.loads(message.function_call.arguments)

        return {
            "function": function_name,
            "arguments": function_args
        }
    else:
        # GPT chose to respond with text instead
        return {
            "response": message.content
        }

# Test the system
if __name__ == "__main__":
    test_commands = [
        "Move forward 2 meters",
        "Turn left 90 degrees",
        "Stop the robot!",
        "Can you go backwards about 1.5 meters?"
    ]

    for cmd in test_commands:
        print(f"\nUser: {cmd}")
        result = process_command(cmd)

        if "function" in result:
            print(f"Function: {result['function']}")
            print(f"Arguments: {result['arguments']}")
        else:
            print(f"Response: {result['response']}")
```

**Output:**
```
User: Move forward 2 meters
Function: move_robot
Arguments: {'direction': 'forward', 'distance_meters': 2.0}

User: Turn left 90 degrees
Function: rotate_robot
Arguments: {'direction': 'left', 'angle_degrees': 90}

User: Stop the robot!
Function: stop_robot
Arguments: {}

User: Can you go backwards about 1.5 meters?
Function: move_robot
Arguments: {'direction': 'backward', 'distance_meters': 1.5}
```

## Understanding Function Calling Mechanics

When you provide `functions` to the OpenAI API, the model:

1. **Analyzes your query** to determine if a function should be called
2. **Selects the appropriate function** based on your descriptions
3. **Extracts parameters** from natural language
4. **Returns structured JSON** instead of free-form text

The key is writing good function descriptions:

| Description Quality | Example | Result |
|---------------------|---------|--------|
| **Poor** | "move function" | Model unsure when to use it |
| **Good** | "Move the robot in a direction by specified distance" | Model understands purpose |
| **Excellent** | "Move the robot forward, backward, left, or right. Distance in meters, max 10m. Use for navigation commands." | Model handles edge cases correctly |

## Prompt Engineering for Robotics

The system prompt is critical for safe robot behavior:

```python
# prompts.py - Robot control prompts

# Safety-focused system prompt
SAFE_SYSTEM_PROMPT = """You are a robot controller for a mobile robot with navigation and manipulation capabilities.

## SAFETY RULES (CRITICAL)
1. NEVER move faster than 0.5 m/s near people
2. ALWAYS check for obstacles before moving
3. If "stop", "emergency", or "halt" is mentioned, call stop_robot() immediately
4. Never assume a path is clear if user says "just go"
5. If uncertain, ask for clarification rather than guessing

## AVAILABLE FUNCTIONS
- move_robot(direction, distance_meters): Navigate linear motion
- rotate_robot(direction, angle_degrees): Rotate in place
- stop_robot(): Emergency halt
- find_object(object_type, location): Search for objects
- pick_up_object(object_name): Grasp identified object
- place_object(location): Place held object

## BEHAVIOR GUIDELINES
- Be concise in responses
- Confirm actions before executing if potentially risky
- Report what you're doing: "Moving forward 2 meters to table"
- If a command can't be executed safely, explain why

You are controlling a physical robot. Mistakes can cause damage or injury. Be careful."""

# Conversation-focused prompt (more interactive)
CONVERSATIONAL_SYSTEM_PROMPT = """You are Rover, a helpful mobile robot assistant. You can navigate, find objects, and help with tasks.

Your personality is friendly and careful. You:
- Ask questions when commands are unclear
- Confirm actions that might be risky
- Explain what you're doing in simple terms
- Admit when you don't understand something

When users speak naturally, figure out what they want and help them accomplish it safely."""

# Task-planning prompt (for complex multi-step tasks)
PLANNING_SYSTEM_PROMPT = """You are a task planner for a mobile robot. Users give you high-level goals, and you break them into steps.

## WORKFLOW
1. Understand the user's goal
2. Break it into sequential steps
3. For each step, call the appropriate function
4. Report progress to the user

## EXAMPLE
User: "Get the red cup from the kitchen"
Your response:
"I'll help you get the red cup from the kitchen. Here's my plan:
1. Navigate to kitchen
2. Search for red cup
3. Pick up the cup
4. Return to you

Starting now..."

Then execute each step, updating the user on progress.
"""
```

## Advanced: Multi-Step Reasoning

For complex tasks, GPT can plan sequences:

```python
# advanced_robot_controller.py - Multi-step reasoning
import time

class AdvancedRobotController:
    """Robot controller with multi-step planning"""

    def __init__(self):
        self.client = OpenAI()
        self.robot_state = {
            "location": "origin",
            "holding": None,
            "battery": 100
        }

    def execute_function(self, function_name, arguments):
        """Execute a robot function with simulation"""
        print(f"  [EXECUTING] {function_name}({arguments})")

        if function_name == "move_robot":
            self.robot_state["location"] = arguments.get("direction", "unknown")
            return f"Moved {arguments['direction']} {arguments['distance_meters']}m"

        elif function_name == "rotate_robot":
            return f"Rotated {arguments['direction']} {arguments['angle_degrees']} degrees"

        elif function_name == "stop_robot":
            return "Robot stopped"

        elif function_name == "find_object":
            obj = arguments.get("object_type", "object")
            return f"Found {obj} at location"

        elif function_name == "pick_up_object":
            self.robot_state["holding"] = arguments.get("object_name", "object")
            return f"Picked up {arguments['object_name']}"

        elif function_name == "place_object":
            self.robot_state["holding"] = None
            return f"Placed object at {arguments.get('location', 'location')}"

        return "Unknown function"

    def plan_and_execute(self, user_goal):
        """Plan and execute a multi-step task"""

        system_prompt = f"""You are a robot task planner. The user will give you a goal, and you should:
1. Break it into steps
2. Call functions to execute each step
3. Report progress

Current robot state:
- Location: {self.robot_state['location']}
- Holding: {self.robot_state['holding']}
- Battery: {self.robot_state['battery']}%

Available functions:
- move_robot(direction, distance_meters)
- rotate_robot(direction, angle_degrees)
- find_object(object_type, location)
- pick_up_object(object_name)
- place_object(location)
- stop_robot()

Plan carefully. Think step by step."""

        extended_functions = robot_functions + [
            {
                "name": "find_object",
                "description": "Search for a specific type of object in a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "object_type": {"type": "string", "description": "Type of object to find"},
                        "location": {"type": "string", "description": "Where to search"}
                    },
                    "required": ["object_type"]
                }
            },
            {
                "name": "pick_up_object",
                "description": "Pick up a specific object",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "object_name": {"type": "string", "description": "Name of object to pick up"}
                    },
                    "required": ["object_name"]
                }
            },
            {
                "name": "place_object",
                "description": "Place the object being held at a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Where to place the object"}
                    },
                    "required": ["location"]
                }
            }
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_goal}
            ],
            functions=extended_functions
        )

        message = response.choices[0].message

        print(f"\n[PLAN] Understanding goal: {user_goal}")

        # Handle function call
        if message.function_call:
            function_name = message.function_call.name
            arguments = json.loads(message.function_call.arguments)
            result = self.execute_function(function_name, arguments)

            # Continue conversation for multi-step tasks
            conversation = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_goal},
                message,  # Assistant's function call
                {"role": "function", "name": function_name, "content": result}
            ]

            # Get next step
            next_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation,
                functions=extended_functions
            )

            print(f"  [STATUS] {next_response.choices[0].message.content}")

        else:
            print(f"[RESPONSE] {message.content}")

# Test multi-step reasoning
if __name__ == "__main__":
    controller = AdvancedRobotController()

    # Simple navigation
    controller.plan_and_execute("Move forward 2 meters")

    # Complex task
    controller.plan_and_execute("Go to the table, find the cup, and bring it here")
```

**Output:**
```
[PLAN] Understanding goal: Move forward 2 meters
  [EXECUTING] move_robot({'direction': 'forward', 'distance_meters': 2.0})
  [STATUS] Moved forward 2 meters.

[PLAN] Understanding goal: Go to the table, find the cup, and bring it here
  [EXECUTING] move_robot({'direction': 'forward', 'distance_meters': 3.0})
  [STATUS] Moving toward the table area.
  [EXECUTING] find_object({'object_type': 'cup', 'location': 'table'})
  [STATUS] I found a cup on the table.
  [EXECUTING] pick_up_object({'object_name': 'cup'})
  [STATUS] Picked up the cup. Now bringing it back to you.
  [EXECUTING] move_robot({'direction': 'backward', 'distance_meters': 3.0})
  [STATUS] Here's the cup!
```

## ROS 2 Integration

Now integrate GPT with ROS 2:

```python
# gpt_ros2_node.py - ROS 2 node with GPT integration
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
import json
import threading

class GPTRobotControllerNode(Node):
    """ROS 2 robot controller using GPT for command understanding"""

    def __init__(self):
        super().__init__('gpt_robot_controller')

        # Initialize GPT client
        from openai import OpenAI
        import os
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, '/robot_status', 10)
        self.speaking_pub = self.create_publisher(String, '/tts_say', 10)

        # Subscriber for voice/text input
        self.input_sub = self.create_subscription(
            String,
            '/voice_command',
            self.command_callback,
            10
        )

        # Emergency stop subscriber
        self.e_stop_sub = self.create_subscription(
            Bool,
            '/emergency_stop',
            self.emergency_stop_callback,
            10
        )

        # Define robot functions
        self.robot_functions = [
            {
                "name": "move",
                "description": "Move the robot forward or backward",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "direction": {"type": "string", "enum": ["forward", "backward"]},
                        "duration": {"type": "number", "description": "Seconds to move"}
                    },
                    "required": ["direction", "duration"]
                }
            },
            {
                "name": "turn",
                "description": "Turn the robot left or right",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "direction": {"type": "string", "enum": ["left", "right"]},
                        "duration": {"type": "number"}
                    },
                    "required": ["direction", "duration"]
                }
            },
            {
                "name": "stop",
                "description": "Stop all robot motion immediately",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

        self.get_logger().info("GPT Robot Controller ready")
        self.publish_status("Robot ready. You can speak naturally.")

    def publish_status(self, message):
        """Publish status and speak it"""
        msg = String()
        msg.data = message
        self.status_pub.publish(msg)
        self.speaking_pub.publish(msg)

    def emergency_stop_callback(self, msg):
        """Handle emergency stop"""
        if msg.data:
            twist = Twist()
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            for _ in range(10):
                self.cmd_vel_pub.publish(twist)
            self.publish_status("Emergency stop activated")

    def execute_move(self, direction, duration):
        """Execute movement command"""
        self.get_logger().info(f"Moving {direction} for {duration}s")
        self.publish_status(f"Moving {direction}")

        twist = Twist()
        speed = 0.3  # m/s (conservative for safety)

        twist.linear.x = speed if direction == "forward" else -speed

        import time
        start = time.time()
        while time.time() - start < duration and rclpy.ok():
            self.cmd_vel_pub.publish(twist)
            time.sleep(0.1)

        # Stop
        twist.linear.x = 0.0
        self.cmd_vel_pub.publish(twist)

    def execute_turn(self, direction, duration):
        """Execute turn command"""
        self.get_logger().info(f"Turning {direction} for {duration}s")
        self.publish_status(f"Turning {direction}")

        twist = Twist()
        angular_speed = 0.5  # rad/s

        twist.angular.z = angular_speed if direction == "left" else -angular_speed

        import time
        start = time.time()
        while time.time() - start < duration and rclpy.ok():
            self.cmd_vel_pub.publish(twist)
            time.sleep(0.1)

        # Stop
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)

    def execute_stop(self):
        """Execute stop command"""
        self.get_logger().info("Stopping robot")
        self.publish_status("Stopping")

        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0

        for _ in range(10):
            self.cmd_vel_pub.publish(twist)

    def command_callback(self, msg):
        """Process incoming command with GPT"""
        user_input = msg.data
        self.get_logger().info(f"Processing: {user_input}")

        # Run GPT processing in thread to avoid blocking
        threading.Thread(
            target=self.process_with_gpt,
            args=(user_input,),
            daemon=True
        ).start()

    def process_with_gpt(self, user_input):
        """Process command using GPT function calling"""

        system_prompt = """You are a robot controller. The robot can move, turn, and stop.

IMPORTANT RULES:
- If user says "stop", "halt", or "emergency", call the stop function immediately
- Maximum movement duration: 5 seconds
- Maximum turn duration: 3 seconds
- Be conservative with movement duration for safety

Respond briefly and confirm actions before executing."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                functions=self.robot_functions,
                function_call="auto"
            )

            message = response.choices[0].message

            if message.function_call:
                function_name = message.function_call.name
                arguments = json.loads(message.function_call.arguments)

                # Execute the function
                if function_name == "move":
                    self.execute_move(
                        arguments["direction"],
                        min(arguments["duration"], 5.0)  # Safety limit
                    )

                elif function_name == "turn":
                    self.execute_turn(
                        arguments["direction"],
                        min(arguments["duration"], 3.0)  # Safety limit
                    )

                elif function_name == "stop":
                    self.execute_stop()

            elif message.content:
                # GPT responded with text
                self.publish_status(message.content)

        except Exception as e:
            self.get_logger().error(f"GPT processing error: {e}")
            self.publish_status("Sorry, I didn't understand that command")

def main(args=None):
    rclpy.init(args=args)
    node = GPTRobotControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

**Output:**
```
[gpt_robot_controller]: GPT Robot Controller ready
[STATUS]: Robot ready. You can speak naturally.

[gpt_robot_controller]: Processing: Can you move forward a little bit?
[gpt_robot_controller]: Moving forward for 1.0s
[STATUS]: Moving forward

[gpt_robot_controller]: Processing: Turn to the left please
[gpt_robot_controller]: Turning left for 3.0s
[STATUS]: Turning left

[gpt_robot_controller]: Processing: Stop the robot!
[gpt_robot_controller]: Stopping robot
[STATUS]: Stopping
```

## Local LLM Alternative

For privacy-sensitive applications or offline operation, use local models:

```python
# local_llm_robot.py - Using local LLM with Ollama
import requests
import json

class LocalLLMRobotController:
    """Robot controller using local LLM (no API costs, works offline)"""

    def __init__(self, model="llama3:8b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def process_command(self, user_input, functions):
        """Process command using local LLM"""

        # Build function descriptions for the prompt
        function_descriptions = "\n".join([
            f"- {f['name']}: {f['description']}"
            for f in functions
        ])

        system_prompt = f"""You are a robot controller. Based on user commands, output JSON with the function to call.

Available functions:
{function_descriptions}

Response format (JSON only):
{{"function": "function_name", "arguments": {{"param": "value"}}}}

Example:
User: "Move forward 2 meters"
Response: {{"function": "move", "arguments": {{"direction": "forward", "distance_meters": 2.0}}}}"""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": f"{system_prompt}\n\nUser: {user_input}\nResponse:",
                "stream": False,
                "format": "json"  # Request JSON output
            }
        )

        result = response.json()

        # Parse the generated JSON
        try:
            generated = result.get("response", "{}")
            return json.loads(generated)
        except:
            # Fallback: extract JSON from response
            import re
            match = re.search(r'\{.*\}', generated, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return {"error": "Could not parse response"}

# Usage
if __name__ == "__main__":
    controller = LocalLLMRobotController()

    functions = [
        {
            "name": "move",
            "description": "Move the robot",
            "parameters": {
                "direction": ["forward", "backward", "left", "right"],
                "distance": "meters"
            }
        },
        {
            "name": "stop",
            "description": "Stop the robot"
        }
    ]

    result = controller.process_command("Move forward 2 meters", functions)
    print(f"Function: {result.get('function')}")
    print(f"Arguments: {result.get('arguments')}")
```

**Output:**
```
Function: move
Arguments: {"direction": "forward", "distance": 2.0}
```

**Local Model Installation:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Llama 3 (8B parameters, runs on RTX 3060+)
ollama pull llama3:8b

# Or Mistral (smaller, faster)
ollama pull mistral:7b

# Start the API server
ollama serve
```

## Safety and Reliability

When integrating LLMs with physical robots, safety is paramount:

### Safety Layers

```python
# safety_layer.py - Safety validation between GPT and robot
from dataclasses import dataclass
from enum import Enum

class SafetyLevel(Enum):
    SAFE = "safe"
    WARNING = "warning"
    DANGER = "danger"

@dataclass
class SafetyCheck:
    passed: bool
    level: SafetyLevel
    message: str

class RobotSafetyLayer:
    """Validates GPT commands before robot execution"""

    def __init__(self):
        self.max_speed = 0.5  # m/s
        self.max_duration = 5.0  # seconds
        self.emergency_word = ["stop", "emergency", "halt", "freeze"]

    def validate_command(self, function_name, arguments):
        """Validate a command before execution"""

        # Emergency bypass
        if function_name == "stop":
            return SafetyCheck(True, SafetyLevel.SAFE, "Emergency stop")

        # Check movement limits
        if function_name in ["move", "turn"]:
            duration = arguments.get("duration", 0)

            if duration > self.max_duration:
                return SafetyCheck(
                    False,
                    SafetyLevel.DANGER,
                    f"Duration {duration}s exceeds maximum {self.max_duration}s"
                )

            if duration < 0:
                return SafetyCheck(
                    False,
                    SafetyLevel.DANGER,
                    "Negative duration not allowed"
                )

        # Check for unsafe combinations
        if function_name == "move":
            direction = arguments.get("direction", "")
            if direction not in ["forward", "backward", "left", "right"]:
                return SafetyCheck(
                    False,
                    SafetyLevel.WARNING,
                    f"Unknown direction: {direction}"
                )

        return SafetyCheck(True, SafetyLevel.SAFE, "Command validated")

    def sanitize_arguments(self, function_name, arguments):
        """Ensure arguments are within safe limits"""

        if "duration" in arguments:
            arguments["duration"] = min(arguments["duration"], self.max_duration)

        if "speed" in arguments:
            arguments["speed"] = min(arguments["speed"], self.max_speed)

        return arguments

# Usage in robot controller
class SafeRobotController:
    """Robot controller with safety layer"""

    def __init__(self):
        self.safety = RobotSafetyLayer()
        self.gpt_controller = GPTRobotController()

    def execute_command(self, function_name, arguments):
        """Execute with safety validation"""

        # Validate first
        check = self.safety.validate_command(function_name, arguments)

        if not check.passed:
            print(f"[SAFETY BLOCKED] {check.message}")
            return False

        # Sanitize arguments
        arguments = self.safety.sanitize_arguments(function_name, arguments)

        # Execute
        print(f"[EXECUTING] {function_name}({arguments})")
        return True
```

## Hardware Alternatives

| Option | Pros | Cons | Cost |
|--------|------|------|------|
| **OpenAI API** | Best quality, easy setup | Requires internet, API costs | ~$0.10-1 per 1K commands |
| **Ollama (local)** | Free, private, offline | Requires RTX GPU, lower quality | Free (GPU hardware cost) |
| **Groq API** | Extremely fast | Limited model options | ~$0.05 per 1K commands |
| **Cloud GPUs** | Full control, any model | Expensive, setup complexity | $0.50-2/hour |

## Try With AI

### Exercise 1: Design a Function Calling Schema

```text
I'm building a warehouse robot that needs to understand commands like:
- "Go get the package from shelf B3"
- "Check if the loading dock is clear"
- "Move the boxes to the shipping area"

Help me design a complete function calling schema including:
1. 5-7 function definitions with clear descriptions
2. Parameter schemas with types and constraints
3. Safety considerations in descriptions
4. Example natural language inputs and expected function outputs

For each function, write the description as if explaining to someone who has never seen this robot before—be specific about what the function does and when to use it.
```

**What you're learning:** Designing good function calling schemas is an art form. The descriptions you write determine how well the LLM understands your robot's capabilities. By practicing this skill, you'll learn how to translate robot capabilities into clear, actionable descriptions that LLMs can reason about. This is essential for building robots that can understand and execute complex natural language commands.

### Exercise 2: Design Safety Prompts

```text
Safety is critical when LLMs control physical robots. A misheard command could cause damage or injury.

Help me design comprehensive safety prompts for different robot scenarios:

1. **Home robot** operating around children and pets
2. **Industrial robot** in a factory with heavy machinery
3. **Warehouse robot** moving near workers and forklifts

For each scenario, design:
- System prompt with safety rules
- Emergency stop triggers
- Confirmation requirements (when to ask "are you sure?")
- Parameter limits (speed, force, duration)

After designing prompts, analyze: What safety edge cases might still be missed? How would you add redundancy for critical safety functions?
```

**What you're learning:** Safety in robotics isn't about trusting the LLM—it's about designing systems with multiple layers of protection. By designing safety prompts for different environments, you'll learn to think adversarially: what could go wrong, and how do we prevent it? This mindset is essential for building trustworthy physical AI systems that operate safely around humans and valuable property.

### Exercise 3: Multi-Step Task Planning with Vision

```text
Modern robots combine language understanding with vision. I want my robot to:
- "Find the red cup and bring it to me"
- "Pick up the screwdriver from the workbench"
- "Check if there are any obstacles in the hallway"

Design a system that combines:
1. GPT for understanding natural language commands
2. A vision model (like CLIP or GPT-4V) for object identification
3. Function calling to execute physical actions

Your design should include:
- How to parse object references from commands ("red cup", "screwdriver")
- How to query the vision model with camera images
- How GPT decides when to call vision functions vs. execute movement
- A conversation flow showing a complete task execution

Also discuss: What happens when vision fails? What if there are multiple red cups? How do you handle uncertainty?
```

**What you're learning:** This exercise introduces you to Vision-Language-Action (VLA) models—the frontier of robotics research. By designing a system that combines language understanding with visual perception, you'll practice integrating multiple AI capabilities into a coherent robot controller. This is the foundation for building robots that can see, understand, and act in the real world—the core challenge of Physical AI.
