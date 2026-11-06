"""
Ponderada CC08 - A4, versao 1: buffer circular SEM sincronizacao.
Autor: Lucas Cofcewicz Faria | N = 7 | 20000 amostras por execucao.

Produtor (sensor) e consumidor (motor) compartilham um contador `ocupadas`
com espera ocupada. O time.sleep(0) entre ler e escrever o contador simula a
thread sendo interrompida no pior momento, expondo a condicao de corrida.
Se o consumidor ficar 1 s sem receber nada, a execucao e encerrada (travou).

Uso: python versao1.py
"""
import threading
import time

N = 7
AMOSTRAS = 20000
EXECUCOES = 3
TIMEOUT = 1.0


def executar():
    """Roda uma execucao e devolve (consumidas, perdidas, duplicadas, travou)."""
    buf = [-1] * N
    estado = {"ocupadas": 0, "entrada": 0, "saida": 0}
    recebidas = []
    parar = threading.Event()

    def produtor():
        """Gera as amostras 0..AMOSTRAS-1 e grava no buffer sem proteger o contador."""
        for i in range(AMOSTRAS):
            while estado["ocupadas"] >= N:  # espera ocupada: buffer cheio
                if parar.is_set():
                    return
                time.sleep(0)
            buf[estado["entrada"]] = i
            estado["entrada"] = (estado["entrada"] + 1) % N
            tmp = estado["ocupadas"]  # le o contador
            time.sleep(0)  # interrupcao no pior momento
            estado["ocupadas"] = tmp + 1  # escreve (pode apagar a escrita do outro)

    def consumidor():
        """Le amostras do buffer; encerra se ficar 1 s sem receber nada."""
        ultimo = time.time()
        while len(recebidas) < AMOSTRAS:
            while estado["ocupadas"] <= 0:  # espera ocupada: buffer vazio
                if time.time() - ultimo > TIMEOUT:
                    return True
                time.sleep(0)
            recebidas.append(buf[estado["saida"]])
            estado["saida"] = (estado["saida"] + 1) % N
            tmp = estado["ocupadas"]
            time.sleep(0)
            estado["ocupadas"] = tmp - 1
            ultimo = time.time()
        return False

    resultado = {}
    tp = threading.Thread(target=produtor, daemon=True)
    tc = threading.Thread(target=lambda: resultado.update(t=consumidor()), daemon=True)
    tp.start()
    tc.start()
    tc.join()
    parar.set()
    tp.join(timeout=2)

    validas = set(r for r in recebidas if 0 <= r < AMOSTRAS)
    consumidas = len(recebidas)
    perdidas = AMOSTRAS - len(validas)
    duplicadas = consumidas - len(validas)
    return consumidas, perdidas, duplicadas, resultado.get("t", True)


def main():
    """Executa a versao 1 tres vezes e imprime uma linha por execucao."""
    for k in range(1, EXECUCOES + 1):
        c, p, d, t = executar()
        print(f"Versao 1 | execucao {k} | consumidas={c} perdidas={p} "
              f"duplicadas={d} travou={'sim' if t else 'nao'}")


if __name__ == "__main__":
    main()
