from datetime import timedelta

from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.protocols.enums.account_type import AccountType
from proalgotrader_core.protocols.enums.symbol_type import SymbolType
from proalgotrader_core.protocols.strategy import StrategyProtocol
from project.position_manager import PositionManager
from project.signal_manager import SignalManager


class Strategy(StrategyProtocol):
    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm

        self.algorithm.set_sleep_time(sleep_time=timedelta(seconds=1))

        self.algorithm.set_signal_manager(signal_manager=SignalManager)

        self.algorithm.set_position_manager(position_manager=PositionManager)

    async def initialize(self) -> None:
        await self.algorithm.set_account_type(
            account_type=AccountType.DERIVATIVE_INTRADAY
        )

        await self.algorithm.set_symbols(symbol_types=[SymbolType.Index.NIFTY])

    async def next(self) -> None:
        pass