from proalgotrader_core.protocols.strategy import Strategy_Protocol

from proalgotrader_core.algorithm import Algorithm

from proalgotrader_core.protocols.enums.account_type import AccountType

from proalgotrader_core.protocols.enums.symbol_type import SymbolType

from project.position_manager import PositionManager

from project.signal_manager import SignalManager


class Strategy(Strategy_Protocol):
    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm

        self.algorithm.set_signal_manager(SignalManager)
        self.algorithm.set_position_manager(PositionManager)

    async def initialize(self) -> None:
        await self.algorithm.set_account_type(AccountType.DERIVATIVE_INTRADAY)
        await self.algorithm.add_symbols(symbols=[SymbolType.NIFTY])

    async def next(self) -> None:
        pass
