import pdb
from unittest import mock
import pytest
from monero_cli.commands.transfer import (
    Destination,
    parse_command,
    parse_destinations,
    DEFAULT_PRIORITY,
    DEFAULT_RINGSIZE,
)
from monero_cli.settings import Network
from monero_cli.exceptions import ValidationError


class TestDestination:
    def test_valid_address(self, dummy_address):
        cases = [
            (dummy_address(net="testnet"), Network(Network.TESTNET)),
            (dummy_address(net="stagenet"), Network(Network.STAGENET)),
            (dummy_address(net="mainnet"), Network(Network.MAINNET)),
        ]

        network_conf = "monero_cli.settings.NETWORK"
        for addr, network in cases:
            with mock.patch(network_conf, network):
                dest = Destination(addr, "2")
                assert str(dest.address) == addr

    def test_invalid_address(self, dummy_address):
        cases = [
            (dummy_address(net="mainnet"), Network(Network.TESTNET)),
            (dummy_address(net="testnet"), Network(Network.STAGENET)),
            (dummy_address(net="stagenet"), Network(Network.MAINNET)),
        ]

        network_conf = "monero_cli.commands.transfer.settings.NETWORK"
        for addr, network in cases:
            with mock.patch(network_conf, network):
                with pytest.raises(ValidationError):
                    Destination(addr, "2")

    def test_valid_amount(self, dummy_address):
        amount = "2"
        addr = dummy_address(net=Network.STAGENET)
        network_conf = "monero_cli.commands.transfer.settings.NETWORK"
        with mock.patch(network_conf, Network(Network.STAGENET)):
            dest = Destination(addr, amount)
            assert str(dest.amount) == amount

    def test_invalid_amount(self, dummy_address):
        amount = "asd"
        addr = dummy_address(net=Network.STAGENET)
        network_conf = "monero_cli.commands.transfer.settings.NETWORK"
        with mock.patch(network_conf, Network(Network.STAGENET)):
            with pytest.raises(ValidationError):
                Destination(addr, amount)

    def test_to_tuple(self, dummy_address):
        amount = "2"
        addr = dummy_address(net=Network.STAGENET)
        network_conf = "monero_cli.commands.transfer.settings.NETWORK"
        with mock.patch(network_conf, Network(Network.STAGENET)):
            dest = Destination(addr, amount)
            tuple_addr, tuple_amount = dest.to_tuple()
            assert str(tuple_addr) == addr
            assert str(tuple_amount) == amount


class TestParseCommand:
    @pytest.mark.parametrize(
        "cmd, ring, prio, dest",
        (
            ("11 normal", 11, "normal", []),
            (
                "12 ad1 am1 ad2 am2",
                12,
                DEFAULT_PRIORITY,
                ["ad1", "am1", "ad2", "am2"],
            ),
            (
                "elevated ad1 am1 ad2 am2",
                DEFAULT_RINGSIZE,
                "elevated",
                ["ad1", "am1", "ad2", "am2"],
            ),
            (
                "1 normal ad1 am1 ad2 am2",
                1,
                "normal",
                ["ad1", "am1", "ad2", "am2"],
            ),
        ),
    )
    def test_valid(self, cmd, ring, prio, dest):
        _ring, _prio, _dest = parse_command(cmd)
        assert _ring == ring
        assert _prio == prio
        assert _dest == dest

    @pytest.mark.parametrize("cmd", ("11", "am2"))
    def test_invalid(self, cmd):
        with pytest.raises(ValidationError):
            parse_command(cmd)


class TestParseDestinations:
    def test_valid_destinations(self, dummy_address):
        args = [
            dummy_address(Network.STAGENET),
            "2",
            dummy_address(Network.STAGENET),
            "7",
        ]
        destinations = parse_destinations(args)
        assert len(destinations) == 2

        dest1, dest2 = destinations
        assert str(dest1.address) == args[0]
        assert str(dest1.amount) == args[1]
        assert str(dest2.address) == args[2]
        assert str(dest2.amount) == args[3]

    @pytest.mark.parametrize(
        "args", ([], ["ad1", "am1", "ad2"], ["ad1"], ["ad1", "ad2", "am2"])
    )
    def test_invalid_number_of_args(self, args):
        with pytest.raises(ValidationError):
            parse_destinations(args)

    def test_invalid_destination_args(self, dummy_address):
        cases = [
            (
                dummy_address(Network.MAINNET),
                "2",
                dummy_address(Network.STAGENET),
                "3",
            ),
            ("asd", "2", dummy_address(Network.STAGENET), "1"),
            (dummy_address(Network.STAGENET), "asd"),
        ]

        network_conf = "monero_cli.commands.transfer.settings.NETWORK"
        with mock.patch(network_conf, Network(Network.STAGENET)):
            for args in cases:
                with pytest.raises(ValidationError):
                    parse_destinations(args)
