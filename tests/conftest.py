import pytest
from monero.seed import Seed


@pytest.fixture
def dummy_address() -> str:
    def create(net: str):
        seed = Seed()
        return str(seed.public_address(net=net))
    
    return create