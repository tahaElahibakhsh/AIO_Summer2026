"""
Synthetic Single-Object Detection Dataset Generator
Generates synthetic geometric objects (Circle, Rectangle, Triangle) on textured backgrounds
and saves RGB images alongside normalized bounding box annotations to local disk.
"""

import os
import json
import random
import numpy as np
from PIL import Image

def generate_single_object_scene(img_size: int = 64, seed: int = None) -> dict:
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
        
    image = np.full((img_size, img_size, 3), 0.92, dtype=np.float32)
    noise = np.random.uniform(-0.03, 0.03, size=(img_size, img_size, 3)).astype(np.float32)
    image = np.clip(image + noise, 0.0, 1.0)
    
    shape_type = random.choice([0, 1, 2])  # 0: Circle, 1: Rectangle, 2: Triangle
    size = random.randint(14, 22)
    cx = random.randint(size, img_size - size)
    cy = random.randint(size, img_size - size)
    
    yy, xx = np.mgrid[:img_size, :img_size]
    class_colors = {
        0: [0.88, 0.22, 0.21],  # Red Circle
        1: [0.18, 0.48, 0.86],  # Blue Rectangle
        2: [0.20, 0.72, 0.32],  # Green Triangle
    }
    
    if shape_type == 0:  # Circle
        rad = size // 2
        mask = ((xx - cx) ** 2 + (yy - cy) ** 2) <= (rad ** 2)
        x1, y1, x2, y2 = cx - rad, cy - rad, cx + rad, cy + rad
    elif shape_type == 1:  # Rectangle
        hw = random.randint(size // 3, size // 2)
        hh = random.randint(size // 3, size // 2)
        mask = (xx >= cx - hw) & (xx <= cx + hw) & (yy >= cy - hh) & (yy <= cy + hh)
        x1, y1, x2, y2 = cx - hw, cy - hh, cx + hw, cy + hh
    else:  # Triangle
        hb = size // 2
        top_y, bot_y = cy - size // 2, cy + size // 2
        in_y = (yy >= top_y) & (yy <= bot_y)
        prog = np.clip((yy - top_y) / max(1, (bot_y - top_y)), 0.0, 1.0)
        mask = in_y & (xx >= cx - prog * hb) & (xx <= cx + prog * hb)
        x1, y1, x2, y2 = cx - hb, top_y, cx + hb, bot_y
        
    image[mask] = np.array(class_colors[shape_type], dtype=np.float32)
    norm_box = [float(x1 / img_size), float(y1 / img_size), float(x2 / img_size), float(y2 / img_size)]
    
    return {
        "image_np": (image * 255.0).astype(np.uint8),
        "box": norm_box,
        "label": shape_type,
        "shape_name": {0: "Circle", 1: "Rectangle", 2: "Triangle"}[shape_type]
    }

def create_dataset(output_dir: str = "./data/detection", num_train: int = 300, num_val: int = 60, num_test: int = 60):
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    splits = {
        "train": (num_train, 1000),
        "val": (num_val, 5000),
        "test": (num_test, 9000)
    }
    
    for split_name, (count, seed_offset) in splits.items():
        records = []
        for i in range(count):
            seed = seed_offset + i
            sample = generate_single_object_scene(img_size=64, seed=seed)
            img_filename = f"{split_name}_{i:04d}.png"
            img_path = os.path.join(images_dir, img_filename)
            
            # Save image
            img_pil = Image.fromarray(sample["image_np"])
            img_pil.save(img_path)
            
            rel_img_path = os.path.join("images", img_filename).replace("\\", "/")
            records.append({
                "id": f"{split_name}_{i:04d}",
                "image_path": rel_img_path,
                "box": sample["box"],
                "label": sample["label"],
                "shape_name": sample["shape_name"]
            })
        
        manifest_path = os.path.join(output_dir, f"{split_name}_annotations.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
        print(f"Saved {len(records)} {split_name} samples to {manifest_path}")

    print(f"Single-Object Detection dataset successfully created in {output_dir}")

if __name__ == "__main__":
    create_dataset()
