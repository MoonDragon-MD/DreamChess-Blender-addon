bl_info = {
    "name": "Esporta DCM DreamChess (.dcm)",
    "author": "MoonDragon",
    "version": (1, 0, 0),
    "blender": (2, 82, 0),
    "location": "File > Export > DreamChess DCM",
    "description": "Export selected mesh to DreamChess Model format (.dcm) for DreamChess game",
    "wiki_url": "https://github.com/MoonDragon-MD/DreamChess-Blender-addon",
    "category": "Import-Export",
    "warning": "",
}

import bpy
from bpy_extras.io_utils import ExportHelper
from . import exporter

class DCMExporter(bpy.types.Operator, ExportHelper):
    bl_idname = "export_mesh.dcm"
    bl_label = "Export DCM"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".dcm"
    filter_glob: bpy.props.StringProperty(default="*.dcm", options={'HIDDEN'})

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        try:
            message = exporter.write(self.filepath, context)
            self.report({'INFO'}, message)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

def menu_func(self, context):
    self.layout.operator(DCMExporter.bl_idname, text="DreamChess DCM (.dcm)")

def register():
    bpy.utils.register_class(DCMExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(DCMExporter)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()