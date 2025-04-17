### Added

- use global binary storage so that already downloaded binaries don't get downloaded twice
- cache latest tailwindcss-cli-extra version to not burden GitHub and your internet connection with repeated and slowing requests
- timeout on all internet requests to fail fast if something is wrong
- progress bar when downloading new tailwindcss-cli-extra binary

### Changed

- BREAKING: removed PYTAILWINDCSS_EXTRA_BIN_DIR environment variable setting
- locked major tailwindcss-cli-extra version to v2 for now to prevent braking changes outside of own major updates
- BREAKING: don't show log level of log messages for cleaner logs
