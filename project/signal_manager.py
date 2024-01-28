from datetime import timedelta

import pandas as pd
import pandas_ta as ta

from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.broker_symbol import BrokerSymbol
from proalgotrader_core.protocols.enums.symbol_type import SymbolType
from proalgotrader_core.protocols.signal_manager import SignalManagerProtocol


class SignalManager(SignalManagerProtocol):
    def __init__(self, symbol: SymbolType, algorithm: Algorithm) -> None:
        self.symbol = symbol
        self.algorithm = algorithm

        self.equity_chart = None
        self.equity_symbol = None

    async def initialize(self) -> None:
        self.equity_symbol = self.algorithm.add_equity(self.symbol)

        self.equity_chart = await self.algorithm.add_chart(
            self.equity_symbol, timedelta(minutes=5)
        )

    @property
    def sma_9(self) -> pd.DataFrame | pd.Series:
        return ta.sma(close=self.equity_chart.data.close, length=9)

    @property
    def sma_14(self) -> pd.DataFrame | pd.Series:
        return ta.sma(close=self.equity_chart.data.close, length=14)

    @property
    def rsi_14(self) -> pd.DataFrame | pd.Series:
        return ta.rsi(close=self.equity_chart.data.close, length=14)

    @property
    def adx_14(self) -> pd.DataFrame | pd.Series:
        return ta.adx(
            high=self.equity_chart.data.high,
            low=self.equity_chart.data.low,
            close=self.equity_chart.data.close,
            length=14,
        )

    @property
    def ce_symbol(self) -> BrokerSymbol:
        return self.algorithm.add_option(SymbolType.NIFTY, ("weekly", 0), -2, "CE")

    @property
    def pe_symbol(self) -> BrokerSymbol:
        return self.algorithm.add_option(SymbolType.NIFTY, ("weekly", 0), +2, "PE")

    async def next(self) -> None:
        print(self.equity_chart.data)

        # between_time = self.algorithm.between_time(time(9, 20), time(15, 20))

        # if not between_time:
        #     return

        # if self.algorithm.positions:
        #     return

        # candle_signal = None

        # if (
        #     self.equity_chart.data.close.iloc[-2] > self.equity_chart.data.open.iloc[-2]
        #     and self.equity_chart.data.close.iloc[-1]
        #     > self.equity_chart.data.open.iloc[-1]
        # ):
        #     candle_signal = "long"

        # if (
        #     self.equity_chart.data.close.iloc[-2] < self.equity_chart.data.open.iloc[-2]
        #     and self.equity_chart.data.close.iloc[-1]
        #     < self.equity_chart.data.open.iloc[-1]
        # ):
        #     candle_signal = "short"

        # sma_signal = None

        # if (
        #     self.sma_9.data["SMA_9"].iloc[-2] > self.sma_14.data["SMA_14"].iloc[-2]
        #     and self.sma_9.data["SMA_9"].iloc[-1] > self.sma_14.data["SMA_14"].iloc[-1]
        # ):
        #     sma_signal = "long"

        # if (
        #     self.sma_9.data["SMA_9"].iloc[-2] < self.sma_14.data["SMA_14"].iloc[-2]
        #     and self.sma_9.data["SMA_9"].iloc[-1] < self.sma_14.data["SMA_14"].iloc[-1]
        # ):
        #     sma_signal = "short"

        # rsi_signal = None

        # if (
        #     self.rsi_14.data["RSI_14"].iloc[-1] > self.rsi_14.data["RSI_14"].iloc[-2]
        #     and self.rsi_14.data["RSI_14"].iloc[-1] > 20
        # ):
        #     rsi_signal = "long"

        # if (
        #     self.rsi_14.data["RSI_14"].iloc[-1] < self.rsi_14.data["RSI_14"].iloc[-2]
        #     and self.rsi_14.data["RSI_14"].iloc[-1] < 80
        # ):
        #     rsi_signal = "short"

        # adx_signal = False

        # if (
        #     self.adx_14.data["ADX_14"].iloc[-2] > 20
        #     and self.adx_14.data["ADX_14"].iloc[-1] > 20
        # ):
        #     adx_signal = True

        # should_long = (
        #     candle_signal == "long"
        #     and sma_signal == "long"
        #     and rsi_signal == "long"
        #     and adx_signal
        # )

        # should_short = (
        #     candle_signal == "short"
        #     and sma_signal == "short"
        #     and rsi_signal == "short"
        #     and adx_signal
        # )

        # if should_long:
        #     await self.algorithm.buy(symbol=self.ce_symbol, quantities=50)

        # if should_short:
        #     await self.algorithm.buy(symbol=self.pe_symbol, quantities=50)
