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
        broker_symbol = self.algorithm.add_equity(symbol_type=SymbolType.Index.NIFTY)

        self.risk_reward = await self.position.get_risk_reward(
            broker_symbol=broker_symbol,
            sl=20,
            tgt=60,
            tsl=5,
            on_exit=self.on_exit
        )

    async def next(self) -> None:
        print(f"{'symbol':<30} {self.position.broker_symbol.symbol_name}")
        print(f"{'ltp':<30} {self.risk_reward.broker_symbol.tick.ltp}")
        print(f"{'trailed_stoploss':<30} {self.risk_reward.trailed_stoploss}")
        print(f"{'stoploss':<30} {self.risk_reward.stoploss}")
        print(f"{'target':<30} {self.risk_reward.target}")
        print(f"{'direction':<30} {self.risk_reward.direction}")
        print("\n")

        await self.risk_reward.next()

    async def on_exit(self) -> None:
        await self.position.exit()