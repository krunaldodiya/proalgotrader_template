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

        self.max_daily_loss_percent = self.algorithm.broker_manager.initial_capital * 0.03

        self.max_daily_profit_percent = self.algorithm.broker_manager.initial_capital * 0.15

        self.min_capital_per_lot = 30_000

        number_lots = math.floor(self.algorithm.broker_manager.current_capital / self.min_capital_per_lot)

        lot_size = self.equity_symbol.base_symbol.lot_size

        self.tradable_quantities = number_lots * lot_size

    @property
    def supertrend_14_2(self) -> pd.DataFrame | pd.Series:        
        data = ta.supertrend(
            high=self.equity_chart.data.high,
            low=self.equity_chart.data.low,
            close=self.equity_chart.data.close,
            length=14,
            multiplier=2,
        )

        return data['SUPERT_14_2.0']

    @property
    def supertrend_14_3(self) -> pd.DataFrame | pd.Series:        
        data = ta.supertrend(
            high=self.equity_chart.data.high,
            low=self.equity_chart.data.low,
            close=self.equity_chart.data.close,
            length=14,
            multiplier=3,
        )
    
        return data['SUPERT_14_3.0']


    @property
    def rsi_14(self) -> pd.DataFrame | pd.Series:
        return ta.rsi(close=self.equity_chart.data.close, length=14)

    @property
    def adx_14(self) -> pd.DataFrame | pd.Series:
        data = ta.adx(
            high=self.equity_chart.data.high,
            low=self.equity_chart.data.low,
            close=self.equity_chart.data.close,
            length=14,
        )
    
        return data['ADX_14']

    @property
    def ce_symbol(self) -> BrokerSymbol:
        return self.algorithm.add_option(SymbolType.Index.NIFTY, ("weekly", 0), -2, "CE")

    @property
    def pe_symbol(self) -> BrokerSymbol:
        return self.algorithm.add_option(SymbolType.Index.NIFTY, ("weekly", 0), +2, "PE")

    async def next(self) -> None:
        between_time = self.algorithm.between_time(time(9, 20), time(15, 25))

        if not between_time:
            return
        
        if self.tradable_quantities == 0:
            print("Insufficient Balance", self.algorithm.broker_manager.current_capital)
            return

        if self.algorithm.positions:
            return
        
        if self.algorithm.total_pnl['loss'] >= self.max_daily_loss_percent:
            return
        
        if self.algorithm.total_pnl['profit'] >= self.max_daily_profit_percent:
            return
        
        # supertrend 14, 2 signal started
        supertrend_14_2_signal = None

        if (
            (self.equity_chart.data.close.iloc[-2] > self.supertrend_14_2.iloc[-2]) and (self.equity_chart.data.close.iloc[-1] > self.supertrend_14_2.iloc[-1])
        ):
            supertrend_14_2_signal = "long"

        if (
            (self.equity_chart.data.close.iloc[-2] < self.supertrend_14_2.iloc[-2]) and (self.equity_chart.data.close.iloc[-1] < self.supertrend_14_2.iloc[-1])
        ):
            supertrend_14_2_signal = "short"
        # supertrend 14, 2 signal started

        # supertrend 14, 3 signal started
        supertrend_14_3_signal = None

        if (
            (self.equity_chart.data.close.iloc[-2] > self.supertrend_14_3.iloc[-2]) and (self.equity_chart.data.close.iloc[-1] > self.supertrend_14_3.iloc[-1])
        ):
            supertrend_14_3_signal = "long"

        if (
            (self.equity_chart.data.close.iloc[-2] < self.supertrend_14_3.iloc[-2]) and (self.equity_chart.data.close.iloc[-1] < self.supertrend_14_3.iloc[-1])
        ):
            supertrend_14_3_signal = "short"
        # supertrend 14, 3 signal finished

        # rsi 14 signal started
        rsi_period = (30, 70)
        rsi_signal = False

        if (rsi_period[0] < self.rsi_14.iloc[-2] < rsi_period[1]) and (rsi_period[0] < self.rsi_14.iloc[-1] < rsi_period[1]):
            rsi_signal = True
        # rsi 14 signal finished

        # adx 14 signal started
        adx_period = (20, 40)
        adx_signal = False

        if (adx_period[0] < self.adx_14.iloc[-2] < adx_period[1]) and (adx_period[0] < self.adx_14.iloc[-1] < adx_period[1]):
            adx_signal = True
        # adx 14 signal finished

        should_long = (
            supertrend_14_2_signal == "long"
            and supertrend_14_3_signal == "long"
            and rsi_signal
            and adx_signal
        )

        should_short = (
            supertrend_14_2_signal == "short"
            and supertrend_14_3_signal == "short"
            and rsi_signal
            and adx_signal
        )

        print("current_datetime", self.algorithm.current_datetime)
        print("supertrend_14_2_signal",supertrend_14_2_signal)
        print("supertrend_14_3_signal",supertrend_14_3_signal)
        print("rsi_signal",rsi_signal)
        print("adx_signal",adx_signal)
        print("\n")

        if should_long:
            await self.algorithm.buy(broker_symbol=self.ce_symbol, quantities=self.tradable_quantities)

        if should_short:
            await self.algorithm.buy(broker_symbol=self.pe_symbol, quantities=self.tradable_quantities)