#!/bin/bash

# In den Ordner wechseln, in dem dieses .command-Skript liegt
cd "$(dirname "$0")" || exit 1

SCRIPT_PATH="napari_annotator_v2.py"
ENV_NAME="dicom-napari"

# Prüfen, ob das Python-Skript existiert
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Konnte Skript nicht finden: $SCRIPT_PATH"
    read -n 1 -s -r -p "Taste drücken zum Beenden ..."
    echo
    exit 1
fi

# Mögliche conda/mamba-Installationspfade
CONDA_PATHS=(
    "$HOME/mambaforge/bin/activate"
    "$HOME/Mambaforge/bin/activate"
    "$HOME/miniforge3/bin/activate"
    "$HOME/Miniforge3/bin/activate"
    "/opt/miniforge3/bin/activate"
    "/opt/Miniforge3/bin/activate"
    "/opt/mambaforge/bin/activate"
    "/opt/Mambaforge/bin/activate"
    "$HOME/miniconda3/bin/activate"
    "$HOME/Miniconda3/bin/activate"
    "/opt/miniconda3/bin/activate"
    "/opt/Miniconda3/bin/activate"
)

FOUND_CONDA=""

# Erste existierende activate-Datei suchen
for ACTIVATE_PATH in "${CONDA_PATHS[@]}"; do
    if [ -f "$ACTIVATE_PATH" ]; then
        FOUND_CONDA="$ACTIVATE_PATH"
        break
    fi
done

# Falls keine conda/mamba-Installation gefunden wurde
if [ -z "$FOUND_CONDA" ]; then
    echo "Konnte keine passende conda/mamba-Installation finden."
    echo "Bitte prüfen, ob Miniforge/Mambaforge/Miniconda installiert ist."
    echo "Erwartetes Environment: $ENV_NAME"
    read -n 1 -s -r -p "Taste drücken zum Beenden ..."
    echo
    exit 1
fi

echo "Gefundene conda/mamba-Installation:"
echo "$FOUND_CONDA"
echo

# Environment aktivieren
source "$FOUND_CONDA" "$ENV_NAME"

# Prüfen, ob Aktivierung erfolgreich war
if [ "$CONDA_DEFAULT_ENV" != "$ENV_NAME" ]; then
    echo "Konnte Environment '$ENV_NAME' nicht aktivieren."
    echo "Aktuelles Environment: $CONDA_DEFAULT_ENV"
    read -n 1 -s -r -p "Taste drücken zum Beenden ..."
    echo
    exit 1
fi

echo "Aktives Environment: $CONDA_DEFAULT_ENV"
echo "Starte Napari Annotator..."
echo

# Python-Skript starten
python -u "$SCRIPT_PATH"

echo
read -n 1 -s -r -p "Taste drücken zum Beenden ..."
echo