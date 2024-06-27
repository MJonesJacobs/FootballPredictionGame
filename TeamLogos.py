from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import numpy as np

LOGOS = {
    "Arsenal":r"TeamLogos\Arsenal.png",
    "Aston Villa":r"TeamLogos\AstonVilla.png",
    "Bournemouth":r"TeamLogos\Bournemouth.png",
    "Brentford":r"TeamLogos\Brentford.png",
    "Brighton":r"TeamLogos\Brighton.png",
    "Burnley":r"TeamLogos\Burnley.png",
    "Chelsea":r"TeamLogos\Chelsea.png",
    "Crystal Palace":r"TeamLogos\CrystalPalace.png",
    "Everton":r"TeamLogos\Everton.png",
    "Fulham":r"TeamLogos\Fulham.png",
    "Liverpool":r"TeamLogos\Liverpool.png",
    "Luton":r"TeamLogos\Luton.png",
    "Man City":r"TeamLogos\ManCity.png",
    "Man Utd":r"TeamLogos\ManUtd.png",
    "Newcastle":r"TeamLogos\Newcastle.png",
    "Nott'm Forest":r"TeamLogos\NottinghamForrest.png",
    "Sheffield Utd":r"TeamLogos\SheffieldUtd.png",
    "Spurs":r"TeamLogos\Spurs.png",
    "West Ham":r"TeamLogos\WestHam.png",
    "Wolves":r"TeamLogos\Wolves.png",
    "Leicester City":r"Teamlogos\Leicester.png",
    "Ipswich Town":r"Teamlogos\Ipswich.png",
    "Southampton":r"Teamlogos\Southampton.png"
}

class TeamImage():
    def __init__(self,team:str) -> None:
        # Load the PNG image
        self.image = Image.open(Path(LOGOS[team]))
        
        self.photoimage = ImageTk.PhotoImage(self.image) 
    
    def resize_img(self,scale:float):
        self.image = self.image.resize([int(self.image.width*scale),int(self.image.height*scale)])
        self.photoimage = ImageTk.PhotoImage(self.image) 

class PlaceholderImage():
    def __init__(self) -> None:
        self.image = Image.open(Path("placeholder.png"))
        self.photoimage = ImageTk.PhotoImage(self.image) 



def process_image(image_path):
    "This method is use to resize the team logos used in the application - This should be used only when adding new images into the app at the start of each season"
    # Open the image file
    img = Image.open(image_path).convert("RGBA")

    # Remove blank space around the image
    bbox = img.getbbox()
    img = img.crop(bbox)

    # Scale to 40 pixel height
    width, height = img.size
    new_height = 40
    new_width  = int(new_height * width / height)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Make the image 50 pixel wide by adding blank space
    final_width = 50
    result = Image.new("RGBA", (final_width, new_height), (0, 0, 0, 0))  # Create a new image with transparent background
    result.paste(img, ((final_width - new_width) // 2, 0))  # Paste the scaled image onto the new image

    return result

def gen_placeholder():
    # Create a new RGBA image with a transparent background
    img = Image.new('RGBA', (1, 40), (255, 255, 255, 0))

    # Save the image as a PNG file
    img.save('placeholder.png', 'PNG')


gen_placeholder()