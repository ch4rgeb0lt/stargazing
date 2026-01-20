import customtkinter as ctk
from user import LogIn
from location import Location
from stargazing import Stars

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Stargazing")
        self.geometry("900x550")
        self.resizable(False, False)

        # ALL SCREENS
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for FrameClass in (LogIn, Location, Stars):
            frame = FrameClass(self.container, self)
            self.frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LogIn")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        if frame_name == "Stars":
            frame.show_night_sky_events()  # update events dynamically



def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
