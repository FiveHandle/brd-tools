# Object Transform Transfer

A Blender add-on for replacing mesh data while preserving the receiver object,
and for transferring transforms between other object types.

## Install

1. In Blender, open **Edit > Preferences > Add-ons**.
2. Choose **Install from Disk** and select `object_transform_transfer.py`.
3. Enable **Object Transform Transfer**.

## Use

1. In Object Mode, select the source object and the target object or objects.
2. Make the source active (the last selected object, shown with the brighter
   outline).
3. In the 3D View sidebar, open the **Transfer** tab and click
   **Transfer Transform**.
4. Confirm the operation.

You can also open the radial menu with **Shift+Alt+T** in the 3D View, or
click **Open Transfer Radial Menu** in the sidebar. It contains the transfer
action and **Check for Updates**.

When the active source and the single non-active receiver are mesh objects, the
active source object stays in place and receives a private copy of the
receiver's mesh data. The receiver remains unchanged. The active object's
transform, hierarchy, constraints, and modifiers are preserved; its old mesh
datablock is removed only when unused. The receiver's mesh datablock is never
removed.

For non-mesh transfers, the receiver keeps its existing data; the source's
world transform is applied and visible bounding-box centers are aligned as
before. The active source object is then deleted.

For non-mesh transfers, object or pose-bone **Copy Transforms** constraints
elsewhere in the scene that target the deleted source are redirected to the
single receiving object. If scene constraints reference the source, select
exactly one receiver. A replacement that would make a constraint target its own
owner, or linked constraint owners, is rejected.

Linked objects that are not library overrides must be made local before they
can be used as a source or target.

## Automatic updates

The add-on checks the latest stable release of the public GitHub repository
`FiveHandle/brd-tools` about 10 seconds after Blender starts. No token or
GitHub account is needed by users. The repository and add-on source must be
public for this check to work.

When a newer release is found, the add-on validates its tag and Python version
before replacing its installed script. Restart Blender to load the update.
To check immediately, click **Check for Updates** in the Transfer sidebar.
Update status appears there and in Blender's system console. A 404 means the
repository is not publicly accessible or no GitHub release has been published
yet.

### Publish a release

GitHub Actions creates a release whenever a version tag is pushed:

1. Update `bl_info["version"]` and add the release notes to `CHANGELOG.md`.
2. Commit the changes and create a matching tag, such as `v1.18.0`.
3. Push the commit and tag to GitHub. The **Publish Release** workflow creates
   the GitHub release, which the add-on checks at startup.

Release archives must contain exactly one `object_transform_transfer.py` file.

## License

This add-on is distributed under the GNU General Public License, version 3 or
later. See [LICENSE](./LICENSE) for the full license text.
