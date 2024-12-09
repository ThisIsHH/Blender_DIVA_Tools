# __init__.py (root)

bl_info = {
    "name": "DIVA Tools",
    "author": "ThisIsHH, FlyingSpirits",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "description": "Utility tools for Project DIVA Games",
    "category": "Import-Export",
}

from .ui import register as register_ui, unregister as unregister_ui

def register():
    register_ui()

def unregister():
    unregister_ui()
