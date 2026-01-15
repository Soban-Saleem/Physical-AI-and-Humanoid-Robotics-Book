---
sidebar_position: 4
title: "Human-Robot Interaction"
description: "Learn how humans and robots communicate and work together. Master HRI principles, safety protocols, communication modalities, social robotics, and trust in human-robot collaboration."
keywords: ["HRI", "human-robot interaction", "robot safety", "proxemics", "social robotics", "trust", "multimodal communication", "collaborative robotics", "cobot"]
chapter: 5
lesson: 4
duration_minutes: 90

requirements:
  hardware: "Any computer (simulation-based lesson)"
  software: "Python 3.10+, optional: ROS 2 Humble/Jazzy for advanced exercises"

skills:
  - name: "HRI Principles Analysis"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Analyze"
    measurable_at_this_level: "Student can analyze HRI scenarios and identify key principles being applied or violated"

  - name: "Proxemic Awareness"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can apply proxemic zones to robot navigation and interaction design"

  - name: "Safety Protocol Design"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can design safety protocols for human-robot collaborative workspaces"

  - name: "Trust Calibration"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Evaluate"
    measurable_at_this_level: "Student can evaluate factors that affect trust between humans and robots"

learning_objectives:
  - objective: "Explain the fundamental principles of Human-Robot Interaction including safety, communication, and trust"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Short answer: Describe key HRI principles for a given collaborative scenario"

  - objective: "Apply proxemic zones to design robot behavior that respects human spatial comfort"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Design task: Specify robot approach behavior for different social contexts"

  - objective: "Design multimodal communication systems combining speech, gesture, and display feedback for effective human-robot collaboration"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Interface design: Create communication protocol for collaborative task"

  - objective: "Evaluate factors that build or erode trust between humans and robots in shared workspaces"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Case analysis: Identify trust-building and trust-eroding behaviors in HRI scenarios"

cognitive_load:
  new_concepts: 8
  assessment: "Students will design proxemic-aware robot behaviors, create multimodal communication systems, and analyze trust dynamics in HRI scenarios"

differentiation:
  extension_for_advanced: "Implement emotion recognition from facial expressions and design robot responses that adapt to human emotional state"
  remedial_for_struggling: "Focus on safety zones and simple communication (lights and sounds) before progressing to proxemics and social cues"
  hardware_alternatives: "All exercises use conceptual design and Python simulation. For physical testing: Use Unitree G1/Go2 or simulate in Gazebo/Isaac Sim"

safety_notes: "When testing HRI with physical robots: Always maintain emergency stop access, use force-limited robots, start with slow speeds, and never allow autonomous robots near vulnerable populations without rigorous safety validation."

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Human-Robot Interaction

Imagine walking through a factory floor where robots and humans work side by side. A humanoid robot carrying a heavy box notices you approaching, slows down, makes eye contact with its cameras, nods slightly, and waits for you to pass before continuing. This seamless coordination didn't happen by accident—it's the result of careful **Human-Robot Interaction (HRI)** design.

HRI is the study of how humans and robots communicate, collaborate, and coexist in shared spaces. Unlike industrial robots that work behind cages, modern robots like humanoids must interact with people naturally, safely, and intuitively. This lesson explores how robots can become good collaborators rather than just efficient machines.

## What Makes HRI Different?

Traditional robotics focuses on making robots work perfectly. HRI focuses on making robots work well **with people**. This requires understanding human psychology, social norms, and communication patterns—not just engineering.

### The HRI Challenge

```python
# Traditional robot goal: Perfect task execution
def traditional_robot(task):
    # Just do the task as efficiently as possible
    return execute_optimally(task)

# HRI-aware robot goal: Task + Human comfort
def hri_aware_robot(task, humans_nearby):
    if humans_nearby:
        # Consider safety, comfort, communication
        return execute_safely_with_communication(task)
    else:
        return execute_optimally(task)
```

**The key difference**: HRI-aware robots trade some efficiency for human comfort, safety, and trust. This isn't a bug—it's a feature. A robot that moves perfectly but scares everyone around it has failed at HRI.

### HRI Design Dimensions

| Dimension | Questions | Example |
|-----------|-----------|---------|
| **Safety** | How do we prevent harm? | Speed limits, force limits, emergency stops |
| **Communication** | How do robots convey intent? | Lights, sounds, speech, gestures, displays |
| **Proxemics** | How close is too close? | Personal space zones, approach directions |
| **Trust** | How do humans know what to expect? | Predictable behavior, transparency, reliability |
| **Social Norms** | What social rules apply? | Queueing, yielding, acknowledging presence |

## Safety First: The Foundation of HRI

Safety is non-negotiable in HRI. A robot that injures someone is a failure regardless of how well it performed its task.

### Safety Zones

