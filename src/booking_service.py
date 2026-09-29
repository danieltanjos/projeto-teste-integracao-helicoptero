"""Servico de agendamento de voos."""
from src.validation import ValidationModule


class BookingService:
    """Orquestra a validacao e a persistencia do agendamento."""

    def __init__(self, database):
        self.db = database
        self.validador = ValidationModule(database)

    def agendar_voo(self, aeronave_id, piloto_id, inicio, fim):
        """Valida as regras e grava o agendamento com status AGENDADO.

        Qualquer reprovacao levanta excecao antes do INSERT, de modo que
        nenhuma alteracao permanece no banco.
        """
        self.validador.validar(aeronave_id, inicio, fim)
        agendamento_id = self.db.inserir_agendamento(
            aeronave_id, piloto_id, inicio, fim
        )
        return self.db.buscar_agendamento(agendamento_id)
