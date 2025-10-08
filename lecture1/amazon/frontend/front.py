import requests

BASE_URL = 'http://localhost:8000/amazon_api/'

def get_clientes():
    response = requests.get(BASE_URL + 'clientes/')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_cliente(data):
    response = requests.post(BASE_URL + 'clientes/', json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return None

def update_cliente(cliente_id, data):
    response = requests.put(BASE_URL + f'clientes/{cliente_id}/', json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def delete_cliente(cliente_id):
    response = requests.delete(BASE_URL + f'clientes/{cliente_id}/')
    return response.status_code == 204

# Exemplo de uso
if __name__ == '__main__':
    # Criar um novo Cliente
    print("----CRIANDO CLIENTE----")
    new_cliente = {'nome': 'João da Silva', 'email': 'joao.silva@gmail.com', 'telefone': '456987789'}
    created_cliente = create_cliente(new_cliente)
    #print('Cliente criado:', created_cliente)

    # Obter todos os Clientes
    print("----LISTANDO CLIENTES----")
    clientes = get_clientes()
    for cliente in clientes:
        print('Cliente:', cliente)
    

    # Atualizar um Cliente
    #cliente_id = 2
    #updated_data = {'nome': 'Cliente atualizado', 'email': 'a.b@gmail.coma', 'telefone': '456789'}
    #updated_cliente = update_cliente(cliente_id, updated_data)
    #print('Cliente atualizado:', updated_cliente)

    #cliente_id = 1
    # Deletar um Cliente
    #if delete_cliente(cliente_id):
    #    print('Cliente deletado com sucesso')
    #else:
    #    print('Falha ao deletar o Cliente')
