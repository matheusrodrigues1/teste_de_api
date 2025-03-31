from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

# Carrega os dados do CSV
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'Relatorio_cadop.csv')
    try:
        # Lê o CSV considerando o encoding e separador corretos
        df = pd.read_csv(file_path, sep=';', encoding='utf-8', dtype=str)
        # Remove linhas totalmente vazias
        df = df.dropna(how='all')
        return df
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return pd.DataFrame()

operadoras_df = load_data()

@app.route('/api/search', methods=['GET'])
def search_operadoras():
    query = request.args.get('q', '').lower().strip()
    
    # Verifica se o parâmetro está vazio
    if not query:
        return jsonify({
            "error": "O parâmetro 'q' é obrigatório",
            "message": "Por favor, informe um termo de busca",
            "example": "/api/search?q=saude"
        }), 400
    
    try:
        results = []
        for _, row in operadoras_df.iterrows():
            # Converte a linha para dict e trata valores NaN/None
            row_dict = {}
            for key, value in row.items():
                if pd.isna(value):
                    row_dict[key] = None
                else:
                    row_dict[key] = str(value)
                    
            full_text = ' '.join(str(v) for v in row_dict.values() if v).lower()
            if query in full_text:
                results.append(row_dict)
        
        results.sort(key=lambda x: sum(str(val).lower().count(query) for val in x.values()), reverse=True)
        return jsonify(results[:50])
    
    except Exception as e:
        print(f"Erro na busca: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
