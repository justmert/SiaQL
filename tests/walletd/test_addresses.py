# tests/walletd/test_addresses.py
import pytest
from datetime import datetime, timezone
from typing import List
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.addresses import AddressQueries
from siaql.graphql.schemas.types import (
    Balance,
    WalletEvent,
    SiacoinElement,
    SiafundElement,
    Currency,
    Address,
    SiacoinOutputID,
    SiafundOutputID,
    ChainIndex,
    BlockID,
    Hash256,
    TransactionID,
    FileContractID,
    SiafundOutput,
)


class TestAddressQueries(BaseWalletdTest):
    @pytest.fixture
    def address_queries(self):
        return AddressQueries()

    @pytest.fixture
    def sample_address(self):
        return Address("addr:testaddress123456789")

    @pytest.fixture
    def sample_balance(self):
        return Balance(siacoins=Currency("1000000000"), immature_siacoins=Currency("500000000"), siafunds=5)

    @pytest.fixture
    def sample_events(self):
        return [
            WalletEvent(
                id=Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                index=ChainIndex(
                    height=100, id=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
                ),
                type="transfer",
                data={"amount": "1000"},
                maturity_height=105,
                timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
                relevant=[Address("addr:testaddress123456789")],
            )
        ]

    @pytest.fixture
    def sample_siacoin_outputs(self):
        return [
            SiacoinElement(
                id=SiacoinOutputID("scoid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                value=Currency("1000000"),
                address=Address("addr:testaddress123456789"),
                maturity_height=100,
            )
        ]

    @pytest.fixture
    def sample_siafund_outputs(self):
        return [
            SiafundElement(
                id=SiafundOutputID("sfoid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                state_element=None,
                siafund_output=SiafundOutput(value=5, address=Address("addr:testaddress123456789")),
                claim_start=Currency("0"),
            )
        ]

    async def test_address_balance(self, address_queries, mock_client, sample_address, sample_balance):
        mock_client.get_address_balance.return_value = sample_balance
        mock_info = self.create_mock_info(mock_client, Balance)

        result = await address_queries.address_balance(info=mock_info, address=sample_address)

        assert isinstance(result, Balance)
        assert result.siacoins == sample_balance.siacoins
        assert result.immature_siacoins == sample_balance.immature_siacoins
        assert result.siafunds == sample_balance.siafunds

        mock_client.get_address_balance.assert_called_once_with(address=sample_address)

    async def test_address_events(self, address_queries, mock_client, sample_address, sample_events):
        mock_client.get_address_events.return_value = sample_events
        mock_info = self.create_mock_info(mock_client, List[WalletEvent])

        result = await address_queries.address_events(info=mock_info, address=sample_address, offset=0, limit=500)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], WalletEvent)
        assert result[0].id == sample_events[0].id
        assert result[0].type == sample_events[0].type

        mock_client.get_address_events.assert_called_once_with(address=sample_address, offset=0, limit=500)

    async def test_address_unconfirmed_events(self, address_queries, mock_client, sample_address, sample_events):
        mock_client.get_address_unconfirmed_events.return_value = sample_events
        mock_info = self.create_mock_info(mock_client, List[WalletEvent])

        result = await address_queries.address_unconfirmed_events(info=mock_info, address=sample_address)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], WalletEvent)
        assert result[0].id == sample_events[0].id

        mock_client.get_address_unconfirmed_events.assert_called_once_with(address=sample_address)

    async def test_address_siacoin_outputs(self, address_queries, mock_client, sample_address, sample_siacoin_outputs):
        mock_client.get_address_siacoin_outputs.return_value = sample_siacoin_outputs
        mock_info = self.create_mock_info(mock_client, List[SiacoinElement])

        result = await address_queries.address_siacoin_outputs(
            info=mock_info, address=sample_address, offset=0, limit=1000
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], SiacoinElement)
        assert result[0].value == sample_siacoin_outputs[0].value
        assert result[0].address == sample_siacoin_outputs[0].address

        mock_client.get_address_siacoin_outputs.assert_called_once_with(address=sample_address, offset=0, limit=1000)

    async def test_address_siafund_outputs(self, address_queries, mock_client, sample_address, sample_siafund_outputs):
        mock_client.get_address_siafund_outputs.return_value = sample_siafund_outputs
        mock_info = self.create_mock_info(mock_client, List[SiafundElement])

        result = await address_queries.address_siafund_outputs(
            info=mock_info, address=sample_address, offset=0, limit=1000
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], SiafundElement)
        assert result[0].siafund_output.value == sample_siafund_outputs[0].siafund_output.value
        assert result[0].siafund_output.address == sample_siafund_outputs[0].siafund_output.address

        mock_client.get_address_siafund_outputs.assert_called_once_with(address=sample_address, offset=0, limit=1000)

    @pytest.mark.parametrize("offset,limit", [(0, 100), (100, 200), (0, 1000), (500, 100)])
    async def test_address_events_pagination(
        self, address_queries, mock_client, sample_address, sample_events, offset, limit
    ):
        mock_client.get_address_events.return_value = sample_events
        mock_info = self.create_mock_info(mock_client, List[WalletEvent])

        result = await address_queries.address_events(
            info=mock_info, address=sample_address, offset=offset, limit=limit
        )

        assert isinstance(result, list)
        mock_client.get_address_events.assert_called_once_with(address=sample_address, offset=offset, limit=limit)
