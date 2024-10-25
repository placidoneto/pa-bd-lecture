import requests

BASE_URL = 'http://localhost:8000/amazon_api/'

def get_clientes():
    response = requests.get(BASE_URL + 'clientes/')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_item(data):
    response = requests.post(BASE_URL + 'items/', json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return None

def update_item(item_id, data):
    response = requests.put(BASE_URL + f'items/{item_id}/', json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def delete_item(item_id):
    response = requests.delete(BASE_URL + f'items/{item_id}/')
    return response.status_code == 204

# Exemplo de uso
if __name__ == '__main__':
    # Criar um novo item
    #new_item = {'name': 'Item 1', 'description': 'Descrição do Item 1'}
    #created_item = create_item(new_item)
    #print('Item criado:', created_item)

    # Obter todos os itens
    clientes = get_clientes()
    for cliente in clientes:
        print('Cliente:', cliente)
    

    # Atualizar um item
    #item_id = created_item['id']
    #updated_data = {'name': 'Item 1 atualizado', 'description': 'Descrição atualizada'}
    #updated_item = update_item(item_id, updated_data)
    #print('Item atualizado:', updated_item)

    # Deletar um item
    #if delete_item(item_id):
    #    print('Item deletado com sucesso')
    #else:
    #    print('Falha ao deletar o item')
