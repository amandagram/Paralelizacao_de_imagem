import os
import math


def ler_header_ppm(f):
    tipo = f.readline().strip()
    if tipo != b'P6':
        raise ValueError("Formato nao suportado. Esperado PPM P6.")
    linha = f.readline().strip()
    while linha.startswith(b'#'):
        linha = f.readline().strip()
    largura, altura = map(int, linha.split())
    linha = f.readline().strip()
    while linha.startswith(b'#'):
        linha = f.readline().strip()
    valor_maximo = int(linha)
    offset_dados = f.tell()
    return largura, altura, valor_maximo, offset_dados


def fatiar(arquivo_entrada, num_fatias, pasta_saida="_fatias_tmp"):
    """
    Le a imagem PPM e divide em num_fatias arquivos PPM menores.
    Retorna: (largura, altura, valor_maximo, lista de caminhos das fatias)
    """
    os.makedirs(pasta_saida, exist_ok=True)

    print(f"Lendo '{arquivo_entrada}'...")
    with open(arquivo_entrada, 'rb') as f:
        largura, altura, valor_maximo, offset_dados = ler_header_ppm(f)
        dados = f.read()

    print(f"Imagem: {largura}x{altura}")
    print(f"Criando {num_fatias} fatias em '{pasta_saida}'...")

    bytes_por_linha = largura * 3
    linhas_por_fatia = math.ceil(altura / num_fatias)

    caminhos = []
    for i in range(num_fatias):
        y_ini = i * linhas_por_fatia
        y_fim = min(y_ini + linhas_por_fatia, altura)
        if y_ini >= altura:
            break

        pixels = dados[y_ini * bytes_por_linha : y_fim * bytes_por_linha]
        caminho = os.path.join(pasta_saida, f"fatia_{i:04d}.ppm")

        with open(caminho, 'wb') as f:
            header = f"P6\n{largura} {y_fim - y_ini}\n255\n".encode('ascii')
            f.write(header)
            f.write(pixels)

        caminhos.append(caminho)
        print(f"  Fatia {i} salva: linhas {y_ini}..{y_fim}")

    print(f"Fatiamento concluido. {len(caminhos)} fatias criadas.\n")
    return largura, altura, valor_maximo, caminhos


def juntar(caminhos, largura, altura_total, valor_maximo, arquivo_saida):
    """
    Junta as fatias PPM convertidas em um unico arquivo de saida.
    """
    print(f"Juntando {len(caminhos)} fatias em '{arquivo_saida}'...")

    with open(arquivo_saida, 'wb') as fout:
        header = f"P6\n{largura} {altura_total}\n{valor_maximo}\n".encode('ascii')
        fout.write(header)
        for caminho in sorted(caminhos):
            with open(caminho, 'rb') as fin:
                ler_header_ppm(fin)
                fout.write(fin.read())

    print("Juncao concluida.\n")


def limpar(caminhos, pasta):
    for c in caminhos:
        if os.path.exists(c):
            os.remove(c)
    if os.path.exists(pasta):
        os.rmdir(pasta)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fatia uma imagem PPM em partes menores")
    parser.add_argument("arquivo_entrada", help="Imagem PPM de entrada")
    parser.add_argument("num_fatias", type=int, help="Numero de fatias")
    parser.add_argument("--pasta", default="_fatias_tmp", help="Pasta de saida das fatias")
    args = parser.parse_args()

    fatiar(args.arquivo_entrada, args.num_fatias, args.pasta)