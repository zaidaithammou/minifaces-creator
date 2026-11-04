import os
import sys
from pathlib import Path
from PIL import Image
import numpy as np
from rembg import remove
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import gc
import time

class MiniFacesCreator:
    def __init__(self, base_dir="C:\\Users\\Zaid Ath\\Desktop\\MiniFaces_Creator"):
        self.base_dir = Path(base_dir)
        self.new_folder = self.base_dir / "New"
        self.export_folder = self.base_dir / "Export folder"
        self.examples_folder = self.base_dir / "Examples"
        
        # Resource optimization settings
        self.ai_delay_between_images = 0.5  # seconds to wait between AI processing
        self.ai_force_gc = True  # force garbage collection after each AI image
        self.ai_model_name = None  # Use default model (most efficient)
        
    def process_all_teams(self, use_ai=False):
        """Process all team folders in the New directory"""
        if not self.new_folder.exists():
            print(f"Error: New folder not found at {self.new_folder}")
            return
        
        team_folders = [f for f in self.new_folder.iterdir() if f.is_dir()]
        print(f"Found {len(team_folders)} team folders to process")
        
        if use_ai:
            print("Using AI-based background removal (slower but more accurate)")
        else:
            print("Using simple white background removal (faster)")
        
        for team_folder in team_folders:
            team_id = team_folder.name.split('_')[0] if '_' in team_folder.name else team_folder.name
            print(f"\nProcessing team: {team_folder.name} (ID: {team_id})")
            self.process_team(team_folder, team_id, use_ai)
    
    def process_team(self, team_folder, team_id, use_ai=False):
        """Process a single team folder"""
        minifaces_folder = team_folder / "minifaces"
        
        if not minifaces_folder.exists():
            print(f"  No minifaces folder found for {team_folder.name}")
            return
        
        # Create export folder for this team
        team_export_folder = self.export_folder / f"{team_id}_{team_folder.name}"
        team_export_folder.mkdir(parents=True, exist_ok=True)
        
        # Process all images in the minifaces folder
        image_files = list(minifaces_folder.glob("*.png")) + list(minifaces_folder.glob("*.jpg")) + list(minifaces_folder.glob("*.jpeg"))
        
        print(f"  Found {len(image_files)} images to process")
        
        # For AI processing, use sequential processing to minimize resource usage
        if use_ai:
            print("  Using sequential processing for AI to reduce resource usage")
            print(f"  Delay between images: {self.ai_delay_between_images}s")
            processed_count = 0
            for i, image_file in enumerate(image_files, 1):
                output_path = team_export_folder / image_file.name
                try:
                    self.remove_background(image_file, output_path, use_ai)
                    processed_count += 1
                    print(f"    Processed ({i}/{len(image_files)}): {image_file.name}")
                    
                    # Add delay between images to let system recover
                    if i < len(image_files):
                        time.sleep(self.ai_delay_between_images)
                except Exception as e:
                    print(f"    Error processing {image_file.name}: {e}")
        else:
            # Use parallel processing for fast method
            processed_count = 0
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {}
                for image_file in image_files:
                    output_path = team_export_folder / image_file.name
                    future = executor.submit(self.remove_background, image_file, output_path, use_ai)
                    futures[future] = image_file.name
                
                for future in as_completed(futures):
                    image_name = futures[future]
                    try:
                        future.result()
                        processed_count += 1
                        print(f"    Processed: {image_name}")
                    except Exception as e:
                        print(f"    Error processing {image_name}: {e}")
        
        print(f"  Successfully processed {processed_count}/{len(image_files)} images")
    
    def remove_background(self, input_path, output_path, use_ai=False):
        """Remove white background from an image"""
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Use AI-based removal if requested, otherwise use simple method
            if use_ai:
                output = self.remove_background_ai_optimized(img)
            else:
                output = self.remove_white_background_simple(img)
            
            # Save the result
            output.save(output_path, 'PNG')
            
            # Clean up memory (only for non-AI, AI handles its own cleanup)
            if not use_ai:
                del img, output
                gc.collect()
    
    def remove_white_background_simple(self, img):
        """Simple white background removal using color thresholding"""
        # Convert image to numpy array
        img_array = np.array(img)
        
        # Create a mask for white/near-white pixels
        # White pixels have high R, G, B values
        r, g, b, a = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2], img_array[:, :, 3]
        
        # Threshold for white background (adjustable)
        threshold = 250
        white_mask = (r > threshold) & (g > threshold) & (b > threshold)
        
        # Set alpha channel to 0 for white pixels
        img_array[white_mask, 3] = 0
        
        # Convert back to PIL Image
        return Image.fromarray(img_array)
    
    def remove_background_ai_optimized(self, img):
        """Optimized AI-based background removal with memory management"""
        try:
            # Process with rembg using default model
            # The rembg library handles model loading and caching
            # Using default model which is relatively efficient
            output = remove(img)
            
            # Force immediate memory cleanup
            if self.ai_force_gc:
                gc.collect()
            
            return output
        except Exception as e:
            print(f"Error in AI processing: {e}")
            # Fall back to simple method if AI fails
            return self.remove_white_background_simple(img)
    
    def process_single_image(self, input_path, output_path, use_ai=False):
        """Process a single image"""
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)
            self.remove_background(input_path, output_path, use_ai)
            print(f"Successfully processed: {input_path}")
            # Force cleanup after single image processing
            gc.collect()
            return True
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            return False

def main():
    import sys
    
    print("MiniFaces Creator - Background Removal Tool")
    print("=" * 50)
    
    creator = MiniFacesCreator()
    
    # Command line arguments
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        print("\nChoose an option:")
        print("1. Process all teams in the New folder (fast)")
        print("2. Process all teams using AI (optimized, slower but more accurate)")
        print("3. Process a specific team (can use AI)")
        print("4. Process a single image (can use AI)")
        choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        creator.process_all_teams(use_ai=False)
    elif choice == '2':
        creator.process_all_teams(use_ai=True)
    elif choice == '3':
        if len(sys.argv) > 2:
            team_name = sys.argv[2]
            use_ai = len(sys.argv) > 3 and sys.argv[3] == 'ai'
        else:
            team_name = input("Enter the team folder name (e.g., '150100_ASFAR'): ").strip()
            ai_choice = input("Use AI processing? (y/n): ").strip().lower()
            use_ai = ai_choice == 'y'
        team_folder = creator.new_folder / team_name
        if team_folder.exists():
            team_id = team_name.split('_')[0] if '_' in team_name else team_name
            creator.process_team(team_folder, team_id, use_ai)
        else:
            print(f"Team folder not found: {team_folder}")
    elif choice == '4':
        if len(sys.argv) > 3:
            input_path = sys.argv[2]
            output_path = sys.argv[3]
            use_ai = len(sys.argv) > 4 and sys.argv[4] == 'ai'
        else:
            input_path = input("Enter the full path to the input image: ").strip()
            output_path = input("Enter the full path for the output image: ").strip()
            ai_choice = input("Use AI processing? (y/n): ").strip().lower()
            use_ai = ai_choice == 'y'
        creator.process_single_image(input_path, output_path, use_ai)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()