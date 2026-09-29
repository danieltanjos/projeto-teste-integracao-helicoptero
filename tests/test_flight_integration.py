"""Testes de integracao: BookingService + ValidationModule + Database."""
import pytest

from src.validation import ConflitoHorarioError, ManutencaoError


def test_agendamento_valido_persiste_com_status_agendado(service, db_populado):
    """Cenario 1 - Caminho feliz: aeronave liberada e horario disponivel."""
    registro = service.agendar_voo(1, 10, "2026-10-01 08:00", "2026-10-01 10:00")

    assert registro["status"] == "AGENDADO"

    gravado = db_populado.buscar_agendamento(registro["id"])
    assert gravado is not None
    assert gravado["aeronave_id"] == 1
    assert gravado["inicio"] == "2026-10-01 08:00"
    assert len(db_populado.listar_agendamentos()) == 1


def test_conflito_de_horario_nao_insere_segundo_agendamento(service, db_populado):
    """Cenario 2 - Conflito de horario da aeronave."""
    service.agendar_voo(1, 10, "2026-10-01 08:00", "2026-10-01 10:00")

    with pytest.raises(ConflitoHorarioError):
        service.agendar_voo(1, 10, "2026-10-01 09:00", "2026-10-01 11:00")

    assert len(db_populado.listar_agendamentos()) == 1


def test_aeronave_em_inspecao_e_reprovada(service, db_populado):
    """Cenario 3 - Aeronave em manutencao preventiva/corretiva."""
    with pytest.raises(ManutencaoError):
        service.agendar_voo(2, 10, "2026-10-01 08:00", "2026-10-01 10:00")

    assert db_populado.listar_agendamentos() == []


def test_isolamento_entre_testes_base_inicia_vazia(service, db_populado):
    """Cenario 4 - Consistencia do banco com fixtures/rollback."""
    assert db_populado.listar_agendamentos() == []

    service.agendar_voo(1, 10, "2026-10-02 14:00", "2026-10-02 16:00")

    assert len(db_populado.listar_agendamentos()) == 1
