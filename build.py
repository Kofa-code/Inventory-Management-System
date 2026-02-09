# build.py
import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.py',
    '--name=ABSAM_SPARES_Trial',
    '--onefile',
    '--windowed',
    '--add-data=trial_data.json:.',
    '--add-data=database.py:.',
    '--add-data=modules:modules',
    '-i bike.jpg',
    '--clean',
    '--noconfirm'
])