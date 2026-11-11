---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: test-audit
description: "Use when: podar suíte de testes existente — achar teste que reafirma a fonte, duplica prova mais forte, acopla a implementação ou mantém seam de produção só para teste. Modo audit (lote pequeno de alta confiança) ou campaign (superfície inteira de um subsistema, ledger R/F/C/D, keeper por contrato, preservation review com mutação). Escrever teste novo é tdd (authoring gate); sondar comportamento sem foco em segurança é diagnose ou verify-runner."
skill: test-audit
version: 1.0
author: Nexus Agent System
source: openclaw/openclaw .agents/skills/test-audit (SKILL.md + CAMPAIGN.md, lido 2026-09-28) — adaptado, comandos do OpenClaw removidos
trigger: ['/test-audit', '@test-audit']
effort: medium
tags: [testing, test-audit, pruning, coverage, mutation, campaign]
updated: 2026-09-28
reads: []
writes:
  - 06-GENERATED/audits/
  - 06-GENERATED/tasks/lessons.md
triggers:
  positive:
    - "/test-audit"
    - "suíte inchada ou frágil"
    - "podar testes"
    - "teste quebra em refactor sem mudar comportamento"
    - "limpar testes duplicados"
  negative:
    - "escrever teste novo"
    - "fix de bug test-first"
    - "sondar comportamento de sistema"
    - "auditoria de segurança"
consumes: ["test-suite", "production-owner"]
tools: []
references:
  - 04-SYSTEM/automation/skills/dev/tdd/SKILL.md
  - 04-SYSTEM/automation/skills/dev/code-review/SKILL.md
  - 04-SYSTEM/automation/workflows/portas/dev.md
verifier: ["Todo candidato a D/C tem os 7 campos de evidência antes de editar; todo contrato restaurado tem uma mutação pega pelo keeper, com a fonte restaurada byte a byte; suíte do dono e irmãos verde depois da edição; LOC de produção reportado separado de teste."]
human_gate: true
reviewed-scope: "checagem mecanica + semantica: 5/5 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 12 secoes, 228 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---

# Skill: Test Audit

## Propósito

Podar teste que custa manutenção sem proteger comportamento. A régua é
confiança, não número de deleções. Dois modos com a mesma régua:

- **audit**: poucos candidatos de alta confiança, um lote coerente por dono.
- **campaign**: a superfície de teste inteira de um subsistema, em 8 fases.

