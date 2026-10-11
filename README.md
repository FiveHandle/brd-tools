# Object Transform Transfer

A Blender add-on that aligns the visible bounding-box centers of selected
objects to the active source object's bounding-box center, then deletes the
source.

## Install

1. In Blender, open **Edit > Preferences > Add-ons**.
2. Choose **Install from Disk** and select `object_transform_transfer.py`.
3. Enable **Object Transform Transfer**.

## Use

1. In Object Mode, select the source object and the target object or objects.
2. Make the source active (the last selected object, shown with the brighter
   outline).
3. In the 3D View sidebar, open the **Transfer** tab and click
   **Transfer Transform & Delete Source**.
4. Confirm the operation.

You can also open the radial menu with **Shift+Alt+T** in the 3D View, or
click **Open Transfer Radial Menu** in the sidebar. It contains the transfer
action and **Check for Updates**.

Each target receives the source's exact world transform, including its origin,
location, rotation, and scale. Target geometry is offset in local space so its
visible bounding-box center aligns with the source's. Geometry data is copied
before editing, so other objects sharing it remain unchanged. The source
object is then deleted. Materials and other object data are not transferred.
Use Blender's Undo immediately afterward to reverse the operation.

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
2. Commit the changes and create a matching tag, such as `v1.9.0`.
3. Push the commit and tag to GitHub. The **Publish Release** workflow creates
   the GitHub release, which the add-on checks at startup.

Release archives must contain exactly one `object_transform_transfer.py` file.

## License

This add-on is distributed under the GNU General Public License, version 3 or
later. See [LICENSE](./LICENSE) for the full license text.