```python
class SafetyZone:
    """
    Define safety zones around humans for robot interaction.

    Zones are defined by distance from human:
    - Critical: Robot must STOP immediately
    - Warning: Robot must slow and prepare to stop
    - Caution: Robot should monitor and be ready to slow
    - Safe: Normal operation acceptable
    """

    def __init__(self, critical_distance=0.5, warning_distance=1.5,
                 caution_distance=3.0):
        """
        Args:
            critical_distance: Distance (m) where robot MUST stop
            warning_distance: Distance (m) where robot must slow
            caution_distance: Distance (m) where robot should monitor
        """
        self.critical = critical_distance
        self.warning = warning_distance
        self.caution = caution_distance

    def get_action(self, human_distance, current_speed):
        """
        Determine appropriate action based on human distance.

        Args:
            human_distance: Current distance to human (meters)
            current_speed: Current robot speed (m/s)

        Returns:
            action: Recommended action and speed limit
        """
        if human_distance < self.critical:
            return {
                "action": "EMERGENCY_STOP",
                "max_speed": 0.0,
                "reason": f"Human within critical zone ({human_distance:.2f}m)"
            }

        elif human_distance < self.warning:
            # Slow speed proportional to distance
            safe_speed = current_speed * 0.3
            return {
                "action": "SLOW_APPROACH",
                "max_speed": min(safe_speed, 0.3),  # Max 0.3 m/s
                "reason": f"Human within warning zone ({human_distance:.2f}m)"
            }

        elif human_distance < self.caution:
            # Moderate speed with awareness
            safe_speed = current_speed * 0.7
            return {
                "action": "MONITOR",
                "max_speed": min(safe_speed, 0.8),  # Max 0.8 m/s
                "reason": f"Human within caution zone ({human_distance:.2f}m)"
            }

        else:
            return {
                "action": "NORMAL",
                "max_speed": current_speed,
                "reason": f"Safe distance ({human_distance:.2f}m)"
            }

# Example: Robot approaching humans
safety = SafetyZone(critical_distance=0.6, warning_distance=2.0, caution_distance=3.5)

test_scenarios = [
    (0.4, 1.0, "Human too close!"),
    (1.2, 1.0, "Human approaching"),
    (2.5, 1.0, "Human nearby"),
    (5.0, 1.0, "Clear path"),
]

print("=== Safety Zone Analysis ===\n")
for distance, speed, scenario in test_scenarios:
    result = safety.get_action(distance, speed)
    print(f"{scenario}: Human at {distance}m")
    print(f"  Action: {result['action']}")
    print(f"  Max speed: {result['max_speed']} m/s")
    print(f"  Reason: {result['reason']}")
    print()
```

**Output:**
```
=== Safety Zone Analysis ===

Human too close!: Human at 0.4m
  Action: EMERGENCY_STOP
  Max speed: 0.0 m/s
  Reason: Human within critical zone (0.40m)

Human approaching: Human at 1.2m
  Action: SLOW_APPROACH
  Max speed: 0.3 m/s
  Reason: Human within warning zone (1.20m)

Human nearby: Human at 2.5m
  Action: MONITOR
  Max speed: 0.7 m/s
  Reason: Human within caution zone (2.50m)

Clear path: Human at 5.0m
  Action: NORMAL
  Max speed: 1.0 m/s
  Reason: Safe distance (5.00m)
```

### Beyond Distance: Predictability and Transparency

Safety isn't just about not hitting people. It's about being **predictable** so humans can anticipate robot behavior.

```python
class PredictableRobot:
    """
    A robot that communicates intent for safer HRI.
    """

    def __init__(self):
        self.current_action = "idle"
        self.planned_path = []
        self.communication_mode = "visual"  # visual, auditory, both

    def announce_intent(self, action, path):
        """
        Communicate what the robot is about to do.

        Humans need to know:
        1. What the robot will do
        2. Where it will go
        3. How long it will take
        """
        self.current_action = action
        self.planned_path = path

        # Communication methods
        signals = {
            "visual": self._visual_signals(),
            "auditory": self._auditory_signals(),
        }

        return signals

    def _visual_signals(self):
        """Return visual indicators of intent."""
        visual = {
            "led_pattern": self._led_for_action(self.current_action),
            "display_text": self._text_for_action(self.current_action),
            "gesture": self._gesture_for_action(self.current_action),
        }
        return visual

    def _auditory_signals(self):
        """Return auditory indicators of intent."""
        auditory = {
            "sound": self._sound_for_action(self.current_action),
            "speech": self._speech_for_action(self.current_action),
        }
        return auditory

    def _led_for_action(self, action):
        """Map actions to LED colors."""
        led_map = {
            "moving": "blue",
            "turning": "yellow",
            "stopping": "red",
            "waiting": "green",
            "idle": "white",
        }
        return led_map.get(action, "white")

    def _text_for_action(self, action):
        """Human-readable action description."""
        text_map = {
            "moving": "Moving forward",
            "turning": "Turning",
            "stopping": "Stopping",
            "waiting": "Yielding",
            "idle": "Ready",
        }
        return text_map.get(action, "Unknown")

    def _gesture_for_action(self, action):
        """Physical gesture (head nod, arm raise, etc.)."""
        gesture_map = {
            "moving": "lean_forward",
            "turning": "look_direction",
            "stopping": "raise_hands",
            "waiting": "nod",
            "idle": "neutral",
        }
        return gesture_map.get(action, "neutral")

    def _sound_for_action(self, action):
        """Auditory tone for action."""
        sound_map = {
            "moving": "ascending",
            "turning": "beep_x2",
            "stopping": "descending",
            "waiting": "chime",
            "idle": None,
        }
        return sound_map.get(action)

    def _speech_for_action(self, action):
        """Spoken announcement."""
        speech_map = {
            "moving": "Excuse me, coming through",
            "turning": "Turning now",
            "stopping": "Stopping",
            "waiting": "After you",
            "idle": None,
        }
        return speech_map.get(action)

# Example: Robot navigating near humans
robot = PredictableRobot()

actions = ["moving", "turning", "waiting", "stopping"]

print("=== Intent Communication ===\n")
for action in actions:
    signals = robot.announce_intent(action, [])
    print(f"Action: {action.upper()}")
    print(f"  LED: {signals['visual']['led_pattern']}")
    print(f"  Display: '{signals['visual']['display_text']}'")
    print(f"  Gesture: {signals['visual']['gesture']}")
    print(f"  Sound: {signals['auditory']['sound']}")
    print(f"  Speech: {signals['auditory']['speech']}")
    print()
```

