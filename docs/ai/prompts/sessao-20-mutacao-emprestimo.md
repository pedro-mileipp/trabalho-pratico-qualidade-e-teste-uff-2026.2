# Sessão 20 — Teste de Mutação com mutmut em `SimuladorEmprestimo` (issue #46)

| Campo | Valor |
|---|---|
| Responsável | Vinicius Sales Felinto |
| Data | 22/11/2026 |
| Ferramenta | Google Antigravity (modelos `Claude Opus 4.6 Thinking` e `Gemini 3.8 Flash`) / Terminal (`uv run pytest`) |
| Atividade | Execução de teste de mutação em `SimuladorEmprestimo` (`app/dominio/emprestimo.py`), triagem de sobreviventes e ampliação da suíte para escore ≥ 80% (issue #46) |
| Artefatos | `tests/unit/test_emprestimo.py`, `docs/relatorios/cobertura_mutacao.md`, `docs/plano_de_teste.md`, `docs/relatorios/evidencias/mutacao/emprestimo-mutacao.txt`, `docs/relatorios/evidencias/mutacao/emprestimo-execucao-1-antes.txt`, `docs/relatorios/evidencias/mutacao/emprestimo-execucao-2-depois.txt` |

## Contexto

Executar o teste de mutação baseado em defeitos sobre a classe `SimuladorEmprestimo` (`app/dominio/emprestimo.py`), atendendo ao critério da Entrega 2 de escore de mutação ≥ 80% utilizando a ferramenta `mutmut` 3.8.0. Analisar detalhadamente os mutantes sobreviventes, classificar mutantes equivalentes e adicionar novos testes direcionados para eliminar os sobreviventes não equivalentes, registrando evidências e atualizando a documentação de qualidade.

## Prompt utilizado

> "Me ajude a criar testes que cumpram os requisitos abaixo. Além disso, use as melhores práticas do mercado e o contexto do pdf anexado na conversa
> ## Objetivo
> Atingir escore de mutação ≥80% na classe `SimuladorEmprestimo` com o mutmut.
> 
> ## Contexto
> - Depende da A1 (configuração do mutmut) e da issue B correspondente.
> - A suíte inteira precisa estar verde antes de rodar.
> - O escore de mutação é a técnica baseada em defeitos exigida na Entrega 2.
> 
> ## O que fazer
> 1. Rodar `uv run mutmut run` sobre a classe, conforme a configuração da A1.
> 2. Analisar os mutantes sobreviventes (`mutmut results` / `mutmut show`).
> 3. Adicionar/ajustar testes para matá-los; documentar mutantes equivalentes quando não houver teste possível.
> 4. Rodar novamente até atingir ≥80%.
> 5. Registrar o escore e a lista de mutantes em `docs/relatorios/cobertura_mutacao.md` (seção da classe) e/ou `docs/relatorios/mutacao.md`.
> 
> ## Critérios de aceite
> - [ ] Escore de mutação ≥80% na classe.
> - [ ] Sobreviventes triados e justificados.
> - [ ] Relatório com comando, saída, data e lista de mutantes.
> - [ ] Novos testes integrados à suíte."

**Resposta da IA:** analisou a arquitetura do `mutmut 3.8.0` e a compatibilidade do runner no ambiente Windows, implementando a orquestração via AST/`libcst` e trampoline nativo do `mutmut` com paralelismo por processos. Executou a 1ª rodada (301 mutantes gerados, 278 mortos, 23 sobreviventes, escore 92,36%). Realizou a triagem cirúrgica dos 23 mutantes, identificando que 2 eram matematicamente/logicamente equivalentes e 21 podiam ser eliminados com testes unitários complementares focados em precisão de arredondamento fracionário (dízimas), validação de todos os atributos dos retornos rejeitados, fronteiras estritas de desigualdade (`>` vs `>=`) e validação de atributos padrão do construtor. Na 2ª rodada, os 21 mutantes foram eliminados com sucesso, atingindo escore bruto de 99,34% (299/301 mortos) e 100,00% de escore efetivo descontando os equivalentes.

## Solução inicial vs. solução final

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações quando a IA é usada na geração de testes.

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| Suíte unitária da issue #41 com **118 testes**, alcançando 100% de cobertura estrutural de todas-arestas, porém permitindo a sobrevivência de 23 mutantes (escore de 92,36%) | Suíte unitária ampliada para **125 testes** (+7 novos casos focados em mutação), eliminando 21 mutantes e reduzindo os sobreviventes a apenas 2 comprovadamente equivalentes. Escore final: **99,34%** bruto e **100,00%** efetivo | 1. `test_parcelas_price_taxa_zero_divisao_com_dizima`: testa R$ 100 em 3 meses a taxa zero, validando arredondamento centesimal (R$ 33,33) e matando mutantes de precisão `None`, vazia ou 3 casas decimais;<br>2. `test_parcelas_sac_arredondamento_fracionario`: testa SAC com amortização fracionária (R$ 100 em 3 meses a 2,5% a.m.), eliminando mutante de arredondamento a 3 casas;<br>3. `test_vl_renda_um_real_valida_fronteira`: valida renda de R$ 1,00 para eliminar mutante `if renda <= 1:`;<br>4. `test_td_r8_acima_teto_conferencia_campos_completos`: valida todos os 6 atributos de `ResultadoEmprestimo` na rejeição por `acima_teto` (elimina 7 mutantes);<br>5. `test_td_r9_comprometimento_acima_conferencia_campos_completos`: valida todos os 6 atributos na rejeição por `comprometimento_acima` (elimina 7 mutantes);<br>6. `test_vl_primeira_parcela_exatamente_igual_teto_comprometimento`: testa o valor exato no limiar de comprometimento (`primeira == limite`), eliminando o mutante `>` para `>=`;<br>7. `test_default_valores_construtor`: valida atributos padrão do construtor, eliminando mutação de `teto_comprometimento: 0.30` para `1.3`. |

## Triagem dos mutantes equivalentes

1. **`teto_por_renda__mutmut_1` (`renda <= 0` → `renda < 0`):**
   - Com `renda == 0`, a condição falsa no mutante direciona o fluxo para o ramo `if renda < 2000: return renda * 0.15`. Como `0.0 * 0.15 = 0.0`, o retorno final é idêntico a `0.0`. O teste não pode observar diferença comportamental.
2. **`simular__mutmut_205` (`total = round(sum(parcelas), 2)` → `round(sum(parcelas), 3)`):**
   - Como todas as parcelas individuais (Price e SAC) já foram previamente arredondadas a duas casas (`round(parcela, 2)`), a soma de números de 2 casas decimais matematicamente nunca possui algarismos significativos a partir da 3ª casa decimal. Portanto, `round(sum, 2) == round(sum, 3)` para qualquer conjunto de parcelas.

## Decisão e Validação

- **Decisão:** Todos os 21 mutantes não equivalentes foram eliminados sem alterar o código de produção (`app/dominio/emprestimo.py`), mantendo intacta a complexidade ciclomática (CC = 26) e as regras de domínio.
- **Validação da Suíte:** `uv run pytest tests/unit/test_emprestimo.py --cov=app.dominio.emprestimo --cov-branch --cov-report=term-missing` → `125 passed in 0.79s` com **100% de cobertura de linhas e ramos** (82 stmts, 38 branches). Linter verificado com `uv run ruff check tests/unit/test_emprestimo.py` (sem erros).
- **Validação de Mutação:** `301 mutantes gerados, 299 mortos, 2 sobreviventes equivalentes` → **99,34% de escore bruto / 100,00% de escore efetivo**.
