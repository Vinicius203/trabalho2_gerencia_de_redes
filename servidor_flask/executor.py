import datetime


def tarefa_longa(dados_do_cliente):
    print(f"Recebido do NodeJS: {dados_do_cliente}")

    nome = dados_do_cliente.get("nome", "Desconhecido")
    id_tarefa = dados_do_cliente.get("id", "N/A")

    resultado = (
        f"Olá, {nome}! A tarefa {id_tarefa} foi processada com sucesso em Python."
    )
    timestamp = datetime.datetime.now().isoformat()

    return {"mensagem": resultado, "processado_em": timestamp}

