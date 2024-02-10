import socketio
import time
import math
import base64
import numpy as np
import cv2


class Wehead:
    """Handles communication with a Wehead via WebSockets."""
    BASE_URL = "https://sio-experiment-2-ule2kkd6ca-wl.a.run.app"

    def __init__(self, token: str):
        """Initializes the connection to Wehead using a WebSocket.
        
        Args:
            token (str): Authentication token for Wehead.
        """
        self._sio = socketio.Client()
        self._sio.connect(
            self.BASE_URL,
            auth={"token": token, "role": "user"},
            socketio_path="msg",
            wait_timeout=100,
            retry=True,
        )
        while not self._sio.connected:
            time.sleep(0.1)

    def move(self, pitch: float, yaw: float):
        """Instructs the Wehead to adjust its position.
        
        Args:
            pitch (float): The pitch angle to set.
            yaw (float): The yaw angle to set.
        """
        self._safe_emit(
            "move",
            {
                "mode": "pose_absolute",
                "pitch": pitch,
                "yaw": yaw,
            },
        )

    def say(self, text: str, voice: str = "shimmer"):
        """Commands the Wehead to speak a given text in a specified voice.
        
        Args:
            text (str): The text for Wehead to say.
            voice (str, optional): The voice Wehead will use. Available
                voices: alloy, echo, fable, onyx, nova, and shimmer.
                Defaults to "shimmer".
        """
        self._safe_emit("tts", {"text": text, "voice": voice})

    def on_video(self, func):
        """Defines a callback for handling video data from the Wehead.
        
        Args:
            func (Callable): The function to process the video data.
        """
        def wrap(data):
            img_data = base64.b64decode(data["img"])
            nparr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            func(img)

        self._sio.on("video")(wrap)
        return func

    def on_phrase(self, func):
        """Sets up a callback for receiving spoken phrases from Wehead.
        
        Args:
            func (Callable): The function to process the phrases.
        """
        def wrap(data):
            func(data["text"])

        self._sio.on("stt")(wrap)
        return func

    def _safe_emit(self, event: str, data: dict):
        """Safely emits an event to the Wehead with provided data.
        
        Args:
            event (str): The name of the event.
            data (dict): The data to be sent with the event.
        """
        try:
            self._sio.emit(event, data)
        except Exception as e:
            print(e)
