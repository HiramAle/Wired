import pygame
import src.engine.assets as assets
import src.engine.input as input
import src.engine.time as time
import src.scene.core.scene_manager as scene_manager
from src.scene.core.scene import StagedScene
from src.scene.subnetting.subnetting_objects import *
from src.game_object.sprite import SpriteGroup
from src.constants.colors import BLUE_MOTION
from src.gui.image import GUIImage
from src.gui.text import GUIText
from src.constants.colors import *
from random import choice
from src.scene.subnetting.subnet_mask_stage import SubnetMask
from src.scene.subnetting.results_stage import Results


class Subnetting(StagedScene):
    def __init__(self):
        super().__init__("subnetting")
        self.starting_time = pygame.time.get_ticks()
        pygame.mouse.set_visible(True)
        zones = ["Museo", "Hotel", "Hospital", "Escuela", "Oficina", "Supermercado"]
        building_names = {
            "Museo": ["Galerías", "Exposiciones", "Colecciones", "Auditorios", "Tienda", "Cafetería", "Recepción",
                      "Talleres"],
            "Hotel": ["Recepción", "Habitaciones", "Restaurante", "Bar", "Gimnasio", "Piscina",
                      "Centro de convenciones", "Área de lavandería"],
            "Hospital": ["Recepción", "Urgencias", "Quirófanos", "Laboratorios", "Salas de recuperación",
                         "Área de cuidados intensivos", "Farmacia", "Salas de espera"],
            "Escuela": ["Dirección", "Secretaría", "Salones de clase", "Laboratorios", "Biblioteca", "Patio de recreo",
                        "Área de comedor", "Auditorios"],
            "Oficina": ["Recepción", "Cubículos", "Sala de juntas", "Área de descanso", "Comedor",
                        "Área de almacenamiento", "Departamento de TI", "Archivo"],
            "Supermercado": ["Área de frutas y verduras", "Carnicería", "Panadería", "Lácteos", "Alimentos enlatados",
                             "Productos de limpieza", "Farmacia", "Cajas"]
        }
        zone = choice(zones)
        buildings = building_names[zone]
        self.problemData = CustomMaskProblem(zone)
        self.group = SpriteGroup()
        self.buildings = SpriteGroup()
        background_image = assets.images_subnetting[f"notebook_{choice(['blue', 'red', 'brown'])}"]
        GUIImage("background", (0, 0), background_image, self.group, centered=False)
        self.base_map = GUIImage("base_map", (40, 18), assets.images_subnetting["base_map"], self.group, centered=False)
        self.map = GUIImage("map", (57, 29), assets.images_subnetting["map"], self.group, centered=False)
        # Fill houses
        selected_buildings = []
        building_positions = []
        # Draw houses
        map_padding_x = 266 / 4
        map_padding_y = 138 / 2
        while len(building_positions) < self.problemData.subnetsNeeded:
            x = randint(0, 3)
            y = randint(0, 1)
            position = (x * map_padding_x, y * map_padding_y)
            if position not in building_positions:
                building_positions.append(position)

        for y in range(2):
            for x in range(4):
                if (x * map_padding_x, y * map_padding_y) in building_positions:
                    building_name: str = choice(buildings)
                    while building_name in selected_buildings:
                        building_name = choice(buildings)
                    selected_buildings.append(building_name)
                    building_name = building_name.replace(" ", "\n")
                    building_x = 57 + (map_padding_x * x) + map_padding_x / 2
                    building_y = 29 + (map_padding_y * y) + map_padding_y / 2
                    Building((building_x, building_y), building_name, self.buildings)
                    # print(building_name)

        self.problemData.buildings = self.buildings.sprites()
        # print(self.problemData.buildings)
        self.set_stage(SubnetMask(self, self.problemData))

    def update(self) -> None:
        self.group.update()
        self.current_stage.update()

        if self.current_stage.name == "zone_stage":
            if not self.current_stage.finished:
                return
            elapsed_time = (pygame.time.get_ticks() - self.starting_time) / 1000
            self.map.deactivate()
            self.base_map.deactivate()
            self.set_stage(Results(self, elapsed_time))
        if self.current_stage.name == "results":
            if game_input.keyboard.keys["space"]:
                scene_manager.exit_scene()

    def render(self) -> None:
        self.display.fill("#242424")
        self.group.render(self.display)
        self.current_stage.render()
