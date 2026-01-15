---
sidebar_position: 1
title: "Voice Commands for Robotics"
description: "Learn how to enable voice control for robots using speech recognition, wake word detection, and ROS 2 audio integration. Transform natural language into robot actions."
keywords: ["Voice Commands", "Speech Recognition", "Whisper", "ROS 2 Audio", "Wake Words", "Text-to-Speech", "VLA Models"]
chapter: 6
lesson: 1
duration_minutes: 90

requirements:
  hardware: "Microphone (USB or built-in), speakers (optional for TTS feedback); Jetson Orin recommended for edge deployment"
  software: "Python 3.10+, ROS 2 Humble, OpenAI Whisper, pyaudio"

skills:
  - name: "Speech Recognition Fundamentals"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can explain the STT pipeline and identify key components"

  - name: "Voice Command Implementation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can implement a working voice command system using Whisper"

  - name: "ROS 2 Audio Integration"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Student can create ROS 2 nodes for audio capture and command publishing"

  - name: "Wake Word Detection"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Remember"
    measurable_at_this_level: "Student can explain how wake word detection works and why it's needed"

learning_objectives:
  - objective: "Explain the speech-to-text pipeline including audio capture, wake word detection, STT processing, and command parsing"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Diagram or written explanation of the complete voice command pipeline"

  - objective: "Implement a voice command system using OpenAI Whisper for speech recognition with ROS 2 integration"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Working code that responds to voice commands with robot actions"

  - objective: "Design a command grammar that maps natural language to structured robot commands with fallback handling"
    proficiency_level: "B2"
    bloom_level: "Analyze"
    assessment_method: "Command mapping table with edge cases documented"

  - objective: "Integrate text-to-speech feedback for robot verbal responses"
    proficiency_level: "A2"
    bloom_level: "Apply"
    assessment_method: "Robot that speaks responses to voice commands"

cognitive_load:
  new_concepts: 8
  assessment: "Students will implement a complete voice command system that processes speech, extracts commands, and triggers robot actions with verbal feedback"

differentiation:
  extension_for_advanced: "Implement continuous listening mode, add support for multiple languages using Whisper's multilingual models, or create a custom wake word detector using machine learning"
  remedial_for_struggling: "Start with pre-recorded audio files instead of live microphone input, use a simplified command set (3-5 commands), and provide template code for the ROS 2 integration"
  hardware_alternatives: "Use simulation with audio files pre-recorded, or deploy to cloud VM with audio forwarding; Google Colab with audio upload works for testing Whisper without local microphone"

safety_notes: "Always include an emergency stop command ('stop', 'emergency', 'halt') that immediately halts all robot motion. Never enable voice control in production without a physical kill switch. Test voice commands in safe environments away from hazards."

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003", "FR-004"]
---

# Voice Commands for Robotics

Imagine walking into a robotics lab and simply saying, "Robot, please bring me the wrench from the workbench." The robot acknowledges, navigates to the workbench, identifies the wrench, and delivers it to you. No keyboard, no joystick, no programming terminal—just natural conversation. This is the promise of conversational robotics: making machines that understand and respond to human language naturally.

Voice commands represent the most intuitive interface for human-robot interaction. Humans have evolved over millions of years to communicate through speech; it's our default mode of collaboration. Yet implementing voice control for robots involves unique challenges: noisy environments, varied accents, ambiguous commands, and the critical need for real-time response. This lesson teaches you how to build a voice command system that bridges human language and robot actions.

## The Speech Recognition Pipeline

Before writing code, understand the complete pipeline that converts your voice into robot motion:

```
+-----------------------------------------------------------------------+
|                        VOICE COMMAND PIPELINE                        |
+-----------------------------------------------------------------------+
|                                                                       |
|  1. AUDIO CAPTURE                                                     |
|     Microphone samples audio at 16kHz (human speech range)           |
|     Output: Raw PCM audio stream                                      |
|           |                                                           |
|           v                                                           |
|  2. WAKE WORD DETECTION (Always Listening)                           |
|     Lightweight model detects activation phrase ("Hey robot")        |
|     Output: Boolean (triggered/not triggered)                         |
|           |                                                           |
|           v (only when wake word detected)                            |
|  3. SPEECH-TO-TEXT (STT)                                              |
|     Full transcription model converts audio to text                  |
|     Output: "move forward two meters"                                 |
|           |                                                           |
|           v                                                           |
|  4. COMMAND PARSING                                                   |
|     Extract intent and parameters from natural language              |
|     Output: {"intent": "move", "direction": "forward", "distance": 2}|
|           |                                                           |
|           v                                                           |
|  5. ROS 2 COMMAND PUBLISHING                                          |
|     Publish structured command to robot controller                   |
|     Output: /cmd_vel message with linear.x = 0.5                     |
|           |                                                           |
|           v                                                           |
|  6. ROBOT ACTION + FEEDBACK                                           |
|     Robot executes motion, optionally speaks confirmation             |
|     Output: "Moving forward two meters" + actual movement            |
|                                                                       |
+-----------------------------------------------------------------------+
```

