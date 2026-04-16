"""
Generate a large uncompressed BMP image for performance testing.
This creates a ~3-5MB uncompressed BMP file to increase transfer size.

Usage:
    python generate_large_image.py

Output:
    large_image.bmp (~3-5MB uncompressed bitmap)
"""

import os
import struct
import random

def create_large_bmp(filename="large_image.bmp", width=1920, height=1080):
    """
    Create a large uncompressed BMP image.
    
    BMP Format (uncompressed) = width * height * 3 bytes (RGB) + headers
    1920x1080 RGB = ~6.2MB (perfect for testing high transfer size)
    
    Parameters:
    -----------
    filename : str
        Output filename
    width : int
        Image width in pixels
    height : int
        Image height in pixels
    """
    
    # BMP file header (14 bytes)
    # BMP info header (40 bytes)
    # Total header size: 54 bytes
    
    row_size = (width * 3 + 3) & ~3  # Row must be multiple of 4 bytes
    pixel_data_size = row_size * height
    file_size = 54 + pixel_data_size
    
    print(f"Creating large uncompressed BMP image...")
    print(f"  Dimensions: {width} x {height} pixels")
    print(f"  Row size: {row_size} bytes (padded to 4-byte boundary)")
    print(f"  Pixel data size: {pixel_data_size:,} bytes")
    print(f"  Total file size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
    
    with open(filename, 'wb') as f:
        # === BMP File Header (14 bytes) ===
        f.write(b'BM')                              # Signature
        f.write(struct.pack('<I', file_size))       # File size
        f.write(struct.pack('<HH', 0, 0))           # Reserved
        f.write(struct.pack('<I', 54))              # Pixel data offset
        
        # === BMP Info Header (40 bytes) ===
        f.write(struct.pack('<I', 40))              # Header size
        f.write(struct.pack('<i', width))           # Width
        f.write(struct.pack('<i', height))          # Height (positive = bottom-up)
        f.write(struct.pack('<HH', 1, 24))          # Planes, Bits per pixel (24-bit RGB)
        f.write(struct.pack('<I', 0))               # Compression (0 = uncompressed)
        f.write(struct.pack('<I', pixel_data_size)) # Image size
        f.write(struct.pack('<i', 2835))            # X pixels per meter (72 DPI)
        f.write(struct.pack('<i', 2835))            # Y pixels per meter (72 DPI)
        f.write(struct.pack('<I', 0))               # Colors used
        f.write(struct.pack('<I', 0))               # Important colors
        
        # === Pixel Data (BGR format, bottom-up) ===
        print("  Generating pixel data (colorful gradient pattern)...")
        
        padding = row_size - (width * 3)
        padding_bytes = b'\x00' * padding
        
        for y in range(height):
            row_data = bytearray()
            for x in range(width):
                # Create a colorful gradient pattern
                # This ensures the image is visually identifiable
                r = int((x / width) * 255)
                g = int((y / height) * 255)
                b = int(((x + y) / (width + height)) * 255)
                
                # Add some random noise to prevent compression effectiveness
                r = min(255, max(0, r + random.randint(-20, 20)))
                g = min(255, max(0, g + random.randint(-20, 20)))
                b = min(255, max(0, b + random.randint(-20, 20)))
                
                # BMP uses BGR order
                row_data.extend([b, g, r])
            
            row_data.extend(padding_bytes)
            f.write(row_data)
            
            # Progress indicator
            if (y + 1) % 200 == 0:
                print(f"    Progress: {(y + 1) / height * 100:.1f}%")
    
    actual_size = os.path.getsize(filename)
    print(f"\n✓ Image created successfully!")
    print(f"  File: {filename}")
    print(f"  Actual size: {actual_size:,} bytes ({actual_size / (1024*1024):.2f} MB)")
    
    return filename


def create_even_larger_bmp(filename="large_image.bmp", width=2560, height=1440):
    """
    Create an even larger BMP image (~11MB) for more extreme testing.
    2560x1440 (2K resolution) = ~11MB uncompressed
    """
    return create_large_bmp(filename, width, height)


if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("LARGE UNCOMPRESSED IMAGE GENERATOR")
    print("For Web Performance Testing Research")
    print("="*60)
    
    # Default: Full HD (1920x1080) ~6MB
    # Can use 2560x1440 for ~11MB if needed
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "large_image.bmp")
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--larger':
        print("\nGenerating LARGER image (2560x1440, ~11MB)...")
        create_even_larger_bmp(output_file, 2560, 1440)
    else:
        print("\nGenerating standard large image (1920x1080, ~6MB)...")
        print("Use --larger flag for ~11MB image")
        create_large_bmp(output_file, 1920, 1080)
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("1. Host this folder on a web server (GitHub Pages, Netlify, etc.)")
    print("2. Run PageSpeed Insights on the hosted URL")
    print("3. Collect metrics for Phase 2 validation")
    print("="*60)
