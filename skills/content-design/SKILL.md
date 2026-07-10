---
name: content-design
description: 5 regras de escrita para todo artefato persistido (nota, resumo, doc, README). Front-load, 1 ideia/frase, concreto. Aplicar antes de salvar qualquer texto que outra pessoa (ou sessão futura) vai ler.
trigger: ["escrever doc", "salvar nota", "resumo", "documentar", "content design", "write docs", "draft readme"]
---

<what-to-do>

Aplique 5 regras ao texto **antes de salvar**. Não mudam o conteúdo — mudam a ordem e o corte. Objetivo: leitor sabe se precisa do resto na 1ª linha. Front-load aplicado à escrita: economia de atenção (e token) na leitura futura.

## As 5 regras

**1. Comece da necessidade do leitor.** Escreva o que a pessoa precisa pra decidir ou fazer algo — não o que você quer contar. Corte introdução-aquecimento ("Neste documento exploraremos...").

**2. Front-load tudo.** Pirâmide invertida: conclusão → detalhe → background. Vale no documento, na seção, no parágrafo e na frase. O veredito vai na linha 1, nunca no §4.

**3. Uma ideia por frase. Um tópico por parágrafo.** Frase com 2 ideias → quebre em 2.

**4. Específico e concreto.** Dê o número, o nome, a data. Corte abstração vaga: "uma gama de", "indo adiante", "de certa forma", "em termos de".

**5. Corte o que não adiciona sentido.** Curto é mais claro. Remova duplicata.

## Fluxo

1. Leia o rascunho inteiro.
2. Ache a conclusão/veredito. Se não está na 1ª linha → mova pra cima (regra 2).
3. Varra frase a frase: 2 ideias → quebra (3). Palavra vaga → número/nome (4). Não adiciona → corta (5).
4. Cheque abertura: fala da necessidade do leitor ou de você? (1)
5. Salve.

## Checklist pré-save

- [ ] Linha 1 entrega o ponto (leitor decide se lê o resto)
- [ ] Nenhuma frase com "e também" carregando 2ª ideia
- [ ] Zero "uma gama de / indo adiante / de certa forma"
- [ ] Números e nomes onde havia vago
- [ ] Nada repetido

## Exemplo

**Antes** (veredito enterrado, vago):
> Neste relatório vamos explorar diversos aspectos da migração. Ao longo do documento, cobriremos uma gama de considerações técnicas. De certa forma, a nova arquitetura traz melhorias. Após análise, concluímos que a latência caiu.

**Depois** (regras 1, 2, 4 aplicadas):
> Latência caiu 340ms→90ms após a migração. Causa: cache de prefixo no edge. Detalhes de config abaixo.

## Escopo

Aplica a: nota, resumo, conceito, README, ADR, relatório — qualquer texto persistido que alguém lê depois.
Não aplica a: transcript cru, captura de inbox (fica cru até processar).

## Par validador

Depois de redigir, rode **content-design-review** (skill irmã) — audita o texto contra estas 5 regras e devolve veredito por linha. Padrão _generate + review_: esta molda, a outra reprova.

</what-to-do>
