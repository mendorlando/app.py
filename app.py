from flask import Flask, render_template, request, jsonify
from arbol import Nodo

app = Flask(__name__)

def buscar_solucion_DFS_rec(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    
    dato_nodo = nodo_inicial.get_datos()
    hijos = [
        Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]),
        Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]),
        Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])
    ]
    nodo_inicial.set_hijos(hijos)
    
    for hijo in hijos:
        if hijo.get_datos() not in visitados:
            sol = buscar_solucion_DFS_rec(hijo, solucion, visitados)
            if sol:
                return sol
    return None

def buscar_solucion_DFS(estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = [Nodo(estado_inicial)]
    while nodos_frontera:
        nodo = nodos_frontera.pop()
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            return nodo
        
        dato_nodo = nodo.get_datos()
        hijos = [
            Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]),
            Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]),
            Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])
        ]
        for hijo in hijos:
            if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo)
        nodo.set_hijos(hijos)
    return None

def buscar_solucion_BFS(estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = [Nodo(estado_inicial)]
    while nodos_frontera:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            return nodo
        
        dato_nodo = nodo.get_datos()
        hijos = [
            Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]),
            Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]),
            Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])
        ]
        for hijo in hijos:
            if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo)
        nodo.set_hijos(hijos)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    data = request.json
    estado_inicial = data['estado_inicial']
    solucion = data['solucion']

    # Ejecutar los tres métodos de búsqueda
    resultados = {
        'dfs_recursivo': ejecutar_busqueda(buscar_solucion_DFS_rec, estado_inicial, solucion),
        'dfs': ejecutar_busqueda(buscar_solucion_DFS, estado_inicial, solucion),
        'bfs': ejecutar_busqueda(buscar_solucion_BFS, estado_inicial, solucion),
    }

    return jsonify(resultados)

def ejecutar_busqueda(metodo_busqueda, estado_inicial, solucion):
    nodo_inicial = Nodo(estado_inicial)
    visitados = []
    nodo_solucion = metodo_busqueda(nodo_inicial, solucion, visitados) if metodo_busqueda == buscar_solucion_DFS_rec else metodo_busqueda(estado_inicial, solucion)

    resultado = []
    if nodo_solucion:
        while nodo_solucion.get_padre() is not None:
            resultado.append(nodo_solucion.get_datos())
            nodo_solucion = nodo_solucion.get_padre()
        resultado.append(estado_inicial)
        resultado.reverse()
    return resultado

if __name__ == '__main__':
    app.run(debug=True)