"""Regras de elegibilidade da aeronave."""


class ValidacaoError(Exception):
    """Erro generico de regra de negocio do agendamento."""


class ManutencaoError(ValidacaoError):
    """Aeronave sem liberacao de manutencao."""


class ConflitoHorarioError(ValidacaoError):
    """Aeronave ja possui missao no mesmo intervalo."""


class ValidationModule:
    """Aplica as regras de elegibilidade consultando o banco de dados."""

    def __init__(self, database):
        self.db = database

    def validar(self, aeronave_id, inicio, fim):
        aeronave = self.db.buscar_aeronave(aeronave_id)
        if aeronave is None:
            raise ValidacaoError(f"Aeronave {aeronave_id} nao cadastrada.")

        if aeronave["status_manutencao"] != "LIBERADO":
            raise ManutencaoError(
                f"Aeronave {aeronave['prefixo']} esta em "
                f"{aeronave['status_manutencao']} e nao pode ser agendada."
            )

        if self.db.buscar_conflitos(aeronave_id, inicio, fim):
            raise ConflitoHorarioError(
                f"Aeronave {aeronave['prefixo']} ja possui missao entre {inicio} e {fim}."
            )

        return True
