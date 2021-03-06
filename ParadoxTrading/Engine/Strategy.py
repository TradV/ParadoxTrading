import logging
import typing
from collections import Hashable

import ParadoxTrading.Engine
from ParadoxTrading.Engine.Event import MarketEvent, SettlementEvent, \
    SignalEvent, SignalType
from ParadoxTrading.Fetch import RegisterAbstract
from ParadoxTrading.Utils import Serializable


class StrategyAbstract(Serializable):
    def __init__(self, _name: str):
        """
        base class of strategy

        :param _name: name of this strategy
        """
        super().__init__()
        self.name: str = _name

        # common variables
        self.engine: ParadoxTrading.Engine.Engine.EngineAbstract = None
        self.registers: typing.Set[str] = set()

    def setEngine(self,
                  _engine: 'ParadoxTrading.Engine.EngineAbstract'):
        """
        PROTECTED !!!

        :param _engine: ref to engine
        :return:
        """
        self.engine = _engine

    def deal(self, _market_event: MarketEvent):
        """
        user defined deal, it will be called when there is
        market event for this strategy

        :param _market_event:
        :return:
        """
        raise NotImplementedError('deal not implemented!')

    def settlement(self, _settlement_event: SettlementEvent):
        """
        user defined settlement, it will be called when there is
        a settlement event

        :param _settlement_event:
        :return:
        """
        raise NotImplementedError('settlement not implemented!')

    def addMarketRegister(
            self,
            _market_register: RegisterAbstract
    ) -> str:
        """
        used in init() to register market data

        :type _market_register: object
        :return: json str key of market register
        """

        key = _market_register.toJson()
        assert key not in self.registers
        # alloc position for market register object
        self.registers.add(key)

        return key

    def addEvent(
            self, _symbol: str, _strength: float,
    ):
        """
        add signal event to event queue.

        :param _symbol: which symbol is the signal for
        :param _strength: defined by user
        :return:
        """
        assert isinstance(_symbol, Hashable)

        if _strength > 0:
            signal_type = SignalType.LONG
        elif _strength < 0:
            signal_type = SignalType.SHORT
        else:
            signal_type = SignalType.EMPTY

        self.engine.addEvent(SignalEvent(
            _symbol=_symbol,
            _strategy=self.name,
            _tradingday=self.engine.getTradingDay(),
            _datetime=self.engine.getDatetime(),
            _signal_type=signal_type,
            _strength=_strength,
        ))
        logging.info('Strategy({}) send {} {} {} when {}'.format(
            self.name, _symbol,
            SignalType.toStr(signal_type),
            _strength,
            self.engine.getDatetime()
        ))

    def __repr__(self) -> str:
        ret = 'Strategy:\n\t{}\nMarket Register:\n\t{}'
        return ret.format(
            self.name,
            self.registers
        )
