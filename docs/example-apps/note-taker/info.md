# Note Taker

A simple note-taking application demonstrating local filesystem access.

## What it shows

- Mounting a local directory on user interaction.
- Writing files to the mounted directory.
- Syncing changes to persist them locally.
- Proper error handling.

## How it works

Click "Select Folder" to mount a local directory. The browser will
prompt you to choose a folder. Once mounted, you can type notes and
save them to your chosen folder.

The key pattern:

```python
# Mount (user selects folder).
await fs.mount("/notes")

# Write files.
with open("/notes/my-note.txt", "w") as f:
    f.write(note_text)

# Sync to persist changes.
await fs.sync("/notes")
```

## Browser support

This only works in Chromium-based browsers (Chrome, Edge, Brave,
Vivaldi). Firefox and Safari don't support the File System Access API
yet.