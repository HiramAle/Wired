import copy

import pygame
import time
from engine.input import Input
from engine.time import Time, Timer
from engine.window import Window
from engine.scene.scene import Scene
from engine.assets import Assets
from engine.ui.text import Text
from engine.ui.image import Image
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from enum import Enum
from engine.loader import Loader

interactions = SpriteGroup()
hide = SpriteGroup()


class Notification(Sprite):
    class Type(Enum):
        INCORRECT_CONFIG = "Configuración incorrecta"
        CONFIG_NOT_MATCH = "Configuración incorrecta"
        STATIC_SHORT = "Faltan comandos"
        NOT_ENABLE = "Falta enable"
        NOT_CONFIG_T = "Falta config t"
        MULTIPLE_ENABLE = "Multplies enable"
        MULTIPLE_CONFIG_T = "Multplies config t"
        BAD_IP_ROUTE = "Comando invalido.\nFormato:\nip route [ip-address]\n[mask] [interface | address]"
        RIP_SHORT = "Faltan comandos de\nRIP V2"
        NOT_ROUTER_RIP = "Faltan comandos de\nRIP V2\nFormato:\nrouter rip"
        NOT_VERSION = "Faltan comandos de\nRIP V2\nFormato:\nversion 2"
        STATIC_ROUTER_RIP = "Comando invalido.\nEnrutamiento estático\nno utliza router rip"
        STATIC_VERSION = "Comando invalido.\nEnrutamiento estático\nno utliza version 2"
        RIP_IP_ROUTE = "Comando invalido.\nRIP V2\nno utliza ip route"
        ROUTER_NOT_SELECTED = "Primero selecciona\nun router a configurar"
        CORRECT_CONFIG = "Configuración correcta"
        ENABLE_NOT_EMPTY = "El comando enable no\nnecesita parámetros"
        CONFIG_T_NOT_EMPTY = "El comando config t no\nnecesita parámetros"
        VERSION_2_NOT_EMPTY = "El comando version 2 no\nnecesita parámetros"
        ROUTER_RIP_NOT_EMPTY = "El comando router rip no\nnecesita parámetros"
        BAD_NETWORK = "Comando invalido.\nFormato:\nnetwork [ip-address]"
        BAD_COMMAND = "¿Estas seguro que se\nutiliza ese comando?"

    def __init__(self, *groups, **kwargs):
        super().__init__((344, 240), Assets.images_routing["notification"], *groups, **kwargs)
        self.pivot = self.Pivot.TOP_LEFT
        self.close_button = Sprite((166 + self.x, 6 + self.y), pygame.Surface((14, 14), pygame.SRCALPHA), interactions,
                                   centered=False)
        self.icon = Sprite((354, self.y + 6), Assets.images_routing["alert"], centered=False)
        self.title = Text((372, self.y + 7), "Advertencia", 16, Colors.SPRITE, centered=False)
        self.type = self.Type.INCORRECT_CONFIG
        self.error = Text((355, self.y + 20), str(self.type.value), 16, Colors.SPRITE, centered=False)
        self.deactivate()

    def update(self, *args, **kwargs):
        if self.close_button.clicked:
            self.deactivate()

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if not self.active:
            return
        super().render(display)
        self.close_button.render(display)
        self.icon.render(display)
        self.title.render(display)
        self.error.render(display)


