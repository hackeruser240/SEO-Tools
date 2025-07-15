import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os

def password_protect_pdf(file, password):
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)
    output_buffer = BytesIO()
    writer.write(output_buffer)
    return output_buffer.getvalue()

if __name__ == "__main__":
    # Define the source PDF file path
    src = r'C:\Users\HP\Downloads\Investor Guide.pdf'
    # Define the password for encryption
    password = '12345'
    # Define the output path for the encrypted PDF
    output_dir = r'C:\Users\HP\Downloads'
    output_filename = 'Investor Guide_protected.pdf'
    output_path = os.path.join(output_dir, output_filename)

    try:
        # Open the source PDF file in binary read mode
        with open(src, 'rb') as file:
            # Call the password_protect_pdf function with the file object and password
            encrypted_pdf_content = password_protect_pdf(file, password)

        # Write the returned encrypted content to a new PDF file
        with open(output_path, 'wb') as output_file:
            output_file.write(encrypted_pdf_content)

        print(f"Successfully encrypted '{src}' and saved it to '{output_path}'")
        print(f"You can now try opening '{output_filename}' with the password '{password}'.")

    except FileNotFoundError:
        print(f"Error: The file '{src}' was not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

