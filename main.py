from tkinter import Tk, Label, Entry, Canvas, Button
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

def on_drop(event):
    global img, imgTk, original_img
    file_path = event.data.strip()

    if file_path.startswith('{') and file_path.endswith('}'):
        file_path = file_path[1:-1]

    try:
        original_img = Image.open(file_path)
        img = original_img.copy()
        imgTk = ImageTk.PhotoImage(img)
        canvas.create_image(20, 20, anchor="nw", image=imgTk)
        canvas.image = imgTk
        # status_label.config(text="Image loaded successfully.", fg="green")
    except Exception as e:
        status_label.config(text=f"Error loading image: {e}", fg="red")

def apply_watermark():
    global img, imgTk, original_img
    watermark_text = entry_watermark.get()
    img = original_img.copy()
    drawing = ImageDraw.Draw(img)

    font_path = "/Library/Fonts/Arial.ttf" if os.name == 'posix' else "C:/Windows/Fonts/Arial.ttf"

    try:
        font = ImageFont.truetype(font_path, 36)
    except IOError:
        status_label.config(text=f"Font not found", fg="red")
        font = ImageFont.load_default()

    drawing.text((10, 10), watermark_text, fill=(255, 255, 255), font=font)
    imgTk = ImageTk.PhotoImage(img)
    canvas.create_image(20, 20, anchor="nw", image=imgTk)
    canvas.image = imgTk
    save_image_with_watermark(img)

def save_image_with_watermark(image):
    downloads_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads') if os.name == 'nt' else os.path.join(os.path.expanduser('~'), 'Downloads')
    output_path = os.path.join(downloads_path, "watermarked_image.png")
    try:
        image.save(output_path)
        status_label.config(text=f"Image saved to {output_path}", fg="green")
    except Exception as e:
        status_label.config(text=f"Error saving image: {e}", fg="red")

root = TkinterDnD.Tk()
root.title("Apply Watermark to Image")
root.geometry("800x600")

canvas = Canvas(root, bg="white", width=400, height=300)
canvas.pack(fill="both", expand=True)

canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<Drop>>', on_drop)

# Upload icon
icon_path = "./drag_icon.png"
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)

icon_x = 400 
icon_y = 240
canvas.create_image(icon_x, icon_y, image=icon_photo)

# Status label
status_label = Label(root, text="")
status_label.pack()

# Watermark text entry
entry_label = Label(root, text="Enter watermark text")
entry_label.pack(pady=(10, 0))
entry_watermark = Entry(root, width=50, highlightbackground='white', highlightthickness=1)
entry_watermark.pack(pady=(10, 0))

# Apply watermark button
button_applica = Button(root, text="Apply Watermark", command=apply_watermark, width=30, height=2)
button_applica.pack(pady=(10, 10))

root.mainloop()