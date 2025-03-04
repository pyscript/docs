# PyScript and Media Devices

For web applications to interact with cameras, microphones, and other media
devices, there needs to be a way to access these hardware components through the
browser. PyScript provides a media API that enables your Python code to interact
with media devices directly from the browser environment.

This section explains how PyScript interacts with media devices and how you can
use these capabilities in your applications.

## Media Device Access

PyScript interacts with media devices through the browser's [MediaDevices
API](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices). This API
provides access to connected media input devices like cameras and microphones,
as well as output devices like speakers.

When using PyScript's media API, it's important to understand:

1. Media access requires **explicit user permission**. The browser will show a
   permission dialog when your code attempts to access cameras or microphones.
2. Media access is only available in **secure contexts** (HTTPS or localhost).
3. All media interactions happen within the **browser's sandbox**, following the
   browser's security policies.

## The `pyscript.media` API

PyScript provides a Pythonic interface to media devices through the
`pyscript.media` namespace. This API includes two main components:

1. The `Device` class - represents a media device and provides methods to
   interact with it
2. The `list_devices()` function - discovers available media devices

### Listing Available Devices

To discover what media devices are available, use the `list_devices()` function:

```python
from pyscript.media import list_devices

async def show_available_devices():
    devices = await list_devices()
    for device in devices:
        print(f"Device: {device.label}, Type: {device.kind}, ID: {device.id}")

# List all available devices
show_available_devices()
```

This function returns a list of `Device` objects, each representing a media
input or output device. Note that the browser will typically request permission
before providing this information.

### Working with the Camera

The most common use case is accessing the camera to display a video stream:

```python
from pyscript import when
from pyscript.media import Device
from pyscript.web import page

async def start_camera():
    # Get a video stream (defaults to video only, no audio)
    stream = await Device.load(video=True)
    
    # Connect the stream to a video element in your HTML
    video_element = page["#camera"][0]._dom_element
    video_element.srcObject = stream
    
    return stream

# Start the camera
camera_stream = start_camera()
```

The `Device.load()` method is a convenient way to access media devices without
first listing all available devices. You can specify options to control which
camera is used:

```python
# Prefer the environment-facing camera (often the back camera on mobile)
stream = await Device.load(video={"facingMode": "environment"})

# Prefer the user-facing camera (often the front camera on mobile)
stream = await Device.load(video={"facingMode": "user"})

# Request specific resolution
stream = await Device.load(video={
    "width": {"ideal": 1280},
    "height": {"ideal": 720}
})
```

### Capturing Images from the Camera

To capture a still image from the video stream:

```python
def capture_image(video_element):
    # Get the video dimensions
    width = video_element.videoWidth
    height = video_element.videoHeight
    
    # Create a canvas to capture the frame
    canvas = document.createElement("canvas")
    canvas.width = width
    canvas.height = height
    
    # Draw the current video frame to the canvas
    ctx = canvas.getContext("2d")
    ctx.drawImage(video_element, 0, 0, width, height)
    
    # Get the image as a data URL
    image_data = canvas.toDataURL("image/png")
    
    return image_data
```

For applications that need to process images with libraries like OpenCV, you
need to convert the image data to a format these libraries can work with:

```python
import numpy as np
import cv2

def process_frame_with_opencv(video_element):
    # Get video dimensions
    width = video_element.videoWidth
    height = video_element.videoHeight
    
    # Create a canvas and capture the frame
    canvas = document.createElement("canvas")
    canvas.width = width
    canvas.height = height
    ctx = canvas.getContext("2d")
    ctx.drawImage(video_element, 0, 0, width, height)
    
    # Get the raw pixel data
    image_data = ctx.getImageData(0, 0, width, height).data
    
    # Convert to numpy array for OpenCV
    frame = np.asarray(image_data, dtype=np.uint8).reshape((height, width, 4))
    
    # Convert from RGBA to BGR (OpenCV's default format)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    
    # Process the image with OpenCV
    # ...
    
    return frame_bgr
```

### Managing Camera Resources

It's important to properly manage media resources, especially when your
application no longer needs them. Cameras and microphones are shared resources,
and failing to release them can impact other applications or cause unexpected
behavior.

### Stopping the Camera

To stop the camera and release resources:

```python
from pyscript.web import page

def stop_camera(stream):
    # Stop all tracks on the stream
    if stream:
        tracks = stream.getTracks()
        for track in tracks:
            track.stop()
        
        # Clear the video element's source
        video_element = page["#camera"][0]._dom_element
        if video_element:
            video_element.srcObject = None
```

### Switching Between Cameras

For devices with multiple cameras, you can implement camera switching:

