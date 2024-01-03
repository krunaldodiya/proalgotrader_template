import pandas_ta as ta

from datetime import timedelta

from proalgotrader_protocols import Algorithm_Protocol


class SignalManager:
    def __init__(self, symbol_key: str, algorithm: Algorithm_Protocol) -> None:
        self.symbol_key = symbol_key
        self.algorithm = algorithm

    async def initialize(self):
        self.equity_symbol = self.algorithm.add_equity(self.symbol_key)

        self.equity_chart = await self.algorithm.add_chart(
            self.equity_symbol, timedelta(minutes=5)
        )

    @property
    def sma_9(self):
        return self.equity_chart.add_indicator(
            "sma_9", lambda data: ta.sma(close=data.close, length=9)
        )

    @property
    def ce_symbol(self):
        return self.algorithm.add_option(
            self.equity_symbol.base_symbol.key, ("weekly", 0), -2, "CE"
        )

    @property
    def open_position_symbols(self):
        return [open_position.symbol for open_position in self.algorithm.open_positions]

    async def next(self):
        if not self.algorithm.open_positions:
            quantities = self.equity_symbol.base_symbol.lot_size * 1
            await self.algorithm.buy(symbol=self.ce_symbol, quantities=quantities)