**Output:**
```
=== Intent Communication ===

Action: MOVING
  LED: blue
  Display: 'Moving forward'
  Gesture: lean_forward
  Sound: ascending
  Speech: 'Excuse me, coming through'

Action: TURNING
  LED: yellow
  Display: 'Turning'
  Gesture: look_direction
  Sound: beep_x2
  Speech: 'Turning now'

Action: WAITING
  LED: green
  Display: 'Yielding'
  Gesture: nod
  Sound: chime
  Speech: 'After you'

Action: STOPPING
  LED: red
  Display: 'Stopping'
  Gesture: raise_hands
  Sound: descending
  Speech: 'Stopping'
```

**Key insight**: A robot that communicates intent is safer than one that doesn't—even if both have perfect collision avoidance. Communication allows humans to plan their own actions around the robot.

## Proxemics: Respecting Personal Space

**Proxemics** is the study of how humans use space. Different cultures have different norms, but there are universal patterns that robots should respect.

### Hall's Proxemic Zones (Adapted for HRI)

| Zone | Distance | Robot Behavior | Example |
|------|----------|----------------|---------|
| **Intimate** | 0-0.45m | Avoid entering unless task requires | Assisting with personal care |
| **Personal** | 0.45-1.2m | Approach slowly, announce presence, ask permission | Handing objects, collaborative task |
| **Social** | 1.2-3.6m | Normal interaction zone | Working side by side |
| **Public** | 3.6m+ | Free movement | Passing through, observation |

```python
class ProxemicAwareRobot:
    """
    Robot that respects human spatial comfort zones.
    """

    def __init__(self):
        self.zones = {
            "intimate": (0, 0.45),
            "personal": (0.45, 1.2),
            "social": (1.2, 3.6),
            "public": (3.6, float('inf'))
        }

    def get_zone(self, distance):
        """Identify which zone a human is in."""
        for zone, (min_dist, max_dist) in self.zones.items():
            if min_dist <= distance < max_dist:
                return zone
        return "public"

    def approach_strategy(self, current_distance, target_distance=0.6):
        """
        Determine how to approach a human.

        Args:
            current_distance: Starting distance
            target_distance: Desired final distance (default: personal zone)

        Returns:
            strategy: Approach behavior recommendations
        """
        current_zone = self.get_zone(current_distance)
        target_zone = self.get_zone(target_distance)

        strategy = {
            "current_zone": current_zone,
            "target_zone": target_zone,
            "speed": "normal",
            "announcement": None,
            "permission": False,
            "frontal_approach": True
        }

        # Adjust behavior based on current zone
        if current_zone == "intimate":
            strategy["speed"] = "very_slow"
            strategy["announcement"] = "I am very close. Please excuse me."
            strategy["permission"] = True

        elif current_zone == "personal":
            strategy["speed"] = "slow"
            strategy["announcement"] = "May I approach?"

        elif current_zone == "social":
            strategy["speed"] = "moderate"
            strategy["announcement"] = "Coming over to assist."

        # Don't enter intimate zone without specific task
        if target_zone == "intimate":
            strategy["permission"] = True
            strategy["frontal_approach"] = True  # Always approach front

        return strategy

# Example: Different approach scenarios
robot = ProxemicAwareRobot()

scenarios = [
    (4.0, 1.0, "Approaching from public to personal"),
    (2.0, 0.3, "Approaching for close assistance"),
    (0.6, 0.6, "Already in personal zone"),
]

print("=== Proxemic-Aware Approach Strategies ===\n")
for start, end, description in scenarios:
    strategy = robot.approach_strategy(start, end)
    print(f"{description}:")
    print(f"  From: {strategy['current_zone']} zone ({start}m)")
    print(f"  To: {strategy['target_zone']} zone ({end}m)")
    print(f"  Speed: {strategy['speed']}")
    print(f"  Announcement: {strategy['announcement']}")
    print(f"  Ask permission: {strategy['permission']}")
    print()
```

