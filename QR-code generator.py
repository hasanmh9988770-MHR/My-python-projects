import qrcode
import os  # Added to open the file automatically

# List of colors you can try: "red", "blue", "green", "purple", "black"
FILL = "darkred"
BACK = "white"

print("--- Welcome to the Pro QR Generator ---")

while True:
    input_URL = input("\nEnter the URL (or type 'quit' to stop): ")

    if input_URL.lower() == 'quit':
        print("Goodbye!")
        break

    # 1. Setup QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher protection
        box_size=15,
        border=4,
    )

    # 2. Add data
    qr.add_data(input_URL)
    qr.make(fit=True)

    # 3. Create and Save Image
    img = qr.make_image(fill_color=FILL, back_color=BACK)

    # We use a simple name, or you could use part of the URL as the filename
    filename = "latest_qr.png"
    img.save(filename)

    print(f"✅ Success! Saved as {filename}")

    # 4. Auto-open on Mac
    os.system(f"open {filename}")