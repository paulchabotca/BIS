# Nikita Akimov
# interplanety@interplanety.org

import bpy
import json
from .NodeManager import NodeManager
from .WebRequests import WebRequest


class BIS_addNodeToStorage(bpy.types.Operator):
    bl_idname = 'bis.add_nodegroup_to_storage'
    bl_label = 'BIS_AddToIStorage'
    bl_description = 'Add nodegroup to common part of BIS'
    bl_options = {'REGISTER', 'UNDO'}

    showMessage = bpy.props.BoolProperty(
        default=False
    )

    def execute(self, context):
        if context.active_node and context.active_node.type == 'GROUP':
            activeNode = context.active_node
            nodeGroupTags = ''
            if context.area.spaces.active.tree_type == 'ShaderNodeTree':
                if context.space_data.shader_type == 'WORLD':
                    activeNode = context.scene.world.node_tree.nodes.active
                    nodeGroupTags = 'world'
                elif context.space_data.shader_type == 'OBJECT':
                    activeNode = context.active_object.active_material.node_tree.nodes.active
                    nodeGroupTags = 'shader'
            elif context.area.spaces.active.tree_type == 'CompositorNodeTree':
                nodeGroupTags = 'compositing'
            nodeGroupJson = NodeManager.nodeGroupToJson(activeNode)
            if nodeGroupJson:
                if context.scene.bis_add_nodegroup_to_storage_vars.tags != '':
                    nodeGroupTags += (';' if nodeGroupTags else '') + context.scene.bis_add_nodegroup_to_storage_vars.tags
                request = WebRequest.sendRequest({
                    'for': 'set_node_group',
                    'node_group': json.dumps(nodeGroupJson),
                    'node_group_subtype': NodeManager.get_subtype(context),
                    'node_group_subtype2': NodeManager.get_subtype2(context),
                    'node_group_name': nodeGroupJson['name'],
                    'node_group_tags': nodeGroupTags.strip()
                })
                if request:
                    context.scene.bis_add_nodegroup_to_storage_vars.tags = ''
                    requestRez = json.loads(request.text)
                    if self.showMessage:
                        bpy.ops.message.messagebox('INVOKE_DEFAULT', message=requestRez['stat'])
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message='No NodeGroup selected')
        return {'FINISHED'}


class BIS_addNodeGroupToStorageVars(bpy.types.PropertyGroup):
    tags = bpy.props.StringProperty(
        name='Tags',
        description='Tags',
        default=''
    )


def register():
    bpy.utils.register_class(BIS_addNodeToStorage)
    bpy.utils.register_class(BIS_addNodeGroupToStorageVars)
    bpy.types.Scene.bis_add_nodegroup_to_storage_vars = bpy.props.PointerProperty(type = BIS_addNodeGroupToStorageVars)


def unregister():
    del bpy.types.Scene.bis_add_nodegroup_to_storage_vars
    bpy.utils.unregister_class(BIS_addNodeGroupToStorageVars)
    bpy.utils.unregister_class(BIS_addNodeToStorage)
