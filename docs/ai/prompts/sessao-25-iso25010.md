# Sessão 25 — Avaliação ISO/IEC 25010:2023 (issue #62)

| Campo | Valor |
|---|---|
| Responsável | Daniel Izu (`danielcamposs`) |
| Data | 22/11/2026 |
| Ferramenta | Claude Code (extensão do VS Code), modelo Claude Opus 5.5 (`claude-opus-5-5`) / Terminal (`uv run pytest`, `radon`) |
| Atividade | Issue #62: avaliação das 9 características da ISO/IEC 25010:2023, com escala, medida e justificativa baseada em evidências |
| Artefatos | `docs/relatorios/iso25010.md`; links em `README.md`, `docs/plano_de_teste.md` (v1.24) e `docs/plano_projeto.md` |

## Contexto

O enunciado pede as medidas de cada atributo de qualidade da ISO 25010, numa escala, com justificativa. O grupo já tinha feito o exercício "Qualidade do Produto", que atribui um nível de **importância** de 1 a 5 a cada uma das 9 características, justificado pelo contexto do Banco Digital. A issue #62 pede que as notas sejam **baseadas em evidências** do trabalho: cobertura, mutação, Sonar, Selenium, testes de segurança e defeitos.

## Prompt utilizado

> 1. "suba esse arquivo para a issue 62 seguindo todas essas instruções", com dois anexos: o arquivo `Exercício - Qualidade do Produto.md`, com a tabela de importância do grupo, e o texto da issue #62. Texto da issue (integral):
>
> Elaborar a avaliação ISO 25010:2023, com medida e justificativa para cada atributo de qualidade.
>
> Contexto
> O enunciado exige indicar as medidas de cada atributo da ISO 25010 seguindo uma escala, com justificativa.
> Usar a versão 2023, com 9 características: adequação funcional, eficiência de desempenho, compatibilidade, capacidade de interação, confiabilidade, segurança, manutenibilidade, flexibilidade e proteção (safety).
> As notas devem ser baseadas em evidências: cobertura, mutação, Sonar, Selenium, testes de segurança e defeitos encontrados.
> O que fazer
> Definir a escala (ex.: 1–5) e o critério objetivo de cada nível.
> Para cada característica (e subcaracterística, se o grupo decidir), dar a nota.
> Justificar com evidências do trabalho; onde não houver evidência, justificar a limitação.
> Criar docs/relatorios/iso25010.md (somente .md, sem Google Docs).
> Linkar o documento no README.
> Critérios de aceite
>
> Escala definida e justificada.
>
> As 9 características da ISO 25010:2023 avaliadas.
>
> Cada nota com evidência ou justificativa de limitação.
>
> Documento em docs/relatorios/iso25010.md e linkado no README.
>
> 2. "siga com o texto do alexandre"

**Resposta da IA:** a IA observou que o exercício do grupo mede a **importância** de cada característica, e não o quanto o produto a atende. Por isso, montou o documento em duas partes: a tabela do grupo como "Importância" (seção 3) e uma **medida obtida** por evidências (seção 4), comparando as duas na seção 5. Antes de escrever, levantou as evidências na `main`:
- `uv run pytest`: 705 passed, 4 xfailed;
- cobertura e mutação por classe (`cobertura_mutacao.md`);
- antes e depois do Sonar (`inspecao_sonar.md` e o JSON da última análise);
- riscos R1 a R5 de `rnf_seguranca.md`;
- divergências da #54;
- issues com o rótulo `bug`.

Também leu o código de `TransacaoService` e `SqliteRepositorio` para justificar a nota de recuperabilidade. Ao conferir os números, apontou que a seção 6.5 do relatório de inspeção diz "9 bugs", enquanto o JSON da mesma análise tem 5. O responsável decidiu seguir o texto do relatório (prompt 2).

## Solução inicial (gerada pela IA) vs. solução final (após validação)

Exigência do enunciado: preservar a solução inicial, a final e descrever as alterações. A solução inicial foi gravada no commit `3ce269d` **antes de qualquer revisão**, e a final no commit `69c9e9b`; o diff está em [`sessao-25-diff-iso25010-inicial-final.diff`](sessao-25-diff-iso25010-inicial-final.diff).

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| **Commit `3ce269d`:** `docs/relatorios/iso25010.md` com: escala de 1 a 5 e critério por nível; importância (exercício do grupo); medida das 9 características por subcaracterística, com evidências; resumo da diferença; melhorias recomendadas. Links no README, no plano de teste (v1.24) e no plano de projeto. Sonar citado pelo JSON da análise: 5 bugs; 19 restantes = autenticação 12, dashboard 1, `app/__init__.py` 1, testes 5 | **Commit `69c9e9b`:** igual, com os números do Sonar alinhados à seção 6.5 de `inspecao_sonar.md` (9 bugs; 19 restantes em outras funcionalidades e 4 em arquivos de teste), citando a seção como fonte | Duas frases trocadas (confiabilidade e manutenibilidade), por decisão do responsável de manter a mesma fonte do relatório de inspeção do grupo. Nenhuma nota mudou: o critério da escala não depende dessa contagem |

**Decisão:** a estrutura em importância e medida foi aceita. As notas ficaram: adequação funcional 4, eficiência de desempenho 2, compatibilidade 2, capacidade de interação 3, confiabilidade 3, segurança 3, manutenibilidade 4, flexibilidade 3 e proteção 4. Para os números do Sonar, **prevalece o texto da seção 6.5 do relatório de inspeção** (Alexandre Colmenero), que é a fonte citada no documento.

**Validação inicial:** cada valor citado foi conferido na fonte antes do commit:
- `uv run pytest -q` → `705 passed, 4 xfailed`;
- contagem por pasta com `--collect-only` (547 unitários, 84 de integração, 56 de sistema, 22 de segurança);
- escores e coberturas em `cobertura_mutacao.md`;
- totais e regras do Sonar em `inspecao_sonar.md` e no JSON da última análise;
- requisitos RF01 a RF07 no plano de teste;
- defeitos com `gh issue list --label bug`;
- gravação do PIX em dois `commit`s, na leitura de `transacoes.py` e `sqlite_repositorio.py`.

Na conferência, a IA corrigiu três afirmações do próprio rascunho antes do commit: "6 requisitos" virou 7 (RF07), o tempo do Selenium passou de "≈ 50 s" para "cerca de 1 min", e a contagem de bugs foi ajustada ao JSON.

**Validação final:** revisão do responsável, que pediu seguir a seção 6.5 do relatório de inspeção (prompt 2); o texto final cita essa seção nas duas frases.

## Ações executadas

1. Criada a branch `docs/issue-62-iso25010` a partir da `main` (`532d2c9`).
2. Levantadas as evidências: suíte completa, relatórios de cobertura e mutação, de inspeção e de segurança, divergências da #54, issues de defeito e leitura do código dos serviços e repositórios.
3. Escrito `docs/relatorios/iso25010.md`; conferidos os números; links no README, no plano de teste (v1.24) e no plano de projeto; solução inicial gravada sem revisão (`3ce269d`).
4. Números do Sonar alinhados ao texto do Alexandre (prompt 2); versão revisada gravada (`69c9e9b`).
5. Registrada esta sessão no AI-LOG.

## Resultado

- **9 características da ISO/IEC 25010:2023 avaliadas**, cada uma com tabela por subcaracterística, evidência ou justificativa de limitação, e nota pela escala de 1 a 5.
- As maiores diferenças em relação à importância estão em **confiabilidade e segurança** (5 → 3), com melhorias recomendadas na seção 6 do documento.
- Documento linkado no README.
