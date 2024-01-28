from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.protocols.enums.account_type import AccountType
from proalgotrader_core.protocols.enums.symbol_type import SymbolType
from proalgotrader_core.protocols.strategy import StrategyProtocol
from project.position_manager import PositionManagerProtocol
from project.signal_manager import SignalManager


class Strategy(StrategyProtocol):
    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm

        self.algorithm.set_signal_manager(
            symbols=[SymbolType.NIFTY], signal_manager=SignalManager
        )

        self.algorithm.set_position_manager(position_manager=PositionManagerProtocol)

    async def initialize(self) -> None:
        await self.algorithm.set_account_type(AccountType.DERIVATIVE_INTRADAY)

    async def next(self) -> None:
        pass
