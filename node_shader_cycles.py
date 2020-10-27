# Nikita Akimov
# interplanety@interplanety.org

import bpy
import os
from . import cfg
from .file_manager import FileManager
from .JsonEx import JsonEx
from .bl_types_conversion import BLObject, BLParticleSystem, BLCurveMapping
from .node_common import NodeCommon, TMCommon, IUCommon, CMCommon, NodeColorRamp
from .TextManager import TextManager


class NodeShaderNodeBsdfGlossy(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['distribution'] = node.distribution

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.distribution = node_in_json['distribution']


class NodeShaderNodeBsdfAnisotropic(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeBsdfGlass(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeBsdfRefraction(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeAttribute(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['attribute_name'] = node.attribute_name

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.attribute_name = node_in_json['attribute_name']


class NodeShaderNodeTangent(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['direction_type'] = node.direction_type
        node_json['axis'] = node.axis
        node_json['uv_map'] = node.uv_map

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.direction_type = node_in_json['direction_type']
        node.axis = node_in_json['axis']
        node.uv_map = node_in_json['uv_map']


class NodeShaderNodeUVMap(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['uv_map'] = node.uv_map
        if hasattr(node, 'from_dupli'):
            node_json['from_dupli'] = node.from_dupli
        if hasattr(node, 'from_instancer'):
            node_json['from_instancer'] = node.from_instancer

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.uv_map = node_in_json['uv_map']
        if 'from_dupli' in node_in_json and hasattr(node, 'from_dupli'):
            node.from_dupli = node_in_json['from_dupli']
        if 'from_instancer' in node_in_json and hasattr(node, 'from_instancer'):
            node.from_instancer = node_in_json['from_instancer']


class NodeShaderNodeTexCoord(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['object'] = ''
        if node.object:
            node_json['object'] = node.object.name
        if hasattr(node, 'from_dupli'):
            node_json['from_dupli'] = node.from_dupli
        if hasattr(node, 'from_instancer'):
            node_json['from_instancer'] = node.from_instancer

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if node_in_json['object']:
            if node_in_json['object'] in bpy.data.objects:
                node.object = bpy.data.objects[node_in_json['object']]
        if 'from_dupli' in node_in_json and hasattr(node, 'from_dupli'):
            node.from_dupli = node_in_json['from_dupli']
        if 'from_instancer' in node_in_json and hasattr(node, 'from_instancer'):
            node.from_instancer = node_in_json['from_instancer']


class NodeShaderNodeTexPointDensity(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if node.object:
            node_json['object'] = BLObject.to_json(instance=node.object)
            if node.particle_system:
                node_json['particle_system'] = BLParticleSystem.to_json(instance=node.particle_system)
        node_json['point_source'] = node.point_source
        node_json['resolution'] = node.resolution
        node_json['radius'] = node.radius
        node_json['space'] = node.space
        node_json['interpolation'] = node.interpolation
        node_json['particle_color_source'] = node.particle_color_source
        node_json['vertex_color_source'] = node.vertex_color_source
        node_json['vertex_attribute_name'] = node.vertex_attribute_name

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'object' in node_in_json and node_in_json['object']:
            BLObject.from_json(instance=node, json=node_in_json['object'])
            if 'particle_system' in node_in_json and node_in_json['particle_system']:
                BLParticleSystem.from_json(instance=node, json=node_in_json['particle_system'])
        node.point_source = node_in_json['point_source']
        node.resolution = node_in_json['resolution']
        node.radius = node_in_json['radius']
        node.space = node_in_json['space']
        node.interpolation = node_in_json['interpolation']
        node.particle_color_source = node_in_json['particle_color_source']
        node.vertex_color_source = node_in_json['vertex_color_source']
        node.vertex_attribute_name = node_in_json['vertex_attribute_name']


class NodeShaderNodeTexEnvironment(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['image'] = ''
        node_json['image_source'] = ''
        if node.image:
            node_json['image'] = os.path.normpath(os.path.join(os.path.dirname(bpy.data.filepath), node.image.filepath.replace('//', '')))
            node_json['image_name'] = FileManager.normalize_file_name(node.image.name)
            node_json['image_source'] = node.image.source
        if hasattr(node, 'color_space'):
            node_json['color_space'] = node.color_space
        if hasattr(node, 'projection'):
            node_json['projection'] = node.projection
        if hasattr(node, 'interpolation'):
            node_json['interpolation'] = node.interpolation
        if hasattr(node, 'texture_mapping'):
            node_json['texture_mapping'] = TMCommon.tm_to_json(node.texture_mapping)
        if hasattr(node, 'image_user'):
            node_json['image_user'] = IUCommon.iu_to_json(node.image_user)
        if hasattr(node, 'color_mapping'):
            node_json['color_mapping'] = CMCommon.cm_to_json(node.color_mapping)

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        attachment_path = ''
        attachment_name = ''
        if 'image_name' in node_in_json and node_in_json['image_name'] and os.path.exists(os.path.join(attachments_path, node_in_json['image_name'])) and os.path.isfile(os.path.join(attachments_path, node_in_json['image_name'])):
            attachment_path = os.path.join(attachments_path, node_in_json['image_name'])
            attachment_name = node_in_json['image_name']
        elif 'image' in node_in_json and node_in_json['image'] and os.path.exists(node_in_json['image']) and os.path.isfile(node_in_json['image']):
            attachment_path = node_in_json['image']
            attachment_name = os.path.basename(node_in_json['image'])
        if attachment_path:
            if attachment_name in bpy.data.images:
                bpy.data.images[attachment_name].reload()
            else:
                attachment_block = bpy.data.images.load(attachment_path, check_existing=False)
                if attachment_block:
                    attachment_name = attachment_block.name
            if attachment_name and attachment_name in bpy.data.images:
                node.image = bpy.data.images[attachment_name]
                node.image.source = node_in_json['image_source']
        if 'color_space' in node_in_json and hasattr(node, 'color_space'):
            node.color_space = node_in_json['color_space']
        if 'projection' in node_in_json and hasattr(node, 'projection'):
            node.projection = node_in_json['projection']
        if 'interpolation' in node_in_json and hasattr(node, 'interpolation'):
            node.interpolation = node_in_json['interpolation']
        if 'texture_mapping' in node_in_json and hasattr(node, 'texture_mapping'):
            TMCommon.json_to_tm(node, node_in_json['texture_mapping'])
        if 'image_user' in node_in_json and hasattr(node, 'image_user'):
            IUCommon.json_to_iu(node, node_in_json['image_user'])
        if 'color_mapping' in node_in_json and hasattr(node, 'color_mapping'):
            CMCommon.json_to_cm(node, node_in_json['color_mapping'])


class NodeShaderNodeTexImage(NodeShaderNodeTexEnvironment):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        node_json['projection_blend'] = node.projection_blend
        node_json['extension'] = node.extension

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        node.projection_blend = node_in_json['projection_blend']
        node.extension = node_in_json['extension']


class NodeShaderNodeTexChecker(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'texture_mapping'):
            node_json['texture_mapping'] = TMCommon.tm_to_json(node.texture_mapping)
        if hasattr(node, 'color_mapping'):
            node_json['color_mapping'] = CMCommon.cm_to_json(node.color_mapping)

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'texture_mapping' in node_in_json and hasattr(node, 'texture_mapping'):
            TMCommon.json_to_tm(node, node_in_json['texture_mapping'])
        if 'color_mapping' in node_in_json and hasattr(node, 'color_mapping'):
            CMCommon.json_to_cm(node, node_in_json['color_mapping'])


class NodeShaderNodeTexBrick(NodeShaderNodeTexChecker):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        node_json['offset_frequency'] = node.offset_frequency
        node_json['squash_frequency'] = node.squash_frequency
        node_json['offset'] = node.offset
        node_json['squash'] = node.squash

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        node.offset_frequency = node_in_json['offset_frequency']
        node.squash_frequency = node_in_json['squash_frequency']
        node.offset = node_in_json['offset']
        node.squash = node_in_json['squash']


class NodeShaderNodeTexGradient(NodeShaderNodeTexChecker):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        node_json['gradient_type'] = node.gradient_type

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        node.gradient_type = node_in_json['gradient_type']


class NodeShaderNodeTexMagic(NodeShaderNodeTexChecker):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        node_json['turbulence_depth'] = node.turbulence_depth

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        node.turbulence_depth = node_in_json['turbulence_depth']


class NodeShaderNodeTexMusgrave(NodeShaderNodeTexChecker):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        node_json['musgrave_type'] = node.musgrave_type
        if hasattr(node, 'musgrave_dimensions'):
            node_json['musgrave_dimensions'] = node.musgrave_dimensions

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        node.musgrave_type = node_in_json['musgrave_type']
        if 'musgrave_dimensions' in node_in_json and hasattr(node, 'musgrave_dimensions'):
            node.musgrave_dimensions = node_in_json['musgrave_dimensions']


class NodeShaderNodeTexVoronoi(NodeShaderNodeTexChecker):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        if hasattr(node, 'coloring'):
            node_json['coloring'] = node.coloring
        if hasattr(node, 'distance'):
            node_json['distance'] = node.distance
        if hasattr(node, 'feature'):
            node_json['feature'] = node.feature
        if hasattr(node, 'voronoi_dimensions'):
            node_json['voronoi_dimensions'] = node.voronoi_dimensions

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        if 'coloring' in node_in_json and hasattr(node, 'coloring'):
            node.coloring = node_in_json['coloring']
        if 'distance' in node_in_json and hasattr(node, 'distance'):
            try:
                node.distance = node_in_json['distance']
            except Exception as exception:
                if cfg.show_debug_err:
                    print(repr(exception))
        if 'feature' in node_in_json and hasattr(node, 'feature'):
            try:
                node.feature = node_in_json['feature']
            except Exception as exception:
                if cfg.show_debug_err:
                    print(repr(exception))
        if 'voronoi_dimensions' in node_in_json and hasattr(node, 'voronoi_dimensions'):
            node.voronoi_dimensions = node_in_json['voronoi_dimensions']


class NodeShaderNodeTexWave(NodeShaderNodeTexChecker):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        node_json['wave_profile'] = node.wave_profile
        node_json['wave_type'] = node.wave_type
        if hasattr(node, 'bands_direction'):
            node_json['bands_direction'] = node.bands_direction
        if hasattr(node, 'rings_direction'):
            node_json['rings_direction'] = node.rings_direction

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        node.wave_profile = node_in_json['wave_profile']
        node.wave_type = node_in_json['wave_type']
        if 'bands_direction' in node_in_json and hasattr(node, 'bands_direction'):
            node.bands_direction = node_in_json['bands_direction']
        if 'rings_direction' in node_in_json and hasattr(node, 'rings_direction'):
            node.rings_direction = node_in_json['rings_direction']


class NodeShaderNodeTexSky(NodeShaderNodeTexChecker):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        node_json['sky_type'] = node.sky_type
        node_json['sun_direction'] = JsonEx.vector3_to_json(node.sun_direction)
        node_json['turbidity'] = node.turbidity
        node_json['ground_albedo'] = node.ground_albedo

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        node.sky_type = node_in_json['sky_type']
        JsonEx.vector3_from_json(node.sun_direction, node_in_json['sun_direction'])
        node.turbidity = node_in_json['turbidity']
        node.ground_albedo = node_in_json['ground_albedo']


class NodeShaderNodeTexNoise(NodeShaderNodeTexChecker):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        super()._node_to_json_spec(node_json=node_json, node=node)
        if hasattr(node, 'noise_dimensions'):
            node_json['noise_dimensions'] = node.noise_dimensions

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        super()._json_to_node_spec(node=node, node_in_json=node_in_json, attachments_path=attachments_path)
        if 'noise_dimensions' in node_in_json and hasattr(node, 'noise_dimensions'):
            node.noise_dimensions = node_in_json['noise_dimensions']


class NodeShaderNodeTexWhiteNoise(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'noise_dimensions'):
            node_json['noise_dimensions'] = node.noise_dimensions

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'noise_dimensions' in node_in_json and hasattr(node, 'noise_dimensions'):
            node.noise_dimensions = node_in_json['noise_dimensions']


class NodeShaderNodeWireframe(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['use_pixel_size'] = node.use_pixel_size

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.use_pixel_size = node_in_json['use_pixel_size']


class NodeShaderNodeBsdfHair(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['component'] = node.component

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.component = node_in_json['component']


class NodeShaderNodeBsdfToon(NodeShaderNodeBsdfHair):
    pass


class NodeShaderNodeSubsurfaceScattering(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['falloff'] = node.falloff

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.falloff = node_in_json['falloff']


class NodeShaderNodeMixRGB(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['blend_type'] = node.blend_type
        node_json['use_alpha'] = node.use_alpha
        node_json['use_clamp'] = node.use_clamp

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.blend_type = node_in_json['blend_type']
        node.use_alpha = node_in_json['use_alpha']
        node.use_clamp = node_in_json['use_clamp']


class NodeShaderNodeBrightContrast(NodeCommon):
    pass


class NodeShaderNodeGamma(NodeCommon):
    pass


class NodeShaderNodeHueSaturation(NodeCommon):
    pass


class NodeShaderNodeInvert(NodeCommon):
    pass


class NodeShaderNodeLightFalloff(NodeCommon):
    pass


class NodeShaderNodeBlackbody(NodeCommon):
    pass


class NodeShaderNodeCombineHSV(NodeCommon):
    pass


class NodeShaderNodeSeparateHSV(NodeCommon):
    pass


class NodeShaderNodeCombineRGB(NodeCommon):
    pass


class NodeShaderNodeSeparateRGB(NodeCommon):
    pass


class NodeShaderNodeCombineXYZ(NodeCommon):
    pass


class NodeShaderNodeSeparateXYZ(NodeCommon):
    pass


class NodeShaderNodeRGBToBW(NodeCommon):
    pass


class NodeShaderNodeWavelength(NodeCommon):
    pass


class NodeShaderNodeRGBCurve(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['mapping'] = BLCurveMapping.to_json(instance=node.mapping)

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        BLCurveMapping.from_json(instance=node.mapping, json=node_in_json['mapping'])


class NodeShaderNodeVectorCurve(NodeShaderNodeRGBCurve):
    pass


class NodeShaderNodeBump(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['invert'] = node.invert

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.invert = node_in_json['invert']


class NodeShaderNodeVectorTransform(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['vector_type'] = node.vector_type
        node_json['convert_from'] = node.convert_from
        node_json['convert_to'] = node.convert_to

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.vector_type = node_in_json['vector_type']
        node.convert_from = node_in_json['convert_from']
        node.convert_to = node_in_json['convert_to']


class NodeShaderNodeValToRGB(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['color_ramp'] = NodeColorRamp.cr_to_json(node.color_ramp)

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        NodeColorRamp.json_to_cr(node.color_ramp, node_in_json['color_ramp'])


class NodeShaderNodeMapping(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['vector_type'] = node.vector_type

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.vector_type = node_in_json['vector_type']


class NodeShaderNodeMapRange(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'clamp'):
            node_json['clamp'] = node.clamp
        cls.attr_to_json(attribute_name='interpolation_type', node=node, node_json=node_json)

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'clamp' in node_in_json and hasattr(node, 'clamp'):
            node.clamp = node_in_json['clamp']
        cls.attr_from_json(attribute_name='interpolation_type', node=node, node_json=node_in_json)


class NodeShaderNodeNormal(NodeCommon):
    pass


class NodeShaderNodeNormalMap(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'space'):
            node_json['space'] = node.space
        if hasattr(node, 'uv_map'):
            node_json['uv_map'] = node.uv_map

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'space' in node_in_json and hasattr(node, 'space'):
            node.space = node_in_json['space']
        if 'uv_map' in node_in_json and hasattr(node, 'uv_map'):
            node.uv_map = node_in_json['uv_map']


class NodeShaderNodeMath(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['operation'] = node.operation
        node_json['use_clamp'] = node.use_clamp

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.operation = node_in_json['operation']
        node.use_clamp = node_in_json['use_clamp']


class NodeShaderNodeVectorMath(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['operation'] = node.operation

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        try:
            node.operation = node_in_json['operation']
        except Exception as exception:
            if cfg.show_debug_err:
                print(repr(exception))


class NodeShaderNodeScript(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['script'] = ''
        node_json['mode'] = node.mode
        if node.mode == 'INTERNAL':
            if node.script:
                node_json['script'] = node.script.name
                rez = TextManager.to_bis(context=bpy.context, text=bpy.data.texts[node.script.name])
                if rez['stat'] == 'OK':
                    bis_linked_item = {
                        'storage': TextManager.storage_type(),
                        'id': rez['data']['id']
                    }
                    node_json['bis_linked_item'] = bis_linked_item
        else:
            node_json['filepath'] = ''
            if node.filepath:
                if node.filepath[:2] == '//':
                    node_json['filepath'] = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath)), node.filepath[2:]))
                else:
                    node_json['filepath'] = os.path.abspath(node.filepath)
        node_json['use_auto_update'] = node.use_auto_update

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.mode = node_in_json['mode']
        if node.mode == 'INTERNAL':
            if node_in_json['bis_linked_item']:
                TextManager.from_bis(context=bpy.context, bis_text_id=node_in_json['bis_linked_item']['id'])
            if node_in_json['script']:
                if node_in_json['script'] in bpy.data.texts:
                    node.script = bpy.data.texts[node_in_json['script']]
        else:
            if node_in_json['filepath']:
                attachment_name = os.path.basename(node_in_json['filepath'])
                if os.path.exists(os.path.join(attachments_path, attachment_name)) and os.path.isfile(os.path.join(attachments_path, attachment_name)):
                    node.filepath = os.path.join(attachments_path, attachment_name)
                elif os.path.exists(node_in_json['filepath']) and os.path.isfile(node_in_json['filepath']):
                    node.filepath = node_in_json['filepath']
        node.use_auto_update = node_in_json['use_auto_update']
        node.update()


class NodeShaderNodeMixShader(NodeCommon):
    pass


class NodeNodeGroupInput(NodeCommon):
    pass


class NodeNodeGroupOutput(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['is_active_output'] = node.is_active_output

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'is_active_output' in node_in_json:
            node.is_active_output = node_in_json['is_active_output']


class NodeShaderNodeAmbientOcclusion(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'inside'):
            node_json['inside'] = node.inside
        if hasattr(node, 'only_local'):
            node_json['only_local'] = node.only_local
        if hasattr(node, 'samples'):
            node_json['samples'] = node.samples

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'inside' in node_in_json and hasattr(node, 'inside'):
            node.inside = node_in_json['inside']
        if 'only_local' in node_in_json and hasattr(node, 'only_local'):
            node.only_local = node_in_json['only_local']
        if 'samples' in node_in_json and hasattr(node, 'samples'):
            node.samples = node_in_json['samples']


class NodeShaderNodeBevel(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'samples'):
            node_json['samples'] = node.samples

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'samples' in node_in_json and hasattr(node, 'samples'):
            node.samples = node_in_json['samples']


class NodeShaderNodeCameraData(NodeCommon):
    pass


class NodeShaderNodeFresnel(NodeCommon):
    pass


class NodeShaderNodeGeometry(NodeCommon):
    pass


class NodeShaderNodeHairInfo(NodeCommon):
    pass


class NodeShaderNodeLayerWeight(NodeCommon):
    pass


class NodeShaderNodeLightPass(NodeCommon):
    pass


class NodeShaderNodeObjectInfo(NodeCommon):
    pass


class NodeShaderNodeParticleInfo(NodeCommon):
    pass


class NodeShaderNodeRGB(NodeCommon):
    pass


class NodeShaderNodeValue(NodeCommon):
    pass


class NodeShaderNodeOutputMaterial(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'is_active_output'):
            node_json['is_active_output'] = node.is_active_output
        if hasattr(node, 'target'):
            node_json['target'] = node.target

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'is_active_output' in node_in_json and hasattr(node, 'is_active_output'):
            node.is_active_output = node_in_json['is_active_output']
        if 'target' in node_in_json and hasattr(node, 'target'):
            node.target = node_in_json['target']


class NodeShaderNodeOutputWorld(NodeShaderNodeOutputMaterial):
    pass


class NodeShaderNodeOutputLight(NodeShaderNodeOutputMaterial):
    pass


class NodeShaderNodeAddShader(NodeCommon):
    pass


class NodeShaderNodeBsdfDiffuse(NodeCommon):
    pass


class NodeShaderNodeEmission(NodeCommon):
    pass


class NodeShaderNodeHoldout(NodeCommon):
    pass


class NodeShaderNodeBsdfPrincipled(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'distribution'):
            node_json['distribution'] = node.distribution
        if hasattr(node, 'subsurface_method'):
            node_json['subsurface_method'] = node.subsurface_method

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'distribution' in node_in_json and hasattr(node, 'distribution'):
            node.distribution = node_in_json['distribution']
        if 'subsurface_method' in node_in_json and hasattr(node, 'subsurface_method'):
            node.subsurface_method = node_in_json['subsurface_method']


class NodeShaderNodeBsdfHairPrincipled(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'parametrization'):
            node_json['parametrization'] = node.parametrization

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'parametrization' in node_in_json and hasattr(node, 'parametrization'):
            node.parametrization = node_in_json['parametrization']


class NodeShaderNodeVolumePrincipled(NodeCommon):
    pass


class NodeShaderNodeBsdfTranslucent(NodeCommon):
    pass


class NodeShaderNodeBsdfTransparent(NodeCommon):
    pass


class NodeShaderNodeBsdfVelvet(NodeCommon):
    pass


class NodeShaderNodeVolumeAbsorption(NodeCommon):
    pass


class NodeShaderNodeVolumeScatter(NodeCommon):
    pass


class NodeShaderNodeVolumeInfo(NodeCommon):
    pass


class NodeShaderNodeTexIES(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['ies'] = ''
        node_json['mode'] = node.mode
        if node.mode == 'INTERNAL':
            if node.ies:
                node_json['ies'] = node.ies.name
                rez = TextManager.to_bis(context=bpy.context, text=bpy.data.texts[node.ies.name])
                if rez['stat'] == 'OK':
                    bis_linked_item = {
                        'storage': TextManager.storage_type(),
                        'id': rez['data']['id']
                    }
                    node_json['bis_linked_item'] = bis_linked_item
        else:
            node_json['filepath'] = ''
            if node.filepath:
                if node.filepath[:2] == '//':
                    node_json['filepath'] = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath)), node.filepath[2:]))
                else:
                    node_json['filepath'] = os.path.abspath(node.filepath)

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        node.mode = node_in_json['mode']
        if node.mode == 'INTERNAL':
            if 'bis_linked_item' in node_in_json and node_in_json['bis_linked_item']:
                TextManager.from_bis(context=bpy.context, bis_text_id=node_in_json['bis_linked_item']['id'])
            if node_in_json['ies']:
                if node_in_json['ies'] in bpy.data.texts:
                    node.ies = bpy.data.texts[node_in_json['ies']]
        else:
            if node_in_json['filepath']:
                if os.path.exists(node_in_json['filepath']) and os.path.isfile(node_in_json['filepath']):
                    node.filepath = node_in_json['filepath']
        node.update()


class NodeShaderNodeDisplacement(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'space'):
            node_json['space'] = node.space

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'space' in node_in_json and hasattr(node, 'space'):
            node.space = node_in_json['space']


class NodeShaderNodeVectorDisplacement(NodeShaderNodeDisplacement):
    pass


class NodeShaderNodeClamp(NodeCommon):
    pass


class NodeShaderNodeVertexColor(NodeCommon):
    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        if hasattr(node, 'layer_name'):
            node_json['layer_name'] = node.layer_name

    @classmethod
    def _json_to_node_spec(cls, node, node_in_json, attachments_path):
        if 'layer_name' in node_in_json and hasattr(node, 'layer_name'):
            node.layer_name = node_in_json['layer_name']