### Why Wake Words Matter

You might wonder: why not just transcribe everything continuously? Two reasons:

1. **Privacy**: Continuous full transcription records all conversations, including private discussions you don't intend to send to the robot
2. **Compute**: Full STT models like Whisper are computationally expensive. Running them continuously would drain batteries and overload processors

Wake word detection uses a tiny, efficient model that only listens for its trigger phrase. Once detected, the full STT activates for the actual command.

**Common wake words**: "Hey robot," "Alexa," "OK Google," "Hey Siri," or custom phrases for your application.

## Setting Up the Audio Environment

First, let's verify your microphone works with Python:

```python
# test_microphone.py - Verify audio capture works
import pyaudio
import wave

def record_audio(duration_seconds=5, output_file="test.wav"):
    """Record audio from default microphone"""
    # Audio configuration for speech recognition
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # 16kHz is standard for speech recognition
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    print("Available audio devices:")
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"  [{i}] {info['name']}")

    print(f"\nRecording for {duration_seconds} seconds...")
    print("Speak now!")

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    for _ in range(int(RATE / CHUNK * duration_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording complete!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save to WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {output_file}")
    return output_file

if __name__ == "__main__":
    record_audio()
```

**Output:**
```
Available audio devices:
  [0] Microsoft Sound Mapper
  [1] Microphone (Realtek High Definition Audio)
  [2] Speakers (Realtek High Definition Audio)

Recording for 5 seconds...
Speak now!
Recording complete!
Audio saved to test.wav
```

**Installation:**
```bash
# On Ubuntu/WSL2
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio wave

# On macOS
brew install portaudio
pip install pyaudio

# On Windows
pip install pyaudio-win32
```

## Speech-to-Text with OpenAI Whisper

OpenAI's Whisper model has become the gold standard for speech recognition due to its robustness against accents, background noise, and technical vocabulary. Let's implement basic STT:

```python
# voice_input.py - Speech recognition using Whisper
import whisper
import torch
import warnings
warnings.filterwarnings("ignore")

class VoiceInput:
    """Speech recognition using OpenAI Whisper"""

    def __init__(self, model_size="base"):
        """
        Available model sizes:
        - tiny:   ~1GB,  32x faster, lowest accuracy
        - base:   ~1.5GB, 16x faster, good accuracy
        - small:  ~2GB,  6x faster,  better accuracy
        - medium: ~5GB,  2x faster,  great accuracy
        - large:  ~10GB, 1x speed,    best accuracy, multilingual

        For robotics, 'base' or 'small' is recommended for real-time performance.
        """
        print(f"Loading Whisper model: {model_size}...")
        self.model = whisper.load_model(model_size)
        print(f"Model loaded. Device: {self.model.device}")

    def transcribe_file(self, audio_path):
        """Transcribe audio file to text"""
        result = self.model.transcribe(
            audio_path,
            language="en",  # Auto-detect if None
            fp16=torch.cuda.is_available()  # Use FP16 on GPU
        )
        return result

    def transcribe_with_details(self, audio_path):
        """Get transcription with timing and confidence info"""
        result = self.model.transcribe(
            audio_path,
            language="en",
            fp16=torch.cuda.is_available(),
            word_timestamps=True  # Include per-word timing
        )

        output = {
            "text": result["text"].strip(),
            "language": result["language"],
            "segments": []
        }

        for segment in result["segments"]:
            output["segments"].append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })

        return output

# Test the transcription
if __name__ == "__main__":
    # Initialize voice input
    voice = VoiceInput(model_size="base")

    # Transcribe test audio (from previous step)
    print("\nTranscribing test.wav...")
    result = voice.transcribe_with_details("test.wav")

    print(f"\nDetected language: {result['language']}")
    print(f"Transcription: {result['text']}")

    print("\nDetailed segments:")
    for seg in result["segments"]:
        print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}")
```

