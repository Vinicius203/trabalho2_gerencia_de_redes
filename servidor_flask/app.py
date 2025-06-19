import csv
import os
import requests
import time
import threading
import uuid
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, send_from_directory, url_for

app = Flask(__name__)

app.config['SERVER_NAME'] = 'localhost:5000'

OUTPUT_FOLDER = 'output'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

tasks = {}


def scrape_books_and_save_csv_task(task_id):
    print(f"Iniciando tarefa de scraping com ID: {task_id}")
    tasks[task_id]["status"] = "processando"

    try:
        base_url = "https://books.toscrape.com/catalogue/"
        url_template = base_url + "page-{}.html"
        scraped_data = []

        for i in range(1, 21):
            url = url_template.format(i)
            print(f"[{task_id}] Raspando página: {url}")
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            books = soup.find_all("article", class_="product_pod")

            for book in books:
                title = book.h3.a["title"]
                rating = book.find("p", class_="star-rating")["class"][1]
                availability = book.find(
                    "p", class_="instock availability"
                ).text.strip()
                book_url = base_url + book.h3.a["href"]

                scraped_data.append(
                    {
                        "Nome": title,
                        "Avaliação": rating,
                        "Disponibilidade": availability,
                        "URL da Página do Livro": book_url,
                    }
                )

            time.sleep(1)

        filename = f"relatorio_livros_{task_id}.csv"
        filepath = os.path.join(OUTPUT_FOLDER, filename)

        print(f"[{task_id}] Salvando dados em: {filepath}")

        with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "Nome",
                "Avaliação",
                "Disponibilidade",
                "URL da Página do Livro",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(scraped_data)

        with app.app_context():
            download_url = url_for("download_file", filename=filename, _external=True)
        tasks[task_id]["status"] = "concluido"
        tasks[task_id]["resultado"] = {
            "mensagem": f"{len(scraped_data)} livros foram salvos com sucesso!",
            "nome_arquivo": filename,
            "url_download": download_url,
        }
        print(f"Tarefa {task_id} concluída. Arquivo gerado: {filename}")

    except Exception as e:
        tasks[task_id]["status"] = "erro"
        tasks[task_id]["resultado"] = str(e)
        print(f"Erro na tarefa {task_id}: {e}")


@app.route("/iniciar-tarefa", methods=["POST"])
def start_task():
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "iniciada"}

    thread = threading.Thread(target=scrape_books_and_save_csv_task, args=(task_id,))
    thread.start()

    status_url = url_for("get_task_status", task_id=task_id, _external=True)
    return (
        jsonify(
            {
                "mensagem": "Tarefa de scraping iniciada.",
                "task_id": task_id,
                "status_url": status_url,
            }
        ),
        202,
    )


@app.route("/status/<task_id>", methods=["GET"])
def get_task_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    response = {"status": task.get("status"), "resultado": task.get("resultado", None)}
    return jsonify(response)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

