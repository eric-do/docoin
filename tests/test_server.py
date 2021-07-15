from flask import Flask, testing, json
from docoin.server import create_app
import pytest


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_mining_returns_block(client):
    keys = [
        'message',
        'index',
        'transactions',
        'proof',
        'previous_hash'
    ]
    response = client.get('/mine')
    data = json.loads(response.data)
    assert all(k in data for k in keys) is True


def test_add_transaction(client):
    transaction = {
        'sender': 'eric-sender',
        'recipient': 'eric-recipient',
        'amount': 10
    }

    response = client.post(
        '/transactions/new',
        data=json.dumps(transaction),
        content_type='application/json'
    )
    print(response.data)
    data = json.loads(response.data)
    assert 'message' in data


def test_consensus_returns_chain(client):
    keys = [
        'message',
        'chain'
    ]
    response = client.get('/nodes/resolve')
    data = json.loads(response.data)
    print(data)
    assert all(k in data for k in keys) is True
