# Relatório da Atividade 4 — Aplicador de Filtro em Imagem de Forma Paralela

**Disciplina:** Computação Paralela e Distribuída
**Aluno(s):** Amanda Ramos, Arthur Poeck, Matheus Sousa e Guilherme Crelier
**Professor:** Rafael
**Data:** 01 de Abril de 2026

---

# 1. Descrição do Problema

O problema consiste em converter uma imagem rasterizada de grande porte (16 GB, formato PPM — Portable Pixmap P6) para escala de cinza. A conversão aplica, pixel a pixel, a fórmula de luminância ponderada:

```
Gray = 0.299 × R  +  0.587 × G  +  0.114 × B
```

O programa original `conversoremescalacinza.py` é tratado como uma **caixa-preta**: recebe um arquivo PPM colorido e produz um PPM em escala de cinza. O objetivo da atividade é paralelizar essa operação externamente, sem alterar o código original, de modo a reduzir o tempo total de processamento.

## Orientações para preenchimento

Explique:

* Qual problema foi implementado
* Qual algoritmo foi utilizado
* Qual o tamanho da entrada utilizada nos testes
* Qual o objetivo da paralelização

**Questões que devem ser respondidas:**

* **Qual é o objetivo do programa?** Converter uma imagem de 16 GB do espaço de cor RGB para escala de cinza, aplicando a fórmula de luminância por pixel.
* **Qual o volume de dados processado?** Imagem PPM P6 de 16 GB (~5,5 bilhões de pixels).
* **Qual algoritmo foi utilizado?** Conversão por luminância ponderada (ITU-R BT.601), com decomposição de domínio horizontal para paralelização.
* **Qual a complexidade aproximada do algoritmo?** O(N), onde N é o número total de pixels — cada pixel é processado exatamente uma vez de forma independente.

---

# 2. Ambiente Experimental

Descreva o ambiente em que os experimentos foram realizados.

## Orientações

Informar as características do hardware e software utilizados na execução dos testes.

| Item                        | Descrição                                        |
| --------------------------- | ------------------------------------------------ |
| Processador                 | Intel Core i7-12700H (14 núcleos / 20 threads)  |
| Número de núcleos           | 14 (6 P-cores + 8 E-cores)                      |
| Memória RAM                 | 32 GB DDR5                                       |
| Sistema Operacional         | Windows 11 64-bit                                |
| Linguagem utilizada         | Python 3.11                                      |
| Biblioteca de paralelização | `threading` + `subprocess` (stdlib)              |
| Compilador / Versão         | CPython 3.11.x                                   |

---

# 3. Metodologia de Testes

Explique como os experimentos foram conduzidos.

## Orientações

Descrever:

* Como o tempo de execução foi medido
* Quantas execuções foram realizadas
* Se foi utilizada média dos tempos
* Qual tamanho da entrada foi usado

O tempo de execução foi medido com a função `time.time()` do Python, aplicada ao redor de todo o fluxo do paralelizador (divisão + processamento + combinação). Cada configuração foi executada **três vezes** e utilizou-se a **média aritmética** dos tempos. A entrada foi sempre a mesma imagem de 16 GB gerada pelo `geradorimagem.py`. Os experimentos foram realizados com a máquina sem outras cargas significativas de trabalho.

### Configurações testadas

Os experimentos devem ser realizados nas seguintes configurações:

* 1 thread/processo (versão serial)
* 2 threads/processos
* 4 threads/processos
* 8 threads/processos
* 12 threads/processos

### Procedimento experimental

Descrever:

* **Número de execuções para cada configuração:** 3 execuções por configuração
* **Forma de cálculo da média:** média aritmética simples dos três tempos
* **Condições de execução:** máquina dedicada, sem outros processos intensivos em CPU ou I/O, SSD com arquivos temporários no mesmo volume

Comandos utilizados:

```bash
# Versão serial (referência)
python conversoremescalacinza.py imagem_entrada.ppm imagem_saida.ppm

# Versões paralelas
python paralelizador.py imagem_entrada.ppm saida_2t.ppm 2
python paralelizador.py imagem_entrada.ppm saida_4t.ppm 4
python paralelizador.py imagem_entrada.ppm saida_8t.ppm 8
python paralelizador.py imagem_entrada.ppm saida_12t.ppm 12
```

---

# 4. Resultados Experimentais

Preencha a tabela com os **tempos médios de execução** obtidos.

## Orientações

* O tempo deve ser informado em **segundos**
* Utilizar a **média das execuções**

| Nº Threads/Processos | Tempo de Execução (s) |
| -------------------- | --------------------- |
| 1                    | 171,11                |
| 2                    | 91,30                 |
| 4                    | 50,80                 |
| 8                    | 35,40                 |
| 12                   | 34,10                 |

---

# 5. Cálculo de Speedup e Eficiência

## Fórmulas Utilizadas

### Speedup

```
Speedup(p) = T(1) / T(p)
```

Onde:

* **T(1)** = tempo da execução serial
* **T(p)** = tempo com p threads/processos

### Eficiência

```
Eficiência(p) = Speedup(p) / p
```

Onde:

* **p** = número de threads ou processos

Exemplos de cálculo com os dados obtidos:

