# Napari Manual Annotation Tool

A lightweight Napari-based tool for manual annotation of OCT B-scans organized in batch folders.

The tool is built for a simple annotation workflow:

- place **exactly one batch folder** inside `input_images`
- start the annotator
- annotate images one by one
- save outputs into a matching folder inside `annotated_images`

This setup is intended for distributed annotation, where each annotator receives one batch folder and processes it independently.

---

## Folder structure

Expected project structure:

```text
manual_annotation/
├── input_images/
│   └── batch_001/
│       ├── image_001.tif
│       ├── image_002.tif
│       └── ...
├── annotated_images/
├── napari_annotator.py
```

### Input
`input_images` must contain **exactly one batch folder**.

Example:

```text
input_images/
└── batch_007/
```

### Output
When the script starts, it automatically creates a corresponding output folder:

```text
annotated_images/
└── batch_007/
```

All saved annotations from that batch are written there.

---

## Purpose

This tool is used for manual annotation of B-scans with two label layers:

- **VITREOUS**
- **RPE**

For each annotated image, the script saves:

- a **combined segmentation mask**
- a **3-channel QC image**

This allows both clean export of training masks and quick visual inspection of the annotation output.

---

## Features

- automatic detection of the active batch folder in `input_images`
- image-by-image navigation through all `.tif` files in that batch
- two editable label layers:
  - `VITREOUS`
  - `RPE`
- saving of combined masks
- saving of 3-channel QC outputs
- reloading of previously saved annotations when revisiting an image
- contour toggle for improved visual inspection

---

## Saved outputs

For each image, the following files are generated in:

```text
annotated_images/<batch_name>/
```

### 1. Combined mask
```text
<image_stem>_mask.tif
```

Label encoding:
- `0` = background
- `1` = vitreous
- `2` = RPE

### 2. QC image
```text
<image_stem>_3ch.tif
```

Channel layout:
- channel 1: original grayscale image
- channel 2: vitreous binary mask
- channel 3: RPE binary mask

---

## Keybindings

### Navigation
- **Right arrow** → next image
- **Left arrow** → previous image

### Saving
- **s** → save current annotation

### Display
- **c** → toggle contour mode on/off for both label layers

---

## Important behavior

### Reloading annotations
If an image has already been saved, its mask is automatically reloaded when returning to that image.

This means:
- saved work is preserved
- going back and forth between images does **not** remove existing saved annotations

### Unsaved changes
Only saved annotations are restored.  
If changes are made and not saved, they are lost when switching images.

---

## Annotation workflow

1. Copy one batch folder into `input_images`
2. Start `napari_annotator.py`
3. Annotate the current image
4. Press **`s`** to save
5. Move with **Left/Right**
6. Continue until the full batch is completed

After finishing one batch:
- remove the processed batch from `input_images`
- place the next batch folder into `input_images`
- run the script again

---

## Notes

- The script expects `.tif` images as input.
- `input_images` should contain only one batch folder at a time.
- If more than one folder is present, the script stops with an error to prevent mixing batches.
- The output folder name always matches the input batch folder name.

---

## Example

Input:

```text
input_images/
└── batch_012/
    ├── scan_001.tif
    ├── scan_002.tif
    └── scan_003.tif
```

Output after annotation:

```text
annotated_images/
└── batch_012/
    ├── scan_001_mask.tif
    ├── scan_001_3ch.tif
    ├── scan_002_mask.tif
    ├── scan_002_3ch.tif
    └── ...
```

---

## Summary

This tool is intended for fast and structured manual annotation of OCT batches in Napari, with:

- simple b
