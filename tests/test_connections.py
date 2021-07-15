from docoin.connections import ConnectionPool


def test_get_address():
    connections = ConnectionPool()
    domain = 'testurl.com'
    path = 'path/to/loc'
    url = f'http://{domain}/{path}'
    assert connections.get_address(url) == domain


def test_add_peer():
    connections = ConnectionPool()
    domain = 'testurl.com'
    path = 'path/to/loc'
    url = f'http://{domain}/{path}'
    num_peers = len(connections.connection_pool)
    connections.add_peer(url)

    assert len(connections.connection_pool) == num_peers + 1


def test_remove_peer():
    connections = ConnectionPool()
    domain = 'testurl.com'
    path = 'path/to/loc'
    url = f'http://{domain}/{path}'
    connections.add_peer(url)
    connections.remove_peer(url)

    assert len(connections.connection_pool) == 0
