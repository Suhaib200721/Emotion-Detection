# Emotion Detection System

## Project overview

Emotion Detection System is a real-time computer vision application that uses
a webcam, OpenCV, and DeepFace to estimate facial emotion. It draws a box
around analyzed faces and shows the dominant emotion and its score on the
camera preview.

## Abstract

Emotion Detection System is a real-time computer vision application that identifies human emotions from facial expressions using a webcam. The system captures live video frames and uses the DeepFace library to analyze facial expressions and recognize the dominant emotion. The detected emotion is displayed directly on the camera window, allowing users to observe the result in real time. The system can identify emotions such as happy, sad, angry, neutral, surprise, fear, and disgust. Python, OpenCV, and DeepFace are used to implement the application. This project demonstrates how facial analysis and artificial intelligence can be applied to understand human emotions and can serve as a basic foundation for applications in human-computer interaction, education, and other emotion-aware systems.

## Objectives

- Capture live frames from the computer's webcam.
- Detect faces and analyze their expressions with DeepFace.
- Display the dominant emotion, confidence score, and face rectangle.
- Keep the preview responsive by reusing predictions between analysis runs.
- Release the webcam and close the preview cleanly when the user exits.

## Technologies used

- Python 3.12 (64-bit)
- OpenCV (`opencv-python`)
- DeepFace
- TensorFlow
- NumPy

## Features

- Real-time webcam preview (camera index `0`).
- Seven emotion labels: happy, sad, angry, neutral, surprise, fear, and disgust.
- Face rectangles and dominant emotion percentages.
- A "No face detected" message when no face is visible.
- Emotion analysis runs once per second; the latest result is shown between runs.
- Press **Q** or **Esc** to quit safely.
- Clear startup messages for missing dependencies and webcam access failures.

The displayed percentage is DeepFace's model score for the dominant emotion; it
should not be interpreted as a calibrated probability or as a reliable measure
of a person's actual internal emotional state.

## Project structure

```text
Emotion_Detection_System/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation (Windows Command Prompt)

1. Install 64-bit Python 3.12 and ensure the `python` command is available.
2. Open Command Prompt and move into the project folder:

   ```bat
   cd /d "D:\Emotion Detection\Emotion_Detection_System"
   ```

3. If `.venv` does not exist yet, create it. Then activate the project
   environment:

   ```bat
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

4. Confirm that the active interpreter is the project's virtual environment,
   then upgrade pip and install the pinned, compatible dependencies:

   ```bat
   python -c "import sys; print(sys.executable)"
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

The interpreter path printed by the first command should end in
`Emotion_Detection_System\.venv\Scripts\python.exe`.

The first installation can take several minutes because TensorFlow and its
dependencies are large. DeepFace may also download its emotion-analysis model
when the application is first run; an internet connection and sufficient disk
space are required for that initial download.

The requirements deliberately pin DeepFace and RetinaFace releases that use
`opencv-python` rather than requiring a second, headless OpenCV distribution.
That lets this webcam application use the Windows GUI functions from a single
OpenCV package.

## Execution

From the activated virtual environment in the project folder:

```bat
python main.py
```

To run it in Visual Studio Code:

1. Select **File > Open Folder...** and open `Emotion_Detection_System`.
2. Open the Command Prompt terminal in VS Code (**Terminal > New Terminal**).
3. Run:

   ```bat
   cd /d "D:\Emotion Detection\Emotion_Detection_System"
   .venv\Scripts\activate.bat
   python main.py
   ```

4. If prompted, select the interpreter at `.venv\Scripts\python.exe` using
   **Python: Select Interpreter** from the Command Palette.

The application opens an OpenCV window. Face analysis may take longer on the
first run while DeepFace downloads and initializes its model. Press **Q** or
**Esc** while the preview window is active to close it.

## Expected output

A live camera window shows green rectangles around faces and labels such as
`Happy: 92.4%`. If no face is detected, the window displays `No face detected`.
The exact scores vary with lighting, camera quality, pose, and the model.

## Troubleshooting

- **`No module named ...` or a dependency import error:** Make sure the
  `.venv` is activated, confirm `python -c "import sys; print(sys.executable)"`
  points into `.venv`, then run `python -m pip install -r requirements.txt`.
  In VS Code, select `.venv\Scripts\python.exe` using **Python: Select
  Interpreter**.
- **OpenCV `imshow` says "The function is not implemented":** This typically
  means a headless OpenCV build is being imported. Check installed distributions
  with `python -m pip list | findstr /i opencv`; this project should have only
  `opencv-python 4.11.0.86`, not `opencv-python-headless`,
  `opencv-contrib-python`, or `opencv-contrib-python-headless`. Remove any
  conflicting builds and reinstall the pinned requirements:

  ```bat
  python -m pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless opencv-contrib-python-headless
  python -m pip install -r requirements.txt
  ```

  Confirm the loaded OpenCV build has GUI support:

  ```bat
  python -c "import cv2; print(cv2.__version__); print([line.strip() for line in cv2.getBuildInformation().splitlines() if line.strip().startswith('GUI:')])"
  ```

  On Windows, the GUI line should report `WIN32` or `WIN32UI`, not `NONE`. If
  it still reports `NONE`, check `sys.executable` and ensure Python is loading
  packages from this project's `.venv`.
- **TensorFlow or Keras import/DLL errors:** Use 64-bit Python 3.12, check
  versions with `python -m pip show tensorflow tf-keras keras`, and reinstall
  the pinned requirements in the active `.venv`. TensorFlow and `tf-keras`
  versions must match; this project pins both to `2.21.0`.
- **Webcam cannot be opened:** Check Windows **Settings > Privacy & security >
  Camera** permissions, connect/enable the camera, close video-call or camera
  applications that may be using it, and try again. The program uses camera
  index `0`; systems with multiple cameras may need a different index in
  `main.py`.
- **DeepFace model download fails:** Check internet access, proxy/firewall
  settings, and available disk space, then run the application again so the
  model download can complete. If a partial download remains, remove only the
  incomplete DeepFace model file from the DeepFace cache and retry.
- **Slow or inconsistent detection:** Use good front lighting, face the camera,
  close other CPU/GPU-intensive applications, and allow the first-run model
  initialization to finish. Inference performance depends on the machine.

## Limitations

- The app needs a working webcam and an initial model download.
- Emotion scores can be inaccurate and may vary with lighting, pose, occlusion,
  camera quality, and model bias.
- Facial-expression classification does not establish a person's true
  emotional state and should not be used for consequential decisions.
- Running analysis on a CPU or analyzing multiple faces can cause delays.
- The lightweight OpenCV face detector and DeepFace may not detect the same
  faces in difficult conditions.

## Future enhancements

- Add a settings screen for selecting cameras and adjusting analysis intervals.
- Improve performance with hardware acceleration or asynchronous inference.
- Add optional logging or aggregate visualizations with privacy safeguards.
- Evaluate performance across diverse, consented datasets and environments.
