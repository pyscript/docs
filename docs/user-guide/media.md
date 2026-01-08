# Media

Modern web applications often need to interact with cameras,
microphones, and other media devices. PyScript provides a Pythonic
interface to these devices through the `pyscript.media` module, letting
your Python code capture video, record audio, and enumerate available
hardware directly from the browser.

This guide explains how to work with media devices in PyScript,
covering device discovery, stream capture, and practical usage
patterns.

## Understanding media access

Media device access in the browser follows strict security and privacy
rules. Your code runs in a sandbox with these constraints:

**User permission is required.** The browser will show a permission
dialog when you first attempt to access cameras or microphones. Users
can grant or deny access, and they can revoke permissions at any time.

**Secure contexts only.** Media access works only over HTTPS or on
localhost. This security requirement prevents malicious sites from
accessing media devices without proper encryption.

**Privacy protections apply.** Device labels may appear as empty strings
until permission is granted. This prevents sites from fingerprinting
users based on their connected hardware before receiving explicit
consent.

These requirements protect users whilst enabling legitimate applications
to work with media devices safely.

## Listing available devices

The `list_devices()` function discovers what media devices are available
on the user's system:

```python
from pyscript.media import list_devices


# Get all available media devices.
devices = await list_devices()

for device in devices:
    print(f"{device.kind}: {device.label}")
```

Each device has three key properties. The `kind` property indicates
device type: `"videoinput"` for cameras, `"audioinput"` for
microphones, or `"audiooutput"` for speakers. The `label` property
provides a human-readable name like "Built-in Camera" or "External USB
Microphone". The `id` property gives a unique identifier for the device.

You can filter devices by type to find specific hardware:

```python
# Find all cameras.
cameras = [d for d in devices if d.kind == "videoinput"]

# Find all microphones.
microphones = [d for d in devices if d.kind == "audioinput"]

# Find a specific device by label.
usb_camera = None
for device in devices:
    if device.kind == "videoinput" and "USB" in device.label:
        usb_camera = device
        break
```

Device labels may be empty strings until the user grants permission to
access media devices. Once permission is granted, labels become
available, helping users understand which hardware is being used.

## Capturing media streams

The `Device.request_stream()` class method requests access to media
devices and returns a stream you can use with HTML video or audio
elements:

```python
from pyscript.media import Device
from pyscript.web import page


# Request video from the default camera.
stream = await Device.request_stream(video=True)

# Display it in a video element.
video = page["#my-video"]
video.srcObject = stream
```

This triggers a permission dialog the first time it runs. If the user
grants permission, you receive a `MediaStream` object containing the
video feed. If they deny permission, an exception is raised.

You can request audio, video, or both:

```python
# Video only (default).
video_stream = await Device.request_stream(video=True)

# Audio only.
audio_stream = await Device.request_stream(audio=True, video=False)

# Both audio and video.
av_stream = await Device.request_stream(audio=True, video=True)
```

For finer control, specify constraints as dictionaries:

```python
# Request specific video resolution.
stream = await Device.request_stream(
    video={"width": 1920, "height": 1080}
)

# Request high-quality audio with echo cancellation.
stream = await Device.request_stream(
    audio={
        "sampleRate": 48000,
        "echoCancellation": True,
        "noiseSuppression": True
    }
)
```

These constraints follow the
[MediaTrackConstraints web standard](https://developer.mozilla.org/en-US/docs/Web/API/MediaTrackConstraints).
The browser does its best to satisfy your constraints but may fall back
to available settings if exact matches aren't possible.

## Using specific devices

Sometimes you need to capture from a particular camera or microphone
rather than the default device. List devices first, then request a
stream from the one you want:

```python
from pyscript.media import list_devices


# Find all cameras.
devices = await list_devices()
cameras = [d for d in devices if d.kind == "videoinput"]

# Use the second camera if available.
if len(cameras) > 1:
    stream = await cameras[1].get_stream()
    video = page["#my-video"]
    video.srcObject = stream
```

The `get_stream()` method on a device instance requests a stream from
that specific device, handling the device ID constraints automatically.

## Example: Photobooth application

Here's a complete application demonstrating webcam access and still
frame capture:

<iframe src="../../example-apps/photobooth/" style="border: 1px solid black; width:100%; min-height: 700px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/photobooth).

This application requests camera access, displays live video, and
captures still frames using a canvas element. Click "Start Camera" to
begin, then "Capture Photo" to grab the current frame.

The technique uses canvas to extract frames from the video stream. The
`drawImage()` method copies the current video frame onto a canvas,
creating a still image you can save or process further.

## Handling permissions

Media access requires user permission, and users can deny access or
revoke it later. Always handle these cases gracefully:

```python
from pyscript.media import Device


try:
    stream = await Device.request_stream(video=True)
    # Use the stream.
    video = page["#camera"]
    video.srcObject = stream
except Exception as e:
    # Permission denied or device not available.
    print(f"Could not access camera: {e}")
    # Show a message to the user explaining what happened.
```

Consider providing fallback content or alternative functionality when
media access isn't available. This improves the experience for users who
deny permission or lack the necessary hardware.

## Stream management

Media streams use system resources. Stop streams when you're finished to
free up cameras and microphones:

```python
# Get stream.
stream = await Device.request_stream(video=True)

# Use it...
video = page["#camera"]
video.srcObject = stream

# Later, stop all tracks.
for track in stream.getTracks():
    track.stop()
```

Stopping tracks releases the hardware, allowing other applications to
use the devices and conserving battery life on mobile devices.

## What's next

Now that you understand media device access, explore these related
topics:

**[Workers](workers.md)** - Display content from background threads
(requires explicit `target` parameter).

**[Filesystem](filesystem.md)** - Learn more about the virtual
filesystem and how the `files` option works.

**[FFI](ffi.md)** - Understand how JavaScript modules integrate with
Python through the foreign function interface.

**[Offline](offline.md)** - Use PyScript while not connected to the internet.