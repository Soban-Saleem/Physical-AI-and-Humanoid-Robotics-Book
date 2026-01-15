#!/usr/bin/env python
# Coding: utf-8

import os

# Full lesson content in base64 to avoid quote escaping

content = """
   "---
sidebar_position: 2
title: \"Sensors and Actuators\"
description: \"Learn how robots perceive and act in the physical world through sensors (perception) and actuators (action). Understand the sensor-actuator loop that enables Physical AI systems.\"
keywords: ["sensors", "actuators", "LIDAR", "IMU", "servo motors", "robot perception", "robot action"]
chapter: 1
lesson: 2
duration_minutes: 60

requirements:

  hardware: "Any computer (simulation-based lesson)"
  software: "Python 3.10+, optional: Gazebo for sensor simulation"
skills:
  - name: "Sensor Fundamentals"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Remember"
    measurable_at_this_level: "Student can identify and describe common robot sensors and their measurements"

  - name: "Actuator Fundamentals"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Remember"
    measurable_at_this_level: "Student can identify and describe common robot actuators and their functions"

  - name: "Sensor-Actuator Loop Understanding"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can explain the perception-decision-action cycle in robotics"


  - name: "Sensor Specification Interpretation"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Understand"
    measurable_at_this_level: "Student can interpret basic sensor specifications like range, resolution, and accuracy"

learning_objectives:
  - objective: "Define sensors and actuators, and explain their roles in the perception and action layers of Physical AI systems"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Written explanation comparing sensor types and actuator types with examples"


  - objective: "Identify five common robot sensors (camera, LIDAR, IMU, encoder, microphone) aY^Z[ˆÚ]XXÚYX\İ\™\È‚ˆ›ÙšXÚY[˜ŞWÛ]™[ˆLˆ‚ˆ›ÛÛWÛ]™[ˆ”™[Y[X™\ˆ‚ˆ\ÜÙ\ÜÛY[ÛY]Ùˆ“X]Ú[™È^\˜Ú\ÙHÜˆ]Z^ˆÛÛ›™Xİ[™ÈÙ[œÛÜœÈÈZ\ˆYX\İ\™[Y[È‚‚‚ˆHØš™Xİ]™Nˆ‘\ØÜšX™H™YH\\ÈÙˆXİX]ÜœÈ
È[İÜœËÙ\›È[İÜœËİ\\ˆ[İÜœÊH[™Z\ˆ\›ÜšX]H\ÙHØ\Ù\È[ˆ›Ø›İXÜÈ‚ˆ›ÙšYY[˜ŞWÛ]™[ˆLˆ‚ˆ›ÛÛWÛ]™[ˆ”™[Y[X™\ˆ‚ˆ\ÜÙ\ÜÛY[ÛY]Ùˆ”ØÙ[˜\š[ËX˜\ÙY]Y\İ[ÛˆÙ[Xİ[™È\›ÜšX]HXİX]Üˆ›ÜˆÜXÚYšXÈ\ÚÜÈ‚‚ˆHØš™Xİ]™Nˆ‘^Z[ˆHÙ[œÛÜ‹XXİX]ÜˆÛÜ
\˜Ù\[Û‹YXÚ\Ú[Û‹XXİ[ÛŠH[™ÚH[YH[^\ÈX]\ˆ[ˆ\ÚXØ[RH‚ˆ›ÙšXÚY[˜ŞWÛ]™[ˆLˆ‚ˆ›ÛÛWÛ]™[ˆ•[™\œİ[™‚ˆ\ÜÙ\ÜÛY[ÛY]Ùˆ‘XYÜ˜[H^[˜][ÛˆÜˆÚÜ\˜YÜ˜\\ØÜšXš[™ÈHÛÜ‚