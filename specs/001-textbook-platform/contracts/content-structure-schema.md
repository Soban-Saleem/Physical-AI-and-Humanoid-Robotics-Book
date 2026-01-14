# Content Structure Schema Contract

**Feature**: `001-textbook-platform` | **Version**: 1.0.0 | **Date**: 2025-01-13

## Purpose

This contract defines the required structure and content sections for all lesson content. Compliance ensures consistent learning experience across all modules.

---

## Required Sections

### Section 1: Narrative Opening (2-3 paragraphs)

**Purpose**: Connect the lesson to real-world robotics scenarios and Physical AI goals.

**Requirements**:
- 2-3 paragraphs minimum
- Must reference a real-world robotics application
- Must explain why this matters for Physical AI
- Must describe practical applications

**Structure**:
```
Paragraph 1: Real-world scenario hook
Paragraph 2: Connection to Physical AI / Embodied Intelligence
Paragraph 3: Practical application / what students will be able to do
```

**Example**:
```markdown
Imagine a delivery robot navigating a busy city sidewalk. As pedestrians walk by, the
robot must detect their presence, predict their movement, and adjust its path in
real-time. This isn't just computer vision—it's physical AI, where digital decisions
meet the physical world through sensors and actuators.

In this lesson, you'll learn about the publish-subscribe communication pattern that
makes this possible. ROS 2 topics allow different components of a robot system to
share information without tight coupling, enabling the kind of modular, scalable
architectures needed for real-world robotics.

By the end, you'll have written a working publisher-subscriber pair and understand
how ROS 2 enables the sensor-actor loops that power embodied intelligence.
```

---

### Section 2: Technical Content

**Purpose**: Deliver the core learning material with explanations, examples, and step-by-step tutorials.

**Requirements**:
- Clear explanations with examples
- Code blocks with **Output:** verification
- Diagrams/tables for complex concepts
- Step-by-step tutorials for practical skills

**Code Example Format**:
````markdown
### Creating a ROS 2 Publisher

A publisher node sends messages to a topic. Here's a minimal example:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('Publisher node started')

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello, Physical AI!'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')

def main():
    rclpy.init()
    publisher = MinimalPublisher()
    rclpy.spin(publisher)
    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Output:**
```
[INFO] [minimal_publisher]: Publisher node started
[INFO] [minimal_publisher]: Publishing: Hello, Physical AI!
[INFO] [minimal_publisher]: Publishing: Hello, Physical AI!
...
```
````

---

### Section 3: Hardware Context

**Purpose**: Inform students about hardware requirements and provide alternatives.

**Requirements**:
- State hardware requirements upfront
- Provide simulation alternatives
- Note cloud-based options where applicable

**Format**:
```markdown
## Hardware Requirements

This lesson uses **simulation only**. No physical hardware required.

For the full course, the recommended hardware is:
- GPU: NVIDIA RTX 4070 Ti (12GB VRAM) or higher
- CPU: Intel i7 (13th Gen+) or AMD Ryzen 9
- RAM: 64 GB DDR5 (32GB minimum)

**Simulation Alternative**: All examples in this module run in Gazebo simulation
on any computer with a GPU.

**Cloud Option**: NVIDIA Omniverse Cloud provides browser-based access to Isaac Sim
without local hardware.
```

---

### Section 4: Try With AI Prompts (Exactly 3)

**Purpose**: Provide hands-on exercises for different skill levels.

**Requirements**:
- Exactly 3 prompts per lesson
- Each targets different skill level (beginner, intermediate, advanced)
- Each has "**What you're learning:**" explanation
- Prompts are copyable (in code blocks)

**Format**:
````markdown
## Try With AI

### Exercise 1: Build Your Understanding

```text
Ask an AI to explain the difference between a ROS 2 topic and a service using
an analogy from everyday life. Have it provide 3 different analogies and explain
which one is most accurate for robotics applications.
```

**What you're learning:** The publish-subscribe pattern vs. request-response,
and how analogies can help (or mislead) when understanding distributed systems.

### Exercise 2: Apply Your Knowledge

```text
Describe a robotics scenario (e.g., autonomous vacuum, warehouse robot) and ask
an AI to help you design the topic structure. Identify what topics would be needed,
what message types to use, and which components would publish/subscribe to each.
```

**What you're learning:** System design skills—breaking down a robotics problem
into the modular communication patterns that ROS 2 enables.

### Exercise 3: Extend and Create

```text
Ask an AI to help you modify the publisher code to accept command-line arguments
for the topic name and message content. Have it explain how to make your code more
flexible and reusable across different projects.
```

**What you're learning:** Practical software engineering skills—parameterizing
your code for reusability and learning about ROS 2 argument passing.
````

---

## Prohibited Elements

### After "Try With AI"

**PROHIBITED**:
- ❌ "## Summary" section
- ❌ "## Key Takeaways" section
- ❌ "## Conclusion" section
- ❌ "## Recap" section
- ❌ Any summarizing content after Try With AI

**RATIONALE**: Lessons should end with action. Summaries are passive; Try With AI
prompts drive continued learning and application.

### Framework Labels

**PROHIBITED**:
- ❌ "### Part 1: AI as Teacher"
- ❌ "### Part 2: Student as Teacher"
- ❌ "### Part 3: Co-Worker"
- ❌ "### The Three Roles Framework"

**RATIONALE**: The framework scaffolds learning but should be invisible to students.
Use action-focused headers instead: "## Build Your Understanding", "## Apply
Your Knowledge", "## Extend and Create".

---

## Content Quality Checklist

Before publishing, verify:

### Structure
- [ ] Narrative opening (2-3 paragraphs)
- [ ] Technical content with explanations
- [ ] At least one code example with **Output:** block
- [ ] Hardware requirements section
- [ ] Exactly 3 Try With AI prompts
- [ ] Lesson ends with Try With AI (no summary after)

### Evidence
- [ ] 70%+ of code blocks have **Output:** sections
- [ ] All output claims are verified
- [ ] Diagrams/tables for complex concepts

### Framework
- [ ] No framework labels visible ("AI as Teacher", etc.)
- [ ] Try With AI prompts have "**What you're learning:**" explanations
- [ ] Prompts are copyable (in code blocks)

### Hardware Awareness
- [ ] Hardware requirements stated
- [ ] Simulation alternatives provided
- [ ] Cloud options noted where applicable

---

## Constitution Compliance

This contract implements the following constitutional principles:

1. **Structural Compliance**: Lessons end with `## Try With AI`, no summary
2. **Evidence Presence**: Code blocks have `**Output:**` sections
3. **Framework Invisibility**: No role labels in headers
4. **Hardware Awareness**: Requirements and alternatives always specified

---

## References

- Constitution: `.specify/memory/constitution.md`
- Data Model: `specs/001-textbook-platform/data-model.md`
- Spec: `specs/001-textbook-platform/spec.md`
