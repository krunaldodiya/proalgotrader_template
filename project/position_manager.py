from proalgotrader_protocols import Algorithm_Protocol


class PositionManager:
    def __init__(self, position, algorithm: Algorithm_Protocol) -> None:
        self.position = position
        self.algorithm = algorithm

        self.risk_reward = self.algorithm.get_risk_reward_manager(
            self.position, self.on_exit
        )

    async def initialize(self):
        await self.risk_reward.initialize(sl=20, tgt=40, tsl=10)

    async def next(self):
        print("ltp", self.risk_reward.ltp)
        print("entry_price", self.risk_reward.entry_price)
        print("stoploss", self.risk_reward.stoploss)
        print("trailing_stoploss", self.risk_reward.trailing_stoploss)
        print("target", self.risk_reward.target)
        print("trailed_stoplosses", self.risk_reward.trailed_stoplosses)
        print("\n")

        await self.risk_reward.next()

    async def on_exit(self, type):
        print("type", type)
        await self.position.exit()
