from PIL import Image, ImageDraw, ImageFont
import os

def create_realistic_medical_note():
    """Create a realistic medical note image (simulating a clinical encounter note)."""
    img = Image.new('RGB', (800, 1000), color='white')
    d = ImageDraw.Draw(img)
    
    # Simulate a realistic clinical encounter note (not pre-formatted as SOAP)
    text = """
    CLINICAL ENCOUNTER NOTE
    
    Date: December 1, 2024
    Patient: Sarah Johnson, 45 y/o Female
    MRN: 12345678
    
    Chief Complaint:
    Patient complaining of persistent cough and shortness of breath 
    for the past 5 days. Also reports low-grade fever.
    
    History of Present Illness:
    Ms. Johnson is a 45-year-old woman who presents with a 5-day 
    history of productive cough with yellow sputum. She reports 
    difficulty breathing, especially with exertion. Fever up to 
    100.8°F at home. Denies chest pain. No recent travel. 
    No known sick contacts.
    
    Past Medical History:
    - Hypertension (controlled)
    - Type 2 Diabetes Mellitus
    
    Medications:
    - Lisinopril 10mg daily
    - Metformin 500mg BID
    
    Physical Examination:
    Vitals: BP 138/82, HR 92, RR 22, Temp 100.4°F, SpO2 94% on RA
    General: Alert, mild respiratory distress
    Lungs: Decreased breath sounds right lower lobe, crackles present
    Heart: Regular rate and rhythm, no murmurs
    
    Diagnostic Results:
    Chest X-ray: Right lower lobe infiltrate consistent with pneumonia
    
    Clinical Impression:
    Community-acquired pneumonia, right lower lobe
    
    Treatment Plan:
    1. Start Azithromycin 500mg day 1, then 250mg daily x 4 days
    2. Increase fluid intake
    3. Rest and avoid strenuous activity
    4. Follow-up in 3-5 days or sooner if symptoms worsen
    5. Return to ED if severe shortness of breath or chest pain
    
    Dr. Michael Chen, MD
    Internal Medicine
    """
    
    # Draw text on image
    y_position = 20
    for line in text.split('\n'):
        d.text((20, y_position), line.strip(), fill=(0, 0, 0))
        y_position += 20
    
    # Save to file
    output_path = "realistic_note.png"
    img.save(output_path)
    print(f"Created {output_path}")

if __name__ == "__main__":
    create_realistic_medical_note()
