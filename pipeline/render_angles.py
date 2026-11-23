import bpy, math, os
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='/home/hatch/workspace/ju_mao_dagongji/3d/dafu_shape_v1.glb')
objs=[o for o in bpy.context.scene.objects if o.type=='MESH']
print('meshes:', [(o.name, len(o.data.polygons)) for o in objs])
mins=Vector((1e9,)*3); maxs=Vector((-1e9,)*3)
for o in objs:
    for c in o.bound_box:
        w=o.matrix_world @ Vector(c)
        mins=Vector(map(min,mins,w)); maxs=Vector(map(max,maxs,w))
center=(mins+maxs)/2; size=maxs-mins; R=max(size)*1.9
print('bbox size:', tuple(round(s,2) for s in size))
mat = bpy.data.materials.new('clay'); mat.use_nodes=True
mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(0.85,0.55,0.3,1)
mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=0.9
for o in objs: o.data.materials.clear(); o.data.materials.append(mat)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=16
scene.cycles.device='CPU'
scene.world=bpy.data.worlds.new('w'); scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0.9,0.9,0.9,1)
scene.render.resolution_x=440; scene.render.resolution_y=440
cam_data=bpy.data.cameras.new('c'); cam=bpy.data.objects.new('cam',cam_data)
scene.collection.objects.link(cam); scene.camera=cam
sun_data=bpy.data.lights.new('s','SUN'); sun=bpy.data.objects.new('sun',sun_data)
scene.collection.objects.link(sun); sun.rotation_euler=(0.8,0.2,0.6)
outdir='/home/hatch/workspace/ju_mao_dagongji/3d/angles'
for name,ang in [('front',0),('q34',40),('side',90),('back',180)]:
    a=math.radians(ang)
    cam.location=center+Vector((R*math.sin(a), -R*math.cos(a), size.z*0.15))
    d=center-cam.location
    cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=f'{outdir}/{name}.png'
    bpy.ops.render.render(write_still=True)
print('RENDERED')
