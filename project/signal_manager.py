import pandas as pd

import pandas_ta as ta

from datetime import time, timedelta

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
    def sma_14(self):
        return self.equity_chart.add_indicator(
            "sma_14", lambda data: ta.sma(close=data.close, length=14)
        )

    @property
    def rsi(self):
        return self.equity_chart.add_indicator(
            "rsi", lambda data: ta.rsi(close=data.close, length=14)
        )

    @property
    def adx(self):
        return self.equity_chart.add_indicator(
            "adx",
            lambda data: ta.adx(
                high=data.high, low=data.low, close=data.close, length=14
            ),
        )

    @property
    def ce_symbol(self):
        return self.algorithm.add_option(
            self.equity_symbol.base_symbol.key, ("weekly", 0), -2, "CE"
        )

    @property
    def pe_symbol(self):
        return self.algorithm.add_option(
            self.equity_symbol.base_symbol.key, ("weekly", 0), -2, "PE"
        )

    @property
    def open_position_symbols(self):
        return [open_position.symbol for open_position in self.algorithm.open_positions]

    def get_quantities(self):
        return self.equity_symbol.base_symbol.lot_size * 1

    def crossover(self, first: pd.DataFrame, second: pd.DataFrame):
        return (first.iloc[-1] > second.iloc[-1]) and (first.iloc[-2] < second.iloc[-2])

    async def next(self):
        between_time = self.algorithm.between_time(time(9, 20), time(15, 15))

        if not between_time:
            return

        if not self.algorithm.open_positions:
            bullish_crossover = self.crossover(
                self.sma_9.data["SMA_9"], self.sma_14.data["SMA_14"]
            )

            bearish_crossover = self.crossover(
                self.sma_14.data["SMA_14"], self.sma_9.data["SMA_9"]
            )

            rsi_signal = (
                self.rsi.data["RSI_14"].iloc[-1] > 20
                and self.rsi.data["RSI_14"].iloc[-1] < 80
            )

            adx_signal = self.adx.data["ADX_14"].iloc[-1] > 25

            if bullish_crossover and rsi_signal and adx_signal:
                await self.algorithm.buy(
                    symbol=self.ce_symbol, quantities=self.get_quantities()
                )

            if bearish_crossover and rsi_signal and adx_signal:
                await self.algorithm.buy(
                    symbol=self.ce_symbol, quantities=self.get_quantities()
                )
