# OCT Segmentation Review Tool

This repository contains a **Napari-based review and correction tool** for manually inspecting, rating, and correcting precomputed OCT segmentations.

The tool is designed for workflows in which segmentation results are already stored as RGB `.tif` files and need to be reviewed one by one by a human annotator. During review, corrected segmentations are saved automatically, and a running CSV table is maintained to document file paths, image dimensions, label areas, and quality ratings.

## Purpose

The script provides a lightweight manual review workflow for segmentation outputs in OCT data.

For each case, the reviewer can:

- open the image together with its segmentation labels in Napari
- inspect the segmentation visually
- manually correct the label layers
- mark the case as **good** or **bad**
- move through the dataset using keyboard shortcuts
- automatically save corrected segmentations
- automatically update a CSV file containing metadata and review results
- resume later from the point where the review was stopped

This setup is intended for datasets with many images, where reproducible manual review and correction must be performed efficiently.


## Folder Structure

The script is expected to be run from the project root directory, for example `OCT_dataset/`.


## Main Features

### 1. Single-case review in Napari

Each file is opened as:

- one grayscale image layer
- one vessel label layer
- one choroid label layer

### 2. Separate editable label layers

The two label masks are loaded as separate Napari label layers so they can be edited independently.

>for manual label correction - on the left side chose the label you want to work on (chor/vit) -> for better visibility it is suggested to hide the label you are not working on by clicking the eye-icon next to the label's name 
> after selecting a layer you can use the brush/eraser/fill tool to manually adjust labels - once you satisfied with the labels remember to save (switching between images will autosave too)

### 3. Contour view by default

Both label layers are shown with:

- `contour = 2` by default

This makes it easier to inspect boundaries without obscuring the underlying OCT image.

### 4. Toggle contour display

Contours can be switched on and off during review via a keyboard shortcut.


### 5. Persistent CSV tracking

A CSV file is maintained continuously to document progress and results.

### 6. Resume support

When the tool is reopened, review resumes from the first image that is not yet represented in the CSV.

If corrected files already exist, they are loaded preferentially instead of the raw segmentation files.

## Keyboard Shortcuts

| Key | Function |
|-----|----------|
| **Right Arrow** | Save current case and open next image |
| **Left Arrow** | Save current case and open previous image |
| **Up Arrow** | Mark current case as **good** |
| **Down Arrow** | Mark current case as **bad** |
| **c** | Toggle contour display on or off |
| **s** | Save current case manually |

## Saved Output

### Corrected segmentation files

Corrected files are written to:

```text
choroid_segmentation/manual_corrected_segmentations/
```

Each corrected file is saved as an RGB TIFF using the same filename as the original input.

The saved output format is:
- **Channel 0**: original image
- **Channel 1**: corrected choroid mask
- **Channel 2**: corrected vessel mask

## Review Workflow

A typical review session works as follows:

1. Start the script from the project root.
2. The tool opens the next image that has not yet been reviewed.
3. Inspect the choroid and vessel contours over the OCT image.
4. Edit the label layers if necessary.
5. Mark the case as **good** or **bad**.
6. Move to the next image using the arrow keys.
7. The current case is saved automatically.
8. Continue until the dataset has been reviewed.

If the session is interrupted, the tool can later be reopened and will continue from the stored review state.


## Requirements

- dicom-napari env (compare github tutorial)

> https://github.com/JoelSchaust/Minimum-Napari-DICOM-setup


### SAVING STATISTICS 
### CSV columns

| Column | Description |
|--------|-------------|
| `index` | Position of the image in the dataset |
| `image_path` | Path to the original input file |
| `corrected_path` | Path to the saved corrected file |
| `height` | Image height |
| `width` | Image width |
| `orig_choroid_pixel_area` | Pixel area of the loaded choroid mask |
| `orig_vessel_pixel_area` | Pixel area of the loaded vessel mask |
| `corrected_choroid_pixel_area` | Pixel area of the saved corrected choroid mask |
| `corrected_vessel_pixel_area` | Pixel area of the saved corrected vessel mask |
| `good` | `True` if marked good |
| `bad` | `True` if marked bad |

> csv is stored in the statistics folder in your project /statistics/segmentation_review.csv