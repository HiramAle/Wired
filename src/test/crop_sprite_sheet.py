import os.path
import time
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))
display = pygame.Surface((640, 320))
clock = pygame.time.Clock()
dt = 0.2
pygame.display.set_caption("character creation")

sprite_sheet_data = {
    "base": {"right": 1, "up": 1, "left": 1, "down": 1},
    "idle": {"right": 6, "up": 6, "left": 6, "down": 6},
    "walk": {"right": 6, "up": 6, "left": 6, "down": 6},
    "sleep": {"down": 6},
    "sit_1": {"right": 6, "left": 6},
    "sit_2": {"right": 6, "left": 6},
    "phone": {"down": 12},
    "book": {"down": 12}
}

body = pygame.image.load("../../assets/character_creation/bodies/body_0.png").convert_alpha()
hairstyle = pygame.image.load("../../assets/character_creation/hairstyles/hairstyle_28_1.png").convert_alpha()
eyes = pygame.image.load("../../assets/character_creation/eyes/eyes_0.png").convert_alpha()
outfit = pygame.image.load("../../assets/character_creation/outfits/outfit_0_0.png").convert_alpha()
# sprites = {key: {direction: [] for direction in value.keys()} for key, value in sprite_sheet_data.items()}
body_idle = {direction: [] for direction in sprite_sheet_data.get("idle").keys()}
hairstyle_idle = {direction: [] for direction in sprite_sheet_data.get("idle").keys()}
eyes_idle = {direction: [] for direction in sprite_sheet_data.get("idle").keys()}
outfit_idle = {direction: [] for direction in sprite_sheet_data.get("idle").keys()}
sprite_height = 48
sprite_width = 32
crop_height = 64
crop_width = 32
font = pygame.Font("../../assets/fonts/monogram.ttf", 32)
# Selector
categories = {
    "body_color": 0,
    "hairstyle_type": 0,
    "hairstyle_color": 0,
    "eyes_color": 0,
    "outfit_type": 0,
    "outfit_color": 0
}
body_color = 0
hairstyle_type = 0
hairstyle_color = 0
eyes_color = 0
outfit_type = 0
outfit_color = 0

# categories = ["body_color", "hairstyle_type", "hairstyle_color", "eyes_color", "outfit_type", "outfit_color"]
category_index = 0


class Animation:
    def __init__(self, frames: list[pygame.Surface]):
        self.frames = frames
        self.frame_index = 0
        self.total_frames = len(frames)
        self.last_frame_index = len(frames) - 1
        self.speed = 8

    def play(self) -> pygame.Surface:
        self.frame_index += self.speed * dt

        if self.frame_index > self.last_frame_index:
            self.frame_index = 0

        return self.frames[int(self.frame_index)]


def rename():
    path = "../../assets/character_creation/outfits"
    for filename in sorted(os.listdir(path)):
        outfit_type = int(str(filename.split("_")[1]))
        outfit_color = int(str(filename.split("_")[3]).split(".")[0])
        new_filename = f"outfit_{outfit_type - 1}_{outfit_color - 1}.png"
        # eye_color = int(str(filename.split("_")[2].split(".")[0]))
        # new_filename = f"eyes_{eye_color - 1}.png"
        os.rename(f"{path}/{filename}", f"{path}/{new_filename}")


def directory_generator():
    start_time = time.time()
    paths = {
        "bodies": "../../assets/character_creation/bodies",
        "eyes": "../../assets/character_creation/eyes",
        "hairstyles": "../../assets/character_creation/hairstyles",
        "outfits": "../../assets/character_creation/outfits"
    }
    files = {option: {} for option in paths.keys()}

    for option, path in paths.items():
        for filename in sorted(os.listdir(path)):
            if option in ["bodies", "eyes"]:
                color = filename.split("_")[1].split(".")[0]
                sprite_sheet = pygame.image.load(f"{path}/{filename}").convert_alpha()
                files[option][color] = export_animation_frames(sprite_sheet)

            elif option in ["hairstyles", "outfits"]:
                type = filename.split("_")[1]
                color = filename.split("_")[2].split(".")[0]
                if type not in files[option]:
                    files[option][type] = {}
                sprite_sheet = pygame.image.load(f"{path}/{filename}").convert_alpha()
                files[option][type][color] = export_animation_frames(sprite_sheet)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución: {elapsed_time} segundos")
    return files

    # for option in files.keys():
    #     print(option)
    #     if option in ["bodies", "eyes"]:
    #         for color in files[option].keys():
    #             print(f"├─ {color}")
    #             for action in files[option][color].keys():
    #                 print(f"│  ├─ {action}")
    #                 for direction in files[option][color][action].keys():
    #                     if direction == list(files[option][color][action].keys())[-1]:
    #                         print(f"│  │  └─ {direction}: {files[option][color][action][direction]}")
    #                     else:
    #                         print(f"│  │  ├─ {direction}: {files[option][color][action][direction]}")
    #     elif option in ["hairstyles", "outfits"]:
    #         for type in files[option].keys():
    #             print(f"├─ {type}")
    #             for color in files[option][type].keys():
    #                 print(f"│  ├─ {color}")
    #                 for action in files[option][type][color].keys():
    #                     print(f"│  │  ├─ {action}")
    #                     for direction in files[option][type][color][action].keys():
    #                         print(f"│  │  │  ├─ {direction}: {files[option][type][color][action][direction]}")


