# Apple Shortcuts & Siri Voice Integration

The Ferryman can be summoned without touching a screen or opening a terminal. By pairing Siri with macOS/iOS Shortcuts, you create an on-demand, zero-screen somatic lifeline.

## The "Knot" Shortcut (Midday Pause / SOS)

When your nervous system is in fight-or-flight, your jaw is clenched, or you are spiraling in a mental loop:

1. Open the **Shortcuts** app on macOS.
2. Click **+** to create a new shortcut.
3. Add the action: **Run Shell Script**.
4. Set the shell to `/bin/zsh` or `/bin/bash`.
5. Enter the command (substituting your actual path):
   ```bash
   /usr/bin/python3 /path/to/the-ferryman-project/ferryman.py pause --voice
   ```
6. Name the shortcut: `Knot`.

### How to Use
Say: **"Hey Siri, Knot."**
The Ferryman immediately speaks the 30-second grounding protocol:
- Foot contact with the earth
- Full lung exhale
- 3 physical objects in the room

No screen turns on. Nothing is recorded. You return directly to your life.

## Dawn and Dusk Shortcuts

Repeat the same process with:
- **Dawn Anchor**:
  ```bash
  /usr/bin/python3 /path/to/the-ferryman-project/ferryman.py dawn --voice
  ```
- **Dusk Release**:
  ```bash
  /usr/bin/python3 /path/to/the-ferryman-project/ferryman.py dusk --voice
  ```
