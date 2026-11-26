"""Inspect the frozen YHRM teaching assembly in Blender background mode."""
from hashlib import file_digest
import json
from pathlib import Path

import bpy

EXPECTED = '80a792514b4a4baaafee2d658da0ed344efbbd3a73f8a5736b18bd1194d5b7e9'
asset = Path(bpy.data.filepath)
with asset.open('rb') as file:
    digest = file_digest(file, 'sha256').hexdigest()

active = bpy.context.scene
active_meshes = sum(obj.type == 'MESH' for obj in active.objects)
external = {
    'libraries': sorted(Path(library.filepath).name for library in bpy.data.libraries),
    'images': sorted(img.name for img in bpy.data.images
                     if img.source in {'FILE', 'SEQUENCE', 'MOVIE', 'TILED'}
                     and img.filepath and not img.packed_files),
    'fonts': sorted(font.name for font in bpy.data.fonts
                    if font.filepath not in {'', '<builtin>'} and font.packed_file is None),
    'sounds': sorted(sound.name for sound in bpy.data.sounds
                     if sound.filepath and sound.packed_file is None),
}
assert digest == EXPECTED, ('Unexpected release assembly fingerprint', digest)
assert active_meshes == 8811, active_meshes
assert len(bpy.data.scenes) == 16, len(bpy.data.scenes)
assert not any(external.values()), external

record = {
    'status': 'PASS_INDEPENDENT_REOPEN',
    'asset': asset.name,
    'sha256': digest,
    'size_bytes': asset.stat().st_size,
    'blender_version': bpy.app.version_string,
    'active_scene': active.name,
    'active_objects': len(active.objects),
    'active_meshes': active_meshes,
    'frame': active.frame_current,
    'scene_count': len(bpy.data.scenes),
    'scenes': [scene.name for scene in bpy.data.scenes],
    'unpacked_dependencies': external,
    'scope': 'Original file integrity, native structure and resource availability. No new engineering acceptance.',
}
print('REOPEN_RECORD='+json.dumps(record, ensure_ascii=False))
