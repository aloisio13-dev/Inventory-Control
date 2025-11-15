
import requests

BASE_URL = 'http://127.0.0.1:5000'


def testar_init():
    resp = requests.get(f'{BASE_URL}/init')
    print('Init:', resp.json())

def testar_entrada():
    dados = {
        'material_id': 1,
        'quantidade': 10
    }
    resp = requests.post(f'{BASE_URL}/entrada', json=dados)
    print('Entrada:', resp.json())

def testar_saida():
    dados = {
        'material_id': 1,
        'quantidade': 5
    }
    resp = requests.post(f'{BASE_URL}/saida', json=dados)
    print('Saída:', resp.json())

def testar_estoque():
    resp = requests.get(f'{BASE_URL}/estoque')
    print('Estoque:', resp.json())

def testar_historico():
    params = {
        'material_id': 1,
        'data_inicio': '2023-01-01',
        'data_fim': '2023-12-31'
    }
    resp = requests.get(f'{BASE_URL}/historico', params=params)
    print('Histórico:', resp.json())

if __name__ == '__main__':
    testar_init()
    testar_entrada()
    testar_saida()
    testar_estoque()
    testar_historico()
