# Relatório do Dia 02 — Grupo 03
 
## Execuções
- Primeira execução (modo auditoria): <link>
- Execução final (modo bloqueio): <link>
- Deploy aprovado por: <nome> em <data/hora> — imagem: <ghcr.io/...@sha256:...>
 
## Placar da esteira
| Etapa | Achados (1ª execução) | Corrigidos | Falsos positivos | Exceções |
|---|---|---|---|---|
| 01 | 3 | 2 | 1 | 0 |
| 02 | 22 | 21 | 1 | 0 |
| 03 | 10 | 9 | 0 | 1 |
| 04 | 48 | 48 | 0 | 0 |
| 05 | 1927 | 0 | 0 | 1927 |
| 06 | 0 (Build, verificado na Etapa anterior) | 0 | 0 | 0 |
| 07 | 9 | 0 | 9 | 0 |
| 08 | 0 (Approval) | 0 | 0 | 0 |
 
## Ameaças do Threat Model cobertas pela esteira
- Cobertas por ferramenta: 
Semgrep: TM-03,TM-07,TM-12,TM-16,TM-17,TM-28,TM-29,TM-33
GITLEAKS: TM-15
TRIVY: TM-31
OWASP: TM-07,TM-08..
- Cobertas por regra própria: TM-15,TM-06
- Cobertas por teste (abuse case): TM-03, TM-23, TM-07, TM-12, TM-29, TM-04, TM-08, TM-20, TM-10..
- Não cobertas (vão para o Dia 03/04): TM-01..
- Achados novos (não estavam no Threat Model): TM-33 ...
 
## Decisões de política
- Na primeira execução, a esteira ficou em modo auditoria para mapear os achados; na execução final, o modo bloqueio deve impedir o deploy quando houver falhas críticas ou altas confirmadas, segredos expostos ou testes de segurança reprovados. Mas conseguimos corigir as vulnerabilidaddes mais graves.
Ficamos com 1 achado o TM-01 força bruta.
 
## Lições aprendidas
- 3 bullets.

