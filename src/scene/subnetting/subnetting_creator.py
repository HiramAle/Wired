import random
import math
import ipaddress
import json

SUBNETTING_EXERCISES_PATH = "../../../data/scenes/subnetting"

ip_classes = {"A": 8, "B": 16, "C": 24}


def generate_random_ip() -> tuple[str, str, int]:
    selected_class = random.choice(list(ip_classes.keys()))
    default_cidr = ip_classes[selected_class]
    first_octet = "0"
    second_octet = "0"
    third_octet = "0"
    forth_octet = "0"
    match selected_class:
        case "A":
            first_octet = str(random.randint(1, 126))
        case "B":
            first_octet = str(random.randint(128, 191))
            second_octet = str(random.randint(0, 255))
        case "C":
            first_octet = str(random.randint(192, 223))
            second_octet = str(random.randint(0, 255))
            third_octet = str(random.randint(0, 255))
    random_ip = f"{first_octet}.{second_octet}.{third_octet}.{forth_octet}"

    return random_ip, selected_class, default_cidr


def generate_json_exercise(subnets_needed=random.randint(2, 8)):
    ip_str, ip_class, ip_cidr = generate_random_ip()
    network = ipaddress.IPv4Network(f"{ip_str}/{ip_cidr}")
    subnets_needed = subnets_needed
    bits_borrowed = math.ceil(math.log(subnets_needed, 2))
    custom_cidr = ip_cidr + bits_borrowed

    custom_network = ipaddress.IPv4Network(f"{ip_str}/{custom_cidr}")
    exercise_data = {
        "ip": str(network.network_address),
        "class": ip_class,
        "default_mask": str(network.netmask),
        "subnets_needed": subnets_needed,
        "custom_mask": str(custom_network.netmask),
        "subnets": {}
    }

    for index, subnet in enumerate(network.subnets(new_prefix=custom_cidr)):
        first_usable = subnet[1]
        area = {
            "id": str(subnet.network_address),
            "broadcast": str(subnet.broadcast_address),
            "first": str(first_usable)
        }
        exercise_data["subnets"][f"subnet_{index + 1}"] = area

    with open(f"{SUBNETTING_EXERCISES_PATH}/11.json", "w") as file:
        file.write(json.dumps(exercise_data))


generate_json_exercise()
