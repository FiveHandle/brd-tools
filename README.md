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

The source's rotation and scale are copied to every other selected object.
Each target is positioned so its local bounding-box center aligns with the
source's visible bounding-box center, compensating for differences between
object origins. The source object is then deleted. Object data such as mesh
geometry and materials is not transferred. Use Blender's Undo immediately
afterward to reverse the operation.

Linked objects that are not library overrides must be made local before they
can be used as a source or target.

## Automatic updates

The add-on checks the latest stable GitHub release about 10 seconds after
Blender starts. For this private repository, configure a fine-grained GitHub
personal access token with **Contents: Read-only** permission for
`fivehandle/brd-tools`:

1. Open **Edit > Preferences > Add-ons** and expand **Object Transform
   Transfer**.
2. Enter the token in **GitHub Read-Only Token**.
3. Publish each update as a GitHub release tagged with the same three-part
   version as `bl_info` (for example, `v1.3.0`). The release source archive
   must contain exactly one `object_transform_transfer.py` file.

When a newer release is found, the add-on validates its tag and Python version
before replacing its installed script. Restart Blender to load the update.
The token is masked in the preferences UI but Blender stores it locally without
encryption. Do not share the token or commit it to the repository. Without a
configured token, update checks are skipped and the reason appears in the
Transfer sidebar and Blender's system console.

### Publish a release

GitHub Actions creates a release whenever a version tag is pushed:

1. Update `bl_info["version"]` and add the release notes to `CHANGELOG.md`.
2. Commit the changes and create a matching tag, such as `v1.4.0`.
3. Push the commit and tag to GitHub. The **Publish Release** workflow creates
   the GitHub release, which the add-on checks at startup.

For this private repository, each update recipient needs GitHub read access to
the repository and their own fine-grained token. Never distribute your own
token.
