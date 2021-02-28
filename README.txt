This is my Final Year Project I call the smart home hub.
I am using the Raspberry Pi and the Peripherals and Display them on a webpage which can be scaled up to a whole home scenario
I am using Python for this project

This Project at the moment controls: Lights, Camera Livestream, A Fan and a DHT22 Temperature and Humidity Sensor from the webserver

I am adding Secondary Features where:
The Lights turn on via motion with a pir Sensor 
The fan will turn on and off depending on the temperature threshold
The Camera Livestream will have motion detection using Opencv's background subtraction algorithm.
The Temperature and Humidity will also be Displayed on a 16x2 LCD Display to simulate when you walk past a thermostat in your home as well as on the webserver

This Repository contains:

app.py                         -- The main app where all the features that work will be displayed 
app_edit.py                    -- The app that I edit and debug and when a feature works it then is copied into app.py
camera_pi.py                   -- The RPi Camera Initialisation Package (This may change depending on how I progress with the opencv libraries)  
camdetect.py                   -- Individual script where I am testing the camera motion detection                                               (IN PROGRESS)
motion_detection_testfile.py   -- Another script testing the camera motion detection                                                             (IN PROGRESS)
pirled_test.py                 -- Individual Script that is testing the PIR motion sensors (They work)                                           (COMPLETE)
tempfan.py                     -- Individual script that turns the fan on depending on the temperature from the DHT22 Sensor                     (COMPLETE)
static Folder                  -- containing style.css that is containing the webservers style
templates Folder               -- containing index.html 
Sep_code Folder                -- containing seperate code for each individual feature which I was testing at the prelimary stage of my project

Below is a link to my google drive where theres a video of my Project progress to date this demonstrates all the feature I have fully working up till now

https://drive.google.com/file/d/1GuMTyyuuai25_aQ4eo7Y7Rtk4A56dI9L/view?usp=sharing