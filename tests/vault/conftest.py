import pytest


@pytest.fixture(scope="function", autouse=False)
def shared_setup(fn_isolation):
    pass


@pytest.fixture(scope='module')
def user1(accounts):
    return accounts[0]


@pytest.fixture(scope='module')
def user2(accounts):
    return accounts[1]


@pytest.fixture(scope='module')
def vault(LidoVault, user1):
    return LidoVault.deploy({"from": user1})


@pytest.fixture(scope='module')
def lido(interface, accounts):
    lido = interface.Lido("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")
    oracle = accounts.at(lido.getOracle(), force=True)
    return interface.Lido(lido, owner=oracle)
