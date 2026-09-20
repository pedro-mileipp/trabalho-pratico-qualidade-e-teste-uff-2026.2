# Caso de Teste Manual — Crédito

> Documento da issue **#10** — caso de teste manual da funcionalidade de análise de crédito do Banco Digital.

## 1. Identificação

| Campo | Valor |
|---|---|
| Funcionalidade | Análise de Crédito (`/credito`) |
| Issue | [#10](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/10) |
| Executor | A definir |
| Data de execução | A definir |
| Ambiente | Linux (Ubuntu) · Google Chrome · `DATABASE=/tmp/teste.db` |
| Build testado | commit `main` |
| Técnica aplicada | Partição de equivalência + análise de valor-limite |

## 2. Pré-condições e preparação

1. Subir a aplicação Flask com banco SQLite isolado em `/tmp/teste.db`:
   ```bash
   DATABASE=/tmp/teste.db uv run flask --app app:create_app run
   ```
2. Acessar `http://127.0.0.1:5000/` no navegador.
3. Registrar-se em `/registro` com um usuário válido.
4. Acessar `/credito` para chegar à tela de análise de crédito.

### Dados de teste

| Dado | Valor | Classificação |
|---|---|---|
| Renda válida | `10000` | entrada válida |
| Valor válido | `5000` | entrada válida |
| Renda zero | `0` | entrada inválida (fronteira) |
| Renda negativa | `-1000` | entrada inválida |
| Valor zero | `0` | entrada inválida (fronteira) |
| Valor negativo | `-500` | entrada inválida |
| Valor muito alto | `100000` | entrada inválida (acima do limite máximo) |

**Nota**: O formulário atual não permite enviar histórico de pagamentos. Com `registros=[]`, o score inicial é 500 (padrão).

## 3. Casos de teste propostos

| ID | Cenário | Origem | Pré-condição | Passos | Dados de entrada | Resultado esperado | Resultado obtido | Status | Evidência |
|---|---|---|---|---|---|---|---|---|---|
| CT-01 | Aprovação — valor dentro do limite | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `10000`; 2) Preencher valor `5000`; 3) Clicar em "Analisar" | renda=`10000`, valor=`5000` | Score 500 · Limite R$ 10000.00 · Motivo: **aprovado** | Score: `500` - Limite: `R$ 10000.00` - Motivo: aprovado| PASS | `ct01-aprovacao-valor-dentro-limite.png` |
| CT-02 | Aprovação — valor exatamente no limite | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `10000`; 2) Preencher valor `10000`; 3) Clicar em "Analisar" | renda=`10000`, valor=`10000` | Score 500 · Limite R$ 10000.00 · Motivo: **aprovado** | Score: `500` - Limite: `R$ 10000.00` - Motivo: aprovado | PASS | `ct02-valor-exatamente-limite.png` |
| CT-03 | Aprovação parcial — valor entre limite e 1.5x limite | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `10000`; 2) Preencher valor `12000`; 3) Clicar em "Analisar" | renda=`10000`, valor=`12000` | Score 500 · Limite R$ 10000.00 · Motivo: **parcial** (liberação parcial até R$ 10000) | Score: `500` · Limite: `R$ 10000.00` · Motivo: parcial | PASS | `ct03-valor-entre-limite-1_5x-limite.png` |
| CT-04 | Negação — valor acima de 1.5x limite | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `10000`; 2) Preencher valor `20000`; 3) Clicar em "Analisar" | renda=`10000`, valor=`20000` | Score 500 · Limite R$ 10000.00 · Motivo: **negado** (motivo: acima_limite) | Score: `500` · Limite: `R$ 10000.00` · Motivo: `acima_limite` | PASS | `ct04-valor-acima-1_5x-limite.png` |
| CT-05 | Negação — valor zero | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `10000`; 2) Preencher valor `0`; 3) Clicar em "Analisar" | renda=`10000`, valor=`0` | Motivo: **negado** (motivo: valor_invalido) | Score: `500` · Limite: `R$ 10000.00` · Motivo: `valor_invalido` | PASS | `ct05-valor-zero.png` |
| CT-06 | Negação — valor negativo | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `10000`; 2) Preencher valor `-500`; 3) Clicar em "Analisar" | renda=`10000`, valor=`-500` | Mensagem de alerta no campo do formulário informando que valor deve ser maior ou igual a 0 | Mensagem de alerta no campo do formulário informando que valor deve ser maior ou igual a 0  | PASS | `ct06-valor-menor-que-zero.png` |
| CT-07 | Negação — renda zero | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `0`; 2) Preencher valor `5000`; 3) Clicar em "Analisar" | renda=`0`, valor=`5000` | Score 500 · Limite R$ 0.00 · Motivo: **negado** (motivo: sem_limite) | Score: `500` · Limite: `R$ 0.00` · Motivo: `sem_limite` | PASS | `ct07-renda-zero.png` |
| CT-08 | Negação — renda negativa | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `-1000`; 2) Preencher valor `5000`; 3) Clicar em "Analisar" | renda=`-1000`, valor=`5000` | Mensagem de alerta no campo do formulário informando que valor deve ser maior ou igual a 0 | Mensagem de alerta no campo do formulário informando que valor deve ser maior ou igual a 0 | PASS | `ct08-renda-negativa.png` |
| CT-09 | Fronteira — valor igual a 1.5x limite exato | Proposto | Usuário autenticado na página de crédito | 1) Preencher renda `10000`; 2) Preencher valor `15000`; 3) Clicar em "Analisar" | renda=`10000`, valor=`15000` | Score: 500 · Limite: R$ 10000.00 · Motivo: parcial | Score: `500` · Limite: `R$ 10000.00` · Motivo: `parcial` | PASS | `ct09-limite-1_5x.png` |
| CT-10 | Fronteira — valor ligeiramente abaixo de 1.5x limite | Adicionado por IA | Usuário autenticado na página de crédito | 1) Preencher renda `10000`; 2) Preencher valor `14999.99`; 3) Clicar em "Analisar" | renda=`10000`, valor=`14999.99` | Score 500 · Limite R$ 10000.00 · Motivo: **parcial** | Score: `500` · Limite: `R$ 10000.00` · Motivo: `parcial` | PASS | `ct10-pouco-abaixo-1_5x.png` |