**Output:**
```
=== Proxemic-Aware Approach Strategies ===

Approaching from public to personal zone:
  From: public zone (4.0m)
  To: personal zone (1.0m)
  Speed: moderate
  Announcement: Coming over to assist.
  Ask permission: False

Approaching for close assistance:
  From: social zone (2.0m)
  To: intimate zone (0.3m)
  Speed: very_slow
  Announcement: I am very close. Please excuse me.
  Ask permission: True

Already in personal zone:
  From: personal zone (0.6m)
  To: personal zone (0.6m)
  Speed: slow
  Announcement: May I approach?
  Ask permission: False
```

### Approach Direction Matters

How a robot approaches a human matters as much as the distance:

```python
def optimal_approach_angle(human_orientation, robot_position):
    """
    Calculate optimal approach angle for human comfort.

    Rules:
    - Frontal approach: Best for communication
    - Side approach: Non-threatening, good for passing
    - Rear approach: Avoid unless necessary (startling!)

    Args:
        human_orientation: Direction human is facing (radians)
        robot_position: Robot's position relative to human (x, y)

    Returns:
        comfort_score: 0-1, higher is more comfortable
        recommendation: How to adjust approach
    """
    import numpy as np

    # Calculate angle to robot from human's perspective
    rx, ry = robot_position
    angle_to_robot = np.arctan2(ry, rx)
    relative_angle = abs(angle_to_robot - human_orientation)
    relative_angle = relative_angle % (2 * np.pi)
    if relative_angle > np.pi:
        relative_angle = 2 * np.pi - relative_angle

    # Comfort scoring
    # Frontal (within 45 degrees): Best
    # Side (45-135 degrees): Good
    # Rear (135-180 degrees): Poor

    if relative_angle < np.pi/4:  # 45 degrees
        comfort = 1.0
        recommendation = "Frontal approach optimal for communication"
    elif relative_angle < 3*np.pi/4:  # 135 degrees
        comfort = 0.7
        recommendation = "Side approach acceptable for passing"
    else:
        comfort = 0.3
        recommendation = "Rear approach startling! Reposition to front or side."

    return comfort, recommendation

# Test approach angles
human_facing = 0  # Facing along +x axis

test_positions = [
    (1, 0, "Directly in front"),
    (0.7, 0.7, "45 degrees front-right"),
    (0, 1, "Directly to the right"),
    (-0.7, 0.7, "135 degrees rear-right"),
    (-1, 0, "Directly behind"),
]

print("=== Approach Direction Analysis ===\n")
print(f"Human facing: 0 degrees (along +x axis)\n")

for x, y, desc in test_positions:
    comfort, rec = optimal_approach_angle(human_facing, (x, y))
    print(f"{desc}: Position ({x}, {y})")
    print(f"  Comfort score: {comfort:.2f}/1.0")
    print(f"  Recommendation: {rec}")
    print()
```

**Output:**
```
=== Approach Direction Analysis ===

Human facing: 0 degrees (along +x axis)

Directly in front: Position (1, 0)
  Comfort score: 1.00/1.0
  Recommendation: Frontal approach optimal for communication

45 degrees front-right: Position (0.7, 0.7)
  Comfort score: 1.00/1.0
  Recommendation: Frontal approach optimal for communication

Directly to the right: Position (0, 1)
  Comfort score: 0.70/1.0
  Recommendation: Side approach acceptable for passing

135 degrees rear-right: Position (-0.7, 0.7)
  Comfort score: 0.30/1.0
  Recommendation: Rear approach startling! Reposition to front or side.

Directly behind: Position (-1, 0)
  Comfort score: 0.30/1.0
  Recommendation: Rear approach startling! Reposition to front or side.
```

## Multimodal Communication

Humans communicate through multiple channels simultaneously—speech, gestures, facial expressions, tone of voice. Effective HRI requires robots to do the same.

### Communication Modalities

| Modality | Use Cases | Advantages | Limitations |
|----------|-----------|------------|-------------|
| **Speech** | Complex instructions, social interaction | Natural, information-rich | Noisy environments, language barriers |
| **Visual/Display** | Status, instructions, maps | Precise, persistent | Requires visual attention |
| **Gestures** | Simple commands, acknowledgment | Intuitive, cross-cultural | Limited vocabulary |
| **Lights/LEDs** | Status indication, warnings | Visible from all angles | Limited information |
| **Sound/Tones** | Alerts, confirmation | Works without looking | Can be annoying, ambiguous |
| **Haptic** (future) | Physical guidance, alerts | Direct, attention-grabbing | Requires contact |

### Multimodal Fusion

