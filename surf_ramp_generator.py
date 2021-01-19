import bpy
import math
import bmesh
import os
import bpy.utils.previews

global custom_icons
custom_icons = bpy.utils.previews.new()
icons_dir = os.path.join(os.path.dirname(__file__), "icons")
custom_icons.load("view", os.path.join(icons_dir, "view.png"), "IMAGE")
custom_icons.load("add", os.path.join(icons_dir, "add.png"), "IMAGE")
custom_icons.load("name", os.path.join(icons_dir, "name.png"), "IMAGE")
custom_icons.load("slope_dimensions", os.path.join(icons_dir, "slope_dimensions.png"), "IMAGE")
custom_icons.load("ramp_properties", os.path.join(icons_dir, "ramp_properties.png"), "IMAGE")
custom_icons.load("wedge", os.path.join(icons_dir, "wedge.png"), "IMAGE")
custom_icons.load("thin", os.path.join(icons_dir, "thin.png"), "IMAGE")
custom_icons.load("thickness", os.path.join(icons_dir, "thickness.png"), "IMAGE")
custom_icons.load("left_surf", os.path.join(icons_dir, "left_surf.png"), "IMAGE")
custom_icons.load("right_surf", os.path.join(icons_dir, "right_surf.png"), "IMAGE")
custom_icons.load("both", os.path.join(icons_dir, "both.png"), "IMAGE")
custom_icons.load("left_ramp", os.path.join(icons_dir, "left_ramp.png"), "IMAGE")
custom_icons.load("right_ramp", os.path.join(icons_dir, "right_ramp.png"), "IMAGE")
custom_icons.load("down", os.path.join(icons_dir, "down.png"), "IMAGE")
custom_icons.load("up", os.path.join(icons_dir, "up.png"), "IMAGE")
custom_icons.load("arc", os.path.join(icons_dir, "arc.png"), "IMAGE")
custom_icons.load("dip", os.path.join(icons_dir, "dip.png"), "IMAGE")
custom_icons.load("smoothness", os.path.join(icons_dir, "smoothness.png"), "IMAGE")
custom_icons.load("angle", os.path.join(icons_dir, "angle.png"), "IMAGE")
custom_icons.load("size", os.path.join(icons_dir, "size.png"), "IMAGE")
custom_icons.load("uv_scale", os.path.join(icons_dir, "uv_scale.png"), "IMAGE")

class SURGE_MainPanel(bpy.types.Panel):
    bl_label = "Surf Ramp Generator"
    bl_idname = "SURGE_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SURGE'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("surge.increase_view", text= "Increase View Distance", icon_value = custom_icons["view"].icon_id)
        
        row = layout.row()
        row.operator("surge.generate_ramp", text= "Add New Ramp", icon_value = custom_icons["add"].icon_id)
        

