class Exercise:
    class RouterData:
        def __init__(self, data: dict):
            super().__init__()
            self.ip_route = data["ip_route"]
            self.network = data["network"]

    def __init__(self, data: dict):
        self.type = data["type"]
        self.routers = [self.RouterData(router_data) for router_data in data["routers"].values()]
        self.cables = data["cables"]

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
