import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from pathlib import Path
import pywinstyles
from database import set_user_location
import requests

class Location(ctk.CTkFrame): 
    def __init__(self, parent, app):  
        super().__init__(parent)     
        self.app = app               

        # PRE-ARRANGED GRID 6X12
        for col in range(6):
            self.grid_columnconfigure(col, weight=1)
        for row in range(12):
            self.grid_rowconfigure(row, weight=1)

        # GIF BG WITH STARS
        currentFolder = Path(__file__).parent
        self.gif_path = currentFolder / "images" / "glowing_stars.gif"

        self.gif_image = Image.open(self.gif_path)
        self.frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(self.gif_image)]
        self.frameIndex = 0

        self.bgCanvas = ctk.CTkCanvas(self, width=900, height=550, highlightthickness=0)
        self.bgCanvas.grid(row=0, column=0, rowspan=12, columnspan=6)
        self.bgCanvasImage = self.bgCanvas.create_image(0, 0, anchor="nw", image=self.frames[0])
        self.after(0, self.animate_gif)

        # MAIN TITLE
        titleLabel = ctk.CTkLabel(
            self,
            text="Your personal guide to the stars",
            font=ctk.CTkFont(family="Segoe UI", size=40, weight="bold"),
            fg_color="#000000",
            text_color="white",
            width=700, height=80
        )
        titleLabel.grid(row=2, column=1, columnspan=4, pady=20)
        pywinstyles.set_opacity(titleLabel, color="#000000")

        # BOX FOR INPUTS
        boxWidth = 500
        boxHeight = 300
        boxFrame = ctk.CTkFrame(self, width=boxWidth, height=boxHeight, corner_radius=30, fg_color="#FFFFFF")
        pywinstyles.set_opacity(boxFrame, value=0.7)

        boxFrame.grid(row=3, column=1, rowspan=5, columnspan=4)
        boxFrame.grid_propagate(False)

        for col in range(7):
            boxFrame.grid_columnconfigure(col, weight=1)
        for row in range(8):
            boxFrame.grid_rowconfigure(row, weight=1)

        self.locationLabel = ctk.CTkLabel(
            boxFrame, text="Enter your location (city)",
            font=("Segoe UI", 18), text_color="#000000"
        )
        self.locationLabel.grid(row=1, column=3)

        self.locationEntry = ctk.CTkEntry(
            boxFrame, width=300,
            fg_color="#000000", text_color="#FFFFFF",
            font=("Segoe UI", 18)
        )
        self.locationEntry.grid(row=2, column=3)

        self.orLabel = ctk.CTkLabel(
            boxFrame, text="OR",
            font=("Segoe UI", 18, "bold"), text_color="#000000"
        )
        self.orLabel.grid(row=3, column=3)

        self.markLabel = ctk.CTkLabel(
            boxFrame, text="Mark my location",
            text_color="#000000", font=("Segoe UI", 18)
        )
        self.markLabel.grid(row=4, column=3)

        # pin image for button
        self.pin_path = currentFolder / "images" / "pin.png"
        self.pinImage = ctk.CTkImage(
            light_image=Image.open(self.pin_path),
            dark_image=Image.open(self.pin_path),
            size=(15, 25)
            )
        
        self.markButton = ctk.CTkButton(
            boxFrame,
            text="",
            image= self.pinImage,
            command= self.get_city_from_ip,
            width=40,
            height=40,
            fg_color="#000000",
            hover_color="grey",
            text_color="black",
            corner_radius=30
        )
        self.markButton.grid(row=5, column=3)

        # BUTTONS
        buttonFrame = ctk.CTkFrame(self, width=250, height=100, fg_color="#000000")
        buttonFrame.grid(row=11, column=4, columnspan=2, sticky="se", padx=20, pady=20)
        buttonFrame.grid_propagate(False)
        pywinstyles.set_opacity(buttonFrame, color="#000000")

        quitButton = ctk.CTkButton(
            buttonFrame,
            text="Quit",
            font=("Segoe UI", 18),
            command=self.app.quit, 
            width=120,
            height=35,
            fg_color="white",
            hover_color="grey",
            text_color="black",
            corner_radius=30
        )
        quitButton.pack(side="right", padx=(10, 0))

        continueButton = ctk.CTkButton(
            buttonFrame,
            text="Continue",
            font=("Segoe UI", 18),
            command=self.continue_pressed,
            width=120,
            height=35,
            fg_color="white",
            hover_color="grey",
            text_color="black",
            corner_radius=30
        )
        continueButton.pack(side="right", padx=(0, 10))

    def animate_gif(self):
        self.frameIndex = (self.frameIndex + 1) % len(self.frames)
        self.bgCanvas.itemconfig(self.bgCanvasImage, image=self.frames[self.frameIndex])
        self.after(100, self.animate_gif)

    def get_city_from_ip(self):
        try:
            response = requests.get("https://ipapi.co/json/", timeout=5)
            data = response.json()
            city = data.get("city", "Unknown city")
            email = self.app.current_user_email

            if email:
                set_user_location(email, city)
                self.app.current_user_location = city 
                print(f"Location '{city}' saved for {email}")

        except Exception as e:
            print("IP location error:", e)


    def continue_pressed(self):
        email = self.app.current_user_email
        if not email:
            print("No user email found!")
            return

        location = self.locationEntry.get().strip()  

        if location: 
            set_user_location(email, location)
            self.app.current_user_location = location  
            print(f"Location '{location}' saved for {email}")
        else:
            pass

        # switch frame
        self.app.show_frame("Stars")




    