## 4. Defeitos e observações

**Nenhum defeito identificado** — todos os 10 casos de teste executados com sucesso.

### Observações

- **CT-06 e CT-08 (valores negativos)**: a validação ocorre no front-end (HTML5 `min="0"`), com mensagem de alerta nativa do navegador. O back-end recebe apenas valores ≥ 0, logo a rota `decidir()` nunca é chamada com `valor_solicitado < 0` — o que é um comportamento correto e seguro.
- **Cobertura de score**: todos os testes usaram `score = 500` (padrão, sem histórico de pagamentos). Não foram exercitadas situações com `score < 300` (motivo `score_baixo`) nem com `score ≥ 850` (limites maiores).
- **Fronteira do limite máximo**: não foi testado o caso em que `renda * 2.0` ultrapassa `limite_maximo` (R$ 50.000,00), o que poderia limitar o crédito mesmo com score alto.
- **Limite de 1.5x exato (CT-09)**: o valor `15000` (1.5 × 10000) foi classificado como `parcial`, confirmando que a fronteira `valor_solicitado <= limite * 1.5` está implementada corretamente.

## 5. Conclusão

O teste manual cobriu os cenários de partitionamento de equivalência e valor-limite para a funcionalidade de análise de crédito. Todos os resultados obtidos coincidiram com os esperados:
p
- **Aprovação** (CT-01, CT-02): comportamento correto para valores dentro do limite.
- **Aprovação parcial** (CT-03, CT-09, CT-10): valores entre o limite e 1.5× o limite são corretamente classificados como `parcial`.
- **Negação por valor** (CT-04, CT-05, CT-06): valores acima de 1.5× limite, zero ou negativos são rejeitados com o motivo adequado.
- **Negação por renda** (CT-07, CT-08): renda zero ou negativa bloqueia a análise.

**Resultado final**: 10/10 casos de teste **APROVADOS**. A funcionalidade atende aos critérios de aceitação documentados para os cenários testados. Recomenda-se a execução de testes automatizados com variações de score (especialmente < 300 e ≥ 850) e com valores de renda elevados para cobrir a fronteira do `limite_maximo`.
