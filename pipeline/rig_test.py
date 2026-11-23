import bpy
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/ju_mao_dagongji/3d/dafu_textured_v1.blend')
obj=[o for o in bpy.context.scene.objects if o.type=='MESH'][0]
bpy.context.view_layer.objects.active=obj
obj.select_set(True)
# decimate for the rig test
mod=obj.modifiers.new('dec','DECIMATE'); mod.ratio=0.12
bpy.ops.object.modifier_apply(modifier='dec')
print('faces after decimate:', len(obj.data.polygons))
# --- armature ---
bpy.ops.object.armature_add(enter_editmode=True)
arm=bpy.context.active_object; arm.name='DafuRig'
eb=arm.data.edit_bones
root=eb[0]; root.name='hips'; root.head=(0,0,-0.30); root.tail=(0,0,0.02)
def bone(name,head,tail,parent):
    b=eb.new(name); b.head=head; b.tail=tail; b.parent=eb[parent]; return b
bone('spine',(0,0,0.02),(0,0,0.30),'hips')
bone('head',(0,0,0.30),(0,0,0.80),'spine')
bone('legL',(0.20,-0.05,-0.32),(0.23,-0.08,-0.66),'hips')
bone('shinL',(0.23,-0.08,-0.66),(0.25,-0.12,-0.97),'legL')
bone('legR',(-0.20,-0.05,-0.32),(-0.23,-0.02,-0.66),'hips')
bone('shinR',(-0.23,-0.02,-0.66),(-0.25,-0.02,-0.97),'legR')
bone('armL',(0.40,-0.02,0.26),(0.52,-0.05,-0.02),'spine')
bone('pawL',(0.52,-0.05,-0.02),(0.50,-0.08,-0.30),'armL')
bone('armR',(-0.40,-0.02,0.26),(-0.52,-0.05,-0.02),'spine')
bone('pawR',(-0.52,-0.05,-0.02),(-0.48,-0.06,0.22),'armR')
bpy.ops.object.mode_set(mode='OBJECT')
# --- parent with automatic weights ---
obj.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active=arm
try:
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    print('AUTO_WEIGHTS_OK')
except Exception as e:
    print('AUTO_WEIGHTS_FAIL', e)
bpy.ops.wm.save_as_mainfile(filepath='/home/hatch/workspace/ju_mao_dagongji/3d/dafu_rig_test.blend')
print('RIG_SAVED')