```python
from pyscript.media import Device, list_devices
from pyscript.web import page

class CameraManager:
    def __init__(self):
        self.cameras = []
        self.current_index = 0
        self.active_stream = None
        self.video_element = page["#camera"][0]._dom_element
    
    async def initialize(self):
        # Get all video input devices
        devices = await list_devices()
        self.cameras = [d for d in devices if d.kind == "videoinput"]
        
        # Start with the first camera
        if self.cameras:
            await self.start_camera(self.cameras[0].id)
    
    async def start_camera(self, device_id=None):
        # Stop any existing stream
        await self.stop_camera()
        
        # Start a new stream
        video_options = (
            {"deviceId": {"exact": device_id}} if device_id 
            else {"facingMode": "environment"}
        )
        self.active_stream = await Device.load(video=video_options)
        
        # Connect to the video element
        if self.video_element:
            self.video_element.srcObject = self.active_stream
    
    async def stop_camera(self):
        if self.active_stream:
            tracks = self.active_stream.getTracks()
            for track in tracks:
                track.stop()
            self.active_stream = None
            
            if self.video_element:
                self.video_element.srcObject = None
    
    async def switch_camera(self):
        if len(self.cameras) <= 1:
            return
        
        # Move to the next camera
        self.current_index = (self.current_index + 1) % len(self.cameras)
        await self.start_camera(self.cameras[self.current_index].id)
```

## Working with Audio

In addition to video, the PyScript media API can access audio inputs:

```python
# Get access to the microphone (audio only)
audio_stream = await Device.load(audio=True, video=False)

# Get both audio and video
av_stream = await Device.load(audio=True, video=True)
```

## Best Practices

When working with media devices in PyScript, follow these best practices:

### Permissions and User Experience

1. **Request permissions contextually**:
   - Only request camera/microphone access when needed
   - Explain to users why you need access before requesting it
   - Provide fallback options when permissions are denied

2. **Clear user feedback**:
   - Indicate when the camera is active
   - Provide controls to pause/stop the camera
   - Show loading states while the camera is initializing

### Resource Management

1. **Always clean up resources**:
   - Stop media tracks when they're not needed
   - Clear `srcObject` references from video elements
   - Be especially careful in single-page applications

2. **Handle errors gracefully**:
   - Catch exceptions when requesting media access
   - Provide meaningful error messages
   - Offer alternatives when media access fails

### Performance Optimization

1. **Match resolution to needs**:
   - Use lower resolutions when possible
   - Consider mobile device limitations
   - Adjust video constraints based on the device

2. **Optimize image processing**:
   - Process frames on demand rather than continuously
   - Use efficient algorithms
   - Consider downsampling for faster processing

## Example Application: Simple Camera Capture

Here's a simplified example that shows how to capture and display images from a
camera:

```python
from pyscript import when, window
from pyscript.media import Device
from pyscript.web import page

class CameraCapture:
    def __init__(self):
        # Get UI elements
        self.video = page["#camera"][0]
        self.video_element = self.video._dom_element
        self.capture_button = page["#capture-button"]
        self.snapshot = page["#snapshot"][0]
        
        # Start camera
        self.initialize_camera()
    
    async def initialize_camera(self):
        # Prefer environment-facing camera on mobile devices
        stream = await Device.load(video={"facingMode": "environment"})
        self.video_element.srcObject = stream
    
    def take_snapshot(self):
        """Capture a frame from the camera and display it"""
        # Get video dimensions
        width = self.video_element.videoWidth
        height = self.video_element.videoHeight
        
        # Create canvas and capture frame
        canvas = window.document.createElement("canvas")
        canvas.width = width
        canvas.height = height
        
        # Draw the current video frame to the canvas
        ctx = canvas.getContext("2d")
        ctx.drawImage(self.video_element, 0, 0, width, height)
        
        # Convert the canvas to a data URL and display it
        image_data_url = canvas.toDataURL("image/png")
        self.snapshot.setAttribute("src", image_data_url)

# HTML structure needed:
# <video id="camera" autoplay playsinline></video>
# <button id="capture-button">Take Photo</button>
# <img id="snapshot">

# Usage:
# camera = CameraCapture()
# 
# @when("click", "#capture-button")
# def handle_capture(event):
#     camera.take_snapshot()
```

This example demonstrates:
- Initializing a camera with the PyScript media API
- Accessing the camera stream and displaying it in a video element
- Capturing a still image from the video stream when requested
- Converting the captured frame to an image that can be displayed

This simple pattern can serve as the foundation for various camera-based
applications and can be extended with image processing libraries as needed for
more complex use cases.


## Conclusion

The PyScript media API provides a powerful way to access and interact with
cameras and microphones directly from Python code running in the browser. By
following the patterns and practices outlined in this guide, you can build
sophisticated media applications while maintaining good performance and user
experience.

Remember that media access is a sensitive permission that requires user consent
and should be used responsibly. Always provide clear indications when media
devices are active and ensure proper cleanup of resources when they're no longer
needed.
