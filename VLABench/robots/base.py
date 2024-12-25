import os
import json
from dm_control import composer
from dm_control import mjcf

class Robot(composer.Robot):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", "default_robot")
        self.robot_asset_root = os.path.join(os.getenv("VLABENCH_ROOT", 
                                                       os.path.join(os.path.dirname(__file__), "..")), 
                                             "assets/robots")
        super().__init__(*args, **kwargs)
        with open(os.path.join(os.getenv("VLABENCH_ROOT"), "configs/robot_config.json"), "r") as f:
            robot_config = json.load(f)
        assert isinstance(robot_config, dict), "robot_config must be a dictionary"
        self.robot_config = robot_config.get(self.name, {})
        self.default_qpos = self.robot_config.get("default_qpos", [])    
            
    def _build(self, *args, **kwargs):
        xml_path = os.path.join(self.robot_asset_root, kwargs.get("xml_path", "robot.xml"))
        if xml_path is not None:
            self._mjcf_model = mjcf.from_path(xml_path)
        else:
            self._mjcf_model = mjcf.RootElement()
        self._mjcf_model.model = self.name
        if kwargs.get("position", None) is not None:
            self.set_base_position(kwargs.get("position"))
        if kwargs.get("euler", None) is not None:
            self.set_base_orientation(kwargs.get("euler"))
    
    @property
    def mjcf_model(self):
        return self._mjcf_model
    
    @property
    def joints(self):
        return self.mjcf_model.find_all("joint")
    
    @property
    def actuators(self):
        return self.mjcf_model.find_all("actuator")
    
    @property
    def n_dof(self):
        return len(self.joint)
    
    @property
    def geoms(self):
        return self.mjcf_model.find_all("geom")
    
    @property
    def sites(self):
        return self.mjcf_model.find_all("site")
    
    @property
    def bodies(self):
        return self.mjcf_model.find_all("body")
    
    def set_base_position(self, pos):
        raise NotImplementedError
    
    def set_base_orientation(self, ori):
        raise NotImplementedError

    
    