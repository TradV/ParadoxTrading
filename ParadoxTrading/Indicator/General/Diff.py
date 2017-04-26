from ParadoxTrading.Indicator.IndicatorAbstract import IndicatorAbstract
from ParadoxTrading.Utils import DataStruct


class Diff(IndicatorAbstract):
    def __init__(
            self, _use_key: str, _idx_key: str = 'time', _ret_key: str = 'diff'
    ):
        super().__init__()

        self.use_key = _use_key
        self.idx_key = _idx_key
        self.ret_key = _ret_key
        self.data = DataStruct(
            [self.idx_key, self.ret_key],
            self.idx_key
        )

        self.last_value = None

    def _addOne(self, _data: DataStruct):
        index_value = _data.index()[0]
        cur_value = _data[self.use_key][0]
        diff_value = 0
        if self.last_value is not None:
            diff_value = cur_value - self.last_value
        self.last_value = cur_value
        self.data.addRow(
            (index_value, diff_value),
            (self.idx_key, self.ret_key)
        )