class Button(Sprite):
    class State(Enum):
        NORMAL = 0
        PRESSED = 1
        HOVERED = 2

    def __init__(self, position: tuple, name: str, *groups, **kwargs):
        super().__init__(position, Assets.images_routing[f"{name}_normal"], *groups, **kwargs)
        self.name = name
        self.state = self.State.NORMAL
        self.outline_width = 2
        self.outline_color = Colors.BLUE

    def draw_outline(self, display: pygame.Surface):
        mask = pygame.mask.from_surface(self.image)
        surface = mask.to_surface(setcolor=self.outline_color, unsetcolor=(0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        if self.pivot == self.Pivot.CENTER:
            rect = surface.get_rect(center=self.position)
        elif self.pivot == self.Pivot.TOP_LEFT:
            rect = surface.get_rect(topleft=self.position)

        display.blit(surface, (rect.left + self.outline_width, rect.top))
        display.blit(surface, (rect.left - self.outline_width, rect.top))
        display.blit(surface, (rect.left, rect.top + self.outline_width))
        display.blit(surface, (rect.left, rect.top - self.outline_width))

    def update(self, *args, **kwargs):
        if self.hovered and Input.mouse.buttons["left_hold"]:
            self.image = Assets.images_routing[f"{self.name}_pressed"]
        else:
            self.image = Assets.images_routing[f"{self.name}_normal"]

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.hovered:
            self.draw_outline(display)
        super().render(display)


class ArrowButton(Button):
    class Side(Enum):
        LEFT = 0
        RIGHT = 1

    def __init__(self, position: tuple, side: Side, *groups):
        super().__init__(position, "arrow", *groups)
        self.side = side
        if side == self.Side.LEFT:
            self.flip = True, False
        self.scale = 2


class Answer(Sprite):
    def __init__(self, position: tuple, options: list[str], *groups, **kwargs):
        super().__init__(position, pygame.Surface((306, 33), pygame.SRCALPHA), *groups, **kwargs)
        self.__index = 0
        self.options = options
        self.text = Text(position, self.current_option, 32, Colors.SPRITE)
        self.left_button = ArrowButton((self.x - 130, self.y), ArrowButton.Side.LEFT, interactions, hide)
        self.right_button = ArrowButton((self.x + 130, self.y), ArrowButton.Side.RIGHT, interactions, hide)
        self.container = Sprite(position, Assets.images_routing["answer"])

    @property
    def current_option(self) -> str:
        return self.options[self.__index]

    def handle_button(self, button: ArrowButton):
        if not button.clicked:
            return
        if button.side == button.Side.LEFT:
            self.__index -= 1
            if self.__index < 0:
                self.__index = len(self.options) - 1
        elif button.side == button.Side.RIGHT:
            self.__index += 1
            if self.__index >= len(self.options):
                self.__index = 0
        self.text.text = self.current_option

    @property
    def changed(self) -> bool:
        return any([self.left_button.clicked, self.right_button.clicked])

    def update(self, *args, **kwargs):
        self.text.update()
        self.left_button.update()
        self.handle_button(self.left_button)
        self.right_button.update()
        self.handle_button(self.right_button)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.text.render(display)
        self.left_button.render(display)
        self.right_button.render(display)
        self.container.render(display)


class Cursor(Text):
    def __init__(self, position: tuple, *groups, **kwargs):
        super().__init__(position, "|", 16, Colors.WHITE, *groups, **kwargs)
        self.timer = Timer(0.5)
        self.timer.start()
        self.pivot = self.Pivot.TOP_LEFT

    def update(self, *args, **kwargs):
        if self.timer.update():
            if self.text == "|":
                self.text = ""
            elif self.text == "":
                self.text = "|"
            self.timer.start()


class CommandLine(Sprite):
    def __init__(self, options: list[Answer | Sprite], *groups, **kwargs):
        super().__init__((40, 285), Assets.images_routing["command_line"], *groups, **kwargs)
        self.text_colors = [Colors.WHITE, Colors.WHITE, Colors.RED, Colors.BLUE, Colors.YELLOW]
        self.options = options
        self.pivot = self.Pivot.TOP_LEFT
        self.strings = ["#"] + [option.text.text for option in options]
        self.texts: list[Text] = []
        self.__space_size = Assets.fonts["monogram"].width(" ", 16)
        self.render_commands()
        self.command = " ".join([option.text.text for option in options])
        self.cursor = Cursor((self.texts[-1].rect.right, 299))

    @staticmethod
    def is_ip(command: str) -> bool:
        return "." in command and "255" not in command

    @staticmethod
    def is_mask(command: str) -> bool:
        return "." in command and "255" in command

    @staticmethod
    def is_interface(command: str) -> bool:
        return "/" in command

    def render_commands(self):
        self.texts = []
        start_x = 49
        start_y = 299
        for index, text in enumerate(self.strings):
            text_obj = Text((start_x, start_y), text, 16, self.text_colors[index])
            text_obj.pivot = text_obj.Pivot.TOP_LEFT
            self.texts.append(text_obj)
            start_x += text_obj.image.get_width() + self.__space_size

    def is_command_valid(self) -> Notification.Type:
        command = self.options[0].text.text
        if command in ["enable", "config t", "version 2", "router rip"]:
            for next_command in self.options[1:]:
                if next_command.text.text != "":
                    match command:
                        case "enable":
                            return Notification.Type.ENABLE_NOT_EMPTY
                        case "config t":
                            return Notification.Type.CONFIG_T_NOT_EMPTY
                        case "version 2":
                            return Notification.Type.VERSION_2_NOT_EMPTY
                        case "router rip":
                            return Notification.Type.ROUTER_RIP_NOT_EMPTY
            return Notification.Type.CORRECT_CONFIG
        elif command == "ip route":
            have_error = False
            for index, next_command in enumerate(self.options[1:]):
                match index:
                    case 0:
                        if not self.is_ip(next_command.text.text):
                            have_error = True
                    case 1:
                        if not self.is_ip(next_command.text.text) and not self.is_mask(next_command.text.text):
                            have_error = True
                    case 2:
                        if not self.is_ip(next_command.text.text) and not self.is_interface(next_command.text.text):
                            have_error = True
            if have_error:
                return Notification.Type.BAD_IP_ROUTE
            return Notification.Type.CORRECT_CONFIG
        elif command == "network":
            have_error = False
            for index, next_command in enumerate(self.options[1:]):
                match index:
                    case 0:
                        if not self.is_ip(next_command.text.text):
                            have_error = True
                    case 1:
                        if next_command.text.text != "":
                            have_error = True
                    case 2:
                        if next_command.text.text != "":
                            have_error = True
            if have_error:
                return Notification.Type.BAD_NETWORK
            return Notification.Type.CORRECT_CONFIG
        elif command == "ip config":
            return Notification.Type.BAD_COMMAND

    def update(self, *args, **kwargs):
        self.cursor.update()
        if any([option.changed for option in self.options]):
            self.strings = [">" if self.options[0].text.text == "enable" else "#"] + [option.text.text for option in
                                                                                      self.options]
            self.render_commands()
            self.command = " ".join([option.text.text for option in self.options])
            self.cursor = Cursor((self.texts[-1].rect.right, 299))

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        for text in self.texts:
            text.render(display)
        self.cursor.render(display)


class Router(Sprite):
    def __init__(self, index: int, *groups, **kwargs):
        super().__init__((0, 0), Assets.images_routing["router"], *groups, **kwargs)
        self.selected = False
        self.index = index
        self.outline_color = Colors.BLUE
        self.outline_width = 3
        self.text = Text((self.x, self.y + 55), f"Router {index + 1}", 16, "#000000", shadow=True)
        self.text.shadow_image.set_alpha(60)
        self.default_commands = ["enable", "config t"]
        self._correct_config: RouterConfig | None = None
        self.current_config: RouterConfig | None = None
        self.configured = False

    @property
    def correct_config(self) -> "RouterConfig":
        return self._correct_config

    @correct_config.setter
    def correct_config(self, value: "RouterConfig"):
        self._correct_config = value
        if self._correct_config.config_type == "rip":
            self.default_commands += ["router rip", "version 2"]

    def check_config(self) -> Notification.Type:
        validate = self.current_config.validate()
        if validate == Notification.Type.CORRECT_CONFIG:
            compare = self.correct_config.compare(self.current_config)
            if compare == Notification.Type.CORRECT_CONFIG:
                self.configured = True
                self.outline_color = Colors.YELLOW
                return Notification.Type.CORRECT_CONFIG
            else:
                return compare
        else:
            return validate

    @property
    def x(self) -> float:
        return self.position.x

    @x.setter
    def x(self, value: float):
        self.position.x = value
        self.text.x = value

    @property
    def y(self) -> float:
        return self.position.x

    @y.setter
    def y(self, value: float):
        self.position.y = value
        self.text.y = value + 28

    def draw_outline(self, display: pygame.Surface):
        mask = pygame.mask.from_surface(self.image)
        surface = mask.to_surface(setcolor=self.outline_color, unsetcolor=(0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        rect = surface.get_rect(center=self.position)
        display.blit(surface, (rect.left + self.outline_width, rect.top))
        display.blit(surface, (rect.left - self.outline_width, rect.top))
        display.blit(surface, (rect.left, rect.top + self.outline_width))
        display.blit(surface, (rect.left, rect.top - self.outline_width))

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.selected or self.configured:
            self.draw_outline(display)
        super().render(display)
        self.text.render(display)


class Topology(Sprite):
    def __init__(self, *groups, **kwargs):
        super().__init__((320, 180), Assets.images_routing["topology"], *groups, **kwargs)
        self.min_button = Sprite((self.rect.x + 451, self.rect.y + 4), pygame.Surface((18, 18), pygame.SRCALPHA),
                                 interactions)
        self.min_button.pivot = self.min_button.Pivot.TOP_LEFT
        self.min_button.image.fill("red")
        self.minimized = False


class TaskBar(Sprite):
    def __init__(self, *groups, **kwargs):
        super().__init__((0, 332), Assets.images_routing["task_bar"], *groups, **kwargs)
        self.pivot = self.Pivot.TOP_LEFT
        self.text_time = Text((574, 331), self.get_time(), 32, Colors.WHITE)
        self.text_time.pivot = self.text_time.Pivot.TOP_LEFT
        self.topology_button = Sprite((121, 334), Assets.images_routing["xp_button_notactive"], interactions)
        self.topology_button.pivot = self.topology_button.Pivot.TOP_LEFT
        self.topology_active = False
        self.change = False
        self.topology = Topology()
        self.notification = Notification()

    @staticmethod
    def get_time() -> str:
        return time.strftime("%H:%M")

    def notify(self, notification: Notification.Type):
        self.notification.type = notification
        self.notification.error.text = str(notification.value)
        self.notification.activate()
        if notification == Notification.Type.CORRECT_CONFIG:
            self.notification.icon.image = Assets.images_routing["check_mark"]
            self.notification.title.text = "Felicidades"

    def update(self, *args, **kwargs):
        self.change = False
        self.topology.update()
        self.notification.update()
        self.text_time.text = self.get_time()
        if self.topology_button.clicked:
            self.topology_active = not self.topology_active
            self.change = True

        if self.change and self.topology_active:
            self.topology_button.image = Assets.images_routing["xp_button_active"]
            self.topology.activate()
        elif (self.change and not self.topology_active) or (self.topology.min_button.clicked and self.topology.active):
            self.topology_button.image = Assets.images_routing["xp_button_notactive"]
            self.topology.deactivate()
            self.topology_active = False

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.text_time.render(display)
        self.topology_button.render(display)
        self.topology.render(display)
        self.notification.render(display)


class Console(Sprite):
    def __init__(self, *group, **kwargs):
        super().__init__((432, 48), Assets.images_routing["console_window"], *group, **kwargs)
        self.commands: list[list[Text]] = []
        self.pivot = self.Pivot.TOP_LEFT
        self.render_commands()
        self.__space_width = Assets.fonts["monogram"].width(" ", 16)
        self.__space_height = Assets.fonts["monogram"].height(" ", 16)

    def get_commands(self) -> list[str]:
        commands = []
        for command in self.commands:
            commands.append(" ".join([text.text for text in command[1:] if text.text != ""]))
        return commands

    def render_commands(self):
        start_x = 445
        y = 86
        x = start_x
        for command in self.commands:
            for text in command:
                if x + text.rect.width > 640:
                    x = start_x + Assets.fonts["monogram"].width("# ", 16)
                    y += self.__space_height
                text.x = x
                text.y = y
                x += text.rect.width + self.__space_width
            y += self.__space_height + 8
            x = start_x

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        for command in self.commands:
            for text in command:
                text.render(display)


class Exercise:
    class RouterData:
        def __init__(self, data: dict):
            super().__init__()
            self.ip_route = data["ip_route"]
            self.network = data["network"]

    def __init__(self, data: dict):
        self.type = data["type"]
        self.routers = [self.RouterData(router_data) for router_data in data["routers"].values()]

    def get_router_config(self, index: int):
        router_data = self.routers[index]
        commands = ["enable", "config t"]
        for ip_route in router_data.ip_route:
            commands.append(f"ip route {ip_route}")
        for network in router_data.network:
            commands.append(f"network {network}")
        return commands

    def get_answers(self):
        answers = [[], [], []]
        for router_config in self.routers:
            for command in router_config.ip_route:
                for index, text in enumerate(command.split(" ")):
                    if text in answers[index]:
                        continue
                    answers[index].append(text)
            for command in router_config.network:
                for index, text in enumerate(command.split(" ")):
                    if text in answers[index]:
                        continue
                    answers[index].append(text)
        return answers


class RouterConfig:
    def __init__(self, config: list[str], config_type: str):
        self.config = config
        self.config_type = config_type
        self.enable = False
        self.config_t = False
        self.rip = False
        self.version = False
        self.ip_route = []
        self.network = []

        for command in config:
            if command.startswith("enable"):
                self.enable = True
            elif command.startswith("config t"):
                self.config_t = True
            elif command.startswith("router rip"):
                self.rip = True
            elif command.startswith("version 2"):
                self.version = True
            elif command.startswith("ip route"):
                self.ip_route.append(command)
            elif command.startswith("network"):
                self.network.append(command)

    def __repr__(self):
        return self.config

    def validate(self) -> Notification.Type:
        # General validation
        if len(self.config) < 2:
            print("Configure size below 2")
            return Notification.Type.STATIC_SHORT
        if self.config[0] != "enable":
            print("Doesnt enter enable mode")
            return Notification.Type.NOT_ENABLE
        if self.config[1] != "config t":
            print("Doesnt enter config t mode")
            return Notification.Type.NOT_CONFIG_T
        if self.config.count("enable") != 1:
            print("Multiple enable")
            return Notification.Type.MULTIPLE_ENABLE
        if self.config.count("config t") != 1:
            print("Multiple config t")
            return Notification.Type.MULTIPLE_CONFIG_T
        # RIP specific validation
        if self.config_type == "rip":
            if len(self.config) < 4:
                print("RIP: Configure size below 4")
                return Notification.Type.RIP_SHORT
            if self.config[2] != "router rip":
                print("RIP: Doesnt enter rip mode")
                return Notification.Type.NOT_ROUTER_RIP
            if self.config[3] != "version 2":
                print("RIP: Doesnt specify version")
                return Notification.Type.NOT_VERSION
        # Static specific validation
        elif self.config_type == "static":
            if "router rip" in self.config:
                return Notification.Type.STATIC_ROUTER_RIP
            if "version 2" in self.config:
                return Notification.Type.STATIC_VERSION

        return Notification.Type.CORRECT_CONFIG

    def compare(self, config: "RouterConfig") -> Notification.Type:
        if sorted(self.ip_route) != sorted(config.ip_route):
            return Notification.Type.CONFIG_NOT_MATCH
        if sorted(self.network) != sorted(config.network):
            return Notification.Type.CONFIG_NOT_MATCH
        return Notification.Type.CORRECT_CONFIG


class Routing(Scene):
    def __init__(self):
        super().__init__("routing")
        self.exercise = Exercise(Loader.load_json("data/scenes/routing/2.json"))
        self.correct = RouterConfig(self.exercise.get_router_config(0), self.exercise.type)
        self.static = SpriteGroup()
        self.answers = SpriteGroup()
        self.routers = SpriteGroup()
        self.buttons = SpriteGroup()
        # Window title
        if self.exercise.type == "rip":
            title = "RIP V2"
        else:
            title = "Enrutamiento estático por "
            if "interface" in self.exercise.type:
                title += "interfaz"
            elif "jump" in self.exercise.type:
                title += "siguiente salto"
            elif "default" in self.exercise.type:
                title += "default"
        self.title = Text((40, 6), title, 32, Colors.SPRITE, self.buttons, centered=False, shadow=True,
                          shadow_color="#5f5f5f")
        self.title.shadow_image.set_alpha(120)
        self.title._shadow_padding = 1.75
        Image((0, 0), Assets.images_routing["background"], self.static, centered=False)
        Image((21, 45), Assets.images_routing["router_area"], self.static, centered=False)
        Answer((225, 140), ["ip route", "ip config", "network", "enable", "config t", "router rip", "version 2"],
               self.answers)
        Answer((225, 181), ["192.45.12.0", "34.2.67.3", ""] + self.exercise.get_answers()[0], self.answers)
        Answer((225, 222), ["255.255.0.0", "255.255.255.0", ""] + self.exercise.get_answers()[1], self.answers)
        Answer((225, 263), ["S0/1/0", "10.0.0.0", ""] + self.exercise.get_answers()[2], self.answers)
        # Routers
        for i in range(len(self.exercise.routers)):
            router = Router(i, self.routers, interactions, hide)
            router.correct_config = RouterConfig(self.exercise.get_router_config(i), self.exercise.type)

        padding = 10
        router_width = sum(router.rect.width for router in self.routers.sprites())
        total_padding = (len(self.routers.sprites()) - 1) * padding
        total_width = router_width + total_padding
        start_x = 21 + 33 + 202 - (total_width / 2)
        for index, router in enumerate(self.routers.sprites()):
            router.y = 75
            router.x = start_x + ((67 + padding) * index)
        self.selected_router: Router | None = None
        # Command Line
        self.command_line = CommandLine(self.answers.sprites(), self.static)
        # Taskbar
        self.taskbar = TaskBar()
        # Console
        self.console = Console(self.static)
        # Buttons
        self.enter = Button((377, 289), "enter", self.buttons, interactions, hide)
        self.enter.pivot = self.enter.Pivot.TOP_LEFT
        self.write = Button((434, 289), "write", self.buttons, interactions, hide)
        self.write.pivot = self.enter.Pivot.TOP_LEFT
        self.erase = Button((531, 289), "erase", self.buttons, interactions, hide)
        self.erase.pivot = self.enter.Pivot.TOP_LEFT

    def update(self) -> None:
        self.answers.update()
        self.static.update()
        self.taskbar.update()
        self.buttons.update()

        if any([sprite.hovered for sprite in interactions.sprites()]):
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
            else:
                Window.set_cursor("hand")
        else:
            Window.set_cursor("arrow")

        for router in self.routers.sprites():
            router: Router
            if not router.clicked or router.configured:
                continue
            if self.selected_router:
                self.selected_router.selected = False
                self.correct = RouterConfig(self.exercise.get_router_config(router.index), self.exercise.type)
            self.selected_router = router
            router.selected = True

        if self.enter.clicked:
            notification = self.command_line.is_command_valid()
            if not self.selected_router:
                self.taskbar.notify(Notification.Type.ROUTER_NOT_SELECTED)
            elif notification != Notification.Type.CORRECT_CONFIG:
                self.taskbar.notify(notification)
            else:
                self.console.commands.append([text.__copy__() for text in self.command_line.texts])
                self.console.render_commands()

        if self.erase.clicked:
            self.console.commands = self.console.commands[:-1]

        if self.write.clicked:
            if not self.selected_router:
                self.taskbar.notify(Notification.Type.ROUTER_NOT_SELECTED)
                return
            self.selected_router.current_config = RouterConfig(self.console.get_commands(), self.exercise.type)
            self.taskbar.notify(self.selected_router.check_config())
            print(self.taskbar.notification.type)
            if self.selected_router.configured:
                self.selected_router = None
                self.console.commands = []

    def render(self) -> None:
        self.static.render(self.display)
        self.answers.render(self.display)
        self.routers.render(self.display)
        self.buttons.render(self.display)

        self.taskbar.render(self.display)
