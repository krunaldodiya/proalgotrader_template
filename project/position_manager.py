from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.position import Position
from proalgotrader_core.protocols.enums.symbol_type import SymbolType
from proalgotrader_core.protocols.position_manager import PositionManagerProtocol
from proalgotrader_core.risk_reward import RiskReward


class PositionManager(PositionManagerProtocol):
    def __init__(self, algorithm: Algorithm, position: Position) -> None:
        self.algorithm = algorithm
        self.position = position

        self.risk_reward: RiskReward | None = None

    async def initialize(self) -> None:
        broker_symbol = self.algorithm.add_equity(symbol_type=SymbolType.NIFTY)

        self.risk_reward = await self.position.get_risk_reward(
            broker_symbol=broker_symbol,
            direction="long",
            sl=20,
            tgt=40,
            tsl=10,
        )

    async def next(self) -> None:
        await self.risk_reward.next()