def get_frames_old(action: str):
    column = 0
    for direction, frames in sprite_sheet_data.get(action).items():
        for frame in range(frames):
            x_crop = column * crop_width
            y_crop = 16 + (crop_height * list(sprite_sheet_data.keys()).index(action))
            # Body
            body_image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            body_image.blit(body, (0, 0), (x_crop, y_crop, crop_width, crop_height))
            body_idle[direction].append(body_image)
            # Hairstyle
            hairstyle_image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            hairstyle_image.blit(hairstyle, (0, 0), (x_crop, y_crop, crop_width, crop_height))
            hairstyle_idle[direction].append(hairstyle_image)
            # Eyes
            eyes_image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            eyes_image.blit(eyes, (0, 0), (x_crop, y_crop, crop_width, crop_height))
            eyes_idle[direction].append(eyes_image)
            # Outfit
            outfit_image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            outfit_image.blit(outfit, (0, 0), (x_crop, y_crop, crop_width, crop_height))
            outfit_idle[direction].append(outfit_image)
            column += 1


def get_frames(sprite_sheet: pygame.Surface, action: str) -> list:
    column = 0
    frames_list = []
    for direction, frames in sprite_sheet_data.get(action).items():
        for frame in range(frames):
            x_crop = column * crop_width
            y_crop = 16 + (crop_height * list(sprite_sheet_data.keys()).index(action))
            image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            image.blit(sprite_sheet, (0, 0), (x_crop, y_crop, crop_width, crop_height))
            frames_list.append(image)
            column += 1
    return frames_list


def export_animation_frames_old():
    row = 0
    column = 0
    for animation, directions in sprite_sheet_data.items():
        for direction, frames in directions.items():
            directory = f"../../sprites/{animation}/{direction}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            for frame in range(frames):
                x_crop = column * crop_width
                y_crop = 16 + (row * crop_height)
                image = pygame.Surface((sprite_width, sprite_height))
                image.set_colorkey(0)
                image.blit(body, (0, 0), (x_crop, y_crop, crop_width, crop_height))
                sprites[animation][direction].append(image)
                file_name = f"{animation}_{direction}_{frame}.png"
                pygame.image.save(image, f"{directory}/{file_name}")
                column += 1
        row += 1
        column = 0


def export_animation_frames(sprite_sheet: pygame.Surface) -> dict:
    animations = {action: {direction: [] for direction in value.keys()} for action, value in sprite_sheet_data.items()}
    row = 0
    column = 0
    for animation, directions in sprite_sheet_data.items():
        for direction, frames in directions.items():
            for frame in range(frames):
                x_crop = column * crop_width
                y_crop = 16 + (row * crop_height)
                image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x_crop, y_crop, crop_width, crop_height))
                animations[animation][direction].append(image)
                column += 1
        row += 1
        column = 0
    return animations


get_frames_old("sit_1")
sprites = directory_generator()


def get_animation(category: str, action: str, direction, option=0, color=0, frame=0) -> Animation:
    animation = None
    if category in ["bodies", "eyes"]:
        animation = Animation(sprites[category][str(color)][action][direction])
    elif category in ["hairstyles", "outfits"]:
        animation = Animation(sprites[category][str(option)][str(color)][action][direction])
    if frame != 0:
        animation.frame_index = frame
    return animation


