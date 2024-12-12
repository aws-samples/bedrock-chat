import os 
import sys
from PIL import Image

SizeList = [16, 32, 48, 64, 72, 96, 128, 144, 152, 192, 384, 512] 

def resize_image(input_file, output_dir):
    print(f'resizing {input_file} to {output_dir}')
    basename = os.path.splitext(os.path.basename(input_file))[0]
    try:
        # Open the input image
        img = Image.open(input_file)

        for size in SizeList:
            img_resized = img.resize((size, size))
            output_file = f"{output_dir}/{basename}_{size}.png" 
            # Save the resized image as PNG
            img_resized.save(output_file)
            print(f"Image successfully resized and saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scale.py <input_file> <output_dir>")
        print("  scale.py in.jpeg out  --> will generate out_16.png, out_32.png ... out_512.png" )
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir= sys.argv[2]
    
    resize_image(input_file, output_dir)
        