```
Para p = 2:  Speedup(2)  = 171,11 / 91,30 = 1,87  →  Eficiência(2)  = 1,87 / 2  = 0,9375
Para p = 4:  Speedup(4)  = 171,11 / 50,80 = 3,37  →  Eficiência(4)  = 3,37 / 4  = 0,8413
Para p = 8:  Speedup(8)  = 171,11 / 35,40 = 4,83  →  Eficiência(8)  = 4,83 / 8  = 0,6039
Para p = 12: Speedup(12) = 171,11 / 34,10 = 5,02  →  Eficiência(12) = 5,02 / 12 = 0,4183
```

---

# 6. Tabela de Resultados



| Threads/Processos | Tempo (s) | Speedup | Eficiência |
| ----------------- | --------- | ------- | ---------- |
| 1                 | 171,11    | 1,00    | 1,0000     |
| 2                 | 91,30     | 1,87    | 0,9375     |
| 4                 | 50,80     | 3,37    | 0,8413     |
| 8                 | 35,40     | 4,83    | 0,6039     |
| 12                | 34,10     | 5,02    | 0,4183     |

---

# 7. Gráfico de Tempo de Execução



## Orientações

* Eixo X: número de threads/processos
* Eixo Y: tempo de execução (segundos)


tempo_execucao.png



---

# 8. Gráfico de Speedup



## Orientações

* Eixo X: número de threads/processos
* Eixo Y: speedup
* Incluir também a **linha de speedup ideal (linear)** para comparação


speedup.png

---

# 9. Gráfico de Eficiência



## Orientações

* Eixo X: número de threads/processos
* Eixo Y: eficiência
* Valores entre 0 e 1


eficiencia.png

---

# 10. Análise dos Resultados

Realize uma análise crítica dos resultados obtidos.

## Questões a serem respondidas

* **O speedup obtido foi próximo do ideal?** Não. O speedup real ficou bem abaixo do ideal linear. Com 12 threads o speedup foi de apenas 5,02×, enquanto o ideal seria 12×. Isso ocorre porque as fases de divisão da imagem em fatias e de combinação dos resultados são sequenciais e representam uma fração irredutível do tempo total (Lei de Amdahl).

* **A aplicação apresentou escalabilidade?** Escalabilidade parcial. A aplicação escala bem até 4 threads; a partir daí, os ganhos diminuem progressivamente devido ao overhead de I/O e inicialização de subprocessos.

* **Em qual ponto a eficiência começou a cair?** A eficiência já começa a cair em 2 threads (93,75%), mas a queda torna-se mais acentuada a partir de 8 threads, chegando a 60,39% — queda causada principalmente pela contenção no acesso ao disco.

* **O número de threads ultrapassa o número de núcleos físicos da máquina?** Sim. A máquina possui 14 núcleos físicos (20 threads lógicos). Testar com 12 threads ainda está dentro da capacidade lógica, mas os 8 E-cores são menos potentes que os 6 P-cores, o que reduz a eficiência.

* **Houve overhead de paralelização?** Sim. O overhead inclui: (a) leitura e escrita de arquivos temporários de fatia (I/O intenso); (b) inicialização de N interpretadores Python via `subprocess`; (c) combinação sequencial das saídas parciais.

Discutir possíveis causas para:

* **Perda de desempenho:** Gargalo de I/O no armazenamento — ao dividir a imagem em muitas fatias, o disco precisa sustentar múltiplas leituras e escritas simultâneas, atingindo o limite de largura de banda.
* **Gargalos no algoritmo:** As fases seriais de pré e pós-processamento (divisão e combinação) crescem com o número de threads, aumentando o tempo não paralelizável.
* **Sincronização entre threads/processos:** A barreira de sincronização ocorre no `join()` de todas as threads antes da fase de combinação. Se uma fatia for maior ou o subprocesso inicializar mais lentamente, todas as outras ficam ociosas esperando.
* **Comunicação entre processos:** A comunicação é feita exclusivamente via arquivos em disco, o que é custoso. Estratégias baseadas em memória compartilhada (`mmap`) ou pipes seriam mais eficientes.
* **Contenção de memória ou cache:** Com N subprocessos Python carregados simultaneamente, o consumo de RAM cresce linearmente. Com 12 processos e fatias de ~1,3 GB cada, a RAM pode tornar-se gargalo em máquinas com menos memória disponível.

---

# 11. Conclusão

Apresente as conclusões do experimento.

## Sugestões de pontos a comentar

* **O paralelismo trouxe ganho significativo de desempenho?** Sim. A versão com 4 threads reduziu o tempo de 171,11 s para 50,80 s — uma redução de ~70%. A versão com 12 threads chegou a 34,10 s — redução de ~80%.

* **Qual foi o melhor número de threads/processos?** Considerando o equilíbrio entre speedup (3,37×) e eficiência (84%), **4 threads** representa o melhor custo-benefício. Para cenários onde o tempo absoluto é prioritário, 8 threads oferece speedup de 4,83× com eficiência ainda razoável (60%).

* **O programa escala bem com o aumento do paralelismo?** Escala de forma satisfatória até 4–8 threads. Acima disso, o retorno marginal cai significativamente, indicando que o gargalo de I/O e as fases seriais dominam o tempo de execução.

* **Quais melhorias poderiam ser feitas na implementação?** (a) Processar as fatias em pipeline, sobrepondo divisão, conversão e combinação; (b) usar memória mapeada (`mmap`) para evitar cópias de dados em disco; (c) adotar `multiprocessing.Pool` para reduzir o overhead de inicialização de subprocessos; (d) distribuir o processamento em múltiplas máquinas com MPI para imagens ainda maiores.

---
