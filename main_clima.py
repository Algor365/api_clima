from flask import Flask, jsonify, request, render_template 
import json

app = Flask(__name__) 
with open('cidades.json', 'r', encoding='utf-8') as f: 
    cidades = json.load(f) 
    
@app.route('/cidades')
def name_cidade():
    nomes=[x['Cidade'] for x in cidades]
    return jsonify(nomes)
@app.route('/')
def home():
    rotas = {
        "/": "Mostra as rotas disponíveis e suas descrições.",
        "/cidades": "Retorna uma lista com os nomes de todas as cidades disponíveis.",
        "/clima": {
            "descrição": "Filtra as cidades com base em estado, temperatura (quente ou frio) e se tem praia.",
            "parâmetros (query string)": {
                "estado": "Nome do estado (ex: SP, RJ, etc.)",
                "temperatura": '"quente" para cidades com temp. > 25°C ou "frio" para temp. < 25°C',
                "praia": '"true" ou "false" para filtrar cidades com ou sem praia'
            },
            "exemplo": "/clima?estado=SP&temperatura=quente&praia=true"
        }
    }
    return jsonify(rotas), 200

@app.route('/clima', methods=['GET'])
def clima():
    estado = request.args.get('estado')
    temperatura = request.args.get('temperatura')
    praia_param = request.args.get('praia')

    if not (estado or temperatura or praia_param): 
        return jsonify({'erro': 'você deve informar ao menos um parâmetro'}), 400

    if temperatura and temperatura not in ['quente', 'frio']: 
        return jsonify({'erro': 'Temperatura deve ser "quente" ou "frio"'}), 400

    if praia_param in ['true', 'false']: 
        praia = praia_param == 'true' 
    else:
        praia = None 

    def filtro(cidade): 
        return (
            (estado is None or cidade['Estado'].lower() == estado.lower()) and 
            (temperatura != 'quente' or float(cidade['Temperatura']) > 25) and 
            (temperatura != 'frio' or float(cidade['Temperatura']) < 25) and 
            (praia is None or cidade['Praia'] == praia) 
        )

    resultado = list(filter(filtro, cidades))

    if not resultado:
        return jsonify({'mensagem': 'nenhuma cidade encontrada com estes parâmetros'}), 404

    return jsonify(resultado) 
if __name__ == '__main__':
    app.run(debug=True)
