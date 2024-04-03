import math
import pandas as pd
import pandas_ta as ta

from datetime import timedelta, time

from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.broker_symbol import BrokerSymbol
from proalgotrader_core.protocols.enums.account_type import AccountType
from proalgotrader_core.protocols.enums.symbol_type import SymbolType
from proalgotrader_core.protocols.strategy import StrategyProtocol

from project.position_manager import PositionManager

class Strategy(StrategyProtocol):
    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm

        self.algorithm.set_account_type(account_type=AccountType.DERIVATIVE_INTRADAY)

        self.algorithm.set_interval(interval=timedelta(seconds=1))

        self.algorithm.set_position_manager(position_manager=PositionManager)

    async def initialize(self) -> None:
        self.equity_symbol = self.algorithm.add_equity(symbol_type=SymbolType.Index.BANKNIFTY)

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
        return self.algorithm.add_option(SymbolType.Index.BANKNIFTY, ("weekly", 0), -2, "CE")

    @property
    def pe_symbol(self) -> BrokerSymbol:
        return self.algorithm.add_option(SymbolType.Index.BANKNIFTY, ("weekly", 0), +2, "PE")

    async def next(self) -> None:
        if self.algorithm.positions:
            return
        
        between_time = self.algorithm.between_time(time(9, 20), time(15, 25))

        if not between_time:
            return
        
        sideways_time = self.algorithm.between_time(time(11, 00), time(14, 00))

        if sideways_time:
            print(f"{self.algorithm.current_datetime}")
            print("No Trade between 11:00 AM to 14:00 PM")
            print("\n")
            return
        
        if self.tradable_quantities == 0:
            print(f"{self.algorithm.current_datetime}")
            print("Insufficient Balance", self.algorithm.broker_manager.current_capital)
            print("\n")
            return
        
        if self.algorithm.total_pnl['loss'] >= self.max_daily_loss_percent:
            print(f"{self.algorithm.current_datetime}")
            print("Daily Max Loss Booked", self.algorithm.total_pnl['loss'])
            print("\n")
            return
        
        if self.algorithm.total_pnl['profit'] >= self.max_daily_profit_percent:
            print(f"{self.algorithm.current_datetime}")
            print("Daily Max Profit Booked", self.algorithm.total_pnl['profit'])
            print("\n")
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
        if supertrend_14_2_signal == "long" and supertrend_14_3_signal == "long":
            rsi_14_period = (20, 60)
        elif supertrend_14_2_signal == "short" and supertrend_14_3_signal == "short":
            rsi_14_period = (40, 80)
        else:
            rsi_14_period = (20, 80)

        rsi_14_signal = False

        if (rsi_14_period[0] < self.rsi_14.iloc[-2] < rsi_14_period[1]) and (rsi_14_period[0] < self.rsi_14.iloc[-1] < rsi_14_period[1]):
            rsi_14_signal = True
        # rsi 14 signal finished

        # adx 14 signal started
        adx_14_period = (25, 40)
        adx_14_signal = False

        if (adx_14_period[0] < self.adx_14.iloc[-2] < adx_14_period[1]) and (adx_14_period[0] < self.adx_14.iloc[-1] < adx_14_period[1]) and (self.adx_14.iloc[-1] > self.adx_14.iloc[-2]):
            adx_14_signal = True
        # adx 14 signal finished

        should_long = (
            supertrend_14_2_signal == "long"
            and supertrend_14_3_signal == "long"
            and rsi_14_signal
            and adx_14_signal
        )

        should_short = (
            supertrend_14_2_signal == "short"
            and supertrend_14_3_signal == "short"
            and rsi_14_signal
            and adx_14_signal
        )

        print(f"{'Current Datetime':<30} {self.algorithm.current_datetime}")
        print(f"{'superTrend 14,2':<30} {supertrend_14_2_signal}")
        print(f"{'superTrend 14,3':<30} {supertrend_14_3_signal}")
        print(f"{'RSI 14':<30} {rsi_14_signal}")
        print(f"{'ADX 14':<30} {adx_14_signal}")
        print("\n")

        if should_long:
            await self.algorithm.buy(broker_symbol=self.ce_symbol, quantities=self.tradable_quantities)

        if should_short:
            await self.algorithm.buy(broker_symbol=self.pe_symbol, quantities=self.tradable_quantities)