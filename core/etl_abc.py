import abc


class ETLBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs):
        self.hsreplay_etl()

    def hsreplay_etl(self):
        extracted = self._extract()
        transformed = self._transform(extracted)
        return self._load(transformed)

    @abc.abstractmethod
    def _extract(self):
        pass

    def _transform(self, extracted):
        return extracted

    def _load(self, transformed):
        return transformed
