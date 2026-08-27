# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Defer Glow history processing until Home Assistant has completed startup.
- Run recorder history queries on Home Assistant's dedicated recorder executor when available.
- Run initial daily and tariff refreshes as config-entry background tasks.

### Fixed

- Prevent the Glow history refresh loop from delaying Home Assistant startup.
- Prevent slow Glow API requests during initial sensor refreshes from delaying Home Assistant startup.
- Include `unit_class` in external statistics metadata on Home Assistant versions that require it.
- Preserve compatibility with older Home Assistant recorder metadata APIs.

## [v0.0.2] - 2026-07-15

### Changed

- Enable `Rate` and `Standing charge` entities by default.
- Disable `Usage (today)`, `Export (today)`, and `Cost (today)` by default because Glow's daily totals can be delayed or stale.
- Expose standing charge as `GBP/day`.

### Fixed

- Normalize tariff API response variants so rate and standing-charge values are consistently available.
- Read electricity tariffs from the cost resource when one is available.

## [v0.0.1] - 2026-07-05

### Added

- Import electricity and gas half-hour history as Home Assistant external statistics, including electricity export and cost data.
- Support Energy dashboard import/export and total-cost statistics.
- Trigger Glow DCC catchup requests before refreshing canonical DCC-backed history.
- Add live smoke-test coverage for resource discovery and usage, export, and cost history.

### Changed

- Document HACS installation, recorder requirements, Energy dashboard setup, and history freshness limitations.

