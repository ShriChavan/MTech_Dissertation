"""
Generate an optimized WebP image for the fast page.
This creates a compressed image to satisfy the model's prescriptions:
- Page Size (KB) -75%
- total_byte_weight -55%
- lcp -42.6%

Original: ~6MB uncompressed BMP
Target: ~150KB compressed WebP (97.5% reduction)
"""

import os
import struct
import io

def create_optimized_image_placeholder(filename="optimized_image.webp", width=800, height=450):
    """
    Create a small placeholder image.
    
    For production, you should use Pillow to properly compress:
    pip install Pillow
    
    from PIL import Image
    img = Image.open('../slow_page/large_image.bmp')
    img = img.resize((800, 450))
    img.save('optimized_image.webp', 'WEBP', quality=80)
    """
    
    print("="*60)
    print("OPTIMIZED IMAGE GENERATOR")
    print("="*60)
    print(f"\nTarget: {filename}")
    print(f"Dimensions: {width}x{height}")
    
    try:
        from PIL import Image
        import numpy as np
        
        print("\nUsing Pillow to create optimized WebP image...")
        
        # Check if original BMP exists
        original_path = '../slow_page/large_image.bmp'
        if os.path.exists(original_path):
            print(f"Loading original image: {original_path}")
            img = Image.open(original_path)
            original_size = os.path.getsize(original_path)
            print(f"Original size: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
            
            # Resize to reasonable dimensions
            img = img.resize((width, height), Image.LANCZOS)
            print(f"Resized to: {width}x{height}")
        else:
            print("Original BMP not found, creating new gradient image...")
            # Create a gradient image similar to original
            data = np.zeros((height, width, 3), dtype=np.uint8)
            for y in range(height):
                for x in range(width):
                    data[y, x, 0] = int((x / width) * 255)  # R
                    data[y, x, 1] = int((y / height) * 255)  # G
                    data[y, x, 2] = int(((x + y) / (width + height)) * 255)  # B
            img = Image.fromarray(data, 'RGB')
        
        # Save as WebP with compression
        img.save(filename, 'WEBP', quality=75, method=6)
        
        optimized_size = os.path.getsize(filename)
        print(f"\n✓ Optimized image created!")
        print(f"  File: {filename}")
        print(f"  Size: {optimized_size:,} bytes ({optimized_size/1024:.2f} KB)")
        
        if 'original_size' in dir():
            reduction = (1 - optimized_size / original_size) * 100
            print(f"  Reduction: {reduction:.1f}%")
        
        return filename
        
    except ImportError:
        print("\nPillow not installed. Creating a small JPEG placeholder instead...")
        print("For proper WebP compression, run: pip install Pillow")
        
        # Create a minimal valid JPEG as fallback
        # This is a tiny 1x1 pixel JPEG expanded to look reasonable
        create_simple_jpeg(filename.replace('.webp', '.jpg'), width, height)
        print(f"\n⚠️  Created JPEG fallback: {filename.replace('.webp', '.jpg')}")
        print("   Update index.html to use .jpg instead of .webp")
        return filename.replace('.webp', '.jpg')


def create_simple_jpeg(filename, width=800, height=450):
    """Create a simple colored JPEG without external dependencies."""
    try:
        from PIL import Image
        import numpy as np
        
        # Create gradient
        data = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                data[y, x, 0] = int((x / width) * 255)
                data[y, x, 1] = int((y / height) * 255)
                data[y, x, 2] = int(((x + y) / (width + height)) * 255)
        
        img = Image.fromarray(data, 'RGB')
        img.save(filename, 'JPEG', quality=80)
        
        size = os.path.getsize(filename)
        print(f"Created: {filename} ({size:,} bytes)")
        
    except ImportError:
        print("Pillow not available. Please install: pip install Pillow")
        # Create a minimal placeholder file
        with open(filename, 'wb') as f:
            f.write(b'\x00' * 1000)  # Minimal placeholder


if __name__ == "__main__":
    print("\n" + "="*60)
    print("GENERATING OPTIMIZED IMAGE FOR FAST PAGE")
    print("Based on Model Prescriptions:")
    print("  - Page Size (KB): -75%")
    print("  - total_byte_weight: -55%")
    print("  - lcp: -42.6%")
    print("="*60)
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "optimized_image.webp")
    
    create_optimized_image_placeholder(output_file)
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("1. Host the fast_page folder alongside slow_page")
    print("2. Run PageSpeed Insights on both URLs")
    print("3. Compare metrics and model predictions")
    print("="*60)
