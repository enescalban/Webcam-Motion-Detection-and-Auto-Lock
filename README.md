# Webcam-Motion-Detection-and-Auto-Lock
SureLock is a Python project that provides a simple security solution for your computer. It detects motion using your webcam, and if no motion is detected for a specified period of time, it automatically locks your computer.

SureLock README:

## Description
SureLock is a computer vision-based security application that detects motion and automatically locks the computer when no motion is detected for a specified amount of time. This can be useful for ensuring privacy and security, especially when leaving your computer unattended in a public area.

## Installation
1. Clone the repository to your local machine.
2. Install the required Python modules by running `pip install -r requirements.txt`.
3. Install OpenCV by running `pip install opencv-python`.
4. Install PyAutoGUI by running `pip install pyautogui`.

## Usage
1. Run the `lock.py` script using the command `python lock.py`.
2. Move around in front of the camera to test motion detection.
3. When no motion is detected for the specified amount of time (default is 5 seconds), the computer will automatically lock.
4. To unlock the computer, enter your password when prompted.

## Customization
1. You can adjust the amount of time it takes for the computer to lock by changing the `no_motion_lock_time` variable in `lock.py`.
2. You can customize the locking mechanism by modifying the `lock_computer()` function in `lock.py`.
3. You can change the threshold values for motion detection by modifying the `varThreshold` and `history` parameters in `createBackgroundSubtractorMOG2()` function in `lock.py`.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the LICENSE file for more details.
