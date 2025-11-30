from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image():
    # Create a white image
    img = Image.new('RGB', (800, 600), color='white')
    d = ImageDraw.Draw(img)
    
    # Add text (simulating a medical note)
    text = """
    Patient Name: John Doe
    Date: 2024-12-01
    
    Subjective:
    Patient presents with severe headache and sensitivity to light.
    Reports nausea but no vomiting.
    Pain level 8/10.
    
    Objective:
    BP 130/85
    Pulse 88
    Temp 98.6
    Neuro exam normal.
    
    Assessment:
    Migraine headache.
    
    Plan:
    Sumatriptan 100mg.
    Rest in dark room.
    Follow up if symptoms worsen.
    """
    
    # Use default font
    d.text((20, 20), text, fill=(0, 0, 0))
    
    # Save to file
    output_path = "sample_note.png"
    img.save(output_path)
    print(f"Created {output_path}")

if __name__ == "__main__":
    create_sample_image()
