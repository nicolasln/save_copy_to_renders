import os
import re
from datetime import datetime, timezone

import bpy


ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base36(number):
    result = ""
    while number:
        number, remainder = divmod(number, 36)
        result = ALPHABET[remainder] + result
    return result or "0"


def get_versionstamp():
    """Encode the current UTC year's elapsed 20-second intervals in Base36."""
    now = datetime.now(timezone.utc)
    epoch = datetime(now.year, 1, 1, tzinfo=timezone.utc)
    value = int((now - epoch).total_seconds()) // 20
    return base36(value).zfill(4)


def versioned_copy_path(blend_filepath, stamp):
    """Replace an existing stamp in place, or queue an unstamped file in Renders."""
    directory = os.path.dirname(os.path.abspath(blend_filepath))
    filename = os.path.basename(blend_filepath)
    stem, extension = os.path.splitext(filename)
    base_stem, separator, old_stamp = stem.rpartition(" ")
    if base_stem and separator and re.fullmatch(r"[0-9A-Z]{4,}", old_stamp):
        stem = base_stem
    else:
        directory = os.path.join(directory, "Renders")
    return os.path.join(directory, f"{stem} {stamp}{extension}")


class WM_OT_save_copy_to_renders(bpy.types.Operator):
    bl_idname = "wm.save_copy_to_renders"
    bl_label = "Save Copy to Renders"
    bl_description = (
        "Save a timestamped copy in the Renders folder. "
        "Already timestamped files are versioned in their current folder"
    )
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return bool(context.blend_data.filepath)

    def execute(self, context):
        source_filepath = context.blend_data.filepath

        if not source_filepath:
            self.report({"ERROR"}, "Save the blend file first so it has a file name")
            return {"CANCELLED"}

        try:
            stamp = get_versionstamp()
            destination = versioned_copy_path(source_filepath, stamp)
            os.makedirs(os.path.dirname(destination), exist_ok=True)

            while os.path.exists(destination):
                stamp = base36(int(stamp, 36) + 1).zfill(4)
                destination = versioned_copy_path(source_filepath, stamp)

            result = bpy.ops.wm.save_as_mainfile(
                filepath=destination,
                check_existing=False,
                copy=True,
            )
        except (OSError, RuntimeError) as error:
            self.report({"ERROR"}, f"Could not save versioned copy: {error}")
            return {"CANCELLED"}

        if "FINISHED" not in result:
            self.report({"ERROR"}, "Blender did not save the versioned copy")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Saved versioned copy: {destination}")
        return {"FINISHED"}


def draw_save_copy_to_renders(self, _context):
    self.layout.operator(
        WM_OT_save_copy_to_renders.bl_idname,
        text="Save Copy to Renders",
    )


classes = (WM_OT_save_copy_to_renders,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file.append(draw_save_copy_to_renders)


def unregister():
    bpy.types.TOPBAR_MT_file.remove(draw_save_copy_to_renders)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
