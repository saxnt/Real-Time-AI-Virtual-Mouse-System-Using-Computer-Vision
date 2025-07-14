# Hand Detection Application

## Overview
The Hand Detection Application is a gesture recognition system that utilizes hand movements to control various system functions such as volume adjustment, brightness control, and mouse actions. The application leverages the MediaPipe library for hand tracking and gesture recognition, providing an intuitive interface for users to interact with their devices.

## Features
- Gesture recognition using hand landmarks.
- Control system brightness and volume through pinch gestures.
- Mouse control through various hand gestures.
- Real-time processing using a webcam.

## Installation Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hand-detector.git
   ```
2. Navigate to the project directory:
   ```
   cd hand-detector
   ```
3. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

## Usage Guidelines
1. Ensure your webcam is connected and functioning.
2. Run the Jupyter Notebook:
   ```
   jupyter notebook src/hand_detector.ipynb
   ```
3. Follow the instructions in the notebook to start using the gesture recognition features.

## Project Structure
```
hand-detector
├── src
│   ├── hand_detector.ipynb       # Jupyter Notebook for hand detection application
│   ├── gesture_controller.py      # Manages camera input and gesture processing
│   ├── controller.py              # Handles actions triggered by gestures
│   ├── hand_recog.py              # Recognizes hand gestures based on landmarks
│   └── utils
│       └── __init__.py            # Initialization file for utils package
├── requirements.txt               # Required Python libraries
├── README.md                      # Project documentation
└── docs
    └── libraries.md               # Documentation for required libraries
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.