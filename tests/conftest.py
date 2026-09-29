"""Fixtures do pytest para criacao e limpeza da base temporaria."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.booking_service import BookingService  # noqa: E402
from src.database import Database  # noqa: E402


@pytest.fixture
def db(tmp_path):
    """Cria um banco SQLite novo em arquivo temporario e o descarta ao fim."""
    banco = Database(str(tmp_path / "aerolog_test.db"))
    yield banco
    banco.fechar()


@pytest.fixture
def db_populado(db):
    """Banco com duas aeronaves (uma liberada, uma em inspecao) e um piloto."""
    db.inserir_aeronave(1, "PR-AER", "LIBERADO")
    db.inserir_aeronave(2, "PR-INS", "EM_INSPECAO")
    db.inserir_piloto(10, "Cap. Daniel Anjos")
    return db


@pytest.fixture
def service(db_populado):
    """BookingService integrado ao banco temporario populado."""
    return BookingService(db_populado)
