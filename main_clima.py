from flask import Flask, jsonify, request #importo as bibliotecas
import json

app = Flask(__name__) #ele fala que esse script que esta rodando é o principal

with open('/home/albatroz/Área de trabalho/365/api_clima/cidades.json', 'r', encoding='utf-8') as f: #aqui eu abro o arquivo de texto e leio ele e dou um apelido de f
    cidades = json.load(f) #aqui coloco na variavel cidades o arquivo de texto
    
@app.route('/cidades')
def name_cidade():
    nomes=[x['Cidade'] for x in cidades]
    return jsonify(nomes)
@app.route('/')#crio uma rota para acessar
def home():
    return jsonify({'mensagem': 'api de clima rodando'}), 200 #digo que está funcionando e retorna o código 200 (OK)

@app.route('/clima', methods=['GET'])#crio uma rota que recebe parametros
def clima():
    estado = request.args.get('estado')#pega da url o parametro estado e salva na variavel estado
    temperatura = request.args.get('temperatura')
    praia_param = request.args.get('praia')

    if not (estado or temperatura or praia_param): #compara se não tem valores nas 3 variaveis
        return jsonify({'erro': 'você deve informar ao menos um parâmetro'}), 400

    if temperatura and temperatura not in ['quente', 'frio']: #verifica se a temperatura está dentro dos valores permitidos
        return jsonify({'erro': 'Temperatura deve ser "quente" ou "frio"'}), 400

    if praia_param in ['true', 'false']: #verifica se o valor dessa variavel está dentro dessa lista
        praia = praia_param == 'true' #aqui ele fala que a variavel praia recebe o valor True se praia_param for igual a palavra true, caso contrário recebe False
    else:
        praia = None #aqui fala que praia não recebeu parametro

    def filtro(cidade): #aqui vai passar por alguns testes para formar a lista de retorno
        return (
            (estado is None or cidade['Estado'].lower() == estado.lower()) and #aqui vemos se a variavel estado não é vazia; se for retorna True, se não ele procura essa cidade
            (temperatura != 'quente' or float(cidade['Temperatura']) > 25) and #aqui ele vê se a variavel temperatura é diferente de quente; se for, retorna True e passa, senão ele vê se a temperatura é > que 25
            (temperatura != 'frio' or float(cidade['Temperatura']) < 25) and #mesma lógica acima, mas para frio
            (praia is None or cidade['Praia'] == praia) #aqui ele fala se praia não é none e, se não for, procura o valor da url
        )

    resultado = list(filter(filtro, cidades)) #aqui ele olha os valores de cidades que passam pelo filtro que passamos

    if not resultado: #aqui diz se não tem resultado algum
        return jsonify({'mensagem': 'nenhuma cidade encontrada com estes parâmetros'}), 404

    return jsonify(resultado) #se encontrou, retorna as cidades

if __name__ == '__main__':
    app.run(debug=True) #roda o servidor em modo debug
