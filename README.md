# Milenio Capital App - API

## Desafio Dev Jr/Pl

Aplicação API REST em FastAPI para o gerenciamento de Grafos (modelo '<b>Yen's K</b>') com suas funções de rotas e distâncias.

## Proposta
<b>Link da Proposta: [Proposta.md](./proposta.md#desafio-dev-jrpl)</b>

## O que o projeto contém
- [FastAPI](https://fastapi.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Docker](https://www.docker.com/) e docker-compose
- Testes unitários

## Defina as variáveis de ambiente
Crie um arquivo mysql.env na pasta do projeto (pasta raiz) e copie o conteúdo do arquivo mysql.env.example. Fique à vontade para modificar de acordo com sua configuração.

## Instalação
Para rodar o projeto faça essas configurações:
- Clone o projeto (utilizando comando git ou baixando em zip)
- Instale o Docker

## Execute o projeto utilizando o docker-composer
```
docker-compose up --build
```

## Execute as migrations do Alembic
As migrations do Alembic vão configurar as tabelas do Banco de Dados
```
docker-compose exec fastapi_server alembic revision --autogenerate -m "create inital tables"
docker-compose exec fastapi_server alembic upgrade head
```

## Execute o pytest para rodar os testes unitários
```
docker-compose exec fastapi_server python test_main.py
```

## Documentação
Você pode acessar a documentação com o seguinte caminho [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

## Endpoints
O Endpoints é formado somente por rotas públicas.
<br>
- Rotas públicas:

<b>Para visualizar um grafo específico</b><br>
<b>GET</b> /graph/cidade/{graphId}<br>
<br>
<b>Para inserir o grafo</b><br>
<b>POST</b> /graph
```
{
    "data": [
        {
        "source": "A", "target": "B", "distance": 6
        },
        {
        "source": "A", "target": "E", "distance": 4
        }
    ]
}
```

<b>Para visualizar todas as rotas de um grafo entre duas cidades específicas</b><br>
<b>GET</b> /routes/{graphId}/from/{town1}/to/{town2}?maxStops=<br>
<b>(com o ultimo parâmetro `maxStops` opcional)</b><br>
<br>
<b>Para visualizar a distância mínima de um grafo entre duas cidades específicas</b><br>
<b>GET</b> /distance/{graphId}/from/{town1}/to/{town2}<br>
<br>
## Preview
![image.png](https://user-images.githubusercontent.com/19514153/166562165-4dee400a-c4cd-4da3-9568-e180a1d11816.png)

## Notas do Dev
Eu Leonardo queria agradecer a esta oportunidade que a Milenio Capital está proporcionando para todos os amantes da programação de todo o Brasil.