class Mono:
    def __init__(self, cuerpo, ogos, peinao, color_peinao, oufis, color_oufis):
        # Data
        self.cuerpo_frames = sprites["bodies"][str(cuerpo)]["idle"]
        self.ogos_frames = sprites["eyes"][str(ogos)]["idle"]
        self.peinao_frames = sprites["hairstyles"][str(peinao)][str(color_peinao)]["idle"]
        self.oufis_frames = sprites["outfits"][str(oufis)][str(color_oufis)]["idle"]
        self.peinao = peinao
        self.oufis = oufis
        # Animation
        self.last_frame_index = len(self.peinao_frames["down"]) - 1
        self.frame_index = 0
        self.direction = "down"
        self.animation_speed = 8
        self.position = 320, 180

    @property
    def image(self) -> pygame.Surface:
        image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        image.blit(self.cuerpo_frames[self.direction][int(self.frame_index)], (0, 0))
        image.blit(self.oufis_frames[self.direction][int(self.frame_index)], (0, 0))
        image.blit(self.peinao_frames[self.direction][int(self.frame_index)], (0, 0))
        image.blit(self.ogos_frames[self.direction][int(self.frame_index)], (0, 0))
        return image

    def update(self):
        self.frame_index += self.animation_speed * dt

        if self.frame_index > self.last_frame_index:
            self.frame_index = 0

    def render(self, display: pygame.Surface):
        display.blit(self.image, self.position)


body_animation = get_animation("bodies", "idle", "down", color=8)
eyes_animation = get_animation("eyes", "idle", "down")
hairstyle_animation = get_animation("hairstyles", "idle", "down")
outfit_animation = get_animation("outfits", "idle", "down")

# UI
# category_text = font.render(list(sprites.keys())[])
mono = Mono(1, 1, 1, 1, 1, 1)
selectable_colors = []

position_x = 0
position_y = 0

while True:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                mono.direction = "left"
            elif keys[pygame.K_d]:
                mono.direction = "right"
            elif keys[pygame.K_w]:
                mono.direction = "up"
            elif keys[pygame.K_s]:
                mono.direction = "down"

            if keys[pygame.K_q]:
                category_index -= 1
            elif keys[pygame.K_e]:
                category_index += 1

            if keys[pygame.K_SPACE]:
                print(display.get_at((position_x, position_y)))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                categories[list(categories.keys())[category_index]] -= 1
            elif event.button == 3:
                categories[list(categories.keys())[category_index]] += 1
                # ["body_color", "hairstyle_type", "hairstyle_color", "eyes_color", "outfit_type", "outfit_color"]
            match list(categories.keys())[category_index]:
                case "body_color":
                    mono.cuerpo_frames = sprites["bodies"][str(categories[list(categories.keys())[category_index]])][
                        "idle"]
                case "eyes_color":
                    mono.ogos_frames = sprites["eyes"][str(categories[list(categories.keys())[category_index]])][
                        "idle"]
                case "hairstyle_type":
                    mono.peinao_frames = \
                        sprites["hairstyles"][str(categories[list(categories.keys())[category_index]])]["0"]["idle"]
                case "hairstyle_color":
                    mono.peinao_frames = \
                        sprites["hairstyles"][str(mono.peinao)][
                            str(categories[list(categories.keys())[category_index]])]["idle"]

                case "outfit_type":
                    mono.oufis_frames = \
                        sprites["outfits"][str(categories[list(categories.keys())[category_index]])]["0"]["idle"]

    display.fill("#242424")

    mouse_x, mouse_y = pygame.mouse.get_pos()
    position_x = int(mouse_x / 1280 * 640)
    position_y = int(mouse_y / 720 * 360)

    mono.update()
    mono.render(display)

    display.blit(font.render(list(categories.keys())[category_index], False, "#f2f2f2"), (320, 230))
    # rect.fill(mono.image.get_at((16, 8)))
    colors = sprites["hairstyles"][str(categories["hairstyle_type"])]
    for index, color in enumerate(colors.keys()):
        image = colors[color]["idle"]["left"][0]
        pantone = pygame.Surface((16, 16))
        pantone.fill(image.get_at((16, 8)))

        display.blit(pantone, (100, 10 + index * 20))

    # display.blit(body_animation.play(), (50, 50))
    # display.blit(outfit_animation.play(), (50, 50))
    # display.blit(hairstyle_animation.play(), (50, 50))
    # display.blit(eyes_animation.play(), (50, 50))

    # offset = 0
    # for direction, frames in hairstyle_idle.items():
    #     for index, frame in enumerate(frames):
    #         display.blit(body_idle[direction][index], (offset * 32, 100))
    #         display.blit(outfit_idle[direction][index], (offset * 32, 100))
    #         display.blit(frame, (offset * 32, 100))
    #         display.blit(eyes_idle[direction][index], (offset * 32, 100))
    #
    #         offset += 1

    # Update Display
    screen.blit(pygame.transform.scale(display, (1280, 720)), (0, 0))
    pygame.display.update()
    dt = clock.tick() / 1000