class SURGE_GenerateRamp(bpy.types.Operator):
    bl_label = "Surf Ramp Generator"
    bl_idname = "surge.generate_ramp"
    bl_description = "Let's make a ramp"
    
    ramp_name : bpy.props.StringProperty (name= "", description = 'This is the name of the visible mesh (the physics mesh uses this name with _phys appended to the end)', default = 'ramp')
    material_name : bpy.props.StringProperty (name= "", description = 'This should match the name of your .vtf file', default = 'default')
    
    style_enum : bpy.props.EnumProperty(
        name = "",
        description = "Select a ramp style",
        items= [ 
        ('Wedge', "Wedge", "", custom_icons["wedge"].icon_id, 1),
        ('Thin', "Thin", "", custom_icons["thin"].icon_id, 2),
        ]
    )
    
    thickness : bpy.props.FloatProperty(name = 'Thickness:', description = 'Thickness of the ramp', default = 32, min = 1)
    
    surf_enum : bpy.props.EnumProperty(
        name = "",
        description = "Select a surf direction",
        items= [ 
        ('Left', "Left", "Creates a ramp where you strafe left to surf along it.", custom_icons["left_surf"].icon_id, 1),
        ('Right', "Right", "Creates a ramp where you strafe right to surf along it.", custom_icons["right_surf"].icon_id, 2),
        ('Both', "Both", "Creates a ramp where you can surf both sides.", custom_icons["both"].icon_id, 3) 
        ]
    )
    
    ramp_enum : bpy.props.EnumProperty(
        name = "",
        description = "Select a ramp direction",
        items= [ 
        ('Left', "Left", "Creates a ramp that turns left", custom_icons["left_ramp"].icon_id, 1),
        ('Right', "Right", "Creates a ramp that turns right", custom_icons["right_ramp"].icon_id, 2),
        ('Up', "Up", "Creates a ramp that turns upwards", custom_icons["up"].icon_id, 3),
        ('Down', "Down", "Creates a ramp that turns downwards", custom_icons["down"].icon_id, 4),
        ('Dip', "Dip", "Creates a u shaped ramp", custom_icons["dip"].icon_id, 5),
        ('Arc', "Arc", "Creates an n shaped ramp", custom_icons["arc"].icon_id, 6),
        ]
    )
    
    width : bpy.props.FloatProperty(name = 'Width:', description = '', default = 256, min = 64)
    height : bpy.props.FloatProperty(name = 'Height:', description = '', default = 320, min = 64)
    smoothness : bpy.props.IntProperty(name = '', description = 'Number of segments in the ramp. Keep this to a sensible value, you can achieve the same experience with less smoothness', default = 16 , min = 3, max = 64)
    angle : bpy.props.FloatProperty(name = '', description = 'Angle of the ramp', default = 90, min = 0, max = 360)
    size : bpy.props.FloatProperty(name= '', description = 'Size of the ramp', default = 1024, min = 0)
    uv_scale : bpy.props.FloatProperty(name= '', description = 'Scale of the UV maps', default = 0.25, min = 0.05, max = 10, step = 5)
    
    cursor_start : bpy.props.FloatVectorProperty(name = "CursorStart", default = (0, 0 ,0))
   
    def draw (self, context):
        layout = self.layout
        
        layout.label(text = "Names", icon_value = custom_icons["name"].icon_id)
        
        box = layout.box()
        row = box.row()
        row.label(text = "Ramp Name:")
        row.prop(self, 'ramp_name')
        
        row = box.row()
        row.label(text = "Material Name:")
        row.prop(self, 'material_name')

        layout.label(text = "Slope Dimensions", icon_value = custom_icons["slope_dimensions"].icon_id)
        box = layout.box()
        row = box.row(align=True)
        row.prop(self, "width")
        row.prop(self, "height")

        layout.label(text = "Ramp Properties", icon_value = custom_icons["ramp_properties"].icon_id)
        
        box = layout.box()
        row = box.row()
        row.label(text = "Ramp Style:")
        row.prop(self,"style_enum")
        if self.style_enum == 'Thin':
            row = box.row()
            row.label(text = "Thickness:", icon_value = custom_icons["thickness"].icon_id)
            row.prop(self, "thickness")
        
        row = box.row()
        row.label(text = "Surf Direction:")
        row.prop(self,"surf_enum")
        
        row = box.row()
        row.label(text = "Ramp Direction:")
        row.prop(self,"ramp_enum")
        
        row = box.row()
        row.label(text = "Smoothness:", icon_value = custom_icons["smoothness"].icon_id)
        row.prop(self, "smoothness")
        
        row = box.row()
        row.label(text = "Angle:", icon_value = custom_icons["angle"].icon_id)
        row.prop(self, "angle")
        
        row = box.row()
        row.label(text = "Size:", icon_value = custom_icons["size"].icon_id)
        row.prop(self, "size")
        
        row = box.row()
        row.label(text = "UV Scale:", icon_value = custom_icons["uv_scale"].icon_id)
        row.prop(self, "uv_scale")

    def execute(self, context):
        
#------------------------------------------------------------------------------------------------------
        # Creating the visible mesh.
