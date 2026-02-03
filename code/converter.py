import os
import numpy as np
import io
import pydicom
import nibabel as nib
from pathlib import Path
import shutil

input_directory = "../input_data/open_batches"
output_directory = "../output_data"

list_subfolders = os.listdir(input_directory)


for subfolder in list_subfolders:
    follow_path = os.path.join(input_directory, subfolder)
    list_subfolders2 = os.listdir(follow_path)

    output_path = os.path.join(output_directory, subfolder)
    os.makedirs(output_path, exist_ok=True)

    for subfolder2 in list_subfolders2:
        follow_path2 = os.path.join(follow_path, subfolder2)


        if os.path.isdir(follow_path2):
            output_path2 = os.path.join(output_path, subfolder2)
            os.makedirs(output_path2, exist_ok=True)
            input_dir = Path(follow_path2)
            current_saving_dir = Path(output_path2)

            for file_path in input_dir.rglob("*"):
                if not file_path.is_file():
                    continue

                if "oct" not in file_path.name.lower():
                    continue

                try:
                    ds = pydicom.dcmread(file_path)
                    img = np.asarray(ds.pixel_array)
        
                    save_path = current_saving_dir / f"{file_path.stem}.npy"
                    np.save(save_path, img)
        #print("Loaded:", file_path, img.shape)

                except Exception as e:
                    print("Failed:", file_path)
                    print("Reason:", e)
     

#move whole directory to closed batches
    source = Path(follow_path)
    destination = Path(f"../input_data/closed_batches")

    shutil.move(
        source,
        destination,
       # wichtig!
    )  





     