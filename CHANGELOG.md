# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Job Tracker Operations**: Added `get_job` and `delete_job` query methods to `JobTrackerDB`.
- **Extended Test Suite**: Added verification for single job lookups, deletion, and empty state assertions.
- **License**: Added official MIT `LICENSE` (2026 Vlad Vinys).

## [1.0.0] - 2026-10-28

### Added
- Async client for German Federal Employment Agency (Bundesagentur für Arbeit) Jobsuche API.
- Local SQLite job application status tracking.
- Google Jules agent rules and verification workflows.
