# 🛰️ Image Restoration for Enhancing Optical Navigation in Space

> Lens flare removal and image restoration for spacecraft pose estimation using transformer-based deep learning.

**Authors:** Menah Hammad, May Hammad  
**Date:** March 17, 2025  
**Report:** *Image Restoration for Enhancing Optical Navigation in Space*

---

## 📖 Overview

Optical navigation systems in space are frequently degraded by lens flare — caused by sunlight reflections and artificial light sources — introducing errors in feature detection and tracking. This project adapts state-of-the-art **nighttime flare removal models** to space-based imagery by:

- Augmenting the **SPEED+** spacecraft pose estimation dataset with synthetic flares from **Flare7K++**
- Fine-tuning **Uformer** (standard and depth-aware variants) for flare suppression
- Evaluating an alternative **FF-Former** window-based transformer model

**Space Deflare** is a deep learning pipeline that removes lens flare from spacecraft images to improve pose estimation and optical navigation. Sunlight reflections in space cameras corrupt the images used to track a spacecraft's position and orientation — this project fights that by fine-tuning transformer models on a synthetic dataset built by injecting realistic flares onto the SPEED+ benchmark.

The star model, **Uformer + Depth**, adds a depth map as a 4th input channel so the network can better distinguish real light sources from artifact glare.

---

## 🔗 Acknowledgements & Original Repositories

This project integrates components from two original repositories:

- **[Flare7K Dataset Repository](https://github.com/ykdai/Flare7K.git)** – for synthetic flare generation.
- **[Flare-Free-Vision: Empowering Uformer with Depth Insights](https://github.com/yousefkotp/Flare-Free-Vision-Empowering-Uformer-with-Depth-Insights.git)** – base Uformer + depth implementation.

We created a **custom workflow** to build and use a modified flare dataset using a combination of modified model files and a new dataset loading/processing script (`flare_dataset.py`). The rest of the original code from the repositories remains **unedited**.

---

## 📁 Project Structure
project_root/
├── create_flare_dataset.py # Script to generate initial dataset
├── flare_dataset.py # Script to handle dataset loading & processing
├── models/
│ └── (modified model files)
├── (other original repository scripts – unmodified)
└── README.md # This file

---

## 📁 Dataset Preparation

### Required Datasets

1. **SPEED+** dataset – download from [Zenodo](https://zenodo.org/record/5588480)
2. **Flare7K++** dataset – download from [Google Drive](https://drive.google.com/uc?id=1PPXWxn7gYvqwHX301SuWmjI7IUUtqxab)

### Dataset Folder Structure (after preparation)
dataset/
├── speed+lightbox/
│ ├── blended/ # Contains flare images
│ ├── resized/ # Contains resized images
├── sunlamp/
│ ├── blended/ # Contains flare images
│ ├── resized/ # Contains resized images
├── synthetic/
│ ├── blended/ # Contains flare images
│ ├── resized/ # Contains resized images

text

- **blended/**: Images with synthetic flares (input to model)
- **resized/**: Clean, resized original images (target for training)

### Dataset Creation Script

Edit the paths in `create_flare_dataset.py` to match your directories:

```python
parent_directory = "/path/to/your/dataset"
flare_images_path = "/path/to/Flare7K++"
main_output_path = "/path/to/output"


## 🔥 Deflaring Results



### Result : Satellite with Strong Lens Flare

 ![Results ](figures/qualitative_results_0000.png)
 ![Results ](figures/qualitative_results_0001.png)
 ![Results ](figures/qualitative_results_0002.png) 
