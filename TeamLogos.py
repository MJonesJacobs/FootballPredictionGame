from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path

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
        
        non_transparent = self.image.getbbox()
        self.image = self.image.crop(non_transparent)
        
        original_width,original_height = self.image.size
        new_height = 40
        scale = new_height/original_height
        new_width = original_width*scale
        new_height = round(new_height)
        new_width = round(new_width)
        
        self.image = self.image.resize((new_width,new_height))
        # Create a PhotoImage object
        self.photoimage = ImageTk.PhotoImage(self.image) #


# offsetimg = Image.open(self.img_rel_path)
#         offsetimg = offsetimg.resize((self.width,self.height), Image.ANTIALIAS)
#         self.offimg = ImageTk.PhotoImage(offsetimg)
#         self.decksectimg = ttk.Label(self.frame, image=self.offimg)
#         self.decksectimg.grid(row=self.irow, column=self.icol, columnspan=self.colspan)