bl_info = {
    'name': 'Vertex Counter',
    'author': 'curly-brace',
    'location': 'Properties Panel',
    'description': 'Shows a REAL vertex count',
    'category': 'System',
}

import bpy
import bmesh
from bpy.props import BoolProperty
from operator import itemgetter

class VertexCounterPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    active_only = BoolProperty(name='Active',
                        description='Display info only for active object',
                        default=True)
    show_polys = BoolProperty(name='Polys',
                        description='Display info about poly(tri) count',
                        default=True)
    count_uvs = BoolProperty(name='UVs',
                        description='Count additional vertices made by uv seams',
                        default=True)

class VertexCounter(bpy.types.Panel):
    bl_label = 'Vertex Counter'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'scene'

    def draw(self, context):
        prefs = bpy.context.user_preferences.addons[__name__].preferences
        layout = self.layout

        row = layout.row()
        row.column().row().prop(prefs, 'active_only')
        row.column().row().prop(prefs, 'show_polys')
        row.column().row().prop(prefs, 'count_uvs')

        row = layout.row()
        meshes = []
        if prefs.active_only:
            if context.object is not None and context.object.type == 'MESH':
                row.label('active object', icon='OBJECT_DATA')
                meshes = [context.object]
            else:
                row.label('no meshes found', icon='X')
        else:
            meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
            row.label(text=str(len(meshes)) + ' mesh(es) found', icon='VIEWZOOM')

        if len(meshes) > 0:
            cols = []
            row = layout.row()
            if not prefs.active_only:
                cols.append(row.column())
            cols.append(row.column())
            if prefs.show_polys:
                cols.append(row.column())

            if prefs.active_only:
                cols[0].row().label(text='Verts/Total')
                if prefs.show_polys:
                    cols[1].row().label(text='Polys/Tris')
            else:
                cols[0].row().label(text='Name')
                cols[1].row().label(text='Verts/Total')
                if prefs.show_polys:
                    cols[2].row().label(text='Polys/Tris')

            for m in meshes:
                me = m.to_mesh(context.scene, apply_modifiers=True, settings='RENDER')

                bm = bmesh.new()
                bm.from_mesh(me)
                bmesh.ops.triangulate(bm, faces=bm.faces)
                bm.to_mesh(me)

                me.calc_normals()
                me.calc_normals_split()
                me.calc_tessface()

                smooth_verts = []
                flat_verts = 0
                total_verts = 0
                for p in me.polygons:
                    if p.use_smooth:
                        for v in p.vertices:
                            if not v in smooth_verts:
                                smooth_verts.append(v)
                                total_verts += 3
                    else:
                        flat_verts += 3
                        total_verts += 3

                uv_loops = []

                for uv_layer in me.uv_layers:
                    for v in uv_layer.data.values():
                        uv_loop = '{0},{1}'.format(*v.uv)
                        if not uv_loop in uv_loops:
                            uv_loops.append(uv_loop)

                if prefs.count_uvs and len(uv_loops) > 0:
                    flat_verts += len(uv_loops) - len(me.vertices)

                real_verts =  len(smooth_verts) + flat_verts
                vert_text = '{0}/{1}'.format(real_verts, total_verts)
                poly_text = '{0}/{1}'.format(len(m.data.polygons), len(me.polygons))

                if prefs.active_only:
                    cols[0].row().label(text=vert_text)
                    if prefs.show_polys:
                        cols[1].row().label(text=poly_text)
                else:
                    cols[0].row().label(text=m.name)
                    cols[1].row().label(text=vert_text)
                    if prefs.show_polys:
                        cols[2].row().label(text=poly_text)

                bpy.data.meshes.remove(me)

def register():
    bpy.utils.register_class(VertexCounterPreferences)
    bpy.utils.register_class(VertexCounter)

def unregister():
    bpy.utils.unregister_class(VertexCounterPreferences)
    bpy.utils.unregister_class(VertexCounter)

if __name__ == '__main__':
    register()
