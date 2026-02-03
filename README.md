# Stargazing – Personal Night Sky Guide

## General Information
Stargazing is a Python application that allows users to discover night sky events visible from their city. Users can enter their location manually or allow the program to detect it automatically via IP. The app calculates sunrise, sunset, and moon phase, and shows visible planets, making it ideal for astronomy enthusiasts or anyone interested in observing the night sky. The program also provides a direct link to [Stellarium Web](https://stellarium-web.org/) for interactive sky exploration.

---

## Author 
- Author: ch4rgeb0lt 
- Contact: alesjaa.agafonova@gmail.com

---

## Known Issues
- Entering an *incorrect or unknown city* may result in empty or default output.  
- Cannot continue if the *email has already been used* in the database.

---

## Build Instructions
1) Clone the repository to your local machine
2) Navigate to the project folder
3) Install dependencies using pip:
   pip install customtkinter, pywinstyles, astral, geopy
5) Ensure the following files and folders are present:
    main.py, user.py, location.py, stargazing.py, database.py
    images/ folder with GIFs and icons
    database/ folder (the program will create users.json if it does not exist)

## Run Instructions
1) Launch the program by running python main.py
2) Enter your username and email, click Continue
3) Either type your city manually / click the pin icon to detect your location automatically and click Continue
4) View night sky events and click Quit at any screen to close the application
