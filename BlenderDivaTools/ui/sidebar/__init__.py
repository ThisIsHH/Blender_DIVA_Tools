from .operators import register_operators, unregister_operators
from .panel import register_panel, unregister_panel
from .properties import register_properties, unregister_properties

def register():
    register_properties()
    register_operators()
    register_panel()

def unregister():
    unregister_panel()
    unregister_operators()
    unregister_properties()
