# Wehead SDK Readme
Welcome to the Wehead SDK! This SDK provides a straightforward and powerful way to control and interact with your Wehead device through WebSockets. With this toolkit, you can command the Wehead to move, speak, process video, and recognize spoken phrases, all programmatically.

## Features
 - __Move:__ Command the Wehead to adjust its camera angle with precision.
 - __Speak:__ Make the Wehead articulate text in a variety of voices.
 - __Video Processing:__ Receive and process video frames from the Wehead in real-time.
 - __Speech Recognition Callbacks:__ Respond to specific phrases that the Wehead detects.

## Installation
First, you'll need a valid token. __As part of a hackathon, you can use any string as a token.__

Before diving into the code, install `wehead_hack_sdk`:

```
pip install git+https://github.com/zerodistanceinc/wehead_hack_sdk.git
```

### Debugging with the 3D Simulation
While developing with the Wehead SDK, you might not always have physical access to a Wehead device. Don't worry; we've got you covered with a lifelike 3D simulation environment. This simulation allows you to test and debug your code as if you were interacting with a real Wehead, providing a seamless development experience.

Accessing the 3D Simulation
The 3D simulation can be accessed via any modern web browser. Simply navigate to the following URL, replacing YOUR_TOKEN_HERE with your actual authentication token:

```
https://wehead-landing--yuy2-wp1w4g77.web.app/wehead_call/?dev=1&loc=full&main=1&token=YOUR_TOKEN_HERE
```

Make sure to use the correct token for authentication. Don't forget to grant access to the camera and microphone!


## Getting Started
### Initialization

```Python
from wehead_hack_sdk import Wehead

token = "YOUR_TOKEN_HERE"
wehead = Wehead(token)
```

### Moving the Wehead
To move the Wehead to a specific pitch and yaw, simply call:

```Python
wehead.move(pitch=0.3, yaw=0.3)
```

### Speaking
To make the Wehead speak, use:

```Python
wehead.say(text="Hello, world!", voice="shimmer")
```

### Processing Video
Define a callback function that processes video frames. Here's an example that simply displays the video frames using OpenCV:

```Python
@wehead.on_video
def process_frame(img):
    cv2.imshow('Wehead Video', img)
    cv2.waitKey(1)
```


### Responding to Spoken Phrases
Similarly, define a callback to handle spoken phrases recognized by the Wehead:

```Python
@wehead.on_phrase
def handle_phrase(text):
    print(f"Wehead heard: {text}")
```

## Example
Below is a simple example that integrates everything mentioned above:

```Python
import cv2
import time

from wehead_hack_sdk import Wehead

token = "YOUR_TOKEN_HERE"
wehead = Wehead(token)

wehead.move(pitch=0, yaw=0)
wehead.say("Initializing Wehead SDK Example")

@wehead.on_video
def process_frame(img):
    cv2.waitKey(30)
    cv2.imshow('Wehead Video', img)
    cv2.waitKey(30)

@wehead.on_phrase
def handle_phrase(text):
    if text == "Exit.":
        wehead.say("Goodbye")
        time.sleep(1)
        exit()

while True:
    pass  # Keep the script running
```

## Conclusion
This SDK offers a flexible and easy way to interact with your Wehead. Whether you're creating interactive installations, developing a surveillance system, or simply having fun, the Wehead SDK empowers you to bring your creative vision to life. Enjoy exploring the capabilities of your Wehead!
