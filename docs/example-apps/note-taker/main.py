"""
Note Taker - demonstrating local filesystem access.
"""
from pyscript import when, fs
from pyscript.web import page


@when("click", "#mount-btn")
async def mount_folder(event):
    """
    Mount a local folder for saving notes.
    """
    status = page["#status"]
    status.content = "Please select a folder..."
    
    try:
        await fs.mount("/notes")
        
        # Enable the UI.
        page["#save-btn"].disabled = False
        page["#note"].disabled = False
        status.content = "Ready! Type your note and click Save."
    except Exception as e:
        status.content = f"Error: {e}"


@when("click", "#save-btn")
async def save_note(event):
    """
    Save the note to the mounted folder.
    """
    status = page["#status"]
    note_text = page["#note"].value
    
    try:
        # Write the note.
        with open("/notes/my-note.txt", "w") as f:
            f.write(note_text)
        
        # Sync to local filesystem.
        await fs.sync("/notes")
        
        status.content = "Note saved successfully!"
    except Exception as e:
        status.content = f"Error saving: {e}"