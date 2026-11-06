"""
Ponderada CC08 - A4, versao 3: semaforos com a ORDEM TROCADA (deadlock).
Autor: Lucas Cofcewicz Faria | N = 7 | 20000 amostras por execucao.

Tres semaforos: vazio (inicia em N), cheio (inicia em 0) e mutex (inicia em 1).
Produtor: wait(mutex) -> wait(vazio) -> grava -> signal(mutex) -> signal(cheio).
O consumidor continua igual a versao 2.
Consumidor: wait(cheio) -> wait(mutex) -> le -> signal(mutex) -> signal(vazio).

Uso: python versao3.py
"""
import threading

N = 7
AMOSTRAS = 20000
EXECUCOES = 3
TIMEOUT = 1.0


def executar():
    """Roda uma execucao e devolve (consumidas, perdidas, duplicadas, travou)."""
    buf = [-1] * N
    idx = {"entrada": 0, "saida": 0}
    vazio = threading.Semaphore(N)
    cheio = threading.Semaphore(0)
    mutex = threading.Semaphore(1)
    recebidas = []
    resultado = {"travou": False}

    def produtor():
        """Gera as amostras 0..AMOSTRAS-1 respeitando os semaforos."""
        for i in range(AMOSTRAS):
            mutex.acquire()  # ORDEM TROCADA: pega o mutex antes de vazio
            vazio.acquire()  # buffer cheio: dorme segurando o mutex
            buf[idx["entrada"]] = i
            idx["entrada"] = (idx["entrada"] + 1) % N
            mutex.release()
            cheio.release()

    def consumidor():
        """Consome AMOSTRAS itens; marca travamento se ficar 1 s sem receber."""
        for _ in range(AMOSTRAS):
            if not cheio.acquire(timeout=TIMEOUT):
                resultado["travou"] = True
                return
            if not mutex.acquire(timeout=TIMEOUT):
                resultado["travou"] = True
                return
            recebidas.append(buf[idx["saida"]])
            idx["saida"] = (idx["saida"] + 1) % N
            mutex.release()
            vazio.release()

    tp = threading.Thread(target=produtor, daemon=True)
    tc = threading.Thread(target=consumidor, daemon=True)
    tp.start()
    tc.start()
    tc.join()

    validas = set(r for r in recebidas if 0 <= r < AMOSTRAS)
    consumidas = len(recebidas)
    return consumidas, AMOSTRAS - len(validas), consumidas - len(validas), resultado["travou"]


def main():
    """Executa a versao 3 tres vezes e imprime uma linha por execucao."""
    for k in range(1, EXECUCOES + 1):
        c, p, d, t = executar()
        print(f"Versao 3 | execucao {k} | consumidas={c} perdidas={p} "
              f"duplicadas={d} travou={'sim' if t else 'nao'}")


if __name__ == "__main__":
    main()
