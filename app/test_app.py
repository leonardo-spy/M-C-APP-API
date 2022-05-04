from fastapi.testclient import TestClient
import pytest

from app import app

client = TestClient(app)

EXAMPLE_ID_1 = EXAMPLE_ID_2 = 0


def test_create_graph_1():
    global EXAMPLE_ID_1
    response = client.post(
        "/graph/",
        json={
            "data": [
                {
                "source": "A", "target": "B", "distance": 6
                },
                {
                "source": "A", "target": "E", "distance": 4
                },
                {
                "source": "B", "target": "A", "distance": 6
                },
                {
                "source": "B", "target": "C", "distance": 2
                },
                {
                "source": "B", "target": "D", "distance": 4
                },
                {
                "source": "C", "target": "B", "distance": 3
                },
                {
                "source": "C", "target": "D", "distance": 1
                },
                {
                "source": "C", "target": "E", "distance": 7
                },
                {
                "source": "D", "target": "B", "distance": 8
                },
                {
                "source": "E", "target": "B", "distance": 5
                },
                {
                "source": "E", "target": "D", "distance": 7
                }
            ]
            },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    EXAMPLE_ID_1 = data["id"]
    assert response.json() == {
        "id" : EXAMPLE_ID_1,
        "data":[
            {
            "source": "A", "target": "B", "distance":6
            },
            {
            "source": "A", "target": "E", "distance":4
            },
            {
            "source": "B", "target": "A", "distance":6
            },
            {
            "source": "B", "target": "C", "distance":2
            },
            {
            "source": "B", "target": "D", "distance":4
            },
            {
            "source": "C", "target": "B", "distance":3
            },
            {
            "source": "C", "target": "D", "distance":1
            },
            {
            "source": "C", "target": "E", "distance":7
            },
            {
            "source": "D", "target": "B", "distance":8
            },
            {
            "source": "E",  "target": "B", "distance":5
            },
            {
            "source": "E", "target": "D", "distance":7
            }
        ]
        }

def test_read_graph():
    global EXAMPLE_ID_1
    response = client.get("/graph/{}".format(EXAMPLE_ID_1))
    assert response.status_code == 200
    assert response.json() == {
        "id" : EXAMPLE_ID_1,
        "data":[
            {
            "source": "A", "target": "B", "distance":6
            },
            {
            "source": "A", "target": "E", "distance":4
            },
            {
            "source": "B", "target": "A", "distance":6
            },
            {
            "source": "B", "target": "C", "distance":2
            },
            {
            "source": "B", "target": "D", "distance":4
            },
            {
            "source": "C", "target": "B", "distance":3
            },
            {
            "source": "C", "target": "D", "distance":1
            },
            {
            "source": "C", "target": "E", "distance":7
            },
            {
            "source": "D", "target": "B", "distance":8
            },
            {
            "source": "E",  "target": "B", "distance":5
            },
            {
            "source": "E", "target": "D", "distance":7
            }
        ]
        }

def test_read_inexistent_graph():
    response = client.get("/graph/{}".format(-1))
    assert response.status_code == 404
    assert response.json() == {"detail": "Graphs not found"}

def test_create_graph_2():
    global EXAMPLE_ID_2
    response = client.post(
        "/graph/",
        json={
            "data":[
                {
                "source": "A", "target": "B", "distance": 5
                },
                {
                "source": "B", "target": "C", "distance": 4
                },
                {
                "source": "C", "target": "D", "distance": 8
                },
                {
                "source": "D", "target": "C", "distance": 8
                },
                {
                "source": "D", "target": "E", "distance": 6
                },
                {
                "source": "A", "target": "D", "distance": 5
                },
                {
                "source": "C", "target": "E", "distance": 2
                },
                {
                "source": "E", "target": "B", "distance": 3
                },
                {
                "source": "A", "target": "E", "distance": 7
                }
            ]
            },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    EXAMPLE_ID_2 = data["id"]
    assert response.json() == {
        "id" : EXAMPLE_ID_2,
        "data":[
                {
                "source": "A", "target": "B", "distance": 5
                },
                {
                "source": "B", "target": "C", "distance": 4
                },
                {
                "source": "C", "target": "D", "distance": 8
                },
                {
                "source": "D", "target": "C", "distance": 8
                },
                {
                "source": "D", "target": "E", "distance": 6
                },
                {
                "source": "A", "target": "D", "distance": 5
                },
                {
                "source": "C", "target": "E", "distance": 2
                },
                {
                "source": "E", "target": "B", "distance": 3
                },
                {
                "source": "A", "target": "E", "distance": 7
                }
            ]
        }

def test_read_graph_routes_1():
    global EXAMPLE_ID_2
    response = client.get("/routes/{}/from/{}/to/{}?maxStops={}".format(EXAMPLE_ID_2,'A','C',3))
    assert response.status_code == 200
    assert response.json() == {
        "routes": [
            {
            "route": "ABC",
            "stops": 2
            },
            {
            "route": "ADC",
            "stops": 2
            },
            {
            "route": "AEBC",
            "stops": 3
            }
        ]
        }

def test_read_graph_routes_2():
    response = client.get("/routes/{}/from/{}/to/{}?maxStops={}".format(-1,'A','C',3))
    assert response.status_code == 404
    assert response.json() == {"detail": "Routes not found"}

def test_read_graph_routes_3():
    global EXAMPLE_ID_2
    response = client.get("/routes/{}/from/{}/to/{}?maxStops={}".format(EXAMPLE_ID_2,'A','A',3))
    assert response.status_code == 404
    assert response.json() == {"detail": "Routes not found"}

def test_read_graph_routes_4():
    global EXAMPLE_ID_2
    response = client.get("/routes/{}/from/{}/to/{}?maxStops={}".format(EXAMPLE_ID_2,'A','F',3))
    assert response.status_code == 404
    assert response.json() == {"detail": "Routes not found"}

def test_read_graph_distance_1():
    global EXAMPLE_ID_1
    response = client.get("/distance/{}/from/{}/to/{}".format(EXAMPLE_ID_1,'A','C'))
    assert response.status_code == 200
    assert response.json() == {
        "distance" : 8,
        "path" : ["A", "B", "C"]
        }

def test_read_graph_distance_2():
    response = client.get("/distance/{}/from/{}/to/{}".format(-1,'A','C'))
    assert response.status_code == 404
    assert response.json() == {"detail": "Distance not found"}

def test_read_graph_distance_3():
    global EXAMPLE_ID_1
    response = client.get("/distance/{}/from/{}/to/{}".format(EXAMPLE_ID_1,'A','A'))
    assert response.status_code == 404
    assert response.json() == {"detail": "Distance not found"}

def test_read_graph_distance_4():
    global EXAMPLE_ID_1
    response = client.get("/distance/{}/from/{}/to/{}".format(EXAMPLE_ID_1,'A','F'))
    assert response.status_code == 404
    assert response.json() == {"detail": "Distance not found"}

