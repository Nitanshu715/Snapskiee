import base64

with open('Snapskiee_Pitch_Deck.pdf', 'rb') as f:
    encoded = base64.b64encode(f.read()).decode('utf-8')

with open('assets/pdf_b64.py', 'w') as out:
    out.write('PDF_DATA = """' + encoded + '"""\n')

print(f"Successfully generated assets/pdf_b64.py with {len(encoded)} bytes")
