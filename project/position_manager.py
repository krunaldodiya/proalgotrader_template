from proalgotrader_core.protocols.position_manager import PositionManager_Protocol

from proalgotrader_core.algorithm import Algorithm

from proalgotrader_core.position import Position


class PositionManager(PositionManager_Protocol):
    def __init__(self, algorithm: Algorithm, position: Position) -> None:
        self.algorithm = algorithm
        self.position = position

    async def initialize(self) -> None:
        self.risk_reward = await self.position.get_risk_reward(
            symbol=self.position.broker_symbol,
            direction="long",
            sl=20,
            tgt=40,
            tsl=10,
        )

    async def next(self) -> None:
        await self.risk_reward.next()
