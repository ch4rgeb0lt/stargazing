import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from pathlib import Path
import pywinstyles
import webbrowser
from astral import LocationInfo
from astral.sun import sun
from astral.moon import phase as moon_phase
from datetime import datetime
from geopy.geocoders import Nominatim


class Stars(ctk.CTkFrame):
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
        self.titleLabel = ctk.CTkLabel(
            self,
            text="Night sky events in your city",
            font=ctk.CTkFont(family="Segoe UI", size=40, weight="bold"),
            fg_color="#000000",
            text_color="white",
            width=700,
            height=80
        )
        self.titleLabel.grid(row=2, column=1, columnspan=4, pady=20)
        pywinstyles.set_opacity(self.titleLabel, color="#000000")

        # BOX FOR EVENTS
        boxWidth = 500
        boxHeight = 300
        self.boxFrame = ctk.CTkFrame(self, width=boxWidth, height=boxHeight, corner_radius=30, fg_color="#FFFFFF")
        pywinstyles.set_opacity(self.boxFrame, value=0.7)

        self.boxFrame.grid(row=3, column=1, rowspan=5, columnspan=4)
        self.boxFrame.grid_propagate(False)

        for col in range(7):
            self.boxFrame.grid_columnconfigure(col, weight=1)
        for row in range(8):
            self.boxFrame.grid_rowconfigure(row, weight=1)

        # BUTTON TO OPEN INTERACTIVE MAP
        self.go_button = ctk.CTkButton(
            self.boxFrame,
            text="Go to Stellarium",
            font=("Segoe UI", 18),
            fg_color="#000000",
            hover_color="grey",
            text_color="white",
            corner_radius=20,
            command=self.open_stellarium
        )
        self.go_button.grid(row=7, column=3, pady=10)

        # QUIT BUTTON
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

    def animate_gif(self):
        self.frameIndex = (self.frameIndex + 1) % len(self.frames)
        self.bgCanvas.itemconfig(self.bgCanvasImage, image=self.frames[self.frameIndex])
        self.after(100, self.animate_gif)

    def show_night_sky_events(self):
        for widget in self.boxFrame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        # GET LOCATION
        location_name = getattr(self.app, "current_user_location", None)
        if not location_name:
            location_name = "New York"  # fallback if no location set

        # GET EVENTS
        events = self.get_night_sky_events(location_name)

        # DISPLAY EVENTS
        for i, event in enumerate(events):
            label = ctk.CTkLabel(
                self.boxFrame,
                text=event,
                font=("Segoe UI", 16),
                text_color="black",
                wraplength=400,
                justify="center"
            )
            label.grid(row=i + 1, column=3, pady=2)

        self.go_button = ctk.CTkButton(
            self.boxFrame,
            text="Go to Stellarium",
            font=("Segoe UI", 18),
            fg_color="#000000",
            hover_color="grey",
            text_color="white",
            corner_radius=20,
            command=self.open_stellarium
        )
        self.go_button.grid(row=7, column=3, pady=10)

    def get_night_sky_events(self, location_name):
        try:
            geolocator = Nominatim(user_agent="stargazing_app")
            location = geolocator.geocode(location_name)
            if not location:
                location = geolocator.geocode("New York")  # fallback

            lat, lon = location.latitude, location.longitude
            city = location_name

            loc_info = LocationInfo(city, "UTC", "", lat, lon)
            today = datetime.now()
            s = sun(loc_info.observer, date=today)
            moon = moon_phase(today)

            events = [
                f"Location: {city}",
                f"Sunrise: {s['sunrise'].strftime('%H:%M')}",
                f"Sunset: {s['sunset'].strftime('%H:%M')}",
                f"Moon phase: {moon:.0f}",
                "Visible planets tonight: Mars, Venus, Jupiter"
            ]
            return events

        except Exception as e:
            print("Error generating events:", e)
            return ["Night sky events unavailable"]

    def open_stellarium(self):
        url = "https://stellarium-web.org/"
        webbrowser.open(url)
