# Changelog

All notable changes to kitchen-display are written in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/).

## [3.0.0] - 2026-11-28

### Added

- The display shows pre-orders in a second list.

### Changed

- **BREAKING:** The setting `font` is renamed to `font_size`. The value does not change.

### Deprecated

- The setting `refresh`. Use `refresh_ms` instead. See [MIGRATION.md](MIGRATION.md).
  `refresh` will be removed in 4.0.0.

### Removed

- **BREAKING:** The option `--fullscreen`. It was deprecated in 2.5.0. Use `--mode full` instead.
- **BREAKING:** The setting `beep`. Use `"sound": "on"` or `"sound": "off"` instead.

## [2.5.0] - 2026-08-20

### Added

- The option `--mode`. Choose `window` or `full`.

### Deprecated

- The option `--fullscreen`. Use `--mode full` instead. `--fullscreen` will be removed in 3.0.0.

### Fixed

- Long order names were cut off on small screens.

## [2.1.0] - 2026-05-15

### Added

- The setting `beep`. When it is `true`, the display makes a sound for every new order.

## [2.0.0] - 2026-03-01

### Added

- The option `--fullscreen`.
