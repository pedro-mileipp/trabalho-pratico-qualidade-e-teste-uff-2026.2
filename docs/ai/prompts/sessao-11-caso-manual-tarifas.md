# Sessão 11 — Caso de teste manual — Tarifas

| Campo | Valor |
|---|---|
| Responsável | Vinicius Sales Felinto  |
| Data | 19/09/2026 |
| Ferramenta | Google Antigravity (modelo `Claude Opus 4.6 Thinking`) |
| Atividade | Projetar casos de teste manual da funcionalidade de consulta de tarifas (`/tarifas`) e documentar |
| Artefatos | `tests/testes_manuais/tarifas/caso_tarifas.md` + `tests/testes_manuais/tarifas/evidencias/` (a preencher na execução) |

## Contexto

Elaborar a suíte de testes manuais para a funcionalidade de consulta de tarifas do Banco Digital. A atividade envolveu analisar o código-fonte do módulo `app/dominio/tarifas.py` (classe `TarifaBancaria`, CC = 12), a rota web `app/web/routes/tarifas.py` e o formulário `app/templates/tarifas.html`, mapear todas as regras de negócio e seus ramos de decisão, avaliar os cenários propostos pelo testador, identificar lacunas e complementar a suíte com cenários de fronteira (BVA) e interação entre variáveis.

## Prompts utilizados na conversa

> **Prompt 1 — Proposta inicial de cenários:**
> "Tenho a tarefa de criar testes manuais para a funcionalidade de tarifa, pensei nos seguintes testes: Testar cada tipo de conta disponível independendo o valor; Testar cada tipo de conta com e sem pacote independendo o valor; Testar cada tipo de conta com valores variáveis no saldo e fixos na transação mensal; Testar cada tipo de conta com valores fixos de saldo e transações mensais variáveis; testar cada tipo de conta com valores zerados; testar cada tipo de conta, com saldo zerado e transações X por mês; Testar cada tipo de conta com X Saldo e transações zeradas. Me ajude a analisar se os casos acima cobrem de maneira satisfatória os cenários possíveis para essa funcionalidade, se sim, me ajude a definir as faixas de valores variáveis para os campos de moeda e numérico, se não for suficiente, me sugira mais testes a serem feitos e também ajuste os valores das variáveis."
>
> **Prompt 2 — Geração do documento:**
> "Gere um documento na pasta tests/testes_manuais sobre os testes manuais desta funcionalidade, mantenha o formato md. Coloque os casos que eu pensei mais os que você me sugeriu. Siga o padrão usado pelos outros Devs na formatação do documento"
>
> **Prompt 3 — Ajuste de escopo (redução para 10):**
> "Diminua a quantidade de testes, para 10"
>
> **Prompt 4 — Ajuste de escopo (ampliação para 15):**
> "Altere o documento para que contenha no máximo 15 casos de teste para teste, mantenha o formato dele, apenas diminua os casos de teste contido nele (caso_tarifas.md)"
>
> **Prompt 5 — Esclarecimento de técnica:**
> "Onde a partição de equivalência está presente nos casos de teste?"

## Resposta da IA — passo a passo

### 1. Análise do código e mapeamento de regras

1. Leu os arquivos do módulo de tarifas: `app/dominio/tarifas.py` (classes `TipoConta`, `TarifasBase` e `TarifaBancaria`), `app/web/routes/tarifas.py` (rota `/tarifas`) e `app/templates/tarifas.html` (formulário).
2. Leu a documentação da aplicação (`docs/aplicacao.md`) para contexto adicional.
3. Mapeou a árvore de decisão completa do método `tarifa_mensal` (CC = 12), identificando:
   - 3 tipos de conta (`CORRENTE`, `POUPANCA`, `PREMIUM`) com tarifas base distintas.
   - Faixas de isenção por saldo: R$ 5.000 (corrente) e R$ 50.000 (premium).
   - Cota de 10 transações gratuitas, R$ 2,50 por excedente.
   - Descontos com pacote: 50% (corrente + saldo ≥ 5.000), 30% (premium × 0,7), isenção total (premium + saldo ≥ 50.000).
   - Ramos de antiguidade (≥ 24 e ≥ 36 meses) e saldo negativo existentes no domínio.
4. Identificou que a rota web **não expõe** os parâmetros `antiguidade_meses` (sempre `0`) e que o formulário tem `min="0"` (bloqueia saldo negativo), limitando os ramos testáveis via interface.

### 2. Avaliação dos cenários propostos pelo testador

1. Avaliou cada um dos 7 cenários propostos, confirmando que cobriam o básico: tipos de conta, bifurcação pacote, variação isolada de saldo e transações, e caso zero.
2. Identificou **6 lacunas**:
   - Ausência de valores de fronteira (BVA) nas faixas de isenção de saldo (R$ 5.000 / R$ 50.000).
   - Ausência de valores de fronteira na cota de transações gratuitas (9/10/11).
   - Falta de interação pacote × faixa de saldo (desconto diferenciado).
   - Falta de verificação de que o pacote ignora transações excedentes.
   - Falta de combinação isenção por saldo + transações excedentes.
   - Cenários de antiguidade e saldo negativo inacessíveis pela interface.
