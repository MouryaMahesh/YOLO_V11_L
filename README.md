# ♻️ AI Smart Waste Detection

A Streamlit-based computer vision application for detecting waste objects in uploaded images using a trained Ultralytics YOLO model. The application provides a dashboard interface for batch image upload, configurable confidence filtering, and visual review of predictions.

> **Project focus:** image-based waste detection and visual inspection. The app loads an existing trained checkpoint; model training and evaluation are performed separately.

---

## ✨ Application Features

- Upload one or multiple images in one session
- Run YOLO detection on uploaded images on demand
- View each original image beside its annotated detection output
- Display predicted class labels and confidence values
- Adjust the confidence threshold from the sidebar
- Switch between dark and light themes
- Review each uploaded image in a separate tab
- Show a message when no objects are detected

## 🧠 Model & Dataset

- **Detector shown in the app interface:** YOLO11L
- **Weights file:** `best.pt`
- **Dataset label shown in the interface:** “Multiple dataset”
- **Inference input:** user-uploaded images

The exact class names and model architecture are determined by the checkpoint loaded at runtime. Add the dataset names, class list, training split, and checkpoint provenance here once you confirm the final training configuration.

### Metrics displayed in the current dashboard

The interface currently displays **Precision: 95.0** and **mAP50: 41.9**. These are UI values; verify them against the evaluation output for the exact checkpoint and dataset before reporting them as validated experimental results. Include the metric scale (e.g. 0–1 or percentage), evaluation split, and evaluation settings in your final report.

---

## 🖥️ Application Workflow

1. Load the trained YOLO checkpoint.
2. Upload one or more JPG, JPEG, or PNG images.
3. Set the confidence threshold in the sidebar.
4. Click **Detect Waste**.
5. Review the original image and annotated prediction.
6. Inspect the detected class labels and confidence scores.

A higher confidence threshold filters out more lower-confidence predictions. A lower threshold may reveal additional detections but can also increase false positives.

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web dashboard |
| Ultralytics YOLO | Object detection and model inference |
| OpenCV | Convert rendered detection output for display |
| Pillow (PIL) | Open and convert uploaded images |

---

## 📂 Project Structure

```text
Waste_Detection/
├── app.py
├── README.md
├── requirements.txt
|
├── Model/
│   └── best.pt
└── ...
```

The application searches for the model in these locations, in order:

```text
Model/best.pt
model/best.pt
best.pt
```

The recommended location is `Model/best.pt`.

---

## ⚙️ Installation & Setup

### 1. Prerequisites

- Python 3.9 or later
- Git (if cloning from GitHub)
- The trained YOLO checkpoint

Check your Python installation:

```bash
python --version
```

### 2. Clone the repository

Replace the URL with the URL of your own GitHub repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Waste_Detection
```

### 3. Create a virtual environment (recommended)

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you do not have a requirements file yet, install the packages used by the application:

```bash
pip install streamlit ultralytics opencv-python Pillow
```

### 5. Add the model checkpoint

Place your trained weights here:

```text
Model/best.pt
```

Make sure the filename is exactly `best.pt`.

---

## 🚀 Run the Application

From the project directory, run:

```bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open that address in your browser.

---

## 🖼️ Supported Inputs & Outputs

**Supported image formats:** `.jpg`, `.jpeg`, `.png`

For each uploaded image, the app can display:

- Original image
- Annotated detection image with bounding boxes
- Detected class names
- Confidence scores
- A no-detections notice when no boxes are returned

The current app does not implement live camera, video-stream, or ZIP-archive input.

---

## 📊 Training & Evaluation Results

Place relevant training and evaluation artifacts in a results folder if you want to publish them alongside the app. Examples include:

- `results.csv`
- `results.png`
- Precision-recall and confidence curves
- Confusion matrices
- Validation prediction examples

Suggested organization (adjust to match the files you actually have):

```text
Training_Results/
├── results.csv
├── results.png
├── BoxPR_curve.png
├── BoxF1_curve.png
├── BoxP_curve.png
├── BoxR_curve.png
├── confusion_matrix.png
└── confusion_matrix_normalized.png
```

Only include filenames that exist in your own results directory. For a meaningful model comparison, document the dataset, class names, split, image size, checkpoint, and metrics for each model.

---

## 🔧 Troubleshooting

### Model file not found

- Confirm that `Model/best.pt` exists.
- Check the capitalization of the folder and filename.
- Confirm that the checkpoint is compatible with the installed Ultralytics package.

### `ModuleNotFoundError`

Activate your virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
```

### No objects detected

- Try adjusting the confidence threshold downward.
- Confirm that the uploaded image contains classes represented in the model's training data.
- Check that the intended checkpoint is being loaded.

### Port 8501 is already in use

Run Streamlit on another port:

```bash
streamlit run app.py --server.port 8502
```

Then open `http://localhost:8502`.

---

## 📌 Current Limitations

- Requires a trained local YOLO checkpoint.
- Accepts image uploads only (JPG, JPEG, PNG).
- Does not train or evaluate models inside the Streamlit interface.
- Dashboard metric labels should be checked against the final evaluation logs before publication.
- Detection quality depends on the trained model, dataset, and confidence threshold.

---


## 👤 Author

**Mourya Mahesh**

[GitHub Profile](https://github.com/MouryaMahesh)

## 📜 License

No specific open-source license is confirmed in the supplied project files. Add a `LICENSE` file and update this section if you choose to publish the project under a particular license.
