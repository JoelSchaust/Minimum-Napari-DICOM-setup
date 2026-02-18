## Instructions on how to use choroid_viewer.py:

# running the python skript allows for quick Quality control of Segmentation labels according to choroidalyzer.onnx


# Requirements: 
The QC Viewer requires the dicom-napari Conda environment.

Please install the environment according to the full installation guide provided in the repository:

➡ See installation instructions in the main README.md


# Features
Fast keyboard-based navigation
Overlay of segmentation masks
Adjustable mask colors
Per-image QC scoring
CSV export of ratings
Works with .tif segmentation outputs


## Launching the QC Viewer

Follow these steps to start the viewer.

---

### 1️ Open Miniforge Prompt

Open **Miniforge Prompt** from the Windows Start menu.

---

### 2️ Activate the environment

```bash
conda activate dicom-napari
```
you should now see (dicom-napari) at the start of the terminal prompt line 

### 3 Navigate to the working directory 

Example (script located on drive D:):

```bash
D:
cd D:\OCT_Project
```

Verify the script is present:
```bash
dir -> should list everything in the active directory - including the choroid_viewer.py file 
```
start the viewer.

```bash
python choroid_viewer.py
```

## Usage & Controls

After launching the viewer, images can be reviewed and rated using keyboard shortcuts.

---

### Navigation

| Key | Function |
|-----|----------|
| →   | Load next image |
| ←   | Load previous image |

---

### Quality Control Rating

| Key | Function |
|-----|----------|
| ↑   | Mark image as **GOOD (1)** |
| ↓   | Mark image as **BAD (0)** |

The current rating status is displayed in the napari status bar.
Rating an image will automatically switch to the next image in line.
Rating can be overwritten by navigating to the image and re-rating it again 
---

### Saving Results

| Key | Function |
|-----|----------|
| `s` | Save QC results to CSV |

The output file will be written to: the the stats_dir (momentarily set to \choroid_segmentation\output_data\stat_tables)+
The output file is batch dependend, so make sure you set the right paths (default momentarly set to batch 2026-02-16)