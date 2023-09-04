import bpy

# Set the name of the loaded image
loaded_image_name = "242472687_384441436609157_1530127914890124143_n.jpg"  # Replace with the name of your loaded image

# Set the blur strength (adjust as needed)
blur_strength = 5

# Set up the compositing nodes
scene = bpy.context.scene
scene.use_nodes = True
tree = scene.node_tree

original_input_node = None
if len(tree.nodes) > 0:
    original_input_node = tree.nodes[0]

# Clear existing nodes
for node in tree.nodes:
    tree.nodes.remove(node)

# Create image input node using the loaded image
loaded_image = bpy.data.images.get(loaded_image_name)
image_node = tree.nodes.new(type='CompositorNodeImage')
image_node.image = loaded_image

# Get the dimensions of the loaded image
input_width = loaded_image.size[0]
input_height = loaded_image.size[1]

# Create blur node
blur_node = tree.nodes.new(type='CompositorNodeBlur')
blur_node.filter_type = 'GAUSS'
blur_node.size_x = blur_strength
blur_node.size_y = blur_strength

# Create output node
output_node = tree.nodes.new(type='CompositorNodeComposite')

# Connect the nodes
tree.links.new(image_node.outputs["Image"], blur_node.inputs[0])
tree.links.new(blur_node.outputs["Image"], output_node.inputs["Image"])

# Set resolution
resolution_x = scene.render.resolution_x
resolution_y = scene.render.resolution_y

scene.render.resolution_x = input_width
scene.render.resolution_y = input_height

# Set view transform
view_transform = scene.view_settings.view_transform

scene.view_settings.view_transform = 'Standard'

# Set up rendering settings
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = "//final_image.png"  # Specify the output path

# Render the current scene
bpy.ops.render.render(write_still=True)

# Restore render resolution
scene.render.resolution_x = resolution_x
scene.render.resolution_y = resolution_y

# Restore view transform
scene.view_settings.view_transform = view_transform

# Reconnect the original input node (if it exists)
if original_input_node is not None:
    tree.links.new(original_input_node.outputs["Image"], output_node.inputs["Image"])