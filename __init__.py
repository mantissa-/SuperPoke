# SuperPoke created by Midge "Mantissa" Sinnaeve (mantissa.xyz)
# Downloaded form https://github.com/mantissa-/RandoMesh
# Licensed under GPLv3

bl_info = {
    "name": "SuperPoke",
    "author": "Midge \"Mantissa\" Sinnaeve",
    "version": (0, 0, 6),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > SuperPoke Tab",
    "description": "Create superpoked geometry",
    "wiki_url": "https://github.com/mantissa-/SuperPoke",
    "category": "3D View",
    "warning": "You might have fun"
}


import bpy, bmesh
from bpy.props import (IntProperty, FloatProperty, BoolProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)


#------------#
# PROPERTIES #
#------------#

class SuperPokeProps(PropertyGroup):
    
    bool_keep_original : BoolProperty(
        name = "Keep Original",
        description = "Keep a copy of the original mesh",
        default = True
        )
        
    bool_apply_modifiers : BoolProperty(
        name = "Apply Modifiers",
        description = "Apply the current modifers to object before processing",
        default = True
        )

    int_iterations : IntProperty(
        name = "Iterations",
        description = "SuperPoke Iterations",
        default = 6,
        min = 1,
        max = 15,
        soft_max = 8
        )

    fl_poke_offset : FloatProperty(
        name = "Poke Offset:",
        description = "Set base poke offset, multiplier applied per iteration",
        default = -0.5,
        soft_min = -1,
        soft_max = 1,
        min = -2.0,
        max = 2.0,
        precision = 2
        )
        
    fl_poke_multiplier : FloatProperty(
        name = "Offset Multiplier:",
        description = "Set base poke offset, halved per iteration",
        default = 0.5,
        soft_max = 1.0,
        min = 0,
        max = 2.0,
        precision = 2
        )

    bool_poke_alternate : BoolProperty(
        name = "Alternate Offset",
        description = "Alternate the poke offset for a recursive look",
        default = True
        )
        
    bool_shape_keys : BoolProperty(
        name = "Create Shape Keys (SLOW)",
        description = "Create a shape key to animate each iteration",
        default = False
        )

#----#
# UI #
#----#

class SuperPokePanel(bpy.types.Panel):
    # Creates a Panel in the sidebar
    bl_label = "SuperPoke"
    bl_idname = "OBJECT_PT_SuperPoke"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "SuperPoke"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=False)
        row = col.row(align=True)
        
        
        
        col.prop(scene.sp_props, "bool_keep_original")
        col.prop(scene.sp_props, "bool_apply_modifiers")
        
        col.prop(scene.sp_props, "int_iterations")
        col.prop(scene.sp_props, "fl_poke_offset")
        col.prop(scene.sp_props, "fl_poke_multiplier")
        
        col.prop(scene.sp_props, "bool_poke_alternate")
        col.prop(scene.sp_props, "bool_shape_keys")

        obj = bpy.context.object
        
        if obj != None and obj.type in ['MESH']:
            spp = bpy.context.scene.sp_props
            iter = spp.int_iterations
            me = bpy.context.object.data
            fpc = ((len(me.polygons))*4)*(3**(iter-1))
            
        
            col.separator()
            col.separator()
            col.label(text=" Final Polycount: " + "{:,}".format(fpc))
            
            col.separator()
            col.separator()
            sub = col.row()
            sub.scale_y = 2.0
            sub.operator("wm.superpoke")
        
     
 
#----------#
# OPERATOR #
#----------#

class SuperPoke(bpy.types.Operator):
    # SuperPoke Operator
    bl_idname = "wm.superpoke"
    bl_label = "POKE THAT SHIT"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        spp = bpy.context.scene.sp_props

        off = spp.fl_poke_offset
        iter = spp.int_iterations
        keep = spp.bool_keep_original
        apply = spp.bool_apply_modifiers
        mult = spp.fl_poke_multiplier
        alt = spp.bool_poke_alternate
        keys = spp.bool_shape_keys 
        
        if keep:
            ori = bpy.context.active_object
            bpy.ops.object.duplicate(linked=False)
            ori.hide_viewport = True
            ori.hide_render = True
        
        if apply:
            bpy.ops.object.convert(target='MESH')
            
        me = bpy.context.object.data
            
        if keys:
            bpy.ops.object.shape_key_add(from_mix=True)
            
            for i in range(iter):        
                bpy.ops.object.shape_key_add(from_mix=True)
                
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(me) 
                
                for f in bm.faces:
                    f.select = True
                    
                bmesh.ops.poke(bm, faces=bm.faces, offset=off, use_relative_offset=True)
                bmesh.update_edit_mesh(me)

                if(alt): 
                    off *= -mult
                else:
                    off *= mult
                
                bpy.ops.object.mode_set(mode='OBJECT')            
                
        else:
            bm = bmesh.new()   # create an empty BMesh
            bm.from_mesh(me)   # fill it in from a Mesh
            
            for i in range(iter):                    
                bmesh.ops.poke(bm, faces=bm.faces, offset=off, use_relative_offset=True)
                
                if(alt): 
                    off *= -mult
                else:
                    off *= mult
                         
            bm.to_mesh(me) # write the bmesh back to mesh
            bm.free()
            me.update() # update obj in viewport
            
        return {'FINISHED'}



#----------#
# REGISTER #
#----------#

def register():
    bpy.utils.register_class(SuperPokePanel)
    bpy.utils.register_class(SuperPoke)
    bpy.utils.register_class(SuperPokeProps)
    bpy.types.Scene.sp_props = PointerProperty(type=SuperPokeProps)

def unregister():
    bpy.utils.unregister_class(SuperPokePanel)
    bpy.utils.unregister_class(SuperPoke)
    bpy.utils.unregister_class(SuperPokeProps)
    del bpy.types.Scene.sp_props

if __name__ == "__main__":
    register()