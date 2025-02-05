from urllib.parse import urlparse
import json
import os

def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    
    currency = "BRL" if '.br' in domain.lower() else "USD"
    domain = domain.split('.')[0]
    

    return domain,currency

def save_data(data, output_file):
        """Salva os dados extraídos em um arquivo JSON."""
        if os.path.exists(output_file):
            with open(output_file, "r+", encoding="utf-8") as f:
                file_contents = f.read().strip()

                if not file_contents:
                    print("Arquivo JSON vazio. Inicializando como uma lista vazia")
                    file_data = []
                else:
                    try:
                        file_data = json.loads(file_contents)
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar JSON: {e}. Corrigindo arquivo...")
                        file_data = []
                        f.truncate(0)
                if not any(item['ASIN'] == data['ASIN'] for item in file_data):
                    file_data.append(data)

                    f.seek(0)
                    json.dump(file_data, f, ensure_ascii=False, indent=4)
                else:
                    print(f"Produto duplicado encontrado (ASIN {data['ASIN']}): {data['Title']}")
                    return None
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump([data], f, ensure_ascii=False, indent=4)
                print(f"Gerando arquivo JSON!")