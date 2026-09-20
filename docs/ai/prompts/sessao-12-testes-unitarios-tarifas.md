# Sessão 12 — Testes unitários de `TarifaBancaria`

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielizu`) |
| Data | 20/09/2026 |
| Ferramenta | VS Code / Terminal (`uv run pytest`) |
| Atividade | Projetar, ampliar e executar casos de testes unitários da classe `TarifaBancaria` |
| Artefatos | `tests/unit/test_tarifas.py` |

## Contexto

Implementar os testes unitários da classe `TarifaBancaria` (`app/dominio/tarifas.py`) a partir das regras descritas em `docs/aplicacao.md`, aplicando partição de equivalência, análise de valor-limite e tabela de decisão sobre `tarifa_mensal`, `tarifa_por_transacao_extra` e `tarifa_anual`. Também foram cobertos os caminhos auxiliares de isenção e pacote.

## Prompt utilizado na conversa

> "Analise os documentos em `@docs/` e a **issue de teste unitário** no meu nome.
>
> Planeje e implemente os testes unitários da classe garantindo **100% de cobertura** das regras de negócio e cenários de borda.
>
> Ao final, **execute a suíte de testes** e mostre os resultados."

## Orientações complementares

Durante a execução, o escopo foi detalhado para incluir `tarifa_mensal` (tipo de conta, pacote, faixas de saldo e transações), `tarifa_por_transacao_extra` e `tarifa_anual`, usando partição de equivalência, análise de valor-limite e tabela de decisão. Também foi solicitado que eventuais defeitos fossem reportados manualmente, fora das issues.

**Resposta da IA:** analisou `app/dominio/tarifas.py` e a seção 4.3 de `docs/aplicacao.md`, criou a suíte parametrizada e executou o comando solicitado. Depois, a pedido do responsável, ampliou os testes com combinações adicionais e cenários de borda.

## Solução inicial (estrutura pensada) vs. solução final (IA complementando e revisando o que foi gerado)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações ocorridas durante o processo de testes.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Mapeamento inicial dos principais cenários de tarifa por tipo de conta e saldo | Suíte parametrizada em Python/pytest com 44 casos aprovados | A IA adicionou casos para pacote, limites exatos, transações acima da cota e combinações de regras. Os cenários explícitos de antiguidade foram removidos posteriormente conforme a decisão do responsável. |

**Decisão:** Os três cenários com expectativas incorretas foram retirados da suíte. O código de domínio não foi alterado, pois as falhas estavam nos valores esperados dos testes, e não em defeitos confirmados da implementação.

**Validação inicial:** `uv run pytest tests/unit/test_tarifas.py` → `34 passed in 0.35s`.

**Validação final:** `uv run pytest tests/unit/test_tarifas.py` → `44 passed in 0.24s`.

## Inputs para reprodução

Os casos abaixo correspondem aos parâmetros utilizados em `tests/unit/test_tarifas.py`. A fixture `tarifa` cria `TarifaBancaria()` com os valores padrão: corrente `30.0`, poupança `0.0`, premium `50.0`, faixas de isenção `(1000.0, 5000.0, 50000.0)`, tarifa por transação `2.5` e 10 transações gratuitas. Os testes utilizam a antiguidade padrão de `0` meses e não cobrem cenários específicos de antiguidade.

### `test_tarifa_mensal_sem_pacote`

| ID | Tipo | Saldo | Esperado |
|---|---|---:|---:|
| `poupanca_sem_taxa` | POUPANCA | 5000.0 | 0.0 |
| `corrente_sem_isencao` | CORRENTE | 1000.0 | 30.0 |
| `corrente_isenta_por_saldo` | CORRENTE | 6000.0 | 0.0 |
| `premium_isento_por_saldo` | PREMIUM | 60000.0 | 0.0 |
| `premium_sem_isencao` | PREMIUM | 20000.0 | 50.0 |

Parâmetros implícitos: `tem_pacote=False`, `quantidade_transacoes=0` e `antiguidade_meses=0`.

### `test_tarifa_mensal_regras_de_negocio`

| ID | Tipo | Saldo | Transações | Esperado |
|---|---|---:|---:|---:|
| `corrente_com_transacoes_extras` | CORRENTE | 3000.0 | 15 | 42.5 |
| `corrente_saldo_negativo` | CORRENTE | -100.0 | 0 | 36.0 |
| `premium_transacoes_extras` | PREMIUM | 30000.0 | 15 | 62.5 |

Parâmetro implícito: `tem_pacote=False`.

### `test_tarifa_mensal_com_pacote`

| ID | Tipo | Saldo | Esperado |
|---|---|---:|---:|
| `corrente_pacote_saldo_alto` | CORRENTE | 6000.0 | 15.0 |
| `corrente_pacote_sem_isencao` | CORRENTE | 3000.0 | 30.0 |
| `premium_pacote_isento` | PREMIUM | 60000.0 | 0.0 |
| `premium_pacote_sem_isencao` | PREMIUM | 4000.0 | 35.0 |

Parâmetros implícitos: `tem_pacote=True` e `quantidade_transacoes=0`.

### `test_tarifa_por_transacao_extra`

| ID | Quantidade de transações | Esperado |
|---|---:|---:|
| `zero_transacoes` | 0 | 0.0 |
| `cota_gratuita` | 10 | 0.0 |
| `uma_extra` | 11 | 2.5 |
| `cinco_extras` | 15 | 12.5 |

### `test_tem_isencao`

| ID | Tipo | Saldo | Esperado |
|---|---|---:|---:|
| `corrente_isencao` | CORRENTE | 6000.0 | `True` |
| `corrente_sem_isencao` | CORRENTE | 4000.0 | `False` |
| `premium_isencao` | PREMIUM | 50000.0 | `True` |
| `poupanca_isencao` | POUPANCA | 1000.0 | `True` |
| `poupanca_sem_isencao` | POUPANCA | 500.0 | `False` |

### `test_tarifa_com_pacote`

| ID | Tipo | Saldo | Esperado |
|---|---|---:|---:|
| `corrente_sem_pacote` | CORRENTE | 3000.0 | 30.0 |
| `corrente_pacote_base` | CORRENTE | 6000.0 | 30.0 |
| `premium_isento` | PREMIUM | 60000.0 | 0.0 |
| `premium_pacote` | PREMIUM | 4000.0 | 35.0 |

### `test_tarifa_anual`

| ID | Tipo | Saldo | Pacote | Transações | Esperado |
|---|---|---:|---|---:|---:|
| `anual_isenta` | CORRENTE | 6000.0 | `False` | 0 | 0.0 |
| `anual_corrente_sem_isencao` | CORRENTE | 1000.0 | `False` | 0 | 360.0 |
| `anual_premium_transacoes_extras` | PREMIUM | 40000.0 | `False` | 15 | 750.0 |

### Configuração da base

Além dos casos parametrizados, foram executados três testes de configuração:

| Teste | Inputs principais | Verificação |
|---|---|---|
| `test_tarifas_base_default` | `TarifasBase()` | Confirma os valores padrão da base. |
| `test_tarifas_base_personalizada` | corrente `35.0`, premium `60.0`, tarifa extra `3.0`, cota `8` | Confirma a personalização dos valores. |
| `test_instancia_personalizada_usa_base_recebida` | corrente `40.0`, premium `70.0`, tarifa extra `3.0`, cota `5` | Confirma a base recebida, tarifa mensal `40.0` e 2 transações extras com valor `6.0`. |

### `test_tarifa_mensal_cenarios_combinados`

| ID | Tipo | Saldo | Pacote | Transações | Antiguidade | Esperado |
|---|---|---:|---|---:|---:|---:|
| `corrente_pacote_alto_saldo` | CORRENTE | 6000.0 | `True` | 0 | 15.0 |
| `corrente_pacote_ignora_transacoes_extra` | CORRENTE | 7000.0 | `True` | 25 | 15.0 |
| `premium_pacote_isencao_5x5` | PREMIUM | 50000.0 | `True` | 0 | 0.0 |

### `test_tarifa_por_transacao_extra_borda`

| ID | Quantidade de transações | Esperado |
|---|---:|---:|
| `quantidade_negativa` | -1 | 0.0 |
| `um_abaixo_da_cota` | 1 | 0.0 |
| `margem_exata` | 11 | 2.5 |
| `duas_extras` | 12 | 5.0 |
| `muito_acima_da_cota` | 20 | 25.0 |

### `test_tarifa_mensal_valor_limite`

| ID | Tipo | Saldo | Pacote | Transações | Esperado |
|---|---|---:|---|---:|---:|
| `poupanca_abaixo_da_isencao` | POUPANCA | 999.0 | `False` | 0 | 0.0 |
| `corrente_abaixo_isencao` | CORRENTE | 999.0 | `False` | 0 | 30.0 |
| `corrente_faixa_limite_exato` | CORRENTE | 5000.0 | `False` | 10 | 0.0 |
| `corrente_limite_exato_mais_um` | CORRENTE | 5000.0 | `False` | 11 | 2.5 |
| `premium_limite_exato` | PREMIUM | 50000.0 | `False` | 0 | 0.0 |

## Ações executadas

1. Revisada a API pública em `app/dominio/tarifas.py` e a regra de negócio na seção 4.3 de `docs/aplicacao.md`.
2. Criado e estruturado `tests/unit/test_tarifas.py` com fixtures e casos parametrizados.
3. Executada a primeira versão da suíte, com 34 testes aprovados.
4. Ampliada a suíte para incluir combinações de regras e valores-limite.
5. Removidos três casos cujos valores esperados não correspondiam à regra implementada.
6. Removidos os cenários explícitos de antiguidade conforme decisão do responsável.
7. Executada a suíte final com 44 casos aprovados.
8. Mantido o código de domínio sem alterações.

## Resultado

- A primeira versão teve **34 testes aprovados** em `tests/unit/test_tarifas.py`.
- A versão final contém **44 casos aprovados**.
- A suíte cobre cenários de:
	- conta corrente, poupança e premium;
	- isenção por faixa de saldo;
	- pacote de serviços;
	- saldo negativo;
	- transações acima da cota gratuita;
	- cálculo anual;
	- valores-limite e combinações de regras.
- Não houve falha intencional nem defeito confirmado no código de produção.
- Os três casos com expectativas incorretas e os cenários explícitos de antiguidade foram removidos conforme decisão do responsável.
