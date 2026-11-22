# Sessão 19 — Testes unitários ampliados e cobertura estrutural de `SimuladorEmprestimo` (issue #41)

| Campo | Valor |
|---|---|
| Responsável | Vinicius Sales Felinto |
| Data | 22/11/2026 |
| Ferramenta | Google Antigravity (modelo `Gemini 3.8 Flash`) / Terminal (`uv run pytest`) |
| Atividade | Ampliar casos de teste unitários e comprovar cobertura estrutural todas-arestas de `SimuladorEmprestimo` (issue #41) |
| Artefatos | `tests/unit/test_emprestimo.py`, `docs/relatorios/cobertura_mutacao.md`, `docs/plano_de_teste.md` |

## Contexto

Ampliar os testes unitários da classe `SimuladorEmprestimo` (`app/dominio/emprestimo.py`) em `tests/unit/test_emprestimo.py` para a issue #41, aplicando partição de equivalência (`pe_`), análise de valor-limite (`vl_`), tabela de decisão (`td_`) e teste de laços (`laco_`), assegurando a cobertura estrutural (todas-arestas) em 100% (meta ≥ 80%) e mitigando mutantes com validação estrita de valores de parcelas e montantes totais.

## Prompt utilizado

> "Me ajude a criar testes que cumpram os requisitos abaixo. Além disso, use as melhores práticas do mercado e o contexto do pdf anexado na conversa
> 
> ## Objetivo
> Ampliar os testes unitários de `SimuladorEmprestimo` (`app/dominio/emprestimo.py`) e comprovar cobertura estrutural ≥80% no critério todas-arestas.
> 
> ## Contexto
> - Arquivo de testes: `tests/unit/test_emprestimo.py`.
> - Cobertura atual: 100%.
> - Não há ramos pendentes; o desafio será a mutação.
> - Cálculos numéricos geram muitos mutantes; conferir os valores exatos das parcelas, não só aprovado/negado.
> 
> ## O que fazer
> 1. Revisar os casos existentes e corrigir expectativas erradas.
> 2. Ampliar com partição de equivalência, análise de valor-limite, tabela de decisão e teste de laços; identificar a técnica no id do `pytest.param` ou em comentário.
> 3. Cobrir as arestas não cobertas: Não há ramos pendentes; o desafio será a mutação.
> 4. Rodar `uv run pytest tests/unit/test_emprestimo.py --cov=app.dominio.emprestimo --cov-branch --cov-report=term-missing`.
> 5. Registrar os números na seção da classe em `docs/relatorios/cobertura_mutacao.md`.
> 6. Abrir issues de bug para defeitos revelados, usando a falha do teste como evidência."

**Resposta da IA:** analisou a implementação de `SimuladorEmprestimo` e a suíte anterior (40 casos), expandindo para 118 casos com identificadores explícitos das técnicas (`pe_`, `vl_`, `td_`, `laco_`, `custom_`). Modelou a tabela de decisão completa de `simular()` com casos de precedência de validações simultâneas, testes de laços cobrindo 0, 1, 2, n, max-1, max e max+1 iterações para SAC, conferência numérica exata de cada parcela e montante acumulado, e testes de customização via construtor.

## Solução inicial vs. solução final

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Suíte de 40 casos parametrizados simples da Entrega 1, sem identificação formal de técnicas nos IDs de teste, sem validação de precedência e com checagens parciais de resultado numérico | Suíte ampliada para **118 casos** organizados em 8 classes de teste, todos aprovados com **100% de cobertura estrutural de linhas e ramos** (82 stmts, 38 branches) | Reestruturação completa com prefixos `pe_`, `vl_`, `td_`, `laco_` e `custom_`; adição de 24 casos para Tabela de Decisão e precedência; ampliação dos testes de laço de SAC para 8 cenários (0 a 61 meses); inclusão de 18 casos de AVL nas decisões de negócio (teto de renda e comprometimento de parcela); conferência exata campo a campo de `ResultadoEmprestimo`; remoção de import não utilizado reportado pelo `ruff` |

**Decisão:** Não foram detectados bugs em `app/dominio/emprestimo.py`; a implementação matemática e os desvios condicionais atendem estritamente à especificação da aplicação. Nenhum bug corretivo necessitou ser aberto.

**Validação:** `uv run pytest tests/unit/test_emprestimo.py --cov=app.dominio.emprestimo --cov-branch --cov-report=term-missing` → `118 passed in 0.88s` (100% cobertura de linhas e ramos).

## Ações executadas

1. Mapeadas as regras de negócio de `SimuladorEmprestimo` (`taxa_por_prazo`, `teto_por_renda`, `parcelas_price`, `parcelas_sac` e `simular`).
2. Projetados casos de PE e AVL com passo unitário e centesimal nas fronteiras das faixas.
3. Projetada a Tabela de Decisão com matriz de regras R1 a R11 e matriz de precedência de erros.
4. Projetados testes de laço para o loop de amortização SAC cobrindo 0, 1, 2, n, max-1, max e max+1 iterações conforme os critérios do material de Teste Estrutural.
5. Executada a suíte com medição de cobertura todas-arestas (100% alcançado).
6. Documentada a seção da classe em `docs/relatorios/cobertura_mutacao.md` e atualizado o plano de testes e histórico de IA.

## Resultado

- **118 casos aprovados** em `tests/unit/test_emprestimo.py` (0.88s).
- Cobertura estrutural mantida em **100%** (82 statements, 38 branches, 0 missed).
- Nenhum defeito de código detectado em `app/dominio/emprestimo.py`.