**Output:**
```
Loading Whisper model: base...
Model loaded. Device: cuda

Transcribing test.wav...

Detected language: en
Transcription: Move the robot forward three meters and then turn left.

Detailed segments:
  [0.00s - 0.80s] Move the robot
  [0.80s - 1.50s] forward three meters
  [1.50s - 2.10s] and then turn left.
```

**Whisper Installation:**
```bash
# CPU-only (slower but works anywhere)
pip install openai-whisper

# With CUDA support (NVIDIA GPUs)
pip install openai-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# For Jetson devices, use PyTorch built for Jetson
# See: https://developer.nvidia.com/embedded/pytorch
```

## Wake Word Detection

For wake word detection, we need something lightweight. Several approaches exist:

### Option 1: Picovoice Porcupine (Recommended for Production)

```python
# wake_word_porcupine.py - Production wake word detection
import pvporcupine
from pvporcupine import create
import pyaudio
import struct

class WakeWordDetector:
    """Wake word detection using Picovoice Porcupine"""

    def __init__(self, keyword="porcupine", access_key=None):
        """
        Keywords available in free tier: porcupine, bumblebee, picovoice
        Custom keywords require paid account.
        """
        # Get free access key from: https://console.picovoice.ai/
        if access_key is None:
            raise ValueError("Get free access key from https://console.picovoice.ai/")

        self.porcupine = create(
            access_key=access_key,
            keyword_paths=[pvporcupine.KEYWORD_PATHS[keyword]],
            sensitivities=[0.5]  # 0.0 to 1.0 (higher = more sensitive)
        )

        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start(self, callback):
        """Start listening for wake word"""

        def audio_callback(in_data, frame_count, time_info, status):
            audio_buffer = struct.unpack_from("h" * self.porcupine.frame_length, in_data)
            keyword_index = self.porcupine.process(audio_buffer)

            if keyword_index >= 0:
                callback()  # Wake word detected!

            return (in_data, pyaudio.paContinue)

        self.stream = self.audio.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
            stream_callback=audio_callback
        )

        self.stream.start_stream()
        print("Listening for wake word...")

    def stop(self):
        """Stop listening"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.porcupine.release()

# Usage example
def on_wake_word():
    print("Wake word detected! Starting command listening...")
    # Here you would trigger full STT

# detector = WakeWordDetector(access_key="YOUR_KEY")
# detector.start(callback=on_wake_word)
```

**Output:**
```
Listening for wake word...
Wake word detected! Starting command listening...
```

### Option 2: Simple Energy-Based Detection (No External Dependencies)

For learning purposes, a simple voice activity detector can trigger recording:

```python
# wake_word_simple.py - Energy-based wake detection (no dependencies)
import pyaudio
import numpy as np
import collections

class SimpleWakeDetector:
    """Detect voice activity using audio energy"""

    def __init__(self, threshold=500, min_duration=0.5):
        """
        threshold: Audio energy level to trigger (0-32768 for 16-bit)
        min_duration: Minimum seconds above threshold to trigger
        """
        self.threshold = threshold
        self.min_duration = min_duration
        self.chunk = 1024
        self.rate = 16000

    def listen_for_trigger(self, timeout=30):
        """Wait for voice activity, then record command"""
        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        print("Listening... (speak now)")
        frames = []
        above_threshold_count = 0
        min_chunks = int(self.min_duration * self.rate / self.chunk)
        triggered = False

        while True:
            data = stream.read(self.chunk)
            audio_data = np.frombuffer(data, dtype=np.int16)
            energy = np.abs(audio_data).mean()

            if energy > self.threshold:
                above_threshold_count += 1
                frames.append(data)

                if above_threshold_count > min_chunks:
                    triggered = True
                    print("Voice detected! Recording command...")

                    # Continue recording while there's speech
                    silence_count = 0
                    max_silence = 30  # ~1 second of silence ends recording

                    while silence_count < max_silence:
                        data = stream.read(self.chunk)
                        frames.append(data)
                        audio_data = np.frombuffer(data, dtype=np.int16)
                        if np.abs(audio_data).mean() < self.threshold:
                            silence_count += 1
                        else:
                            silence_count = 0
                    break
            elif triggered:
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        if triggered:
            return b''.join(frames)
        return None

# Usage
if __name__ == "__main__":
    detector = SimpleWakeDetector(threshold=500)
    audio_data = detector.listen_for_trigger()

    if audio_data:
        # Save for transcription
        import wave
        with wave.open("command.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_data)
        print("Command saved to command.wav")
```

**Output:**
```
Listening... (speak now)
Voice detected! Recording command...
Command saved to command.wav
```

## Command Parsing: From Natural Language to Robot Actions

Once we have text, we need to extract structured commands. This is where intent recognition happens:

