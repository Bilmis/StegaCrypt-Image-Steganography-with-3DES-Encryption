
from pathlib import Path
import tkinter as tk
from Crypto.Cipher import DES3
import base64
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
import subprocess
from PIL import Image

window = Tk()
window.title("StegaCrypt")
window.geometry("862x519")
window.configure(bg = "#093545")



canvas = Canvas(
    window,
    bg = "#093545",
    height = 519,
    width = 862,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame5")
global selected
def open_login_interface():
    window.withdraw()  # Hide the current interface
    # ... Save any necessary data ...
    subprocess.Popen(["python", "gui.py"])
    window.destroy()  # Close the current interface

def open_encoding_interface():
    window.withdraw()  # Hide the current interface
    # ... Save any necessary data ...
    subprocess.Popen(["python", "gui4.py"])
    window.destroy()  # Close the current interface

def open_home_interface():
    window.withdraw()  # Hide the current interface
    # ... Save any necessary data ...
    subprocess.Popen(["python", "gui3.py"])
    window.destroy()  # Close the current interface

def open_decoding_interface():
    window.withdraw()  # Hide the current interface
    # ... Save any necessary data ...
    subprocess.Popen(["python", "gui5.py"])
    window.destroy()  # Close the current interface

def handle_enter(event):
    entry_1.insert(tk.END, "\n")  # Insert a newline character when Enter is pressed

def open_file_dialog():
    global selected
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        selected = Image.open(file_path)
        entry_1.delete(0, tk.END)  # Clear the current text in the Entry widget
        entry_1.insert(0, file_path)  # Insert the selected file path into the Entry widget

######################################
def open_key_file_dialog():
    key_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if key_file_path:
        try:
            with open(key_file_path, 'rb') as key_file:  # Read the key in binary mode
                key = key_file.read().strip()  # Read the 24-byte key
                if len(key) != 24:  # Ensure the key is valid
                    tk.messagebox.showerror("Error", "Invalid key file. Please select a valid Triple DES key.")
                    return
                
                entry_2.delete(0, tk.END)  # Clear the entry field
                entry_2.insert(0, "*****")  # Mask the key for privacy
                entry_2.actual_key = key  # Store the real key in a hidden attribute
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load the key: {str(e)}")

####################################

#decryption
def unpad(text):
    return text[:-ord(text[-1])]

# Triple DES Decryption
def decrypt(encrypted_message, key):
    encrypted_message = base64.b64decode(encrypted_message.encode('utf-8'))
    iv = encrypted_message[:8]  # Extract the IV from the beginning of the message
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    decrypted_message = cipher.decrypt(encrypted_message[8:]).decode('utf-8')
    return unpad(decrypted_message)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)




canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    438.0,
    474.0,
    image=image_image_1
)

canvas.create_text(
    296.0,
    28.0,
    anchor="nw",
    text="Decoding with StegaCrypt!",
    fill="#FFFFFF",
    font=("LexendDeca Regular", 24 * -1)
)

canvas.create_text(
    339.0,
    74.0,
    anchor="nw",
    text="1. Choose the Encrypted image",
    fill="#FFFFFF",
    font=("Poppins Regular", 12 * -1)
)

canvas.create_text(
    361.0,
    92.0,
    anchor="nw",
    text="2. Decode the message",
    fill="#FFFFFF",
    font=("Poppins Regular", 12 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    431.0,
    166.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#224957",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=308.0,
    y=148.0,
    width=246.0,
    height=35.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_2 = canvas.create_image(
    431.0,
    225.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#224957",
    fg="#FFFFFF",
    highlightthickness=0
)

from steganography_functions import decode_lsb

global decoded_message
decoded_message=''
def decode_photo():
    if selected is not None:
        image_path = entry_1.get()
        key = getattr(entry_2, "actual_key", "").strip()
        if not key:  # If the key is still empty, show an error and return
            tk.messagebox.showerror("Error", "Please select an encryption key file before decoding.")
            return
        # Perform decoding using the selected photo
        decoded_message = decode_lsb(selected)
        final = decrypt(decoded_message, key)  # Decrypt the message using Triple DES
        canvas.itemconfig(Final_text, text=final)

# Create the error text widget
Final_text = canvas.create_text(
    380.0,
    330.0,
    anchor="nw",
    fill="#FFFFFF",
    font=("Poppins Regular", 12 * -1)
)
'''entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_3 = canvas.create_image(
    431.0,
    350.5,
    image=entry_image_3
)'''

canvas.create_text(
    325.0,
    310.0,
    anchor="nw",
    text="Here you find your hidden message :",
    fill="#FFFFFF",
    font=("Poppins Regular", 12 * -1)
)

#print("The hidden message is : ",final)
entry_2.place(
    x=308.0,
    y=210.0,
    width=246.0,
    height=35.0
)

"""image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    541.0,
    167.0,
    image=image_image_2
)"""

button_image_locate = PhotoImage(
    file=relative_to_assets("image_2.png"))
button_locate = Button(
    image=button_image_locate,
    borderwidth=0,
    highlightthickness=0,
    command=open_file_dialog,
)

button_locate.place(
    x=541.0,
    y=158.0,
)

canvas.create_text(
    404.0,
    126.0,
    anchor="nw",
    text="Locate ...",
    fill="#FFFFFF",
    font=("Poppins Regular", 12 * -1)
)
####################################3##########################################
canvas.create_text(
    355.0,
    188.0,
    anchor="nw",
    text="Enter the Encryption code :",
    fill="#FFFFFF",
    font=("Poppins Regular", 12 * -1)
)
# Button to locate and load the encryption key file
button_image_key = PhotoImage(file=relative_to_assets("image_2.png"))
button_key = Button(
    image=button_image_key,
    borderwidth=0,
    highlightthickness=0,
    command=open_key_file_dialog
)
button_key.place(x=541.0, y=210.0)  # Adjust placement as needed
#########################################################################

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_home_interface,
    relief="flat"
)
button_1.place(
    x=739.0,
    y=30.0,
    width=91.0,
    height=34.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=decode_photo,
    relief="flat"
)
button_2.place(
    x=358.0,
    y=255.0,
    width=71.0,
    height=23.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=open_decoding_interface,
    relief="flat"
)
button_3.place(
    x=434.0,
    y=255.0,
    width=71.0,
    height=23.0
)
window.resizable(False, False)
window.mainloop()
