import random
import math
import ipaddress
import json
import time

SUBNETTING_EXERCISES_PATH = "../../../data/scenes/subnetting"


def random_ip() -> tuple[str, str, int]:
    ip_class = random.choice(["A", "B", "C"])
    cidr = 0
    first_octet, second_octet, third_octet, forth_octet = "0.0.0.0".split(".")
    match ip_class:
        case "A":
            first_octet = str(random.randint(1, 126))
            cidr = 8
        case "B":
            first_octet = str(random.randint(128, 191))
            second_octet = str(random.randint(0, 255))
            cidr = 16
        case "C":
            first_octet = str(random.randint(192, 223))
            second_octet = str(random.randint(0, 255))
            third_octet = str(random.randint(0, 255))
            cidr = 24
    ip = ".".join([first_octet, second_octet, third_octet, forth_octet])
    return ip, ip_class, cidr


def generate_exercise(subnets_needed) -> dict:
    ip, ip_class, cidr = random_ip()
    network = ipaddress.IPv4Network(f"{ip}/{cidr}")
    total_subnets = subnets_needed + 2
    bits_borrowed = math.ceil(math.log(total_subnets, 2))
    new_cidr = cidr + bits_borrowed
    new_network = ipaddress.IPv4Network(f"{ip}/{new_cidr}")
    exercise_data = {
        "ip": str(network.network_address),
        "class": ip_class,
        "default_mask": str(network.netmask),
        "subnets_needed": subnets_needed,
        "custom_mask": str(new_network.netmask),
        "subnets": {}
    }
    for index, subnet in enumerate(network.subnets(new_prefix=new_cidr)):
        if index == 0:
            continue
        if index > subnets_needed:
            break
        exercise_data["subnets"][f"subnet_{index}"] = {
            "id": str(subnet.network_address),
            "broadcast": str(subnet.broadcast_address),
            "first": str(subnet[1])
        }
    return exercise_data


def exercise_as_json(filename: str, exercise: dict):
    with open(f"{filename}.json", "w") as file:
        file.write(json.dumps(exercise, indent=2))


if __name__ == '__main__':
    for index, subnets in enumerate([2, 2, 2, 3, 3, 4, 5, 6, 7, 8]):
        exercise = generate_exercise(subnets)
        exercise_as_json(f"{SUBNETTING_EXERCISES_PATH}/{index + 1}", exercise)
