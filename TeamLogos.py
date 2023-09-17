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
    "Wolves":r"TeamLogos\Wolves.png"
}

class TeamImage():
    def __init__(self,team:str) -> None:
        # Load the PNG image
        self.image = Image.open(Path(LOGOS[team]))
        
        # original_width,original_height = self.image.size
        # new_height = 40
        # scale = new_height/original_height
        # new_width = original_width*scale
        # new_height = round(new_height)
        # new_width = round(new_width)
        
        # self.image = self.image.resize((new_width,new_height))
        # Create a PhotoImage object
        self.photoimage = ImageTk.PhotoImage(self.image) 


# for key,im_path in LOGOS.items():
#     image = Image.open(Path(im_path))
#     original_width,original_height = image.size
#     new_height = 40
#     scale = new_height/original_height
#     new_width = original_width*scale
#     new_height = round(new_height)
#     new_width = round(new_width)
#     image = image.resize((new_width,new_height))
#     image.save(Path(im_path))
    