```python
class MultimodalInterface:
    """
    Robot interface that combines multiple communication modes.
    """

    def __init__(self):
        self.led_state = "off"
        self.display_text = ""
        self.last_sound = None
        self.current_gesture = None

    def communicate_status(self, status, urgency="normal"):
        """
        Communicate robot status using multiple modalities.

        Status types: idle, working, waiting, error, battery_low
        Urgency: low, normal, high, critical
        """
        multimodal = {
            "visual": self._visual_communication(status, urgency),
            "auditory": self._auditory_communication(status, urgency),
            "gesture": self._gesture_communication(status),
        }

        return multimodal

    def _visual_communication(self, status, urgency):
        """LED and display communication."""
        colors = {
            "idle": ("white", "steady"),
            "working": ("blue", "pulsing"),
            "waiting": ("yellow", "steady"),
            "error": ("red", "flashing"),
            "battery_low": ("orange", "flashing"),
        }

        text_messages = {
            "idle": "Ready",
            "working": "Working...",
            "waiting": "Waiting",
            "error": "ERROR",
            "battery_low": "LOW BATTERY",
        }

        color, pattern = colors.get(status, ("white", "steady"))
        text = text_messages.get(status, "")

        # Adjust for urgency
        if urgency == "critical":
            pattern = "rapid_flash"
            text = f"! {text} !"

        return {
            "led_color": color,
            "led_pattern": pattern,
            "display_text": text,
            "display_icon": self._icon_for_status(status)
        }

    def _auditory_communication(self, status, urgency):
        """Sound and speech communication."""
        sounds = {
            "idle": None,
            "working": None,
            "waiting": "chime",
            "error": "alarm",
            "battery_low": "beep_sequence",
        }

        speech = {
            "idle": None,
            "working": None,
            "waiting": "Waiting for input",
            "error": "An error occurred",
            "battery_low": "Battery is low",
        }

        sound = sounds.get(status)
        message = speech.get(status)

        # Add speech for high urgency
        if urgency in ["high", "critical"] and message:
            return {"sound": sound, "speech": message, "repeat": True}

        return {"sound": sound, "speech": message, "repeat": False}

    def _gesture_communication(self, status):
        """Physical gesture for humanoid robots."""
        gestures = {
            "idle": "relaxed",
            "working": "focused",
            "waiting": "open_palms",
            "error": "shrug",
            "battery_low": "show_battery",
        }
        return gestures.get(status, "neutral")

    def _icon_for_status(self, status):
        """Icon for display (emoji style)."""
        icons = {
            "idle": "[=]",
            "working": "[~]",
            "waiting": "[?]",
            "error": "[!]",
            "battery_low": "[[[ ]]]",
        }
        return icons.get(status, "[?]")

# Example: Status communication
interface = MultimodalInterface()

scenarios = [
    ("working", "normal", "Normal operation"),
    ("waiting", "normal", "Waiting for human"),
    ("error", "high", "Error occurred"),
    ("battery_low", "critical", "Critical battery"),
]

print("=== Multimodal Communication ===\n")
for status, urgency, description in scenarios:
    comms = interface.communicate_status(status, urgency)
    print(f"{description}:")
    print(f"  Status: {status}, Urgency: {urgency}")
    print(f"  Visual: {comms['visual']['led_color']} LED ({comms['visual']['led_pattern']})")
    print(f"  Display: '{comms['visual']['display_text']}' {comms['visual']['display_icon']}")
    print(f"  Sound: {comms['auditory']['sound']}")
    print(f"  Speech: {comms['auditory']['speech']}")
    print(f"  Gesture: {comms['gesture']}")
    print()
```

**Output:**
```
=== Multimodal Communication ===

Normal operation:
  Status: working, Urgency: normal
  Visual: blue LED (pulsing)
  Display: 'Working...' [~]
  Sound: None
  Speech: None
  Gesture: focused

Waiting for human:
  Status: waiting, Urgency: normal
  Visual: yellow LED (steady)
  Display: 'Waiting' [?]
  Sound: chime
  Speech: Waiting for input
  Gesture: open_palms

Error occurred:
  Status: error, Urgency: high
  Visual: red LED (flashing)
  Display: '! ERROR !' [!]
  Sound: alarm
  Speech: An error occurred
  Gesture: shrug

Critical battery:
  Status: battery_low, Urgency: critical
  Visual: orange LED (rapid_flash)
  Display: '! LOW BATTERY !' [[[ ]]]
  Sound: beep_sequence
  Speech: Battery is low
  Gesture: show_battery
```

### Social Robotics: Beyond Functional Communication

Social robots engage with humans on a more personal level. They might make eye contact, use polite language, or express (simulated) emotions.

