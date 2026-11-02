import os
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
    """Return <blend directory>/Renders/<stem> <stamp>.blend."""
    directory = os.path.dirname(os.path.abspath(blend_filepath))
    filename = os.path.basename(blend_filepath)
    stem, extension = os.path.splitext(filename)
    return os.path.join(directory, "Renders", f"{stem} {stamp}{extension}")


class WM_OT_save_versioned_copy(bpy.types.Operator):
    bl_idname = "wm.save_versioned_copy"
    bl_label = "Save Versioned Copy"
    bl_description = "Save a stamped copy in the Renders folder beside the current blend file"
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


def draw_save_versioned_copy(self, _context):
    self.layout.operator(
        WM_OT_save_versioned_copy.bl_idname,
        text="Save Versioned Copy",
    )


classes = (WM_OT_save_versioned_copy,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file.append(draw_save_versioned_copy)


def unregister():
    bpy.types.TOPBAR_MT_file.remove(draw_save_versioned_copy)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