3. Identificou redundância parcial entre dois cenários propostos (saldo zerado + transações e saldo + transações zeradas) com os cenários de variação isolada.

### 3. Geração e iteração do documento

1. Gerou o documento `tests/testes_manuais/tarifas/caso_tarifas.md` no formato dos outros devs (seções: Identificação, Pré-condições, Dados de teste, Casos de teste, Defeitos e observações, Conclusão), com **35 casos** organizados em 9 grupos (A–I).
2. Criou a pasta `tests/testes_manuais/tarifas/evidencias/` para screenshots.
3. A pedido do testador, **reduziu para 10 casos**, selecionando os mais representativos para maximizar cobertura de ramos.
4. A pedido do testador, **ampliou para 15 casos**, adicionando 5 cenários que preenchiam lacunas importantes: BVA da fronteira premium (R$ 49.999,99 / R$ 50.000,00), BVA da cota de transações (exatamente 10), poupança com transações (prova que é sempre isenta), e pacote ignorando transações extras.

### 4. Esclarecimento sobre Partição de Equivalência

A pedido do testador, a IA explicou como a PE está presente nos casos:
- **PE define as classes**: tipo de conta (3 classes), saldo por tipo (2 classes: abaixo/acima da isenção), transações (2 classes: dentro/acima da cota), pacote (2 classes: sim/não), e pacote × saldo (3 classes de desconto).
- **BVA testa nas fronteiras** entre essas classes: valores como `4.999,99` / `5.000,00` estão exatamente na divisa entre a classe "abaixo da isenção" e "isento".
- Os casos com valores "típicos" (saldo 0, saldo 3.000) são PE pura; os casos com valores de fronteira são BVA complementando a PE.

## Solução inicial (cenários pensados) vs. solução final (IA complementando)

| Solução inicial | Solução final | Alterações realizadas |
|---|---|---|
| 7 cenários descritivos sem valores concretos, focados em variação isolada de cada variável (tipo de conta, saldo, transações, pacote e valores zerados) | Suíte com 15 casos concretos com dados de entrada, resultado esperado calculado, BVA nas fronteiras de isenção e interação entre variáveis | A IA definiu as faixas de valores (BVA nas fronteiras R$ 5.000, R$ 50.000 e cota de 10 transações), adicionou cenários de interação (pacote × saldo, isenção + transações extras, pacote ignorando extras), calculou os resultados esperados para cada caso e documentou as limitações da interface |

**Decisão:** Os cenários iniciais do testador foram mantidos como base (Grupos A–D, representados nos CT-01 a CT-10) e complementados com 5 cenários adicionados pela IA (CT-11 a CT-15) para cobrir interações entre variáveis e descontos diferenciados.

## Ações executadas

1. Análise do código-fonte de `app/dominio/tarifas.py`, `app/web/routes/tarifas.py` e `app/templates/tarifas.html`.
2. Mapeamento da árvore de decisão do `tarifa_mensal` (CC = 12) e das constantes de `TarifasBase`.
3. Avaliação dos 7 cenários propostos pelo testador e identificação de 6 lacunas.
4. Definição de faixas de valores por BVA para saldo e transações.
5. Geração do documento de teste manual em `tests/testes_manuais/tarifas/caso_tarifas.md` (3 iterações: 35 → 10 → 15 casos).
6. Criação da pasta `tests/testes_manuais/tarifas/evidencias/`.
7. Esclarecimento sobre a relação entre Partição de Equivalência e BVA nos casos.

## Limitações registradas no documento

- **Antiguidade não exposta:** o campo `antiguidade_meses` existe no domínio (desconto de 50% com pacote para ≥ 24 meses e de 20% sem pacote para ≥ 36 meses), mas a rota web sempre envia `0`. Ramos de antiguidade não são testáveis via interface.
- **Saldo negativo bloqueado:** o formulário tem `min="0"`, mas o domínio cobra taxa adicional de R$ 6,00 para saldo negativo. Ramo não testável via interface.
- Ambos os cenários devem ser cobertos por testes unitários diretamente na classe `TarifaBancaria`.

## Resultado

- **Artefato principal:** `tests/testes_manuais/tarifas/caso_tarifas.md` — 15 casos projetados cobrindo todos os ramos acessíveis pela interface web do método `tarifa_mensal` (8 dos 12 caminhos; os 4 restantes dependem de parâmetros não expostos pela UI).
- **Técnicas:** Partição de Equivalência (classes de tipo de conta, faixas de saldo, cota de transações, pacote) + Análise de Valor-Limite (fronteiras R$ 4.999,99/5.000,00, R$ 49.999,99/50.000,00, 10/11 transações).
- **Evidências:** a preencher durante a execução dos testes em `tests/testes_manuais/tarifas/evidencias/`.