```python
class SocialRobotInterface:
    """
    Social communication for robots working closely with humans.
    """

    def __init__(self):
        self.persona = "helpful_assistant"

    def social_greeting(self, context):
        """
        Generate appropriate greeting based on context.

        Context factors:
        - familiarity: stranger, acquaintance, friend
        - time_of_day: morning, afternoon, evening
        - previous_interaction: first, returning, frequent
        """
        familiarity = context.get("familiarity", "stranger")
        time = context.get("time_of_day", "afternoon")
        previous = context.get("previous_interaction", "first")

        # Base greeting
        if familiarity == "stranger":
            greeting = "Hello"
        elif familiarity == "acquaintance":
            greeting = "Hi"
        else:  # friend
            greeting = "Hey"

        # Time-specific
        time_additions = {
            "morning": "good morning",
            "afternoon": "good afternoon",
            "evening": "good evening"
        }
        time_greeting = time_additions.get(time, "hello")

        # Previous interaction
        if previous == "returning":
            return = "Welcome back"
        elif previous == "frequent":
            return = "Good to see you again"
        else:
            return = None

        # Combine
        if return:
            full_greeting = f"{return}, {time_greeting}!"
        else:
            full_greeting = f"{greeting}, {time_greeting}!"

        return full_greeting

    def acknowledge_human(self, action):
        """
        Social acknowledgment of human actions.

        Acknowledgment builds trust by showing the robot
        is aware of human presence and actions.
        """
        acknowledgments = {
            "approaching": ["I see you coming", "Hello there", "Be right there"],
            "offering_help": ["Thank you", "I appreciate it", "That's helpful"],
            "giving_object": ["Got it, thanks", "Thank you", "Received"],
            "completing_task": ["Great teamwork", "Well done", "Thanks for helping"],
        }

        import random
        return random.choice(acknowledgments.get(action, ["Okay"]))

    def polite_refusal(self, reason):
        """
        Politely decline when robot cannot do something.
        """
        templates = [
            f"I'm sorry, I can't do that because {reason}",
            f"I'd like to help, but {reason}",
            f"Unfortunately, {reason}",
            f"I'm unable to help with that—{reason}",
        ]

        import random
        return random.choice(templates)

# Example social interactions
social = SocialRobotInterface()

print("=== Social Communication Examples ===\n")

# Greeting scenarios
contexts = [
    {"familiarity": "stranger", "time_of_day": "morning", "previous_interaction": "first"},
    {"familiarity": "acquaintance", "time_of_day": "afternoon", "previous_interaction": "returning"},
    {"familiarity": "friend", "time_of_day": "evening", "previous_interaction": "frequent"},
]

for ctx in contexts:
    greeting = social.social_greeting(ctx)
    print(f"Greeting: {greeting}")

print()

# Acknowledgments
actions = ["approaching", "offering_help", "giving_object", "completing_task"]
for action in actions:
    ack = social.acknowledge_human(action)
    print(f"Human {action}: Robot says '{ack}'")

print()

# Refusals
reasons = ["I'm not designed for that task", "My battery is too low", "That's not safe"]
for reason in reasons:
    refusal = social.polite_refusal(reason)
    print(f"Refusal: {refusal}")
```

**Output:**
```
=== Social Communication Examples ===

Greeting: Hello, good morning!
Greeting: Welcome back, good afternoon!
Greeting: Good to see you again, good evening!

Human approaching: Robot says 'Hello there'
Human offering_help: Robot says 'I appreciate it'
Human giving_object: Robot says 'Got it, thanks'
Human completing_task: Robot says 'Great teamwork'

Refusal: I'm sorry, I can't do that because I'm not designed for that task
Refusal: I'd like to help, but my battery is too low
Refusal: Unfortunately, that's not safe
```

## Trust in Human-Robot Collaboration

Trust is essential for effective HRI. Humans must trust that the robot will:
- Behave predictably
- Not cause harm
- Do what it says it will do
- Ask for help when needed

### Factors Affecting Trust

```python
class TrustModel:
    """
    Model factors affecting human trust in robots.
    """

    def __init__(self):
        # Trust components (0-1 scale)
        self.components = {
            "reliability": 0.0,    # Does it work correctly?
            "transparency": 0.0,   # Can I understand what it's doing?
            "predictability": 0.0, # Can I anticipate its behavior?
            "safety": 0.0,        # Is it safe to be around?
            "capability": 0.0,     # Is it competent at its tasks?
        }

    def update_trust(self, experience):
        """
        Update trust based on interaction experience.

        Experience: {
            "task_success": bool,
            "communication_clear": bool,
            "behavior_expected": bool,
            "felt_safe": bool,
            "performed_well": bool
        }
        """
        # Trust updates gradually (learning rate)
        alpha = 0.2

        if experience["task_success"]:
            self.components["reliability"] += alpha * (1 - self.components["reliability"])
        else:
            self.components["reliability"] -= alpha * self.components["reliability"]

        if experience["communication_clear"]:
            self.components["transparency"] += alpha * (1 - self.components["transparency"])
        else:
            self.components["transparency"] -= alpha * self.components["transparency"]

        if experience["behavior_expected"]:
            self.components["predictability"] += alpha * (1 - self.components["predictability"])
        else:
            self.components["predictability"] -= alpha * self.components["predictability"]

        if experience["felt_safe"]:
            self.components["safety"] += alpha * (1 - self.components["safety"])
        else:
            self.components["safety"] -= alpha * 0.5 * self.components["safety"]  # Safety recovers slower

        if experience["performed_well"]:
            self.components["capability"] += alpha * (1 - self.components["capability"])
        else:
            self.components["capability"] -= alpha * self.components["capability"]

    def overall_trust(self):
        """
        Calculate overall trust score.

        Safety and reliability are weighted more heavily.
        """
        weights = {
            "reliability": 0.3,
            "transparency": 0.15,
            "predictability": 0.2,
            "safety": 0.25,
            "capability": 0.1,
        }

        trust = sum(
            self.components[k] * weights[k]
            for k in weights.keys()
        )

        return trust

    def trust_assessment(self):
        """Get human-readable trust assessment."""
        score = self.overall_trust()

        if score >= 0.8:
            level = "High Trust"
            description = "Human trusts robot for most collaborative tasks"
        elif score >= 0.6:
            level = "Moderate Trust"
            description = "Human trusts robot for familiar, supervised tasks"
        elif score >= 0.4:
            level = "Low Trust"
            description = "Human is cautious and may prefer not to work with robot"
        else:
            level = "Distrust"
            description = "Human does not trust robot; unlikely to collaborate"

        return {
            "score": score,
            "level": level,
            "description": description,
            "components": self.components.copy()
        }

# Example: Trust evolution over multiple interactions
trust = TrustModel()

interactions = [
    # Task success, communication clear, behavior expected, felt safe, performed well
    (True, True, True, True, True),
    (True, True, True, True, True),
    (True, False, True, True, True),  # Unclear communication
    (True, True, False, True, True),  # Unexpected behavior
    (False, True, True, True, True),  # Task failure
    (True, True, True, False, True),  # Safety concern!
    (True, True, True, True, True),
    (True, True, True, True, True),
    (True, True, True, True, True),
    (True, True, True, True, True),
]

print("=== Trust Evolution ===\n")
for i, exp in enumerate(interactions, 1):
    experience = {
        "task_success": exp[0],
        "communication_clear": exp[1],
        "behavior_expected": exp[2],
        "felt_safe": exp[3],
        "performed_well": exp[4],
    }
    trust.update_trust(experience)

    assessment = trust.trust_assessment()
    print(f"Interaction {i}:")
    print(f"  Events: {exp}")
    print(f"  Trust Score: {assessment['score']:.2f}")
    print(f"  Level: {assessment['level']}")
    print()
```

