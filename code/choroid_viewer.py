import numpy as np
import imageio.v3 as iio
import napari
import csv
from pathlib import Path

# --- config (expects these to exist in your notebook/context) ---
DATA_ROOT = Path("/macu bilder")
BATCH_DATE = "2026-02-16"
# in readme it should explain that people go into first layer of project folder, do pwd and copy the path to set to DATA_ROOT 
#and they should also give the date_argument in bash 

BATCH_ROOT = DATA_ROOT / "choroid_segmentation/output_data/"

SEGMENTED_DIR = BATCH_ROOT / "segmented_images" / BATCH_DATE
#SEGMENTED_DIR.exists()
STATS_DIR = BATCH_ROOT / "stat_tables"


# --- collect files ---
image_files = sorted(list(Path(SEGMENTED_DIR).glob("*.tif")))
if not image_files:
    raise FileNotFoundError(f"No .tif files found in: {SEGMENTED_DIR}")

current_index = 0

# QC: per-image score aligned to image_files index
# None = unrated, 0 = BAD, 1 = GOOD
qc_scores = [None] * len(image_files)

csv_output_path = Path(STATS_DIR) / f"{BATCH_DATE}_QC.csv"

# --- viewer once ---
viewer = napari.Viewer(title="quality control images")


def _set_label_colors(v_layer, r_layer):
    """Works with older napari: uses color_mode + color_map."""
    v_layer.color_mode = "auto"
    r_layer.color_mode = "auto"

    # RGBA in 0..1, background transparent
    v_layer.color_map = {0: (0, 0, 0, 0), 2: (0, 0, 1, 1)}       # blue
    r_layer.color_map = {0: (0, 0, 0, 0), 6: (1, 0.5, 0, 1)}     # orange

    v_layer.refresh()
    r_layer.refresh()


def load_new_case(viewer, image_path):
    global current_index

    img = iio.imread(image_path)  # expected (H, W, 3)

    layer1 = img[:, :, 0]                      # original
    layer2 = img[:, :, 2].astype(np.int32)     # vessels (0/1)
    layer3 = img[:, :, 1].astype(np.int32)     # region  (0/1)
    layer2[layer2 == 1] = 2
    layer3[layer3 == 1] = 6
    viewer.layers.clear()

    viewer.add_image(layer1, name="original_image", colormap="gray")
    viewer.add_labels(layer2, name="vessels", opacity=0.5)
    viewer.add_labels(layer3, name="region", opacity=0.5)

    v_layer = viewer.layers["vessels"]
    r_layer = viewer.layers["region"]
    _set_label_colors(v_layer, r_layer)

    score = qc_scores[current_index]
    score_txt = "unrated" if score is None else ("GOOD" if score == 1 else "BAD")
    viewer.status = f"{current_index+1}/{len(image_files)} | {score_txt} | {Path(image_path).name}"


def show_current():
    load_new_case(viewer, image_files[current_index])


def save_qc_csv():
    Path(STATS_DIR).mkdir(parents=True, exist_ok=True)  # remove if you don't want auto-create
    with open(csv_output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["index", "filename", "path", "qc_score"])  # header
        for i, p in enumerate(image_files):
            w.writerow([i, Path(p).name, str(p), qc_scores[i]])

    viewer.status = f"Saved QC → {csv_output_path.name}"
    print("Saved:", csv_output_path)


# --- initial load ---
show_current()


@viewer.bind_key('Right', overwrite=True)
def forward_image(viewer):
    global current_index
    if current_index < len(image_files) - 1:
        current_index += 1
        show_current()


@viewer.bind_key('Left', overwrite=True)
def backward_image(viewer):
    global current_index
    if current_index > 0:
        current_index -= 1
        show_current()


@viewer.bind_key('Up', overwrite=True)
def accept_image(viewer):
    global current_index
    qc_scores[current_index] = 1
    viewer.status = f"GOOD (1) | {current_index+1}/{len(image_files)} | {Path(image_files[current_index]).name}"
    print("GOOD:", image_files[current_index])

    # auto-forward
    if current_index < len(image_files) - 1:
        current_index += 1
        show_current()


@viewer.bind_key('Down', overwrite=True)
def reject_image(viewer):
    global current_index
    qc_scores[current_index] = 0
    viewer.status = f"BAD (0)  | {current_index+1}/{len(image_files)} | {Path(image_files[current_index]).name}"
    print("BAD:", image_files[current_index])

    # auto-forward
    if current_index < len(image_files) - 1:
        current_index += 1
        show_current()


@viewer.bind_key('s', overwrite=True)
def save_csv(viewer):
    save_qc_csv()




napari.run()