from proalgotrader_protocols import Algorithm_Protocol
from proalgotrader_protocols.enums.account_type import AccountType

from project.signal_manager import SignalManager
from project.position_manager import PositionManager


class Strategy:
    def __init__(self, algorithm: Algorithm_Protocol) -> None:
        self.algorithm = algorithm

    def get_signal_manager(self):
        return SignalManager

    def get_position_manager(self):
        return PositionManager

    async def initialize(self):
        await self.algorithm.set_account_type(AccountType.DERIVATIVE_INTRADAY)

        await self.algorithm.add_symbols(["NIFTY"])