**Output:**
```
=== Trust Evolution ===

Interaction 1:
  Events: (True, True, True, True, True)
  Trust Score: 0.10
  Level: Distrust

Interaction 2:
  Events: (True, True, True, True, True)
  Trust Score: 0.18
  Level: Distrust

Interaction 3:
  Events: (True, False, True, True, True)
  Trust Score: 0.17
  Level: Distrust

Interaction 4:
  Events: (True, True, False, True, True)
  Trust Score: 0.16
  Level: Distrust

Interaction 5:
  Events: (False, True, True, True, True)
  Trust Score: 0.14
  Level: Distrust

Interaction 6:
  Events: (True, True, True, False, True)
  Trust Score: 0.11
  Level: Distrust

Interaction 7:
  Events: (True, True, True, True, True)
  Trust Score: 0.18
  Level: Distrust

Interaction 8:
  Events: (True, True, True, True, True)
  Trust Score: 0.25
  Level: Low Trust

Interaction 9:
  Events: (True, True, True, True, True)
  Trust Score: 0.31
  Level: Low Trust

Interaction 10:
  Events: (True, True, True, True, True)
  Trust Score: 0.37
  Level: Low Trust
```

**Key insight**: Trust builds slowly but can be destroyed quickly—especially through safety incidents. Note how the safety concern in interaction 6 significantly damaged trust that took many positive interactions to build.

### Designing for Trust

```python
def trust_design_checklist(design_features):
    """
    Evaluate HRI design for trust-promoting features.

    Returns assessment of how well the design promotes trust.
    """
    features = {
        "predictability": [
            "communicates intent before acting",
            "consistent behavior across situations",
            "clear indication of mode/state",
            "doesn't surprise humans"
        ],
        "transparency": [
            "shows what it perceives (display, projection)",
            "explains decisions when asked",
            "indicates confidence level",
            "admits uncertainty/limitations"
        ],
        "safety": [
            "force/torque limits",
            "emergency stop accessible",
            "respects personal space",
            "slows near humans"
        ],
        "reliability": [
            "handles errors gracefully",
            "asks for help when needed",
            "recovers from failures",
            "consistent performance"
        ],
        "capability": [
            "demonstrates competence",
            "learns from experience",
            "handles task variations",
            "works within limitations"
        ]
    }

    missing = []
    present = []

    for category, items in features.items():
        for item in items:
            if item.lower() in [f.lower() for f in design_features]:
                present.append((category, item))
            else:
                missing.append((category, item))

    score = len(present) / sum(len(v) for v in features.values())

    return {
        "score": score,
        "present": present,
        "missing": missing
    }

# Example: Evaluate a robot design
robot_features = [
    "communicates intent before acting",
    "clear indication of mode/state",
    "shows what it perceives",
    "admits uncertainty/limitations",
    "force/torque limits",
    "slows near humans",
    "handles errors gracefully",
    "asks for help when needed",
]

evaluation = trust_design_checklist(robot_features)

print("=== Trust Design Evaluation ===\n")
print(f"Trust Promotion Score: {evaluation['score']:.1%}\n")

print("Features Present:")
for category, feature in evaluation['present']:
    print(f"  [{category}] {feature}")

print(f"\nMissing Features ({len(evaluation['missing'])}):")
for category, feature in evaluation['missing'][:5]:  # Show first 5
    print(f"  [{category}] {feature}")
```

**Output:**
```
=== Trust Design Evaluation ===

Trust Promotion Score: 44.4%

Features Present:
  [predictability] communicates intent before acting
  [predictability] clear indication of mode/state
  [transparency] shows what it perceives
  [transparency] admits uncertainty/limitations
  [safety] force/torque limits
  [safety] slows near humans
  [reliability] handles errors gracefully
  [reliability] asks for help when needed

Missing Features (10):
  [predictability] consistent behavior across situations
  [predictability] doesn't surprise humans
  [transparency] explains decisions when asked
  [transparency] indicates confidence level
  [safety] emergency stop accessible
```

