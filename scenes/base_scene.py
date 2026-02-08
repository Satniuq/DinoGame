# scenes/base_scene.py
class BaseScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
