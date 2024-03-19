import math
import pandas as pd
import pandas_ta as ta

from datetime import timedelta, time
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.broker_symbol import BrokerSymbol
from proalgotrader_core.protocols.enums.symbol_type import SymbolType
from proalgotrader_core.protocols.signal_manager import SignalManagerProtocol


class SignalManager(SignalManagerProtocol):
    def __init__(self, symbol_type: SymbolType, algorithm: Algorithm) -> None:
        self.symbol_type = symbol_type
        self.algorithm = algorithm

        self.equity_chart = None
        self.equity_symbol = None

    async def initialize(self) -> None:
        self.equity_symbol = self.algorithm.add_equity(symbol_type=self.symbol_type)

        self.equity_chart = await self.algorithm.add_chart(
            self.equity_symbol, timedelta(minutes=5)
        )

        min_capital_per_lot = 30_000

        number_lots = math.floor(self.algorithm.broker_manager.current_capital / min_capital_per_lot)

        lot_size = self.equity_symbol.base_symbol.lot_size

        self.tradable_quantities = number_lots * lot_size

    @property
    def supertrend_14(self) -> pd.DataFrame | pd.Series:
        return ta.supertrend(
            high=self.equity_chart.data.high,
            low=self.equity_chart.data.low,
            close=self.equity_chart.data.close,
            length=14,
            multiplier=1,
        )

    @property
    def sma_7(self) -> pd.DataFrame | pd.Series:
        return ta.sma(close=self.equity_chart.data.close, length=7)

    @property
    def sma_14(self) -> pd.DataFrame | pd.Series:
        return ta.sma(close=self.equity_chart.data.close, length=14)

    @property
    def sma_21(self) -> pd.DataFrame | pd.Series:
        return ta.sma(close=self.equity_chart.data.close, length=21)

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
        return self.algorithm.add_option(SymbolType.Index.NIFTY, ("weekly", 0), -2, "CE")

    @property
    def pe_symbol(self) -> BrokerSymbol:
        return self.algorithm.add_option(SymbolType.Index.NIFTY, ("weekly", 0), +2, "PE")

    async def next(self) -> None:
        between_time = self.algorithm.between_time(time(9, 20), time(15, 20))

        if not between_time:
            return
        
        if self.tradable_quantities == 0:
            print("Insufficient Balance", self.algorithm.broker_manager.current_capital)
            return

        if self.algorithm.positions:
            return
        
        max_daily_loss = self.algorithm.broker_manager.initial_capital * 0.05
        max_daily_profit = self.algorithm.broker_manager.initial_capital * 0.15
        
        if self.algorithm.total_pnl['loss'] >= max_daily_loss:
            return
        
        if self.algorithm.total_pnl['profit'] >= max_daily_profit:
            return
        
        supertrend_signal = None

        if (
            self.equity_chart.data.close.iloc[-2] > self.supertrend_14["SUPERT_14_1.0"].iloc[-2]
        ):
            supertrend_signal = "long"

        if (
            self.equity_chart.data.close.iloc[-2] < self.supertrend_14["SUPERT_14_1.0"].iloc[-2]
        ):
            supertrend_signal = "short"

        sma_signal = None

        if (
            self.sma_7.iloc[-2] > self.sma_14.iloc[-2] > self.sma_21.iloc[-2]
        ):
            sma_signal = "long"

        if (
            self.sma_7.iloc[-2] < self.sma_14.iloc[-2] < self.sma_21.iloc[-2]
        ):
            sma_signal = "short"

        rsi_signal = False

        if 30 < self.rsi_14.iloc[-2] < 70:
            rsi_signal = True

        adx_signal = False

        if 25 < self.adx_14["ADX_14"].iloc[-2] < 50:
            adx_signal = True

        should_long = (
            supertrend_signal == "long"
            and sma_signal == "long"
            and rsi_signal
            and adx_signal
        )

        should_short = (
            supertrend_signal == "short"
            and sma_signal == "short"
            and rsi_signal
            and adx_signal
        )

        print("supertrend_signal",supertrend_signal)
        print("sma_signal",sma_signal)
        print("rsi_signal",rsi_signal)
        print("adx_signal",adx_signal)
        print("\n")

        if should_long:
            await self.algorithm.buy(broker_symbol=self.ce_symbol, quantities=self.tradable_quantities)

        if should_short:
            await self.algorithm.buy(broker_symbol=self.pe_symbol, quantities=self.tradable_quantities)