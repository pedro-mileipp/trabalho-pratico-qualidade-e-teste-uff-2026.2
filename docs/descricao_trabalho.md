# Trabalho Prático

## Descrição

O grupo deverá aplicar os conceitos aprendidos na disciplina Qualidade e Teste em até dois softwares livres à escolha. Poderá ser um software existente ou gerado ou adaptado por AI.

A professora deverá ser consultada previamente para analisar o grau de dificuldade e a aderência no escopo da disciplina Qualidade e Teste.

**Sugestão de repositórios:** https://github.com/orgs/repo-software-testing-courses/repositories

Além da aplicação das técnicas de teste, o trabalho também considera o cenário atual de desenvolvimento de software com apoio de Inteligência Artificial Generativa (IA). O uso de ferramentas de IA é permitido e incentivado, desde que seu uso seja documentado, avaliado criticamente e acompanhado de evidências de validação.

## Entrega

A entrega deverá ser feita no repositório em repositório público e enviar o link na entrega do Google Classroom. Entregar link da documentação editável com histórico de versões aqui na atividade. Façam alterações logados de modo a ser possível identificar as colaborações.

### Importante

- Todos os artefatos devem estar disponíveis na branch principal (main ou master) do repositório acima. Artefatos incluídos em outras branches ou em outros repositórios não serão considerados para avaliação.
- O arquivo `README.md` deve conter links diretos ou instruções claras para localizar todos os artefatos entregues (códigos, documentos, diagramas, evidências, etc.). Caso um artefato não esteja devidamente referenciado ou seja difícil de localizar, ele não será avaliado.
- Os slides e material de apresentação devem ser disponibilizados no diretório apropriado enviado pela professora.

## Uso de Inteligência Artificial

É permitido utilizar ferramentas de Inteligência Artificial Generativa durante o trabalho, incluindo, entre outras, ChatGPT, Claude, Gemini, GitHub Copilot, etc.

- O uso de IA não deverá ser ocultado.
- A utilização de IA não reduz a responsabilidade do grupo pelo conteúdo entregue.
- O grupo é responsável por todo artefato entregue, independentemente de ter sido produzido manualmente ou com auxílio de IA. Não será aceita como justificativa para erros a afirmação de que determinado conteúdo foi produzido por uma ferramenta de IA.
- Todo integrante deverá ser capaz de explicar, defender e, quando solicitado, modificar os artefatos sob sua responsabilidade.

### Registro do uso de IA

O grupo deverá manter no repositório o arquivo: `docs/ai/AI-LOG.md`.

O documento deverá registrar as interações com IA que tenham contribuído substancialmente para os artefatos do trabalho. Não é necessário documentar interações utilizadas exclusivamente para correções ortográficas, configurações de IDE, etc.

Para cada uso relevante deverão ser registradas, sempre que aplicável, as seguintes informações:

| Informação | Descrição |
|---|---|
| Responsável | integrante que realizou a interação |
| Atividade | atividade do trabalho associada |
| Ferramenta | ChatGPT, Claude, Copilot etc. |
| Prompt/instrução | prompt ou instrução utilizada |
| Resultado | breve descrição da resposta da IA |
| Decisão | o que foi aceito, alterado ou rejeitado |
| Validação | como o resultado foi verificado |

- Quando possível, conversas completas, prompts, configurações ou outros registros poderão ser armazenados em uma pasta própria dentro do diretório `docs/ai/`.
- Para agentes ou ferramentas configuráveis, deverão ser registradas também as instruções, ferramentas e configurações definidas pelo grupo, quando estas informações estiverem disponíveis.

### Critérios de avaliação do uso de IA

- O simples uso de IA não será considerado mérito. Será considerada principalmente a capacidade de verificar a resposta produzida, identificar erros, casos ausentes, melhorar a solução, apresentar evidências sobre a qualidade da solução final, etc.
- Sempre que a IA for utilizada de forma relevante na geração ou melhoria de testes, o grupo deverá preservar, quando viável, a solução inicialmente produzida com auxílio da IA, a solução final após revisão e uma descrição das alterações realizadas.

## Entregas

Serão realizadas duas entregas:

### Entrega 1 (Peso 3)

