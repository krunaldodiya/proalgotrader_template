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
    def rsi_14(self):
        return self.equity_chart.add_indicator(
            "rsi_14", lambda data: ta.rsi(close=data.close, length=14)
        )

    @property
    def adx_14(self):
        return self.equity_chart.add_indicator(
            "adx_14",
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
        between_time = self.algorithm.between_time(time(9, 20), time(15, 20))

        if not between_time:
            return

        if not self.algorithm.open_positions:
            candle_signal = None

            if (
                self.equity_chart.data.close.iloc[-2]
                > self.equity_chart.data.open.iloc[-2]
                and self.equity_chart.data.close.iloc[-1]
                > self.equity_chart.data.open.iloc[-1]
            ):
                candle_signal = "long"

            if (
                self.equity_chart.data.close.iloc[-2]
                < self.equity_chart.data.open.iloc[-2]
                and self.equity_chart.data.close.iloc[-1]
                < self.equity_chart.data.open.iloc[-1]
            ):
                candle_signal = "short"

            sma_signal = None

            if (
                self.sma_9.data["SMA_9"].iloc[-2] > self.sma_14.data["SMA_14"].iloc[-2]
                and self.sma_9.data["SMA_9"].iloc[-1]
                > self.sma_14.data["SMA_14"].iloc[-1]
            ):
                sma_signal = "long"

            if (
                self.sma_9.data["SMA_9"].iloc[-2] < self.sma_14.data["SMA_14"].iloc[-2]
                and self.sma_9.data["SMA_9"].iloc[-1]
                < self.sma_14.data["SMA_14"].iloc[-1]
            ):
                sma_signal = "short"

            rsi_signal = None

            if (
                self.rsi_14.data["RSI_14"].iloc[-1]
                > self.rsi_14.data["RSI_14"].iloc[-2]
                and self.rsi_14.data["RSI_14"].iloc[-1] > 20
            ):
                rsi_signal = "long"

            if (
                self.rsi_14.data["RSI_14"].iloc[-1]
                < self.rsi_14.data["RSI_14"].iloc[-2]
                and self.rsi_14.data["RSI_14"].iloc[-1] < 80
            ):
                rsi_signal = "short"

            adx_signal = False

            if (
                self.adx_14.data["ADX_14"].iloc[-2] > 20
                and self.adx_14.data["ADX_14"].iloc[-1] > 20
            ):
                adx_signal = True

            should_long = (
                candle_signal == "long"
                and sma_signal == "long"
                and rsi_signal == "long"
                and adx_signal
            )

            should_short = (
                candle_signal == "short"
                and sma_signal == "short"
                and rsi_signal == "short"
                and adx_signal
            )

            print("candle_signal", candle_signal)
            print("sma_signal", sma_signal)
            print("rsi_signal", rsi_signal)
            print("adx_signal", adx_signal)
            print("\n")

            if should_long:
                await self.algorithm.buy(
                    symbol=self.ce_symbol, quantities=self.get_quantities()
                )

            if should_short:
                await self.algorithm.buy(
                    symbol=self.pe_symbol, quantities=self.get_quantities()
                )
