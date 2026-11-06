# Ponderada CC08: do pipeline ao deadlock

**Aluno:** Lucas Cofcewicz Faria

Repositório da ponderada de CC08, com a análise de arquitetura, pipeline, processos/threads e deadlock de uma pulseira com sensor e motor de vibração, mais o código em Python do buffer produtor/consumidor da A4.

## Como rodar o Código

Requer Python 3 (apenas biblioteca padrão, sem dependências). A partir da raiz do repositório:

```powershell
cd ponderada/codigo
python versao1.py   # sem sincronização (condição de corrida)
python versao2.py   # com semáforos vazio, cheio e mutex
python versao3.py   # ordem trocada (deadlock)
```

Cada comando executa a versão 3 vezes (N = 7, 20.000 amostras) e imprime uma linha por execução com amostras consumidas, perdidas, duplicadas e se travou.
