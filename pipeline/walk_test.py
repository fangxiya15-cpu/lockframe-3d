import bpy, math, os
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/ju_mao_dagongji/3d/dafu_rig_test.blend')
arm=bpy.context.scene.objects['DafuRig']
bpy.context.view_layer.objects.active=arm
bpy.ops.object.mode_set(mode='POSE')
pb=arm.pose.bones
scene=bpy.context.scene
scene.frame_start=1; scene.frame_end=48
def key(bone, frame, rx=0.0, rz=0.0, locz=None):
    b=pb[bone]; b.rotation_mode='XYZ'
    b.rotation_euler=(rx,0,rz)
    b.keyframe_insert('rotation_euler', frame=frame)
    if locz is not None:
        b.location=(0,0,locz); b.keyframe_insert('location', frame=frame)
for f in range(1,50,4):
    t=(f-1)/24*2*math.pi  # one full cycle = 24 frames
    s=math.sin(t)
    key('legL', f, rx=0.38*s)
    key('legR', f, rx=-0.38*s)
    key('shinL', f, rx=max(0.0,-0.45*s)+0.08)
    key('shinR', f, rx=max(0.0,0.45*s)+0.08)
    key('armL', f, rx=-0.14*s)
    key('armR', f, rx=0.14*s)
    key('pawR', f, rx=0.10*math.sin(t+1.2))
    key('head', f, rx=0.04*math.sin(2*t))
    key('hips', f, locz=0.035*abs(math.sin(t)))
bpy.ops.object.mode_set(mode='OBJECT')
# camera + light + ground
obj=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name!='DafuRig'][0]
mins=Vector((1e9,)*3); maxs=Vector((-1e9,)*3)
for c in obj.bound_box:
    w=obj.matrix_world @ Vector(c)
    mins=Vector(map(min,mins,w)); maxs=Vector(map(max,maxs,w))
center=(mins+maxs)/2; size=maxs-mins; R=max(size)*1.8
scene.render.engine='CYCLES'; scene.cycles.samples=12; scene.cycles.device='CPU'
scene.world=bpy.data.worlds.new('w'); scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0.92,0.92,0.92,1)
scene.render.resolution_x=400; scene.render.resolution_y=400
cam_data=bpy.data.cameras.new('c'); cam=bpy.data.objects.new('cam',cam_data)
scene.collection.objects.link(cam); scene.camera=cam
a=math.radians(18)
cam.location=center+Vector((R*math.sin(a), -R*math.cos(a), size.z*0.1))
d=center-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
sun_data=bpy.data.lights.new('s','SUN'); sun=bpy.data.objects.new('sun',sun_data)
sun.data.energy=2.0; scene.collection.objects.link(sun); sun.rotation_euler=(0.8,0.2,0.6)
out='/home/hatch/workspace/ju_mao_dagongji/3d/walkframes'; os.makedirs(out,exist_ok=True)
scene.render.filepath=out+'/f_'
scene.render.image_settings.file_format='PNG'
bpy.ops.render.render(animation=True)
print('WALK_RENDERED')
