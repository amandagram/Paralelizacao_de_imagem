import subprocess
import sys
import os
import time
import multiprocessing

from fatiador import fatiar, juntar, limpar

CONVERSOR = "conversoremescalacinza.py"
PASTA_TMP = "_fatias_tmp"


def executar_conversor(args):
    indice, entrada, saida = args
    resultado = subprocess.run(
        [sys.executable, CONVERSOR, entrada, saida],
        capture_output=True
    )
    if resultado.returncode != 0:
        raise RuntimeError(f"Erro na fatia {indice}:\n{resultado.stderr.decode('utf-8', errors='ignore')}")
    print(f"  Fatia {indice} concluida")
    return indice


def converter_paralelo(arquivo_entrada, arquivo_saida, num_threads):
    # 1. Fatia a imagem
    largura, altura, valor_maximo, fatias_in = fatiar(
        arquivo_entrada, num_threads, PASTA_TMP
    )
    fatias_out = [c.replace("fatia_", "fatia_out_") for c in fatias_in]

    # 2. Processa em paralelo com multiprocessing
    print(f"Executando {num_threads} processos em paralelo...\n")
    inicio = time.time()

    args = list(enumerate(zip(fatias_in, fatias_out)))
    args = [(i, ent, sai) for i, (ent, sai) in args]

    with multiprocessing.Pool(processes=num_threads) as pool:
        pool.map(executar_conversor, args)

    tempo = time.time() - inicio

    # 3. Junta e limpa
    juntar(fatias_out, largura, altura, valor_maximo, arquivo_saida)
    limpar(fatias_in + fatias_out, PASTA_TMP)

    print(f"✅ Processamento concluido!")
    print(f"⏱️ Processos: {num_threads}")
    print(f"⏱️ Tempo total: {tempo:.2f} segundos")
    print(f"⏱️ Tempo total: {tempo/60:.2f} minutos")
    return tempo


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Paralelizador externo do conversoremescalacinza.py"
    )
    parser.add_argument("arquivo_entrada", help="Imagem PPM de entrada")
    parser.add_argument("arquivo_saida",   help="Imagem PPM de saida")
    parser.add_argument("--threads", type=int, default=4,
                        help="Numero de processos (padrao: 4)")
    args = parser.parse_args()

    converter_paralelo(args.arquivo_entrada, args.arquivo_saida, args.threads)