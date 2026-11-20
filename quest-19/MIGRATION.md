# Moving from kitchen-display 2.x to 3.0

Most changes are listed in [CHANGELOG.md](CHANGELOG.md). This guide explains the ones that need more than a new name.

## `refresh` → `refresh_ms`

The meaning of the number changed, so you cannot only change the name.

| Setting | Unit | Example |
| --- | --- | --- |
| `refresh` (2.x) | **seconds** | `5` |
| `refresh_ms` (3.0) | **milliseconds** | `5000` |

One second is 1000 milliseconds. So: **refresh_ms = refresh × 1000**.

For example, `"refresh": 5` becomes `"refresh_ms": 5000`.

## `beep` → `sound`

`"beep": true` becomes `"sound": "on"`. `"beep": false` becomes `"sound": "off"`.
