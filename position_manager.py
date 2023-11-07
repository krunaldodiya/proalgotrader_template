from proalgotrader_protocols import Algorithm_Protocol


class PositionManager(Algorithm_Protocol):
    def __init__(self, position):
        self.position = position

    async def next(self):
        self.position.exit()