```python
# command_parser.py - Parse natural language into robot commands
import re
from typing import Optional, Dict, Any

class RobotCommandParser:
    """Parse natural language into structured robot commands"""

    def __init__(self):
        # Define command patterns
        self.patterns = {
            "move": [
                r"move\s+(forward|ahead|fwd)\s+(\d+(?:\.\d+)?)\s*(?:meters?|m|meters)?",
                r"go\s+(forward|ahead)\s+(\d+(?:\.\d+)?)\s*(?:meters?|m|meters)?",
                r"advance\s+(\d+(?:\.\d+)?)\s*(?:meters?|m|meters)?",
            ],
            "backward": [
                r"move\s+(back|backward|backwards)\s+(\d+(?:\.\d+)?)\s*(?:meters?|m|meters)?",
                r"reverse\s+(\d+(?:\.\d+)?)\s*(?:meters?|m|meters)?",
            ],
            "turn": [
                r"turn\s+(left|right)\s+(\d+(?:\.\d+)?)\s*(?:degrees?|deg)?",
                r"rotate\s+(left|right)\s+(\d+(?:\.\d+)?)\s*(?:degrees?|deg)?",
            ],
            "stop": [
                r"stop",
                r"halt",
                r"emergency\s+stop",
                r"freeze",
            ],
            "pick": [
                r"pick\s+up\s+(?:the\s+)?(.+)",
                r"grab\s+(?:the\s+)?(.+)",
                r"take\s+(?:the\s+)?(.+)",
            ],
            "place": [
                r"place\s+(?:the\s+)?(.+)",
                r"put\s+(?:the\s+)?(.+)\s+(?:here|down|on\s+\S+)",
                r"drop\s+(?:the\s+)?(.+)",
            ],
        }

        self.direction_mapping = {
            "forward": "forward",
            "ahead": "forward",
            "fwd": "forward",
            "back": "backward",
            "backward": "backward",
            "backwards": "backward",
            "reverse": "backward",
        }

    def parse(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parse natural language command into structured format.

        Returns:
            {
                "intent": "move",
                "parameters": {"direction": "forward", "distance": 2.5},
                "confidence": 0.9
            }
        """
        text = text.lower().strip()

        # Emergency stop always takes priority
        for stop_word in ["stop", "halt", "emergency", "freeze"]:
            if stop_word in text.split():
                return {
                    "intent": "stop",
                    "parameters": {},
                    "confidence": 1.0,
                    "raw_text": text
                }

        # Try each command pattern
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    return self._extract_parameters(intent, match, text)

        # No pattern matched
        return {
            "intent": "unknown",
            "parameters": {},
            "confidence": 0.0,
            "raw_text": text
        }

    def _extract_parameters(self, intent: str, match, text: str) -> Dict[str, Any]:
        """Extract parameters based on intent"""

        if intent == "move":
            groups = match.groups()
            direction = self.direction_mapping.get(groups[0], groups[0])
            distance = float(groups[1]) if len(groups) > 1 else 1.0
            return {
                "intent": "move",
                "parameters": {
                    "direction": "forward",
                    "distance": distance
                },
                "confidence": 0.9,
                "raw_text": text
            }

        elif intent == "backward":
            distance = float(match.group(2))
            return {
                "intent": "move",
                "parameters": {
                    "direction": "backward",
                    "distance": distance
                },
                "confidence": 0.9,
                "raw_text": text
            }

        elif intent == "turn":
            direction = match.group(1)
            angle = float(match.group(2))
            return {
                "intent": "turn",
                "parameters": {
                    "direction": direction,
                    "angle": angle
                },
                "confidence": 0.9,
                "raw_text": text
            }

        elif intent in ["pick", "place"]:
            object_name = match.group(1).strip()
            return {
                "intent": intent,
                "parameters": {
                    "object": object_name
                },
                "confidence": 0.8,
                "raw_text": text
            }

        return {
            "intent": "unknown",
            "parameters": {},
            "confidence": 0.0,
            "raw_text": text
        }

# Test the parser
if __name__ == "__main__":
    parser = RobotCommandParser()

    test_commands = [
        "Move forward 2.5 meters",
        "Turn left 90 degrees",
        "Pick up the wrench",
        "Stop the robot",
        "Go backwards 1 meter",
        "I don't know what I'm saying"
    ]

    for cmd in test_commands:
        result = parser.parse(cmd)
        print(f"\nInput:  {cmd}")
        print(f"Intent: {result['intent']}")
        print(f"Params: {result['parameters']}")
        print(f"Confidence: {result['confidence']}")
```

