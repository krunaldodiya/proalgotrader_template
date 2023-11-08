import pandas_ta as ta

from datetime import timedelta

from proalgotrader_protocols import Algorithm_Protocol
from proalgotrader_protocols.enums.account_type import AccountType


class Strategy(Algorithm_Protocol):
    async def initialize(self):
        self.set_account_type(AccountType.DERIVATIVE_INTRADAY)

        self.nifty = self.add_equity("NIFTY")

        self.nifty_chart = await self.add_chart(
            self.nifty, timedelta(minutes=5)
        )

    @property
    def sma_20(self):
        return self.nifty_chart.add_indicator(
            "sma_20", lambda data: ta.sma(close=data.close, length=20)
        )

    @property
    def sma_50(self):
        return self.nifty_chart.add_indicator(
            "sma_50", lambda data: ta.sma(close=data.close, length=50)
        )
    
    @property
    def nifty_ce(self) -> None:
        return self.add_option("NIFTY", ("weekly", 0), 0, "CE")
    
    @property
    def nifty_pe(self) -> None:
        return self.add_option("NIFTY", ("weekly", 0), 0, "PE")
    
    def crossover(sma1, sma2):
        return (sma1.iloc[-1] > sma2.iloc[-1]) and (
            sma1.iloc[-2] < sma2.iloc[-2]
        )
    
    async def next(self):
        sma_20 = self.sma_20.data["SMA_20"]
        sma_50 = self.sma_50.data["SMA_50"]

        bullish_crossover = self.crossover(sma_20, sma_50)
        bearish_crossover = self.crossover(sma_50, sma_20)

        if not self.open_positions:
            if bullish_crossover:
                await self.buy(symbol=self.nifty_ce, quantities=50)

            if bearish_crossover:
                await self.buy(symbol=self.nifty_pe, quantities=50)