#------------------------------------------------------------------------------------------------------

        # If we're in edit mode, switch.
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
        
        w = self.width
        
        if self.surf_enum == 'Both':
            w = self.width * 2
         
        # Add a plane, rotate it and select the top edge.
        self.cursor_start = bpy.context.scene.cursor.location
        bpy.ops.mesh.primitive_plane_add(size=w, enter_editmode=False, location=(0, 0, 0))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        obj = bpy.context.active_object
        obj.name = 'SURGEMesh'
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.editmode_toggle()
        obj.data.edges[0].select = True
        bpy.ops.object.editmode_toggle()
    
        # Move the top edge to the correct height and move the entire plane up so that the origin is correct.
        bpy.ops.transform.translate(value=(0, 0, self.height - w), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0, 0, w / 2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.editmode_toggle()
        
        # If the ramp is double sided, select the top edge and merge at center.
        if self.surf_enum == 'Both':
            obj.data.edges[0].select = True
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.merge(type='CENTER')
        # If the ramp is single sided, create slope shape by merging the top vertices depending on the slope direction.
        elif self.surf_enum == 'Left':
                obj.data.vertices[0].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.view3d.snap_cursor_to_selected()
                bpy.ops.object.editmode_toggle()
                obj.data.vertices[2].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.merge(type='CURSOR')
        elif self.surf_enum == 'Right':
                obj.data.vertices[2].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.view3d.snap_cursor_to_selected()
                bpy.ops.object.editmode_toggle()
                obj.data.vertices[0].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.merge(type='CURSOR')
          
        # If the ramp is thin, delete the redundant edges.     
        if self.style_enum == 'Thin':
            if self.surf_enum == 'Both':
                bpy.ops.mesh.select_all(action = 'DESELECT')
                bpy.ops.object.editmode_toggle()
                obj.data.edges[1].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.delete(type='EDGE')
            elif self.surf_enum == 'Left':
                bpy.ops.object.editmode_toggle()
                obj.data.edges[0].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.delete(type='EDGE')
                bpy.ops.object.editmode_toggle()
                obj.data.edges[0].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.delete(type='EDGE')
            else:
                bpy.ops.mesh.select_all(action = 'DESELECT')
                bpy.ops.object.editmode_toggle()
                obj.data.edges[1].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.delete(type='EDGE')
                bpy.ops.object.editmode_toggle()
                obj.data.edges[1].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.delete(type='EDGE')
                       
        # Prepare for the spin tool - snap the cursor back to the center and delete only the faces of the plane.
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Spin the edges into the correct shape depending on ramp type.
        if self.ramp_enum == 'Right':
            bpy.ops.mesh.spin(steps=self.smoothness, dupli=False, angle=self.angle * math.pi / 180, use_auto_merge=True, use_normal_flip=False, center=(0, self.size, 0), axis=(0.0, 0.0, 1))
        elif self.ramp_enum == 'Left':
            bpy.ops.mesh.spin(steps=self.smoothness, dupli=False, angle=-self.angle * math.pi / 180, use_auto_merge=True, use_normal_flip=False, center=(0, -self.size, 0), axis=(0.0, 0.0, 1))
        elif self.ramp_enum == 'Down' or self.ramp_enum == 'Arc':
            bpy.ops.mesh.spin(steps=self.smoothness, dupli=False, angle=-self.angle * math.pi / 180, use_auto_merge=True, use_normal_flip=False, center=(0, 0, -self.size), axis=(0.0, -1, 0.0))
        elif self.ramp_enum == 'Up' or self.ramp_enum == 'Dip':
            bpy.ops.mesh.spin(steps=self.smoothness, dupli=False, angle=self.angle * math.pi / 180, use_auto_merge=True, use_normal_flip=False, center=(0, 0, self.size + self.height), axis=(0.0, -1, 0))
         
        # If the ramp is thin, add the solidify modifier.
        if self.style_enum != 'Wedge':
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].thickness = self.thickness
            bpy.context.object.modifiers["Solidify"].offset = 1
            bpy.context.object.modifiers["Solidify"].use_even_offset = True
            bpy.context.object.modifiers["Solidify"].use_quality_normals = True
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.modifier_apply(modifier="Solidify")
            bpy.ops.object.editmode_toggle()
      
        # If ramp is an Arc or a Dip, move into correct position and rotation.
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.editmode_toggle()

        faces = len(obj.data.polygons)
        vertices = len(obj.data.vertices) 
        edges = len(obj.data.edges)
        
        if self.ramp_enum == 'Arc' or self.ramp_enum == 'Dip':
            if self.style_enum == 'Wedge':
                if (self.smoothness % 2) == 0:
                    obj.data.edges[faces - 2].select = True
                else:
                    obj.data.polygons[int((faces-1) / 2)].select = True
            else:
                if (self.smoothness % 2) == 0:
                    if self.surf_enum != 'Both':
                        obj.data.vertices[(vertices - self.smoothness) - 1].select = True
                    else:
                        obj.data.vertices[int(faces - faces / 4)].select = True
                else:
                    if self.surf_enum == 'Left':
                        obj.data.edges[int((edges + self.smoothness + 1) / 2)].select = True
                    elif self.surf_enum == 'Right':
                        obj.data.edges[int((edges + self.smoothness) / 2)].select = True
                    else:
                        obj.data.edges[int((faces + self.smoothness) + self.smoothness / 2)].select = True
                        
                     
            bpy.ops.object.editmode_toggle() 
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            bpy.ops.view3d.snap_cursor_to_center()
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
        
        if self.ramp_enum == 'Arc':
            bpy.ops.transform.rotate(value=self.angle / 2 * math.pi /180, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        elif self.ramp_enum == 'Dip':
            bpy.ops.transform.rotate(value=-self.angle / 2 * math.pi /180, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        
        
        if self.style_enum == 'Thin': 
            if self.ramp_enum == 'Arc' or self.ramp_enum == 'Dip':
                if self.surf_enum == 'Left':
                    bpy.ops.transform.translate(value=(0, self.width / 2, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                elif self.surf_enum == 'Right':
                    bpy.ops.transform.translate(value=(0, -self.width / 2, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                else:
                    bpy.ops.transform.translate(value=(0, 0, self.height), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
   
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')                 
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Finish the visible mesh by adding the end caps and shading smooth.
        if self.angle != 360:
            if self.style_enum == 'Wedge':  
                bpy.ops.mesh.edge_face_add()
        
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()                
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 0.785398
        bpy.context.scene.cursor.location = self.cursor_start
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
        
#------------------------------------------------------------------------------------------------------
        # Creating the physics mesh.
#------------------------------------------------------------------------------------------------------ 
        
        # Duplicate the visible mesh.
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        obj = bpy.context.active_object
        bpy.ops.object.editmode_toggle()
        bpy.context.object.data.use_auto_smooth = False
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.editmode_toggle()
        
        # Select every other face on the mesh.
        # Wedge.
        if self.style_enum == 'Wedge':
            n = 6
            for face in range(faces):
                if face % n == 3 or face % n == 4 or face % n == 5:
                    obj.data.polygons[face].select = True    
            
            # Not looping, even ramp - add the last face.                           
            if self.angle != 360:
                if self.smoothness % 2 == 0:
                    obj.data.polygons[(self.smoothness * 3) + 1].select = True
            
            # Looping, odd ramp - separate odd piece.        
            else:
                if self.smoothness % 2 != 0:
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.separate(type = 'SELECTED')  
                    bpy.ops.object.editmode_toggle()
                    obj.data.polygons[len(obj.data.polygons) - 1].select = True
                    obj.data.polygons[len(obj.data.polygons) - 2].select = True
                    obj.data.polygons[len(obj.data.polygons) - 3].select = True               
   
            # With correct faces selected, separate and add faces.
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.separate(type = 'SELECTED')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()
            
            # If an odd loop, select the odd section.
            if self.angle == 360 and self.smoothness % 2 != 0:
                obj = bpy.context.scene.objects["SURGEMesh.003"]
            else:
                obj = bpy.context.scene.objects["SURGEMesh.002"]
                
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = obj 
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()

            # Join the objects together and name them using ramp_name.
            for ob in bpy.data.objects:
                if ob.name in ("SURGEMesh.001","SURGEMesh.002","SURGEMesh.003"):
                    ob.select_set(True) 
            bpy.ops.object.join()
            bpy.ops.object.editmode_toggle()
            obj.name = self.ramp_name+'_phys'
            obj = bpy.context.scene.objects["SURGEMesh"]
            obj.name = self.ramp_name
            obj.select_set(True)      

        # Thin.
        else:
            # Select every other face on the mesh.
            # Not looping.
            if self.angle != 360: 
                if self.surf_enum != 'Both':
                    obj.data.edges[2].select = True
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.loop_multi_select(ring=False)
                    bpy.ops.mesh.select_mode(type="EDGE")
                else:
                    obj.data.edges[5].select = True
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.loop_multi_select(ring=False)
                    bpy.ops.mesh.select_mode(type="EDGE")
            
                # Not looping, even.
                if (self.smoothness % 2) == 0:
                    bpy.ops.mesh.select_nth(skip=1, nth=1, offset=0)
                # Not looping, odd.
                else:
                    bpy.ops.mesh.select_nth(skip=1, nth=1, offset=1)
                    
            # Not looping
            if self.angle != 360:
                bpy.ops.object.editmode_toggle()
                if self.surf_enum != 'Both':
                    obj.data.edges[1].select = True
                    obj.data.edges[len(obj.data.edges) - (self.smoothness * 2)].select = True
                else:
                    obj.data.edges[1].select = True
                    obj.data.edges[2].select = True
                    obj.data.edges[len(obj.data.edges) - 1].select = True
                
            # Looping
            else:
                if self.surf_enum != 'Both':
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_mode(type="EDGE")
                    bpy.ops.object.editmode_toggle()
                    obj.data.edges[0].select = True
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.loop_multi_select(ring=False)
                else:
                    obj.data.edges[0].select = True
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.loop_multi_select(ring=False)           
            
            # Not looping
            if self.angle != 360:
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.loop_multi_select(ring=True)
            else:
                bpy.ops.mesh.loop_multi_select(ring=True)
                bpy.ops.mesh.loop_to_region(select_bigger=False)
            
            # Separate.
            bpy.ops.mesh.separate(type = 'SELECTED')
           
            if self.angle != 360:
                # Even ramps, not looping.
                if (self.smoothness % 2) == 0:
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.object.select_all(action='DESELECT')
                    obj = bpy.context.scene.objects["SURGEMesh.002"]
                    bpy.context.view_layer.objects.active = obj
                    # Select extra face and delete.
                    if self.surf_enum != 'Both':
                        obj.data.polygons[self.smoothness].select = True
                    else:
                        obj.data.polygons[self.smoothness * 2].select = True
                        obj.data.polygons[(self.smoothness * 2) + 1].select = True
                        obj.data.polygons[self.smoothness * 3].select = True
                        obj.data.polygons[(self.smoothness * 3) + 1].select = True
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.delete(type='FACE')
                    bpy.ops.mesh.select_all(action='SELECT')
            else:
                # Odd ramps, looping.
                if (self.smoothness % 2) != 0:
                    bpy.ops.object.editmode_toggle()                  
                    bpy.ops.object.select_all(action='DESELECT')
                    obj = bpy.context.scene.objects["SURGEMesh.002"]
                    bpy.context.view_layer.objects.active = obj
                    if self.surf_enum != 'Both':
                        obj.data.polygons[self.smoothness].select = True
                        obj.data.polygons[int((self.smoothness) / 2)].select = True
                        obj.data.polygons[self.smoothness * 2].select = True
                        obj.data.polygons[(self.smoothness * 2) + 1].select = True
                    else:
                        obj.data.polygons[self.smoothness].select = True
                        obj.data.polygons[self.smoothness - 1].select = True
                        obj.data.polygons[self.smoothness * 2].select = True
                        obj.data.polygons[(self.smoothness * 2) + 1].select = True
                        obj.data.polygons[(self.smoothness * 3) + 1].select = True
                        obj.data.polygons[(self.smoothness * 3) + 2].select = True
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.separate(type = 'SELECTED')

            # Add faces in between.
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            
            if self.angle != 360:
                # Not looping
                obj = bpy.context.scene.objects["SURGEMesh.001"]
            else:
                # Looping
                obj = bpy.context.scene.objects["SURGEMesh.002"]
                
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
 
            # Even.
            if (self.smoothness % 2) == 0:
                bpy.ops.mesh.edge_face_add()    
                bpy.ops.object.editmode_toggle()
            else:
                # Odd, not looping.
                if self.angle != 360:
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.object.select_all(action='DESELECT')
                    obj = bpy.context.scene.objects["SURGEMesh.002"]
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.edge_face_add()
                    bpy.ops.object.editmode_toggle()
                # Odd, looping.
                else:
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.object.select_all(action='DESELECT')
                    obj = bpy.context.scene.objects["SURGEMesh.001"]
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.edge_face_add()
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.object.select_all(action='DESELECT')
                    obj = bpy.context.scene.objects["SURGEMesh.003"]
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.edge_face_add()
                    bpy.ops.object.editmode_toggle()
                
            # Select and join together.
            for ob in bpy.data.objects:
                if ob.name in ("SURGEMesh.001","SURGEMesh.002","SURGEMesh.003"):
                    ob.select_set(True) 

            bpy.ops.object.join()
            bpy.ops.object.editmode_toggle()
            obj.name = self.ramp_name+'_phys'
            obj = bpy.context.scene.objects["SURGEMesh"]
            obj.name = self.ramp_name
            obj.select_set(True)
                   
#------------------------------------------------------------------------------------------------------
        # Adding / creating the material.
#------------------------------------------------------------------------------------------------------                                             
        
        name = self.material_name
        
        # Check whether the material already exists.
        if self.material_name in bpy.data.materials:
            obj.active_material = bpy.data.materials[name]
        # If it doesn't, make one and assign it to the visible mesh.
        else:
            obj.active_material = bpy.data.materials.new(name = self.material_name) 

#------------------------------------------------------------------------------------------------------
        # UV Unwrap
#------------------------------------------------------------------------------------------------------   
     
        # Reset UV maps.
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.editmode_toggle()  
        bpy.ops.uv.reset()
        bpy.ops.mesh.select_all(action = 'DESELECT') 
         
        # Select what our first face will be for Follow Active Quads and rotate it correctly.
        bpy.ops.object.editmode_toggle()
        
        selected_face = 0
        
        if self.style_enum == 'Wedge':
            if self.surf_enum != 'Right':
                obj.data.polygons[selected_face].select = True
            else:
                selected_face = 2
                obj.data.polygons[selected_face].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.uvs_rotate(use_ccw=False)
                bpy.ops.mesh.uvs_rotate(use_ccw=False)
                bpy.ops.object.editmode_toggle()
        else:
            if self.surf_enum != 'Both':
                selected_face = self.smoothness
                obj.data.polygons[selected_face].select = True
                if self.surf_enum == 'Right':
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.uvs_rotate(use_ccw=False)
                    bpy.ops.mesh.uvs_rotate(use_ccw=False)
                    bpy.ops.object.editmode_toggle()
            else:
                selected_face = self.smoothness * 2
                obj.data.polygons[selected_face].select = True
 
        bpy.ops.object.editmode_toggle()

        # Select all the faces and turn our first face into the active face for UV Unwrap - Follow Active Quads.
        bm = bmesh.from_edit_mesh(obj.data)

        for face in bm.faces:
            face.select = True

        bm.faces.ensure_lookup_table()
        bm.faces.active = bm.faces[selected_face]  
        bm.faces.active.select = True 
        bpy.ops.uv.follow_active_quads(mode='EVEN')
    
        # Select the faces which are upside down and rotate them.
        bpy.ops.mesh.select_all(action = 'DESELECT') 
        bpy.ops.object.editmode_toggle()
        
        if self.style_enum == 'Wedge':
            if self.surf_enum != 'Right':
                obj.data.polygons[2].select = True
            else:
                obj.data.polygons[0].select = True  
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_similar(type='AREA', threshold=1)         
        else:
            if self.surf_enum != 'Both':
                for face in range(0, self.smoothness):
                    obj.data.polygons[face].select = True
            else:
                for face in range(0, (self.smoothness * 2) - 1):
                    n = 2
                    if face % n != 1:
                        obj.data.polygons[face].select = True      
                for face in range(self.smoothness * 2, self.smoothness * 4):
                    n = 2 
                    if face % n == 1:       
                        obj.data.polygons[face].select = True
            bpy.ops.object.editmode_toggle() 
    

        original_area = bpy.context.area.type            
        bpy.context.area.type = 'IMAGE_EDITOR'
        bpy.context.area.ui_type = 'UV'
        bpy.ops.mesh.reveal()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.context.space_data.pivot_point = 'CENTER'
        bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.area.type = original_area
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.editmode_toggle() 
        
        # Move and rotate the end cap UVs into the correct positions.
        if self.style_enum == 'Wedge':
            if self.angle != 360:
                obj.data.polygons[self.smoothness * 3].select = True
                obj.data.polygons[(self.smoothness * 3) + 1].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.uvs_rotate(use_ccw=False)
                bpy.ops.object.editmode_toggle()

                vertices = faces * 4
                print (vertices)

                mesh = obj.data
                bm = bmesh.new()
                bm.from_mesh(mesh)
                uv_layer = bm.loops.layers.uv.active
                   
                for face in bm.faces:
                    for vert in face.loops:
                        if self.surf_enum == 'Both':
                            if vert.index == vertices+2:
                                vert1 = vert[bm.loops.layers.uv.active]
                            if vert.index == vertices+5:
                                vert2 = vert[bm.loops.layers.uv.active]
                        else:
                            if vert.index == vertices:
                                vert1 = vert[bm.loops.layers.uv.active]
                            if vert.index == vertices+3:
                                vert2 = vert[bm.loops.layers.uv.active]

                if self.surf_enum == 'Both':
                    vert1.uv.x = vert1.uv.x + 1 
                    vert2.uv.x = vert2.uv.x + 1
                else:
                    if self.surf_enum == 'Left':
                        vert1.uv.x = vert1.uv.x - 1
                    else: 
                        vert2.uv.x = vert2.uv.x - 1 
                    
                bm.to_mesh(mesh)
        
            if self.surf_enum == 'Both':
                if self.angle != 360:
                    obj.data.polygons[faces].select = True
                    obj.data.polygons[faces+1].select = True
                    
                    original_area = bpy.context.area.type
                    bpy.context.area.type = 'IMAGE_EDITOR'
                    bpy.context.area.ui_type = 'UV'
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.reveal()
                    bpy.ops.uv.select_all(action='SELECT')
                    bpy.ops.transform.translate(value=(-0.5, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

                    bpy.context.area.type = original_area
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    bpy.ops.object.editmode_toggle()  
        # Thin.    
        else:
            if self.angle != 360:
                if self.surf_enum != 'Both':
                    obj.data.polygons[self.smoothness * 2].select = True
                    bpy.ops.object.editmode_toggle()
                    
                    if self.surf_enum == 'Left':
                        original_area = bpy.context.area.type
                        bpy.context.area.type = 'IMAGE_EDITOR'
                        bpy.context.area.ui_type = 'UV'
                        bpy.ops.mesh.reveal()
                        bpy.ops.uv.select_all(action='SELECT')
                        bpy.context.space_data.pivot_point = 'CENTER'
                        bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.resize(value=(1, 0.125, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.translate(value=(0, 0.4375, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.context.area.type = original_area
                        bpy.ops.mesh.select_all(action = 'DESELECT')
                        bpy.ops.object.editmode_toggle()
                    else:
                        original_area = bpy.context.area.type
                        bpy.context.area.type = 'IMAGE_EDITOR'
                        bpy.context.area.ui_type = 'UV'
                        bpy.ops.mesh.reveal()
                        bpy.ops.uv.select_all(action='SELECT')
                        bpy.context.space_data.pivot_point = 'CENTER'
                        bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.resize(value=(1, 0.125, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.translate(value=(0, 0.4375, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.context.area.type = original_area
                        bpy.ops.mesh.select_all(action = 'DESELECT')
                        bpy.ops.object.editmode_toggle()
                    
                    bpy.ops.object.editmode_toggle()   
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    bpy.ops.object.editmode_toggle()
                    obj.data.polygons[(self.smoothness * 4) - 1].select = True
                    bpy.ops.object.editmode_toggle()
                    
                    if self.surf_enum == 'Left':
                        original_area = bpy.context.area.type
                        bpy.context.area.type = 'IMAGE_EDITOR'
                        bpy.context.area.ui_type = 'UV'
                        bpy.ops.mesh.reveal()
                        bpy.ops.uv.select_all(action='SELECT')
                        bpy.context.space_data.pivot_point = 'CENTER'
                        bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.resize(value=(1, 0.125, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.translate(value=(0, 0.4375, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.context.area.type = original_area
                        bpy.ops.mesh.select_all(action = 'DESELECT')
                        bpy.ops.object.editmode_toggle()
                    else:
                        original_area = bpy.context.area.type
                        bpy.context.area.type = 'IMAGE_EDITOR'
                        bpy.context.area.ui_type = 'UV'
                        bpy.ops.mesh.reveal()
                        bpy.ops.uv.select_all(action='SELECT')
                        bpy.context.space_data.pivot_point = 'CENTER'
                        bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.resize(value=(1, 0.125, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.translate(value=(0, 0.4375, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.context.area.type = original_area
                        bpy.ops.mesh.select_all(action = 'DESELECT')
                        bpy.ops.object.editmode_toggle()
                     
                    bpy.ops.object.editmode_toggle()    
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    bpy.ops.object.editmode_toggle()
                else:
                    obj.data.polygons[self.smoothness * 4].select = True
                    obj.data.polygons[(self.smoothness * 4) + 1].select = True
                    bpy.ops.object.editmode_toggle()
                    
                    original_area = bpy.context.area.type
                    bpy.context.area.type = 'IMAGE_EDITOR'
                    bpy.context.area.ui_type = 'UV'
                    bpy.ops.mesh.reveal()
                    bpy.ops.uv.select_all(action='SELECT')
                    bpy.context.space_data.pivot_point = 'CENTER'
                    bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    bpy.ops.transform.resize(value=(1, 0.125, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    bpy.ops.transform.translate(value=(1.5, -0.0625, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    bpy.context.area.type = original_area
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    bpy.ops.object.editmode_toggle()

                    obj.data.polygons[self.smoothness * 6].select = True
                    obj.data.polygons[(self.smoothness * 6) + 1].select = True
                    bpy.ops.object.editmode_toggle()
                    
                    original_area = bpy.context.area.type
                    bpy.context.area.type = 'IMAGE_EDITOR'
                    bpy.context.area.ui_type = 'UV'
                    bpy.ops.mesh.reveal()
                    bpy.ops.uv.select_all(action='SELECT')
                    bpy.context.space_data.pivot_point = 'CENTER'
                    bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    bpy.ops.transform.resize(value=(1, 0.125, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    bpy.ops.transform.translate(value=(0.5, -0.0625, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
 
                    bpy.context.area.type = original_area
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    bpy.ops.object.editmode_toggle()

                if self.surf_enum == 'Left':
                    obj.data.polygons[(self.smoothness * 2) + 2].select = True
                    obj.data.polygons[(self.smoothness * 4) + 1].select = True
                elif self.surf_enum == 'Right':
                    obj.data.polygons[(self.smoothness * 2) + 1].select = True
                    obj.data.polygons[self.smoothness * 4].select = True
                else:
                    obj.data.polygons[self.smoothness * 4 + 2].select = True
                    obj.data.polygons[self.smoothness * 6 + 2].select = True 
                
                bpy.ops.object.editmode_toggle()    
                bpy.ops.mesh.select_mode(type="FACE")
                bpy.ops.mesh.shortest_path_select(edge_mode='SELECT')
                    
            else:
                if self.surf_enum == 'Left':
                    obj.data.polygons[(self.smoothness * 4) - 1].select = True
                elif self.surf_enum == 'Right':
                    obj.data.polygons[self.smoothness * 2].select = True
                else:
                    obj.data.polygons[(self.smoothness * 4) + 2].select = True
                    
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_mode(type="FACE")
                bpy.ops.mesh.select_similar(type='AREA', compare='EQUAL', threshold=1)

            original_area = bpy.context.area.type
            bpy.context.area.type = 'IMAGE_EDITOR'
            bpy.context.area.ui_type = 'UV'
            bpy.ops.mesh.reveal()
            bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(1, 0.125, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.transform.translate(value=(0, 1, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.context.area.type = original_area
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.editmode_toggle()
            
            if self.angle != 360:
                if self.surf_enum == 'Left':
                    obj.data.polygons[(self.smoothness * 2) + 1].select = True
                    obj.data.polygons[self.smoothness * 4].select = True 
                elif self.surf_enum == 'Right':
                    obj.data.polygons[(self.smoothness * 4) + 1].select = True
                    obj.data.polygons[(self.smoothness * 2) + 2].select = True
                else:
                    obj.data.polygons[(self.smoothness * 6) + 3].select = True
                    obj.data.polygons[(self.smoothness * 4) + 3].select = True

                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_mode(type="FACE")
                bpy.ops.mesh.shortest_path_select(edge_mode='SELECT')
            else:
                if self.surf_enum == 'Left':
                    obj.data.polygons[self.smoothness * 2].select = True
                elif self.surf_enum == 'Right':
                    obj.data.polygons[(self.smoothness * 2) + 1].select = True
                else:
                    obj.data.polygons[(self.smoothness * 4) + 1].select = True

                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_mode(type="FACE")
                bpy.ops.mesh.select_similar(type='AREA', compare='EQUAL', threshold=1)
            
            original_area = bpy.context.area.type
            bpy.context.area.type = 'IMAGE_EDITOR'
            bpy.context.area.ui_type = 'UV'
            bpy.ops.mesh.reveal()
            bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CENTER'
            bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.transform.resize(value=(1, 0.125, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.transform.translate(value=(0, -0.5625, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.context.area.type = original_area

        # Select all of the relevant faces and scale to the uv_scale.
        if self.style_enum == 'Wedge':
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.object.editmode_toggle()
            
            if self.angle != 360:
                obj.data.polygons[self.smoothness * 3].select = False
                obj.data.polygons[(self.smoothness * 3) + 1].select = False 
        else:
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.object.editmode_toggle()
            if self.angle != 360:
                if self.surf_enum != 'Both':
                    obj.data.polygons[self.smoothness * 2].select = False
                    obj.data.polygons[(self.smoothness * 4) - 1].select = False
                else:
                    obj.data.polygons[self.smoothness * 4].select = False
                    obj.data.polygons[(self.smoothness * 4) + 1].select = False
                    obj.data.polygons[self.smoothness * 6].select = False
                    obj.data.polygons[(self.smoothness * 6) + 1].select = False
   
        original_area = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'
        bpy.context.area.ui_type = 'UV'
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.reveal()
        bpy.ops.uv.select_all(action='SELECT')
        if self.surf_enum == 'Right':
            bpy.context.space_data.cursor_location[0] = 1
        else:
            bpy.context.space_data.cursor_location[0] = 0
        bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.ops.transform.resize(value=(self.uv_scale, 1, 1), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.area.type = original_area
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

    def invoke (self, context, event):
        return context.window_manager.invoke_props_dialog(self)
       
    
class SURGE_IncreaseView(bpy.types.Operator):
    bl_label = "Increase View Distance"
    bl_idname = "surge.increase_view"
    bl_description = "Increases the 3D View far clipping distance"

    def execute(self, context):
        bpy.context.space_data.clip_start = 10
        bpy.context.space_data.clip_end = 50000

        return {'FINISHED'}
    
    
def register():
    bpy.utils.register_class(SURGE_MainPanel)
    bpy.utils.register_class(SURGE_GenerateRamp)
    bpy.utils.register_class(SURGE_IncreaseView)

def unregister():
    bpy.utils.unregister_class(SURGE_MainPanel)
    bpy.utils.unregister_class(SURGE_GenerateRamp)
    bpy.utils.unregister_class(SURGE_IncreaseView)

if __name__ == "__main__":
    register()