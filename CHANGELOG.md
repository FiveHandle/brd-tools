# Changelog

All notable project changes are documented here.

## [Unreleased]

### Added

- GitHub Actions workflow to validate version tags and publish GitHub releases.

## [1.9.0] - 2026-10-11

### Changed

- Restored the v1.6.0 bounding-box-center alignment behavior while retaining
  the radial menu.

## [1.8.0] - 2026-10-11

### Changed

- Preserve each target's pre-transfer visible world position while applying the
  source's origin and transform.

## [1.7.0] - 2026-10-11

### Added

- Transfer radial menu, available in the 3D View with **Shift+Alt+T** or from
  the Transfer sidebar.

## [1.6.0] - 2026-10-11

### Changed

- Copy the source's exact world transform to targets and compensate for origin
  offsets in each target's local geometry.

## [1.5.0] - 2026-10-11

### Added

- Manual **Check for Updates** button in the Transfer sidebar.

## [1.4.0] - 2026-10-11

### Changed

- Simplified automatic updates to use public GitHub releases without requiring
  users to configure tokens.
- Added a clear sidebar message for missing or unpublished public releases.
- Licensed the add-on under GPL-3.0-or-later.

## [1.3.0] - 2026-10-11

### Added

- Startup check for the latest private GitHub release, using a locally
  configured read-only token.
- Release archive and version validation before updating the installed add-on.
- Update status in the Transfer sidebar and setup instructions.

## [1.2.0] - 2026-10-11

### Changed

- Compensated for differing object origins by aligning target bounding-box
  centers with the source's visible bounding-box center.

## [1.1.0] - 2026-10-11

### Changed

- Moved the tool into its own **Transfer** tab in the 3D View sidebar.

## [1.0.0] - 2026-10-11

### Added

- Blender add-on operator to copy the active object's world transform to all
  other selected objects and delete the active source.
- Confirmation prompt and undo support for the destructive operation.
- Sidebar panel and installation/use instructions.
