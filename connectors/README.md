# Connectors

Ways to reach the Ferryman without opening a terminal. All of them run `ferryman.py --voice`, which speaks each line with the offline system voice (`say` on macOS). Nothing is installed, nothing leaves the machine.

When a crossing is spoken with no keyboard attached, it does not ask you to type. It asks the question, leaves a silence, and closes. The answer stays with you; nothing is logged.

## launchd (scheduled Dawn and Dusk)

```bash
python3 connectors/launchd/schedule.py install                        # dawn 07:00, dusk 21:30
python3 connectors/launchd/schedule.py install --dawn 06:30 --dusk 22:00
python3 connectors/launchd/schedule.py uninstall
```

This writes two LaunchAgents (`org.ferryman.dawn`, `org.ferryman.dusk`) into `~/Library/LaunchAgents`.

If the Mac is asleep at the hour, launchd fires the job on wake. A crossing more than 90 minutes late stays silent rather than speaking into whatever room you have carried the laptop to.

There is no scheduled Midday Pause. It is an SOS, not an appointment.

## Siri / Apple Shortcuts (Midday Pause by voice)

1. Shortcuts → new shortcut → add the **Run Shell Script** action.
2. Script (use the absolute path to your checkout):

   ```bash
   /usr/bin/python3 /path/to/the-ferryman-project/ferryman.py pause --voice
   ```

3. Name the shortcut `Knot`. "Hey Siri, knot" now runs the 30-second grounding aloud.

The same recipe works for `dawn` and `dusk`.

## Try it

```bash
python3 ferryman.py dusk --voice              # spoken, typed answer
python3 ferryman.py dusk --voice </dev/null   # spoken, no keyboard: the scheduled experience
```
