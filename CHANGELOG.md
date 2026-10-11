# Changelog

All notable project changes are documented here.

## [Unreleased]

### Added

- GitHub Actions workflow to validate version tags and publish GitHub releases.

## [1.18.0] - 2026-10-11

### Changed

- Reverse mesh replacement direction: copy the non-active receiver's mesh data
  into the active source object, keeping both objects and preserving their
  transforms, constraints, and hierarchy.
- Remove the active source's old mesh datablock only when it is unused.

## [1.17.0] - 2026-10-11

### Changed

- For mesh-to-mesh transfers, copy source mesh data onto each receiver while
  preserving receiver objects, transforms, hierarchy, constraints, and
  modifiers.
- Remove old receiver/source mesh datablocks only when unused, then delete the
  active source object.

## [1.16.0] - 2026-10-11

### Changed

- Detect the wheel Bone/Subtarget from the active source wheel's Copy Transforms
  constraint or bone parent, validate it on the hierarchy Target armature, and
  use Pose/Local spaces.

## [1.15.0] - 2026-10-11

### Changed

- Use the object one level above the active source wheel's parent as the Copy
  Transforms Target, rather than the intermediate `.mesh` object.

## [1.14.0] - 2026-10-11

### Changed

- Use the active source wheel's parent as the receiving wheel's Copy Transforms
  Target.
- Keep the active source wheel in the scene for this wheel-target workflow.

## [1.13.0] - 2026-10-11

### Changed

- Retarget a receiving Sollumz wheel's Copy Transforms constraint to the active
  source wheel mesh, clear its Bone/Subtarget, and keep the source in the scene
  as the new target.
- Continue deleting the source for ordinary transfers.

## [1.12.0] - 2026-10-11

### Changed

- Preserve and reapply each receiving Sollumz wheel's armature Target and bone
  Subtarget after transfer, even when no other scene constraint targets the
  deleted source.

## [1.11.0] - 2026-10-11

### Changed

- Retarget Copy Transforms constraints to a receiving Sollumz wheel's armature
  Target and wheel-bone Subtarget when the receiver has that configuration.
- Keep ordinary object receivers as the fallback target and reject ambiguous
  or invalid receiver armature/bone settings.

## [1.10.0] - 2026-10-11

### Added

- Retarget scene and pose-bone Copy Transforms constraints from the deleted
  source to the single receiving object.
- Cancel safely when multiple receivers, self-targeting, or linked constraint
  owners make retargeting ambiguous or unsafe.

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