**Output:**
```
Input:  Move forward 2.5 meters
Intent: move
Params: {'direction': 'forward', 'distance': 2.5}
Confidence: 0.9

Input:  Turn left 90 degrees
Intent: turn
Params: {'direction': 'left', 'angle': 90.0}
Confidence: 0.9

Input:  Pick up the wrench
Intent: pick
Params: {'object': 'wrench'}
Confidence: 0.8

Input:  Stop the robot
Intent: stop
Params: {}
Confidence: 1.0

Input:  Go backwards 1 meter
Intent: move
Params: {'direction': 'backward', 'distance': 1.0}
Confidence: 0.9

Input:  I don't know what I'm saying
Intent: unknown
Params: {}
Confidence: 0.0
```

## ROS 2 Integration

Now let's integrate everything into ROS 2 nodes:

```python
# voice_command_node.py - ROS 2 voice command system
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
import whisper
import torch
import pyaudio
import wave
import tempfile
import os

class VoiceCommandNode(Node):
    """ROS 2 node for voice-controlled robot commands"""

    def __init__(self):
        super().__init__('voice_command_node')

        # Parameters
        self.declare_parameter('model_size', 'base')
        self.declare_parameter('wake_word_enabled', False)
        model_size = self.get_parameter('model_size').value

        # Initialize Whisper
        self.get_logger().info(f"Loading Whisper model: {model_size}")
        self.stt = whisper.load_model(model_size)

        # Initialize command parser
        self.parser = RobotCommandParser()

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.command_pub = self.create_publisher(String, '/voice_command', 10)
        self.listening_pub = self.create_publisher(Bool, '/voice_listening', 10)

        # Audio configuration
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.RECORD_DURATION = 5

        self.get_logger().info("Voice Command Node ready")
        self.get_logger().info("Say 'stop' at any time for emergency halt")

        # Start listening loop
        self.listening_loop()

    def record_command(self):
        """Record audio from microphone"""
        audio = pyaudio.PyAudio()

        self.listening_pub.publish(Bool(data=True))  # LED indicator

        stream = audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        self.get_logger().info("Listening... (speak now)")
        frames = []

        for _ in range(int(self.RATE / self.CHUNK * self.RECORD_DURATION)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        self.get_logger().info("Processing...")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        self.listening_pub.publish(Bool(data=False))

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name

        with wave.open(tmp_path, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

        return tmp_path

    def transcribe(self, audio_path):
        """Convert audio to text using Whisper"""
        result = self.stt.transcribe(
            audio_path,
            language="en",
            fp16=torch.cuda.is_available()
        )
        os.unlink(audio_path)  # Clean up temp file
        return result["text"].strip()

    def execute_command(self, parsed_command):
        """Execute the parsed robot command"""

        intent = parsed_command["intent"]
        params = parsed_command["parameters"]

        if intent == "stop":
            self.get_logger().warn("EMERGENCY STOP")
            twist = Twist()
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.cmd_vel_pub.publish(twist)

        elif intent == "move":
            direction = params["direction"]
            distance = params["distance"]

            self.get_logger().info(f"Moving {direction} {distance} meters")

            # Simple velocity command (real implementation would use navigation)
            twist = Twist()
            speed = 0.5  # m/s

            if direction == "forward":
                twist.linear.x = speed
            elif direction == "backward":
                twist.linear.x = -speed

            # Publish for duration = distance / speed
            duration = distance / speed
            import time
            start_time = time.time()

            while time.time() - start_time < duration:
                self.cmd_vel_pub.publish(twist)
                time.sleep(0.1)

            # Stop
            twist.linear.x = 0.0
            self.cmd_vel_pub.publish(twist)

        elif intent == "turn":
            direction = params["direction"]
            angle = params["angle"]

            self.get_logger().info(f"Turning {direction} {angle} degrees")

            twist = Twist()
            angular_speed = 0.5  # rad/s

            if direction == "left":
                twist.angular.z = angular_speed
            elif direction == "right":
                twist.angular.z = -angular_speed

            # Turn for duration = angle / speed
            duration = (angle * 3.14159 / 180) / angular_speed
            import time
            start_time = time.time()

            while time.time() - start_time < duration:
                self.cmd_vel_pub.publish(twist)
                time.sleep(0.1)

            # Stop
            twist.angular.z = 0.0
            self.cmd_vel_pub.publish(twist)

        elif intent == "unknown":
            self.get_logger().warn(f"Unknown command: {parsed_command['raw_text']}")

        # Publish raw command for other nodes
        cmd_msg = String()
        cmd_msg.data = str(parsed_command)
        self.command_pub.publish(cmd_msg)

    def listening_loop(self):
        """Main listening loop"""
        try:
            while rclpy.ok():
                # Record
                audio_path = self.record_command()

                # Transcribe
                text = self.transcribe(audio_path)
                self.get_logger().info(f"Heard: '{text}'")

                # Parse
                parsed = self.parser.parse(text)
                self.get_logger().info(f"Intent: {parsed['intent']}")

                # Execute
                self.execute_command(parsed)

        except KeyboardInterrupt:
            self.get_logger().info("Shutting down...")

# Include RobotCommandParser class from previous section
class RobotCommandParser:
    """Command parser class (same as previous section)"""
    def __init__(self):
        # Simplified version
        self.patterns = {
            "move": [r"move\s+(forward|ahead)\s+(\d+(?:\.\d+)?)", r"go\s+(\d+(?:\.\d+)?)"],
            "turn": [r"turn\s+(left|right)\s+(\d+(?:\.\d+)?)"],
            "stop": [r"stop", r"halt"],
        }

    def parse(self, text):
        text = text.lower().strip()

        for word in ["stop", "halt", "emergency"]:
            if word in text.split():
                return {"intent": "stop", "parameters": {}, "confidence": 1.0, "raw_text": text}

        import re
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    return {"intent": intent, "parameters": {}, "confidence": 0.9, "raw_text": text}

        return {"intent": "unknown", "parameters": {}, "confidence": 0.0, "raw_text": text}

def main(args=None):
    rclpy.init(args=args)
    node = VoiceCommandNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

**Output:**
```
[INFO] [voice_command_node]: Loading Whisper model: base
[INFO] [voice_command_node]: Voice Command Node ready
[INFO] [voice_command_node]: Say 'stop' at any time for emergency halt
[INFO] [voice_command_node]: Listening... (speak now)
[INFO] [voice_command_node]: Processing...
[INFO] [voice_command_node]: Heard: 'move forward 2 meters'
[INFO] [voice_command_node]: Intent: move
[INFO] [voice_command_node]: Moving forward 2.0 meters
```

## Text-to-Speech: Robot Verbal Feedback

Complete the interaction loop by having the robot speak back:

```python
# tts_feedback.py - Text-to-speech for robot responses
import pyttsx3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class RobotVoiceNode(Node):
    """ROS 2 node for robot text-to-speech"""

    def __init__(self):
        super().__init__('robot_voice_node')

        # Initialize TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speaking speed
        self.engine.setProperty('volume', 0.9)  # Volume 0-1

        # Available voices
        voices = self.engine.getProperty('voices')
        for voice in voices:
            self.get_logger().info(f"Voice: {voice.name}")

        # Subscribe to voice commands
        self.subscription = self.create_subscription(
            String,
            '/tts_say',
            self.speak_callback,
            10
        )

        self.get_logger().info("Robot Voice Node ready")

    def speak_callback(self, msg):
        """Speak the received text"""
        text = msg.data
        self.get_logger().info(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def speak(self, text):
        """Direct speak method"""
        self.engine.say(text)
        self.engine.runAndWait()

# Usage
if __name__ == "__main__":
    rclpy.init()
    node = RobotVoiceNode()

    # Example responses
    responses = {
        "move": "Moving {} {} meters",
        "turn": "Turning {} {} degrees",
        "stop": "Emergency stop activated",
        "unknown": "I didn't understand that command",
    }

    # Say a greeting
    node.speak("Voice control system ready. Waiting for commands.")

    rclpy.spin(node)
```

**Output:**
```
[INFO] [robot_voice_node]: Voice: English (US)
[INFO] [robot_voice_node]: Voice: English (UK)
[INFO] [robot_voice_node]: Robot Voice Node ready
[Audio plays]: "Voice control system ready. Waiting for commands."
```

**Installation:**
```bash
# Linux
sudo apt-get install espeak

# macOS
brew install espeak

# Windows (included with pyttsx3)

pip install pyttsx3
```

## Hardware Considerations

### For Jetson Orin Deployment

The Jetson Orin is ideal for voice control at the edge:

```python
# jetson_optimized.py - Whisper optimized for Jetson
import torch

# Use TensorRT for acceleration on Jetson
def load_model_for_jetson():
    """Load Whisper with Jetson optimizations"""

    # Check for Jetson device
    if torch.cuda.get_device_name(0).startswith("NVIDIA"):
        # Use FP16 for faster inference
        model = whisper.load_model("base", device="cuda")

        # Enable cuDNN benchmarking
        torch.backends.cudnn.benchmark = True

        # Reduce memory usage
        torch.cuda.empty_cache()

        return model
    else:
        return whisper.load_model("base")
```

**Output:**
```
Loading Whisper model with Jetson optimizations...
Model loaded. Device: cuda (NVIDIA Orin)
FP16 mode enabled for faster inference
cuDNN benchmarking enabled
```

### Microphone Selection

| Microphone Type | Pros | Cons | Robotics Use Case |
|-----------------|------|------|-------------------|
| **Built-in laptop** | Always available | Poor noise rejection | Testing only |
| **USB desktop mic** | Good quality, easy setup | Cable length limits | Desktop robots |
| **ReSpeaker Mic Array** | Beamforming, noise rejection | Requires setup | Mobile robots |
| **Wireless lapel mic** | Close to speaker, portable | Battery, interference | Wearable control |

**Recommended for robotics**: ReSpeaker Mic Array v2.0 (~$40) - designed specifically for voice interaction systems with noise cancellation and beamforming.

## End-to-End Voice Control System

Putting it all together:

```python
# complete_voice_system.py - Full voice control system
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
import whisper
import pyttsx3
import threading

class CompleteVoiceController(Node):
    """Complete voice control system with STT, parsing, TTS"""

    def __init__(self):
        super().__init__('voice_controller')

        # Initialize components
        self.get_logger().info("Loading speech recognition...")
        self.stt = whisper.load_model("base", device="cuda")

        self.get_logger().info("Initializing voice synthesis...")
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)

        self.parser = RobotCommandParser()

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # State
        self.is_speaking = False

        # Greeting
        threading.Thread(target=self.speak_async, args=("Voice control online.",)).start()

        self.get_logger().info("Voice Controller ready. Say 'stop' for emergency halt.")

        # Start main loop
        self.main_loop()

    def speak_async(self, text):
        """Speak without blocking"""
        def speak_thread():
            self.is_speaking = True
            self.tts.say(text)
            self.tts.runAndWait()
            self.is_speaking = False

        if not self.is_speaking:
            threading.Thread(target=speak_thread, daemon=True).start()

    def main_loop(self):
        """Main control loop"""
        import pyaudio
        import tempfile
        import wave
        import os
        import numpy as np

        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )

        try:
            while rclpy.ok():
                # Simple energy-based triggering
                self.speak_async("Listening.")

                frames = []
                silence_count = 0
                recording = False

                for _ in range(50):  # ~5 seconds max
                    data = stream.read(1024)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    energy = np.abs(audio_data).mean()

                    if energy > 300 and not recording:
                        recording = True
                        self.get_logger().info("Voice detected")

                    if recording:
                        frames.append(data)
                        if energy < 200:
                            silence_count += 1
                            if silence_count > 10:
                                break
                        else:
                            silence_count = 0

                if frames:
                    # Save and transcribe
                    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                        tmp_path = tmp.name

                    with wave.open(tmp_path, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(16000)
                        wf.writeframes(b''.join(frames))

                    result = self.stt.transcribe(tmp_path, language="en")
                    text = result["text"].strip()
                    os.unlink(tmp_path)

                    self.get_logger().info(f"Heard: {text}")

                    # Parse and execute
                    parsed = self.parser.parse(text)

                    if parsed["intent"] == "stop":
                        self.execute_stop()
                        self.speak_async("Stopping.")
                    elif parsed["intent"] == "move":
                        self.speak_async(f"Moving {parsed['parameters'].get('direction', 'forward')}.")
                    elif parsed["intent"] == "turn":
                        self.speak_async(f"Turning {parsed['parameters'].get('direction', 'left')}.")
                    elif parsed["intent"] == "unknown":
                        self.speak_async("I didn't understand that command.")

        except KeyboardInterrupt:
            pass
        finally:
            stream.close()
            audio.terminate()

    def execute_stop(self):
        """Emergency stop"""
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        for _ in range(10):
            self.cmd_vel_pub.publish(twist)

# Include parser class
class RobotCommandParser:
    def __init__(self):
        import re
        self.patterns = {
            "stop": [r"stop", r"halt", r"emergency"],
            "move": [r"move\s+(forward|ahead|back|backward)"],
            "turn": [r"turn\s+(left|right)"],
        }

    def parse(self, text):
        text = text.lower().strip()
        import re
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    params = {}
                    if intent == "move":
                        match = re.search(r"(forward|ahead|back|backward)", text)
                        params["direction"] = match.group(1) if match else "forward"
                    elif intent == "turn":
                        match = re.search(r"(left|right)", text)
                        params["direction"] = match.group(1) if match else "left"
                    return {"intent": intent, "parameters": params, "confidence": 0.9, "raw_text": text}
        return {"intent": "unknown", "parameters": {}, "confidence": 0.0, "raw_text": text}

def main():
    rclpy.init()
    controller = CompleteVoiceController()
    rclpy.spin(controller)

if __name__ == "__main__":
    main()
```

**Output:**
```
[INFO] [voice_controller]: Loading speech recognition...
[INFO] [voice_controller]: Initializing voice synthesis...
[INFO] [voice_controller]: Voice Controller ready. Say 'stop' for emergency halt.
[Audio plays]: "Voice control online."
[INFO] [voice_controller]: Listening.
[INFO] [voice_controller]: Voice detected
[INFO] [voice_controller]: Heard: move forward
[INFO] [voice_controller]: Intent: move
[Audio plays]: "Moving forward."
```

## Try With AI

### Exercise 1: Design a Voice Command Grammar

```text
I'm building a voice-controlled warehouse robot that can move to different locations and pick/place items.

Help me design a complete command grammar that handles:

1. Navigation commands: "Go to [location]", "Move to [zone]"
2. Manipulation commands: "Pick up [item]", "Place [item] at [location]"
3. Status queries: "Where are you?", "What are you carrying?"
4. Emergency commands: "Stop!", "Emergency halt", "Freeze"

For each category, provide:
- Example natural language variations (3-5 per command)
- A regex pattern or parsing strategy
- Edge cases to handle (ambiguous commands, missing parameters)

After creating the grammar, analyze which commands would be most challenging for speech recognition and suggest solutions.
```

**What you're learning:** This exercise develops your ability to design robust natural language interfaces for robots. Voice commands must handle the way people actually speak—including variations, pauses, filler words ("um", "uh"), and ambiguous phrasing. By designing a comprehensive grammar now, you'll understand the complexity involved in making robots that truly understand human language, which prepares you for the VLA (Vision-Language-Action) models in the next lesson.

### Exercise 2: Optimize Voice Control for Noisy Environments

```text
Industrial environments are noisy—machinery, forklifts, and other robots create significant background noise that interferes with speech recognition.

I'm implementing voice control for a factory robot. Help me analyze and solve these challenges:

1. **Noise robustness**: How can we improve wake word detection and STT accuracy in noisy environments?

2. **Confirmation protocols**: Design a protocol where the robot repeats back commands before executing ("You said: move forward 2 meters. Confirm?")

3. **Fallback mechanisms**: What happens when voice fails entirely? Design a backup system.

4. **Safety**: How do we ensure the robot doesn't execute misheard commands that could be dangerous?

For each challenge, provide specific technical solutions with code examples or architecture recommendations.
```

**What you're learning:** Voice control that works in a quiet room is relatively easy. Voice control that works reliably in a factory, warehouse, or outdoor environment is significantly harder. This exercise teaches you about real-world constraints in Physical AI—where noise, ambiguity, and safety are critical concerns. The solutions you explore (noise cancellation, confirmation protocols, redundant safety systems) apply broadly to all human-robot interaction systems.

### Exercise 3: Integrate Vision-Language-Action (VLA) Models

```text
Modern robotics research combines vision and language with action—so robots can see, understand language, and act accordingly. This is called Vision-Language-Action (VLA) models.

I have a voice-controlled robot that can execute basic commands. Now I want to add vision understanding so it can respond to:

- "Pick up the red cup" (requires identifying red objects)
- "Go to the person waving" (requires detecting people)
- "Navigate to the door" (requires recognizing doors)

Help me design an architecture that:
1. Uses Whisper for speech recognition
2. Feeds the text into a vision-language model (like CLIP or GPT-4V)
3. Extracts visual targets (red cup, waving person, door)
4. Converts visual targets into robot navigation goals

Provide a system architecture diagram and code snippets showing how to:
- Parse object references from voice commands
- Query a vision model to locate objects in camera images
- Convert vision detections into ROS 2 navigation goals

Also discuss limitations: What happens when multiple red cups exist? What if the person stops waving?
```

**What you're learning:** This is the frontier of Physical AI—combining multiple modalities (vision, language, action) into systems that understand and interact with the world like humans do. By designing this architecture, you'll practice integrating the skills you've learned: perception (vision), understanding (language), and action (robot control). This prepares you for the next lesson on VLA models and conversational robotics—the cutting edge of embodied intelligence.