- **Descrição do escopo do(s) sistema(s)**: Definir quais módulos/componentes serão testados. Descrever o escopo no Plano de Teste.
- **Código-fonte original**: Projetar casos de testes unitários de pelo menos uma classe (não CRUD [entidade] e com complexidade razoável) para cada membro do grupo.
- **Plano de teste**: Elaborar o documento de Plano de Teste. Sugestão: utilizar template apresentado em aula. Incluir quais artefatos serão gerados, ferramentas que serão utilizadas, etc.
- **Projetar e executar casos de testes manuais**: Pelo menos uma funcionalidade para cada membro do grupo.
- **Uso da ferramenta Testlink** para ao menos um cenário de teste. O grupo pode optar por usar outra ferramenta. Os demais casos podem ser feitos por ferramenta ou documentos de texto/planilha.
- **Reportar os erros** em uma ferramenta de bug tracking (ou git issues).

### Entrega 2 (Peso 5)

Realizar no mínimo:

- Melhorar e aumentar os casos de testes unitários, isolando suas dependências.
- Implementar casos de teste de integração.
- Indicação das medidas de cada atributo de qualidade da ISO 25010 seguindo uma escala. Justificar as decisões para indicação das medidas.
- Implementar testes de sistema considerando requisitos funcionais.
- **Selenium**.
- Pelo menos um requisito não funcional (atributos de qualidade - Exemplo: desempenho, segurança) (último opcional).
- Projetar e melhorar o conjunto de casos de teste, utilizando as técnicas:
  - **Funcional**.
  - **Estrutural** (ao menos 80% de cobertura no critério todas-arestas). Pelo menos uma classe (não CRUD [entidade] e com alta complexidade) para cada membro do grupo.
  - **Baseada em Defeitos** (80% de escore de mutação nas mesmas classes do teste estrutural).
- **Relatório de inspeção do código-fonte** (ex., usando Sonar). Executar a ferramenta e enviar print.
- Resolver os problemas de pelo menos uma classe (não CRUD [entidade] e com complexidade razoável) para cada membro do grupo. Enviar print depois das correções.

> Documentos de texto devem ser elaborados no Google Docs, com todos os membros logados em suas contas, de forma que seja possível visualizar a colaboração individual de cada integrante. Os links para esses documentos devem estar disponíveis no arquivo README do repositório.

## Avaliação

Para a solução serão avaliados:

- O uso adequado dos conceitos de Qualidade e Teste.
- Artefatos produzidos com base na sua completude, corretude e capacidade de argumentação em relação às decisões tomadas.
- Resultados e colaboração individual no trabalho. Serão considerados participação em sala no desenvolvimento do trabalho, colaboração no GitHub e descrição das responsabilidades do aluno.
- Apresentação e corretude das respostas individuais durante as apresentações do trabalho.

## Regras

- O trabalho deve ser feito em grupos de 5 pessoas. As responsabilidades de cada aluno deve ser documentada e registrada.
- Todos os alunos devem apresentar o trabalho no prazo definido. O não cumprimento do prazo invalida o trabalho. Alunos que não participarem da apresentação ficarão sem nota do trabalho.

## Cronograma

| Data | Atividade |
|---|---|
| 17/09/2025 | Apresentar a formação dos grupos e escolha do(s) sistema(s) adotado |
| — | Criar repositório do grupo no GitHub Classroom e fazer fork do(s) sistema(s) escolhido(s) |
| 06/10/2025 | Entrega 1 |
| 06 e 08/10/2025 | Apresentação parcial do trabalho |
| 07/07/2025 | Entrega 2 |
| 01 e 03/12/2025 | Apresentação final do trabalho |

## Requisitos dos softwares a ser adotado

### Obrigatório

- O código-fonte precisa estar disponível publicamente.
- Ao menos um dos projetos não deve ser composto apenas por funcionalidades simples, como formulários de cadastro sem algoritmos mais elaborados. Um dos projetos deve conter classes com uma complexidade razoável, ou seja, que incluam comandos com desvios, laços, ou estruturas de controle.
- Um dos projetos deve possuir ao menos uma classe com alta complexidade para cada membro do grupo. Mínimo: complexidade ciclomática de cada classe sob teste: 10.

### Desejável

- Um dos projetos ser um sistema web.
- Projeto com complexidade mais alta ser desenvolvido em Java (para conseguir aplicar todas as ferramentas que serão abordadas no curso).

## Considerações

- Os membros da equipe serão avaliados pelo resultado final e pelos resultados individuais alcançados. Assim, numa mesma equipe, um membro pode ficar com nota 9.0 e outro com nota 5.0, por exemplo.
- Será considerado o nível de dificuldade dos projetos na composição da nota final. Importante consultar a professora para adequação.