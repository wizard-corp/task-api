from ...infraestructure.broker.kafka import Kafka
from ...infraestructure.repositories.mongo import Mongo
from ...utils.IdentityHandler import IdentityHandler
from ..dto.keyword import KeywordDTO


class Meeting:
    def __init__(self, ref_write_uid, ref_repository=None, ref_producer=None):
        self._w = ref_write_uid
        self._r = Mongo.setToDefault() if ref_repository is None else ref_repository
        self._p = Kafka.setToDefault() if ref_producer is None else ref_producer
        self._uc = MeetingUseCase(self._w, self._r, self._p)

    def fetch(self) -> list:
        datos = self._uc.fetch()
        return datos

    def create(self, ref_object: KeywordDTO):
        return self._uc.create(ref_object)

    def update(self, ref_object: KeywordDTO):
        return self._uc.update(ref_object)

    def getByID(self, keyword_id: IdentityHandler) -> dict:
        data = self._uc.getByID(keyword_id)
        return data

    def delete(self, keyword_id: IdentityHandler):
        return self._uc.delete(keyword_id)
