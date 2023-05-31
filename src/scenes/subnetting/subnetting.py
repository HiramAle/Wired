import engine.scene.scene_manager as scene_manager
from engine.scene.scene import StagedScene
from src.scenes.subnetting.subnetting_objects import *
from engine.objects.sprite import SpriteGroup
from engine.ui.image import Image
from random import choice
from src.scenes.subnetting.subnet_mask_stage import SubnetMask
from src.scenes.subnetting.results_stage import Results
from engine.playerdata import PlayerData
from engine.data import Data


class Subnetting(StagedScene):
    def __init__(self, zone_id: str):
        super().__init__("subnetting")
        self.starting_time = pygame.time.get_ticks()
        pygame.mouse.set_visible(True)
        # zones = ["Museo", "Hotel", "Hospital", "Escuela", "Oficina", "Supermercado"]
        # building_names = {
        #     "Museo": ["Galerías", "Exposiciones", "Colecciones", "Auditorios", "Tienda", "Cafetería", "Recepción",
        #               "Talleres"],
        #     "Hotel": ["Recepción", "Habitaciones", "Restaurante", "Bar", "Gimnasio", "Piscina",
        #               "Centro de convenciones", "Área de lavandería"],
        #     "Hospital": ["Recepción", "Urgencias", "Quirófanos", "Laboratorios", "Salas de recuperación",
        #                  "Área de cuidados intensivos", "Farmacia", "Salas de espera"],
        #     "Escuela": ["Dirección", "Secretaría", "Salones de clase", "Laboratorios", "Biblioteca", "Patio de recreo",
        #                 "Área de comedor", "Auditorios"],
        #     "Oficina": ["Recepción", "Cubículos", "Sala de juntas", "Área de descanso", "Comedor",
        #                 "Área de almacenamiento", "Departamento de TI", "Archivo"],
        #     "Supermercado": ["Área de frutas y verduras", "Carnicería", "Panadería", "Lácteos", "Alimentos enlatados",
        #                      "Productos de limpieza", "Farmacia", "Cajas"]
        # }
        # zone = self.zones[zone_id]
        # buildings = zone["areas"]
        # exercise_num = zone["exercise"]
        self.problemData = Data.subnetting[zone_id]
        self.group = SpriteGroup()
        self.buildings = SpriteGroup()
        background_image = Assets.images_subnetting[f"notebook_{choice(['blue', 'red', 'brown'])}"]
        Image((0, 0), background_image, self.group, centered=False)
        self.base_map = Image((40, 18), Assets.images_subnetting["base_map"], self.group, centered=False)
        self.map = Image((57, 29), Assets.images_subnetting["map"], self.group, centered=False)
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
                    building_name: str = choice(self.problemData.areas)
                    while building_name in selected_buildings:
                        building_name = choice(self.problemData.areas)
                    selected_buildings.append(building_name)
                    building_name = building_name.replace(" ", "\n")
                    building_x = 57 + (map_padding_x * x) + map_padding_x / 2
                    building_y = 29 + (map_padding_y * y) + map_padding_y / 2
                    Building((building_x, building_y), building_name, self.buildings)
                    # print(building_name)

        self.problemData.buildings = self.buildings.sprites()
        # print(self.problemData.buildings)
        self.set_stage(SubnetMask(self, self.problemData.zone_id))
        self.crossover = self.problemData.subnetsNeeded - 1
        self.direct = self.problemData.subnetsNeeded
        print(f"Subnetting will remove {self.crossover} crossover")
        print(f"Subnetting will remove {self.direct} straight")

    def update(self) -> None:
        self.group.update()
        self.current_stage.update()

        if self.current_stage.name == "zone_stage":
            if not self.current_stage.finished:
                return
            elapsed_time = (pygame.time.get_ticks() - self.starting_time) / 1000
            self.map.deactivate()
            self.base_map.deactivate()
            crossover_used = PlayerData.inventory.remove_cable("cable_crossover", self.crossover)
            straight_used = PlayerData.inventory.remove_cable("cable_straight", self.direct)
            self.set_stage(Results(self, elapsed_time, crossover_used, straight_used))

        if self.current_stage.name == "results":
            if Input.keyboard.keys["space"]:
                from engine.scene.scene_manager import SceneManager
                PlayerData.complete_task(f"subnetting_{self.problemData.zone_id}")
                SceneManager.exit_scene()

        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            from src.scenes.pause_menu.pause import Pause
            SceneManager.change_scene(Pause())

    def render(self) -> None:
        self.display.fill("#242424")
        self.group.render(self.display)
        self.current_stage.render()
