# Projeto Teste de Integração — Agendamento de Voos de Helicóptero

Suíte de testes de integração (pytest + SQLite) para o módulo de agendamento de voos
da **AeroLog Helicópteros**. Os testes exercitam a integração real entre
`BookingService`, `ValidationModule` e `Database`, sem mocks e sem API HTTP.

## Estrutura

```
src/
  database.py          # Conexão e operações no SQLite
  validation.py        # Regras de elegibilidade da aeronave
  booking_service.py   # Serviço de agendamento de voos
tests/
  conftest.py                  # Fixtures (banco temporário por teste)
  test_flight_integration.py   # Testes de integração
```

## Regras de negócio

1. **Disponibilidade:** um helicóptero não pode ter dois voos em intervalos sobrepostos.
2. **Manutenção:** apenas aeronaves com `status_manutencao = "LIBERADO"` podem ser agendadas.
3. **Confirmação:** aprovado, o voo é gravado com status `AGENDADO`; reprovado, nada é gravado.

## Instalação

```bash
git clone https://github.com/<usuario>/projeto-teste-integracao-helicoptero.git
cd projeto-teste-integracao-helicoptero
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
```

## Execução dos testes

```bash
python -m pytest -v                              # execução detalhada
python -m pytest --cov=src --cov-report=term-missing   # cobertura
```

## Cenários cobertos

| # | Cenário | Resultado esperado |
|---|---------|--------------------|
| 1 | Agendamento válido | Registro gravado com status `AGENDADO` |
| 2 | Conflito de horário | `ConflitoHorarioError`; base mantém 1 registro |
| 3 | Aeronave `EM_INSPECAO` | `ManutencaoError`; base permanece vazia |
| 4 | Isolamento por fixtures | Cada teste inicia com a base zerada |