O gate de autoria (teste novo) mora em
[tdd](../tdd/SKILL.md#authoring-gate) — esta skill usa a mesma
lista de junk patterns para caçar teste existente.

> **Leading word: keeper.** Cada contrato tem um único teste dono na fronteira
> mais forte. Todo o resto justifica um risco distinto ou sai.

## Quando NÃO usar

- Escrever teste novo ou fix test-first → `tdd`.
- Sondar comportamento de sistema, QA exploratório → `diagnose` (falha sem causa) ou `verify-runner` (execução com evidência). Não há skill dedicada a QA exploratório. Scan de segurança com payloads → `test-probing`.
- Revisar um diff → `/code-review`.
- Teste lento ou estático sem outro defeito: lento não é motivo de deleção.

## Value bar

Teste justifica o custo quando protege comportamento, regressão crível ou
contrato independente. Teste que precisa mudar numa reorganização que preserva
comportamento é **suspeito**, não automaticamente deletável.

Antes de julgar um candidato, leia inteiros: o teste, o dono em produção, o
entry point, callers, callees, implementações irmãs, testes sobrepostos, CI e
histórico (`git log -S`, `git blame`). Leia `AGENTS.md`/`CLAUDE.md` da raiz e
do escopo primeiro. Se o teste afirma comportamento de dependência, leia a
fonte ou os tipos da dependência.

## Junk patterns

Lista compartilhada com o authoring gate do `tdd`:

- teste sem asserção (probe de cobertura);
- auto-comparação ou copiador de identidade;
- fixture, inventário, manifest ou lista de export copiados;
- grep exato de fonte, import ou string;
- teste de predicado privado ou formato de chamada, duplicado na fronteira real;
- invocação duplicada do mesmo contrato;
- replay local de helper compartilhado;
- teste que só existe para preservar export, global ou wrapper de teste;
- código de produção morto cujo único caller é teste;
- valor esperado produzido pelo helper ou renderer sob teste;
- mock que implementa o comportamento afirmado, ou um mock idêntico no lugar
  de APIs diferentes;
- fixture que fornece o receipt, a admissão ou a ordem de callback que o dono
  deveria produzir; persistência afirmada contra um store que o caminho nunca
  escreve;
- teste de capability que reafirma a flag declarada em vez de exercer a
  entrega que a flag promete;
- controle negativo que passa por motivo não relacionado (negação de outro
  guard, rejeição que o caminho de produção nunca alcança);
- nome ou fixture que promete mais que o input exercita.

## Retention bar

Mantenha o teste quando ele guarda sozinho um contrato de API pública,
protocolo, config, migration, storage, segurança, plataforma, default,
bytes de prompt, artefato gerado, pacote, release ou arquitetura. Mantenha
também:

- ordem de chamada, quando a ordem é comportamento observável;
- regressão com modo de falha crível;
- inspeção de fonte quando é o guard independente mais barato: falha quando o
  contrato muda (chave, byte ou path que o usuário vê) e sobrevive a rename de
  identificador;
- teste mantido que falha no baseline: trate como possível bug de produto,
  reproduza e conserte o dono em vez de deletar.

Teste parecido com a implementação pode ser o contrato independente. Prove o
contrário antes de remover.

## Evidência por candidato

Registre todos os campos antes de editar. Campo faltando = candidato não
está pronto:

1. nome exato e local do teste;
2. qual falha ele detecta de fato;
3. callers fora de teste do seam coberto;
4. prova mais forte que continua, ou por que nenhuma prova é necessária;
5. histórico e motivo pelo qual o teste ou o seam existe;
6. deleção de produção ou suporte que ele destrava;
7. risco e o comando de validação focada.

## Modo audit

1. **Descoberta read-only.** Relate evidência antes de editar. Escopo amplo →
   lanes paralelas de `finder`/`scout` (core, plugins/áreas, UI/scripts, uma
   varredura transversal de padrão). Prefira poucos candidatos certos a um
   inventário especulativo.
2. **Forma da edição.** Um lote coerente por dono. Delete export, global,
   wrapper e caminho de produção morto que só teste usava — sem alias. Mova a
   regressão mantida para o dono canônico. Consolide asserção repetida num
   contrato genérico. Prefira LOC de produção líquido negativo. Não adicione
   teste substituto que reafirma a mesma implementação.
3. **Validação.**
   1. Rode os menores testes do dono e dos irmãos.
   2. Para grep de fonte removido, rode o script ou dry-run dono do contrato real.
   3. Formatação focada e `git diff --check`.
   4. Rode os gates que a política do repo exige para os paths mudados.
   5. `git diff --numstat`: produção e tooling separados de teste e suporte.
   6. `/code-review` sobre o diff final.

Não edite fonte nem teste com o runner de teste rodando no mesmo checkout.

## Modo campaign

Uma superfície de subsistema inteira. Cada fase fecha no critério de done;
não comece a próxima antes. Multi-sessão por natureza: handoff entre fases
pela skill `handoff`.

| Fase | Trabalho | Done quando |
|---|---|---|
| C1 Baseline | contagem de linhas de teste e suporte; pass/fail de cada arquivo num SHA fixo; falhas do baseline numa lista própria | todo arquivo no escopo tem resultado registrado **e** aparece na coleta do runner (`--collect-only` ou equivalente); arquivo ausente da coleta é defeito, não verde |
| C2 Lanes | dividir a superfície por **fronteira de dono em produção**, não por prefixo de arquivo; incluir casos do subsistema em fronteiras compartilhadas e harness de QA | todo arquivo de teste pertence a exatamente uma lane |
| C3 Ledger | um agente read-only por lane lê cada teste inteiro (tabelas de parâmetro inclusas) e o dono; cada declaração recebe uma marca e uma linha de evidência | toda declaração da lane tem marca e evidência |
| C4 Plano de camada | segunda passada read-only a partir do ledger procura a **camada** redundante (camadas: boundary = 1 adaptador com IO real · composition = fiação · acceptance = CLI ponta a ponta · evaluation = teste sobre a própria suíte; o keeper fica na camada mais baixa que observa o contrato `[hyp]`); nomeia o keeper por contrato; prefere transporte real com rede fake a colaborador mockado; corrige o ledger | cada lane nomeia arquivos aposentados, keeper por contrato, asserções a levar e seams de teste destravados |
| C5 Cutover | editar lane a lane; harness e suporte compartilhados serializados por um único dono; remover os seams destravados; atualizar CI e inventários; regra durável de posse de teste no `AGENTS.md` do subsistema, tirada de erro que a campanha achou | todo plano aplicado e keepers verdes |
| C6 Preservation review | revisores independentes, um por grupo de fronteira, comparam cobertura deletada com keepers: contrato que perdeu a única prova, asserção nova que não pode falhar; para cada contrato restaurado, **uma mutação** deliberada no dono → keeper fica vermelho → fonte restaurada byte a byte | todo gap restaurado ou rejeitado com evidência de fonte, e todo contrato restaurado tem mutação pega |
| C7 Defeitos | falha do baseline que sobrevive num keeper é bug: fix no dono em commit separado, provado pelo fluxo real, com **control run** que reverte o fix e mostra o comportamento antigo; discrepância não relacionada vira follow-up | cada defeito tem control vermelho e candidato verde no mesmo harness |
| C8 Reconciliar | campanha longa: merge da base, não rebase; se a base mexeu num arquivo deletado, mantenha a deleção e porte o contrato novo para o keeper; rode a suíte inteira do subsistema na cabeça mesclada | toda regressão nova da base tem casa; suíte inteira verde |

Marcas do ledger (C3):

- **R** retain — nomeia o contrato e o bug que pega (mover de arquivo continua R);
- **F** fix — mantém o contrato, conserta a asserção (ex.: negativo vazio que
  passa quando só um de vários itens falta);
- **C** consolidate — nomeia primeiro o dono que absorve a asserção;
- **D** delete — nomeia a prova que continua, ou por que não há contrato.

Julgue pela asserção, não pelo nome: na campanha de origem, um teste chamado
"retires the window" afirmava que a janela *não* foi limpa. Trate o ledger como
entrada do C4, não como lista de edição.

Ledger e plano ficam em `06-GENERATED/audits/<data>--test-audit--<subsistema>/`.

## Completion

- [ ] Todo candidato editado tem os 7 campos de evidência
- [ ] Nenhuma deleção sem prova mais forte nomeada
- [ ] Falha de baseline tratada como possível bug, não apagada
- [ ] (campaign) Todo contrato restaurado tem mutação pega e fonte restaurada
- [ ] Suíte do dono e irmãos verde; `git diff --check` limpo
- [ ] LOC de produção reportado separado de teste
- [ ] `/code-review` sem bloqueante

## Handoff

Relate:

- causa raiz e categorias de baixo valor removidas;
- simplificações no dono em produção;
- falsos positivos mantidos e por que valem;
- prova focada e completa que rodou de fato;
- LOC de produção vs teste (campaign: baseline e final);
- (campaign) lanes, camadas aposentadas e keepers; gaps de preservação e suas
  mutações; defeitos com control e candidato;
- estado de PR/merge e follow-ups nomeados.

Commit, push e PR só com autorização. Um lote coerente por vez; depois de
integrar, rode a descoberta read-only de novo sobre a base atual. Pare quando o
lote estiver verificado ou o próximo candidato não tiver os 7 campos; incerteza
vai para a lista do handoff, não para rodada nova.

## Failure modes

- **Contar deleção**: converter candidato incerto em limpeza para subir número.
- **Julgar pelo nome**: marcar pelo título do teste sem ler a asserção.
- **Ledger vira lista de edição**: pular o C4 e perder a camada redundante.
- **Negativo de graça**: controle negativo novo que passa por outro guard.
- **Apagar vermelho do baseline**: o teste pode estar certo e o produto errado.
- **Retry verde**: rerun só testa uma hipótese transitória nomeada; guarde a falha original. Verde no retry não é causa nem fix.
- **Subagente escreve em massa**: lanes são read-only; escrita serializada num
  único dono.

## Relacionado

- [tdd](../tdd/SKILL.md) — authoring gate (teste novo)
- [test-probing](../test-probing/SKILL.md) — scan de segurança automatizado (static, dynamic, harness)
- [code-review](../code-review/SKILL.md) — review do diff final
- dev — porta de entrada
