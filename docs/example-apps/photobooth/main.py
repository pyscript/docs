"""
Photobooth - demonstrating webcam capture and still frame extraction.
"""
from pyscript import when
from pyscript.media import Device
from pyscript.web import page


# Track the current stream.
current_stream = None


@when("click", "#start-btn")
async def start_camera(event):
    """
    Start the camera and display live video.
    """
    global current_stream
    
    status = page["#status"]
    status.content = "Requesting camera access..."
    
    try:
        # Request video stream.
        current_stream = await Device.request_stream(video=True)
        
        # Display in video element.
        video = page["#camera"]
        video.srcObject = current_stream
        
        # Update UI.
        page["#start-btn"].disabled = True
        page["#capture-btn"].disabled = False
        status.content = "Camera ready! Click 'Capture Photo' to take a picture."
    except Exception as e:
        status.content = f"Error accessing camera: {e}"


@when("click", "#capture-btn")
def capture_photo(event):
    """
    Capture a still frame from the video stream.
    """
    video = page["#camera"]
    canvas = page["#photo"]
    
    # Get the canvas 2D context.
    ctx = canvas.getContext("2d")
    
    # Draw the current video frame onto the canvas.
    ctx.drawImage(video, 0, 0, 400, 300)
    
    # Update status.
    status = page["#status"]
    status.content = "Photo captured!"