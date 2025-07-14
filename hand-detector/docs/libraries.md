# Libraries Documentation

This document provides detailed information about the libraries used in the Hand Detector project, including their purpose and how they are utilized within the application.

## OpenCV
- **Purpose**: OpenCV (Open Source Computer Vision Library) is used for real-time computer vision tasks. It provides tools for image processing, video capture, and analysis.
- **Usage**: In this project, OpenCV is utilized to capture video from the webcam, process frames, and display the output with detected hand landmarks.

## MediaPipe
- **Purpose**: MediaPipe is a cross-platform framework for building multimodal applied machine learning pipelines. It is particularly effective for tasks involving computer vision and audio processing.
- **Usage**: This project uses MediaPipe's Hands solution to detect and track hand landmarks in real-time, enabling gesture recognition based on the positions of the fingers.

## PyAutoGUI
- **Purpose**: PyAutoGUI is a library that allows for programmatic control of the mouse and keyboard. It can simulate user input, making it useful for automation tasks.
- **Usage**: In the Hand Detector application, PyAutoGUI is used to control the mouse cursor, perform clicks, and scroll based on detected hand gestures.

## Pycaw
- **Purpose**: Pycaw (Python Core Audio Windows) is a library that provides a simple interface to control audio settings on Windows.
- **Usage**: This library is used to adjust the system volume based on pinch gestures detected by the application.

## Screen Brightness Control
- **Purpose**: This library allows for programmatic control of the screen brightness on supported devices.
- **Usage**: It is utilized to change the screen brightness in response to specific hand gestures, enhancing user experience by allowing adjustments without physical interaction.

## Tkinter
- **Purpose**: Tkinter is the standard GUI toolkit for Python, providing tools to create graphical user interfaces.
- **Usage**: In this project, Tkinter is used to create the main application window, including buttons and labels for user interaction.

## PIL (Pillow)
- **Purpose**: Pillow is a fork of the Python Imaging Library (PIL) that adds image processing capabilities to Python.
- **Usage**: It is used to handle image display within the Tkinter GUI, allowing for the inclusion of images in the application interface.

## Math
- **Purpose**: The math library provides mathematical functions and constants.
- **Usage**: It is used for calculations related to distance and geometry, which are essential for gesture recognition based on hand positions.

## Enum
- **Purpose**: The enum module provides support for creating enumerations, which are a set of symbolic names bound to unique, constant values.
- **Usage**: In this project, enums are used to define gesture types and hand labels, making the code more readable and maintainable.

This documentation serves as a reference for understanding the libraries utilized in the Hand Detector project and their respective roles in the application.