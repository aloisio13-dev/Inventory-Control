from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from db_config import popular_db
from estoque_service import registrar_entrada, registrar_saida, consultar_estoque, historico_movimentacoes

app = Flask(__name__)
CORS(app)

@app.route('/init', methods=['GET'])
def init_db():
    popular_db()
    return jsonify({'status': 'Banco de dados criado com sucesso'})

@app.route('/entrada', methods=['POST'])
def entrada():
    data = request.json
    registrar_entrada(data['material_id'], data['quantidade'])
    return jsonify({'status': 'Entrada registrada com sucesso'})

@app.route('/saida', methods=['POST'])
def saida():
    data = request.json
    registrar_saida(data['material_id'], data['quantidade'])
    return jsonify({'status': 'Saída registrada com sucesso'})

@app.route('/estoque', methods=['GET'])
def estoque():
    resultado = consultar_estoque()
    return jsonify(resultado)

@app.route('/historico', methods=['GET'])
def historico():
    material_id = request.args.get('material_id')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    resultado = historico_movimentacoes(material_id, data_inicio, data_fim)
    return jsonify(resultado)

@app.route('/')
def index():
    # Renderiza a página inicial usando os dados do estoque
    produtos = consultar_estoque()
    return render_template('index.html', produtos=produtos)

@app.route('/favicon.ico')
def favicon():
    # Retorna vazio com status 204 para evitar 404 no navegador
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
