---
name: Garmin data interpretation caveats
description: Garmin temperature is device-sensor-in-sun, not air temp — discount the reported temps. General Garmin data interpretation notes.
type: reference
originSessionId: c08792a8-673b-4a3d-ac4c-5b4079505d25
---
When Roger pastes Garmin Connect activity data, certain fields need interpretation, not face-value logging.

**Temperature:** Garmin temp is read from the device sensor, which sits on the bike or wrist in direct sun. **Reported temps run hot vs actual air temp** — often 10–20°F higher on sunny rides. When the Garmin says "98°F max," real ambient was probably 80°F. Use the reported temp as a *trend* (hot vs cool day) but cite air temp explicitly when discussing race conditions or heat tolerance.

**How to apply:** When logging activities, note the Garmin reading but qualify it ("Garmin 98°F max — device-in-sun, actual air was low 80s"). When discussing heat as a coaching factor, anchor to Roger's reported actual conditions, not the Garmin number.

**Other Garmin caveats worth remembering:**
- "Training Effect" / "Aerobic Overreaching" flags are calibrated for general fitness users, not racers with high chronic load — read them as one signal, not gospel
- FTP setting in Garmin is whatever was last manually set; it doesn't auto-update from race data. We update it intentionally based on race evidence
- Walks logged as runs (sub-15:00/mi pace) are mis-classified — flag but don't sweat it
