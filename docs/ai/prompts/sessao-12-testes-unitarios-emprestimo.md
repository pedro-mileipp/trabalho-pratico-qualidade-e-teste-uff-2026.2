# Sessão 12 - Testes unitários de `SimuladorEmprestimo`

| Campo | Valor |
|---|---|
| Responsável | Vinicius Sales Felinto |
| Data | 19/09/2026 |
| Ferramenta | Gemini (modelo `Gemini 3.1 Pro`) |
| Atividade | Projetar e executar casos de testes unitários da classe `SimuladorEmprestimo` |
| Artefatos | `tests/unit/test_emprestimo.py` |

## Contexto

Implementar os testes unitários para `app/dominio/emprestimo.py`, aplicando as técnicas de partição de equivalência, análise de valor-limite e teste de laços. Os testes devem cobrir os métodos `taxa_por_prazo`, `teto_por_renda`, `parcelas_price`, `parcelas_sac` e `simular` (validações iniciais, teto por renda e sistemas de amortização).

## Prompt utilizado

> "preciso criar testes unitarios para app/dominio/emprestimo.py que cumpra os requisitos abaixo:
>
> Criar tests/unit/test_emprestimo.py cobrindo as regras: taxa_por_prazo, teto_por_renda, parcelas_price, parcelas_sac e simular (validações, teto por renda, sistemas de amortização).
> Aplicar técnicas funcionais: partição de equivalência, análise de valor-limite e teste de laços."

**Resposta da IA:** Projetou e executou a implementação da suíte de testes no arquivo `tests/unit/test_emprestimo.py`. Criou testes cobrindo as partições de equivalência (PE) e a análise de valor-limite (AVL) para `taxa_por_prazo`, `teto_por_renda` e validações de input do método `simular`. Aplicou o teste de laços no método `parcelas_sac` (0, 1 e n iterações). Foram mapeados e gerados 40 casos de testes parametrizados no total.

## Solução inicial (gerada pela IA) vs. solução final (após revisão)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| 40 casos parametrizados; todos verdes (nenhuma falha encontrada durante a execução) | 40 casos parametrizados; todos verdes | Nenhuma alteração foi necessária nos casos mapeados, pois a implementação da IA conseguiu refletir as regras matemáticas corretamente sem acionar defeitos intencionais e obter sucesso (100% passed). |

**Validação:** A execução `uv run pytest tests/unit/test_emprestimo.py` retornou `40 passed in 0.29s`.

## Ações executadas

1. Criado o arquivo `tests/unit/test_emprestimo.py` estruturado por classes abordando PE, AVL e testes de laço.
2. Executado comando `uv run pytest tests/unit/test_emprestimo.py` garantindo que todos os 40 casos parametrizados passassem.

## Resultado

- **40 testes passam**, abrangendo as lógicas de negócio do `SimuladorEmprestimo`.

