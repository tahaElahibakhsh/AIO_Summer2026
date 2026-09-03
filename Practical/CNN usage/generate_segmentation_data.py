"""
Synthetic Microscopy Cell Segmentation Dataset Generator
Generates synthetic microscopy scenes with cell blobs, cytoplasm/nucleus textures,
and heavy background dominance (>90% background).
Saves images, binary semantic masks, and instance masks to local disk.
"""

import os
import json
import random
from typing import Tuple, Dict
import numpy as np
from PIL import Image

def generate_cell_scene(img_size: int = 64, num_cells_range: Tuple[int, int] = (2, 4), seed: int = None) -> Dict[str, np.ndarray]:
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
        
    # Dark microscopy background (>90% of image pixels)
    image = np.full((img_size, img_size, 3), 0.12, dtype=np.float32)
    noise = np.random.normal(0.0, 0.02, size=(img_size, img_size, 3)).astype(np.float32)
    image = np.clip(image + noise, 0.0, 1.0)
    
    semantic_mask = np.zeros((img_size, img_size), dtype=np.uint8)
    instance_mask = np.zeros((img_size, img_size), dtype=np.uint8)
    num_cells = random.randint(*num_cells_range)
    yy, xx = np.mgrid[:img_size, :img_size]
    
    for c_id in range(1, num_cells + 1):
        rx = random.randint(6, 10)
        ry = random.randint(6, 10)
        cx = random.randint(rx + 4, img_size - rx - 4)
        cy = random.randint(ry + 4, img_size - ry - 4)
        
        cell_mask = (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) <= 1.0
        nucleus_mask = (((xx - cx) / (rx * 0.45)) ** 2 + ((yy - cy) / (ry * 0.45)) ** 2) <= 1.0
        
        if np.sum(cell_mask) > 15:
            # Cytoplasm texture (cyan/green fluorescence)
            image[cell_mask, 0] = np.random.uniform(0.15, 0.25)
            image[cell_mask, 1] = np.random.uniform(0.65, 0.85)
            image[cell_mask, 2] = np.random.uniform(0.65, 0.85)
            # Bright cell nucleus
            image[nucleus_mask, 0] = np.random.uniform(0.60, 0.80)
            image[nucleus_mask, 1] = np.random.uniform(0.85, 0.98)
            image[nucleus_mask, 2] = 1.0
            
            semantic_mask[cell_mask] = 1
            instance_mask[cell_mask] = c_id
            
    return {
        "image_np": (image * 255.0).astype(np.uint8),
        "semantic_mask": semantic_mask,
        "instance_mask": instance_mask,
        "num_cells": int(instance_mask.max())
    }

def create_dataset(output_dir: str = "./data/segmentation", num_train: int = 120, num_val: int = 30, num_test: int = 30):
    images_dir = os.path.join(output_dir, "images")
    sem_masks_dir = os.path.join(output_dir, "semantic_masks")
    inst_masks_dir = os.path.join(output_dir, "instance_masks")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(sem_masks_dir, exist_ok=True)
    os.makedirs(inst_masks_dir, exist_ok=True)
    
    splits = {
        "train": (num_train, 2000),
        "val": (num_val, 6000),
        "test": (num_test, 10000)
    }
    
    for split_name, (count, seed_offset) in splits.items():
        records = []
        for i in range(count):
            seed = seed_offset + i
            sample = generate_cell_scene(img_size=64, seed=seed)
            base_name = f"{split_name}_{i:04d}"
            
            img_filename = f"{base_name}.png"
            sem_filename = f"{base_name}_mask.png"
            inst_filename = f"{base_name}_inst.png"
            
            # Save files
            Image.fromarray(sample["image_np"]).save(os.path.join(images_dir, img_filename))
            Image.fromarray(sample["semantic_mask"] * 255).save(os.path.join(sem_masks_dir, sem_filename))
            Image.fromarray(sample["instance_mask"]).save(os.path.join(inst_masks_dir, inst_filename))
            
            records.append({
                "id": base_name,
                "image_path": os.path.join("images", img_filename).replace("\\", "/"),
                "semantic_mask_path": os.path.join("semantic_masks", sem_filename).replace("\\", "/"),
                "instance_mask_path": os.path.join("instance_masks", inst_filename).replace("\\", "/"),
                "num_cells": sample["num_cells"]
            })
            
        manifest_path = os.path.join(output_dir, f"{split_name}_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
        print(f"Saved {len(records)} {split_name} samples to {manifest_path}")

    print(f"Microscopy Cell Segmentation dataset successfully created in {output_dir}")

if __name__ == "__main__":
    create_dataset()
