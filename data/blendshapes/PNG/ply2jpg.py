#!/usr/bin/env python3
import open3d as o3d
import sys
import numpy as np
from pathlib import Path

input_file = sys.argv[1]
pcd = o3d.io.read_point_cloud(input_file)
filename = Path(input_file).stem

vis = o3d.visualization.Visualizer()
vis.create_window(width = 1024, height = 1024)
opt = vis.get_render_option()
opt.background_color = np.asarray([1, 1, 1])
opt.point_size = 3.0
pcd.paint_uniform_color([0, 0, 0])

# turn downside up
if len(sys.argv) == 3 and sys.argv[2] == '--flip':
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    print("flipping")
else:
    print("not flipping")
vis.add_geometry(pcd)

output_file = str(filename + ".png")
print("saving as image: " + output_file)
vis.capture_screen_image(output_file, do_render=True)
vis.destroy_window()

