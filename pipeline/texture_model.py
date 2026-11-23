import bpy, math
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='/home/hatch/workspace/ju_mao_dagongji/3d/dafu_shape_v1.glb')
obj=[o for o in bpy.context.scene.objects if o.type=='MESH'][0]
bpy.context.view_layer.objects.active=obj
print('uv layers:', [l.name for l in obj.data.uv_layers])
# --- UV project from view: emulate front camera projection manually ---
# Compute bbox
mins=Vector((1e9,)*3); maxs=Vector((-1e9,)*3)
for c in obj.bound_box:
    w=obj.matrix_world @ Vector(c)
    mins=Vector(map(min,mins,w)); maxs=Vector(map(max,maxs,w))
size=maxs-mins
print('bbox:', tuple(round(s,2) for s in size), 'mins:', tuple(round(s,2) for s in mins))
# Front of character faces -Y (camera for 'front' render sat at -Y).
# Project: u from X, v from Z, matching the input photo framing.
# Photo (dafu_3d_bleed.jpg) framing: cat fills frame; use bbox with small margins.
mx=size.x*0.06; mz=size.z*0.04
uv_layer=obj.data.uv_layers.new(name='ProjUV')
mw=obj.matrix_world
for loop in obj.data.loops:
    v=obj.data.vertices[loop.vertex_index]
    w=mw @ v.co
    u=(w.x-(mins.x-mx))/(size.x+2*mx)
    vv=(w.z-(mins.z-mz))/(size.z+2*mz)
    uv_layer.data[loop.index].uv=(u*0.94+0.03, vv*0.93+0.07)
obj.data.uv_layers.active=uv_layer
# --- Materials: projected photo for front-facing faces, fur color for the rest ---
img=bpy.data.images.load('/home/hatch/workspace/refs_ascii/dafu_3d_bleed.jpg')
matF=bpy.data.materials.new('PhotoFront'); matF.use_nodes=True
bsdf=matF.node_tree.nodes['Principled BSDF']
tex=matF.node_tree.nodes.new('ShaderNodeTexImage'); tex.image=img
uvn=matF.node_tree.nodes.new('ShaderNodeUVMap'); uvn.uv_map='ProjUV'
matF.node_tree.links.new(uvn.outputs['UV'], tex.inputs['Vector'])
matF.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value=0.85
matB=bpy.data.materials.new('FurBack'); matB.use_nodes=True
b2=matB.node_tree.nodes['Principled BSDF']
b2.inputs['Base Color'].default_value=(0.87,0.52,0.22,1)
b2.inputs['Roughness'].default_value=0.95
obj.data.materials.clear(); obj.data.materials.append(matF); obj.data.materials.append(matB)
for p in obj.data.polygons:
    n=p.normal  # local space; glTF import keeps front toward -Y in world, local approx same
    p.material_index = 0 if n.y < -0.45 else 1
bpy.ops.wm.save_as_mainfile(filepath='/home/hatch/workspace/ju_mao_dagongji/3d/dafu_textured_v1.blend')
print('TEXTURED_SAVED')
