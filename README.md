# Minimum Setup for opening DICOM files in Napari
## (1) First time users of Git
if already have Git installed, skip to step 2  

## Install Git

### Windows

1. Download Git for Windows:

https://git-scm.com/install/windows

2. Run the installer and keep **all default settings**.

3. Open **Git Bash** (anywhere) and verify the installation:

```bash
git --version
```

If a version number is displayed, Git is installed correctly.


### macOS

1. Open the Terminal.

2. Check if Git is already installed:

```bash
git --version
```

- If a version number appears → Git is ready to use.
- If not, macOS will prompt you to install the **Command Line Tools**. Confirm the installation.



## (2) Install Python (Miniforge)

We use **Miniforge** to manage Python and all required packages.

It's recommended to not install Anaconda or Miniconda for this setup to avoid dependency conflicts.

---

### Windows & macOS

1. Download Miniforge:

https://github.com/conda-forge/miniforge/releases/latest



2. Run the installer using the **default settings**.

3. Open a terminal:

- **Windows:**  
  Click the Start menu, search for **"Miniforge Prompt"**, and open it.

- **macOS:**  
  Press `Cmd + Space`, type **Terminal**, and press Enter.

4. Verify the installation:

```bash
conda --version
```

- If a version number appears →  ready to use.