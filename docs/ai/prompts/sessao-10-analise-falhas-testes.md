# Sessão 10 — Análise das falhas de teste e distinção entre bugs no código e erros nos testes

| Campo | Valor |
|---|---|
| Responsável | Pedro Mileipp (`pedro-mileipp`) |
| Data | 18/09/2026 |
| Ferramenta | opencode (modelo `minimax-coding-plan/MiniMax-M2.7`) |
| Atividade | Análise das 16 falhas de teste e distinção entre bugs no código e erros nos testes |

## Contexto

Após a execução dos 78 casos de teste de `DecisorCredito`, 16 testes falharam. Esta sessão tratou de analisar cada falha para distinguir entre bugs reais no código e erros de expectativa nos próprios testes.

## Prompts utilizados

> "escreva esse resumo final em um markdown chamado resumo_final.md e coloque na minha pasta Documentos"
>
> "O executor nesse caso foi Pedro Mileipp, eu que fiz os testes dessa classe."

**Resposta da IA:** Auditou os valores esperados e confirmou se os resultados observados eram bugs do código ou dos testes.

## O que foi feito pela IA

- Auditou os valores esperados dos testes
- Confirmou se os resultados observados eram bugs do código ou erros nos testes

## O que foi feito pelo usuário

- Executou os testes com `uv run pytest tests/unit/test_credito.py`
- Analisou cada uma das 16 falhas manualmente
- Identificou que 11 testes tinham expectativa errada (não eram bugs do código)
- Identificou que 5 eram bugs reais no código
- Separou BUG-1 (limite_maximo não aplicado) e BUG-2 (tipo_desconhecido ignora peso) de BUG-3 (erros nos testes)
- Reviu manualmente o código fonte de `app/dominio/credito.py` para confirmar os bugs

## Bugs identificados para Entrega 2

| ID | Bug | Local |
|---|---|---|
| **BUG-1** | `limite_maximo` não aplicado para renda alta com score ≥ 850 | `app/dominio/credito.py:74` |
| **BUG-2** | `tipo_desconhecido` ignora `peso` do registro | `app/dominio/credito.py:56` |

## Resultado

- **62 testes passam**, **16 falham** como resultado final
- Bugs reais separados de erros de expectativa para correção direcionada na Entrega 2
