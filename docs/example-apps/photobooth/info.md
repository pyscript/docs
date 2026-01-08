# Photobooth

A simple webcam application demonstrating media device access and still
frame capture.

## What it shows

- Requesting camera access with `Device.request_stream()`.
- Displaying live video in a video element.
- Capturing still frames from video using canvas.
- Proper error handling for permission denial.

## How it works

Click "Start Camera" to request webcam access. Once granted, the live
video feed appears. Click "Capture Photo" to grab the current frame and
display it as a still image on the canvas.

The key technique is using the canvas `drawImage()` method to copy the
current video frame:

```python
# Get the canvas context.
ctx = canvas.getContext("2d")

# Draw the current video frame.
ctx.drawImage(video, 0, 0, width, height)
```

## Browser support

This requires a browser with webcam support and HTTPS (or localhost).
The user must grant camera permission when prompted.