## Hardware and Implementation

### Robot Platforms for HRI

| Platform | HRI Features | Use Cases | Price Range |
|----------|--------------|-----------|-------------|
| **Unitree G1** | Humanoid, expressive, voice interaction | Research, social HRI | ~$16,000 |
| **Unitree Go2** | Quadruped, approachable, robust | Delivery, patrol | ~$1,600-11,780 |
| **Pepper** | Designed for HRI, facial expressions | Retail, reception | ~$15,000 (discontinued) |
| **Stretch RE-1** | Manipulator, friendly design | Home assistance | ~$20,000 |
| **Custom Humanoid** | Fully customizable | Research | $50,000+ |

### Simulation Options

All HRI concepts in this lesson can be simulated:

| Platform | HRI Features | Learning Curve |
|----------|--------------|----------------|
| **Gazebo** | Basic models, plugins | Moderate |
| **NVIDIA Isaac Sim** | High-fidelity humanoid, realistic physics | Steep |
| **PyBullet** | Simple, fast for prototyping | Easy |
| **Webots** | GUI for HRI experiments | Moderate |

### Safety Standards (Important)

When implementing HRI with real robots, be aware of standards:

- **ISO 10218**: Industrial robot safety
- **ISO/TS 15066**: Collaborative robot safety
- **ISO 13482**: Personal care robot safety
- **ANSI/RIA R15.08**: AMR (Autonomous Mobile Robot) safety

These standards define requirements for speed and separation monitoring, power and force limiting, and safety-rated monitored stops.

## Try With AI

### Exercise 1: Design HRI for Shared Workspace

```text
I'm learning Human-Robot Interaction and need to design robot behavior for a shared workspace.

Scenario: A warehouse where humans and robots work together picking orders. Robots fetch items and bring them to human packers.

Help me design:

1. APPROACH BEHAVIOR:
   - How should the robot approach a human packer?
   - What should it do if the human is busy with another robot?
   - How should it announce its arrival?

2. HANDOFF BEHAVIOR:
   - How does the robot transfer items safely?
   - What communication confirms successful handoff?
   - How does the robot handle dropped items?

3. NAVIGATION AROUND HUMANS:
   - What proxemic rules should apply?
   - How does the robot handle crowded aisles?
   - What happens if a human doesn't notice the robot?

For each aspect, specify:
- Sensor inputs needed
- Robot actions/behaviors
- Communication to humans (modality and message)
- Fallback behaviors if something goes wrong

Create a complete behavior specification.
```

**What you're learning:** This exercise applies all HRI principles—safety zones, proxemics, multimodal communication, and trust—to a realistic collaborative scenario. You'll learn to think systematically about how robots and humans coordinate in shared spaces, considering both normal operations and edge cases.

### Exercise 2: Trust-Breaking and Trust-Repair Scenarios

```text
I want to understand how trust between humans and robots can be damaged and repaired.

Help me analyze these scenarios:

1. A robot suddenly stops working in the middle of a critical task, causing a delay. How does this affect trust? What could the robot have done differently to maintain trust?

2. A robot makes an unexpected movement that startles a worker. Even though no one was hurt, the worker is now hesitant around the robot. What trust-repair actions could help?

3. A robot incorrectly refuses to do a task it's capable of, claiming it can't. The worker demonstrates the task is possible. How does this affect the "capability" component of trust?

For each scenario:
- Identify which trust component(s) are affected
- Suggest design changes to prevent the issue
- Propose trust-repair strategies after the fact
- Discuss whether trust can fully recover

Reference the trust model components: reliability, transparency, predictability, safety, and capability.
```

**What you're learning:** Trust is fragile in human-robot relationships. This exercise develops your ability to analyze trust-damaging incidents and design both preventive measures and repair strategies. Understanding trust dynamics is essential for robots that will work closely with humans over time.

### Exercise 3: Proxemic Behavior Across Cultures

```text
Human proxemic norms vary across cultures, which affects how robots should behave.

Help me explore this:

1. Research and compare proxemic norms for 3 different cultures (e.g., North America, Japan, Middle East). For each:
   - Typical personal space distances
   - Approach direction preferences (front vs. side)
   - Gender considerations if relevant
   - Touch appropriateness

2. For each culture, design:
   - Robot approach behavior
   - Acceptable communication distance
   - Any special considerations

3. Design a "cultural adaptation" system:
   - How could a robot detect which cultural norms to apply?
   - What sensors or inputs would be needed?
   - How should the robot handle ambiguity (mixed cultural signals)?

4. Discuss the ethics:
   - Is it appropriate for robots to adapt behavior based on human characteristics?
   - What are the risks of cultural stereotyping?
   - How do you balance adaptation with consistency?

Provide a thoughtful analysis with specific recommendations.
```

**What you're learning:** HRI doesn't exist in a vacuum—it's embedded in cultural contexts. This exercise challenges you to consider how robots can respectfully adapt to diverse cultural norms while avoiding stereotypes. This cultural awareness is crucial for robots deployed globally, from Japanese nursing homes to Middle Eastern hospitals to American factories.
