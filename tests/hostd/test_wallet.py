# tests/hostd/test_wallet.py
import pytest
from typing import List, Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.wallet import WalletQueries, WalletMutations
from siaql.graphql.schemas.types import (
    WalletResponse,
    WalletEvent,
    Address,
    Currency,
    TransactionID,
    WalletSendSiacoinsRequest,
    Balance,
    ChainIndex,
    Hash256,
)
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


@pytest.fixture
def sample_wallet_response():
    return WalletResponse(
        scan_height=150000,
        address=Address("addr:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
        spendable=Currency("1000000"),
        confirmed=Currency("1500000"),
        unconfirmed=Currency("500000"),
        immature=Currency("100000"),
    )


@pytest.fixture
def sample_wallet_events(make_timestamp):
    return [
        WalletEvent(
            id="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            timestamp=make_timestamp,
            index=ChainIndex(height=100000, id=Hash256("123")),
            type="send",
            data={"amount": "1000000", "address": "addr:recipient"},
            maturity_height=150000,
            relevant=[Address("addr:sender"), Address("addr:recipient")],
        ),
        WalletEvent(
            id=Hash256("2234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            timestamp=make_timestamp,
            index=ChainIndex(height=100001, id=Hash256("123")),
            type="receive",
            data={"amount": "2000000", "address": "addr:recipient"},
            maturity_height=150000,
            relevant=[Address("addr:sender"), Address("addr:recipient")],
        ),
    ]


class TestWalletQueries(BaseHostdTest):
    @pytest.fixture
    def wallet_queries(self):
        return WalletQueries()

    async def test_get_wallet(self, wallet_queries, mock_client, sample_wallet_response):
        mock_client.get_wallet.return_value = sample_wallet_response
        mock_info = self.create_mock_info(mock_client, WalletResponse)

        result = await wallet_queries.wallet(info=mock_info)

        assert isinstance(result, WalletResponse)
        assert result.scan_height == sample_wallet_response.scan_height
        assert result.address == sample_wallet_response.address
        assert result.spendable == sample_wallet_response.spendable
        assert result.confirmed == sample_wallet_response.confirmed
        assert result.unconfirmed == sample_wallet_response.unconfirmed
        assert result.immature == sample_wallet_response.immature
        mock_client.get_wallet.assert_called_once()

    async def test_get_wallet_events(self, wallet_queries, mock_client, sample_wallet_events):
        mock_client.get_wallet_events.return_value = sample_wallet_events
        mock_info = self.create_mock_info(mock_client, List[WalletEvent])

        result = await wallet_queries.wallet_events(info=mock_info, limit=100, offset=0)

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], WalletEvent)
        assert result[0].id == sample_wallet_events[0].id
        mock_client.get_wallet_events.assert_called_once_with(limit=100, offset=0)

    async def test_get_wallet_pending(self, wallet_queries, mock_client, sample_wallet_events):
        mock_client.get_wallet_pending.return_value = sample_wallet_events
        mock_info = self.create_mock_info(mock_client, List[WalletEvent])

        result = await wallet_queries.wallet_pending(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], WalletEvent)
        mock_client.get_wallet_pending.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="spendable", operator=FilterOperator.GTE, value="1000000"), None, None),
            (None, SortInput(field="scanHeight", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_wallet_with_filters(
        self, wallet_queries, mock_client, sample_wallet_response, filter_input, sort_input, pagination_input
    ):
        mock_client.get_wallet.return_value = sample_wallet_response
        mock_info = self.create_mock_info(mock_client, WalletResponse)

        result = await wallet_queries.wallet(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, WalletResponse)
        assert result.spendable == sample_wallet_response.spendable
        mock_client.get_wallet.assert_called_once()

    async def test_get_wallet_empty(self, wallet_queries, mock_client):
        mock_client.get_wallet.return_value = None
        mock_info = self.create_mock_info(mock_client, WalletResponse)

        result = await wallet_queries.wallet(info=mock_info)

        assert result is None
        mock_client.get_wallet.assert_called_once()

    async def test_get_wallet_events_empty(self, wallet_queries, mock_client):
        mock_client.get_wallet_events.return_value = []
        mock_info = self.create_mock_info(mock_client, List[WalletEvent])

        result = await wallet_queries.wallet_events(info=mock_info, limit=100, offset=0)

        assert len(result) == 0
        mock_client.get_wallet_events.assert_called_once_with(limit=100, offset=0)


class TestWalletMutations(BaseHostdTest):
    @pytest.fixture
    def wallet_mutations(self):
        return WalletMutations()

    @pytest.fixture
    def sample_send_request(self):
        return WalletSendSiacoinsRequest(
            address=Address("addr:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            amount=Currency("1000000"),
            subtract_miner_fee=True,
        )

    @pytest.fixture
    def sample_transaction_id(self):
        return TransactionID("txid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")

    async def test_send_siacoins(self, wallet_mutations, mock_client, sample_send_request, sample_transaction_id):
        mock_client.post_wallet_send.return_value = sample_transaction_id
        mock_info = self.create_mock_info(mock_client, TransactionID)

        result = await wallet_mutations.send_siacoins(info=mock_info, req=sample_send_request)

        assert result == sample_transaction_id
        mock_client.post_wallet_send.assert_called_once_with(req=sample_send_request)

    async def test_send_siacoins_error(self, wallet_mutations, mock_client, sample_send_request):
        mock_client.post_wallet_send.side_effect = Exception("Insufficient funds")
        mock_info = self.create_mock_info(mock_client, TransactionID)

        with pytest.raises(Exception):
            await wallet_mutations.send_siacoins(info=mock_info, req=sample_send_request)
