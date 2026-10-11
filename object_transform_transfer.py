# SPDX-License-Identifier: GPL-3.0-or-later

bl_info = {
    "name": "Object Transform Transfer",
    "author": "BRD-Tools",
    "version": (1, 4, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Transfer",
    "description": "Align selected objects to the active object's bounds, delete it, and update automatically",
    "category": "Object",
}

import ast
import bpy
from mathutils import Vector
import io
import json
import logging
import os
from pathlib import Path
import re
import tempfile
import urllib.error
import urllib.request
import zipfile


_REPOSITORY = "FiveHandle/brd-tools"
_RELEASE_API = f"https://api.github.com/repos/{_REPOSITORY}/releases/latest"
_ADDON_FILENAME = "object_transform_transfer.py"
_MAX_ARCHIVE_BYTES = 20 * 1024 * 1024
_MAX_ADDON_BYTES = 2 * 1024 * 1024
_UPDATE_STATUS = "Automatic update check has not run."
_LOGGER = logging.getLogger(__name__)


def _bounding_box_center(obj):
    corners = [Vector(corner) for corner in obj.bound_box]
    center = Vector((0.0, 0.0, 0.0))
    for corner in corners:
        center += corner
    return center / len(corners)


def _extract_version(source):
    module = ast.parse(source)
    for node in module.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "bl_info"
            for target in node.targets
        ):
            metadata = ast.literal_eval(node.value)
            version = metadata["version"]
            if (
                isinstance(version, tuple)
                and len(version) == 3
                and all(isinstance(part, int) and part >= 0 for part in version)
            ):
                return version
            break
    raise ValueError("The release add-on has no valid three-part bl_info version")


def _read_url(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Object-Transform-Transfer-Updater",
        },
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        data = response.read(_MAX_ARCHIVE_BYTES + 1)
    if len(data) > _MAX_ARCHIVE_BYTES:
        raise ValueError("The GitHub response exceeds the 20 MB update limit")
    return data


def _install_latest_release():
    release = json.loads(_read_url(_RELEASE_API))
    tag = release.get("tag_name", "")
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", tag)
    if not match:
        raise ValueError(f"Unsupported GitHub release tag: {tag!r}; use X.Y.Z or vX.Y.Z")

    latest_version = tuple(int(part) for part in match.groups())
    if latest_version <= bl_info["version"]:
        return "Add-on is up to date."

    archive_url = release.get("zipball_url")
    if not archive_url or not archive_url.startswith(
        f"https://api.github.com/repos/{_REPOSITORY}/"
    ):
        raise ValueError("The GitHub release does not have a valid repository archive URL")

    with zipfile.ZipFile(io.BytesIO(_read_url(archive_url))) as archive:
        members = [
            name
            for name in archive.namelist()
            if Path(name).name == _ADDON_FILENAME and not name.endswith("/")
        ]
        if len(members) != 1:
            raise ValueError(
                f"Expected one {_ADDON_FILENAME} in the release archive; found {len(members)}"
            )
        info = archive.getinfo(members[0])
        if info.file_size > _MAX_ADDON_BYTES:
            raise ValueError("The add-on file in the release exceeds the 2 MB limit")
        addon_source = archive.read(info)

    source_version = _extract_version(addon_source.decode("utf-8"))
    if source_version != latest_version:
        raise ValueError(
            f"Release tag {tag} does not match add-on version {source_version}"
        )

    addon_path = Path(__file__).resolve()
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{_ADDON_FILENAME}.",
            suffix=".tmp",
            dir=addon_path.parent,
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(addon_source)
        os.replace(temporary_path, addon_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    return f"Updated to {'.'.join(str(part) for part in latest_version)}. Restart Blender to load it."


def _check_for_update():
    global _UPDATE_STATUS
    _UPDATE_STATUS = "Checking GitHub for updates..."
    try:
        _UPDATE_STATUS = _install_latest_release()
        _LOGGER.info(_UPDATE_STATUS)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            _UPDATE_STATUS = (
                "Update unavailable (404): make the repo public and publish a release."
            )
        else:
            _UPDATE_STATUS = f"Automatic update failed: GitHub HTTP {error.code}."
        _LOGGER.error("%s (%s)", _UPDATE_STATUS, error)
    except (
        urllib.error.URLError,
        TimeoutError,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        SyntaxError,
        zipfile.BadZipFile,
    ) as error:
        _UPDATE_STATUS = f"Automatic update failed: {error}"
        _LOGGER.error(_UPDATE_STATUS)
    return None


class OBJECT_OT_transfer_transform_delete_source(bpy.types.Operator):
    """Align selected objects' bounding-box centers to the active object, then delete it"""

    bl_idname = "object.transfer_transform_delete_source"
    bl_label = "Transfer Transform & Delete Source"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.mode == "OBJECT"
            and context.view_layer.objects.active is not None
            and len(context.selected_objects) >= 2
        )

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        source = context.view_layer.objects.active
        targets = [obj for obj in context.selected_objects if obj != source]

        if source is None or not targets:
            self.report(
                {"ERROR"},
                "Select a source object and at least one target, with the source active",
            )
            return {"CANCELLED"}

        linked_objects = [
            obj
            for obj in [source, *targets]
            if obj.library is not None and obj.override_library is None
        ]
        if linked_objects:
            names = ", ".join(obj.name for obj in linked_objects)
            self.report(
                {"ERROR"},
                f"Linked objects must be made local or library overrides before use: {names}",
            )
            return {"CANCELLED"}

        source_matrix = source.matrix_world.copy()
        source_center = _bounding_box_center(source)
        source_linear = source_matrix.to_3x3()
        for target in targets:
            target_matrix = source_matrix.copy()
            target_matrix.translation = (
                source_matrix.translation
                + source_linear @ (source_center - _bounding_box_center(target))
            )
            target.matrix_world = target_matrix

        bpy.data.objects.remove(source, do_unlink=True)
        return {"FINISHED"}


class VIEW3D_PT_object_transform_transfer(bpy.types.Panel):
    bl_label = "Object Transform Transfer"
    bl_idname = "VIEW3D_PT_object_transform_transfer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Transfer"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Active object is the source.")
        layout.label(text="Align visible bounds, then delete source.")
        layout.operator(OBJECT_OT_transfer_transform_delete_source.bl_idname)
        layout.separator()
        layout.label(text=_UPDATE_STATUS, icon="INFO")


classes = (
    OBJECT_OT_transfer_transform_delete_source,
    VIEW3D_PT_object_transform_transfer,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.timers.register(_check_for_update, first_interval=10.0)


def unregister():
    if bpy.app.timers.is_registered(_check_for_update):
        bpy.app.timers.unregister(_check_for_update)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
