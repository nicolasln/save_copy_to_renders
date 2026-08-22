import os
import subprocess

import bpy


VERSIONSTAMP_SCRIPT = "/Users/nicolas/Code/scripts/versionstamp.py"


def get_versionstamp():
    """Run versionstamp.py and return its output without surrounding whitespace."""
    result = subprocess.run(
        [VERSIONSTAMP_SCRIPT],
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout.strip()


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

            if os.path.exists(destination):
                self.report(
                    {"ERROR"},
                    f"Versioned copy already exists: {destination}",
                )
                return {"CANCELLED"}

            result = bpy.ops.wm.save_as_mainfile(
                filepath=destination,
                check_existing=False,
                copy=True,
            )
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
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
