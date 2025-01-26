# tests/walletd/test_wallets.py
import pytest
from datetime import datetime, timezone
from typing import List
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.wallets import WalletQueries, WalletMutations
from siaql.graphql.schemas.types import (
    Wallet,
    Balance,
    Address,
    Currency,
    WalletUpdateRequest,
    WalletEvent,
    SiacoinElement,
    SiafundElement,
    WalletReserveRequest,
    WalletReleaseRequest,
    WalletFundRequest,
    WalletFundResponse,
    Transaction,
    SiacoinOutputID,
    SiafundOutputID,
    ChainIndex,
    BlockID,
    Hash256,
    FileContractID,
    TransactionID,
    SiafundOutput,
)


@pytest.fixture
def sample_wallet():
    return Wallet(
        id=1,
        name="Test Wallet",
        description="Test wallet description",
        date_created=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        last_updated=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        metadata={"key": "value"},
    )


@pytest.fixture
def sample_balance():
    return Balance(siacoins=Currency("1000000000"), immature_siacoins=Currency("500000000"), siafunds=5)


@pytest.fixture
def sample_address():
    return Address("addr:testaddress123456789")


class TestWalletQueries(BaseWalletdTest):
    @pytest.fixture
    def wallet_queries(self):
        return WalletQueries()

    @pytest.fixture
    def sample_wallet_event(self):
        return WalletEvent(
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

    @pytest.fixture
    def sample_siacoin_output(self):
        return SiacoinElement(
            id=SiacoinOutputID("scoid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            value=Currency("1000000"),
            address=Address("addr:testaddress123456789"),
            maturity_height=100,
        )

    @pytest.fixture
    def sample_siafund_output(self):
        return SiafundElement(
            id=SiafundOutputID("sfoid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            state_element=None,
            siafund_output=SiafundOutput(value=5, address=Address("addr:testaddress123456789")),
            claim_start=Currency("0"),
        )

    async def test_get_wallets(self, wallet_queries, mock_client, sample_wallet):
        mock_client.get_wallets.return_value = [sample_wallet]
        mock_info = self.create_mock_info(mock_client, List[Wallet])

        result = await wallet_queries.wallets(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Wallet)
        assert result[0].id == sample_wallet.id
        assert result[0].name == sample_wallet.name

        mock_client.get_wallets.assert_called_once()

    async def test_get_wallet_addresses(self, wallet_queries, mock_client, sample_address):
        mock_client.get_wallet_addresses.return_value = [sample_address]
        mock_info = self.create_mock_info(mock_client, List[Address])

        result = await wallet_queries.wallet_addresses(info=mock_info, wallet_id="1")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == sample_address

        mock_client.get_wallet_addresses.assert_called_once_with(wallet_id="1")

    async def test_get_wallet_balance(self, wallet_queries, mock_client, sample_balance):
        mock_client.get_wallet_balance.return_value = sample_balance
        mock_info = self.create_mock_info(mock_client, Balance)

        result = await wallet_queries.wallet_balance(info=mock_info, wallet_id="1")

        assert isinstance(result, Balance)
        assert result.siacoins == sample_balance.siacoins
        assert result.immature_siacoins == sample_balance.immature_siacoins
        assert result.siafunds == sample_balance.siafunds

        mock_client.get_wallet_balance.assert_called_once_with(wallet_id="1")

    async def test_get_wallet_events(self, wallet_queries, mock_client, sample_wallet_event):
        mock_client.get_wallet_events.return_value = [sample_wallet_event]
        mock_info = self.create_mock_info(mock_client, List[WalletEvent])

        result = await wallet_queries.wallet_events(info=mock_info, wallet_id="1", offset=0, limit=500)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], WalletEvent)
        assert result[0].id == sample_wallet_event.id

        mock_client.get_wallet_events.assert_called_once_with(wallet_id="1", offset=0, limit=500)

    async def test_get_wallet_unconfirmed_events(self, wallet_queries, mock_client, sample_wallet_event):
        mock_client.get_wallet_unconfirmed_events.return_value = [sample_wallet_event]
        mock_info = self.create_mock_info(mock_client, List[WalletEvent])

        result = await wallet_queries.wallet_unconfirmed_events(info=mock_info, wallet_id="1")

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], WalletEvent)
        assert result[0].id == sample_wallet_event.id

        mock_client.get_wallet_unconfirmed_events.assert_called_once_with(wallet_id="1")


class TestWalletMutations(BaseWalletdTest):
    @pytest.fixture
    def wallet_mutations(self):
        return WalletMutations()

    @pytest.fixture
    def sample_wallet_update_request(self):
        return WalletUpdateRequest(
            name="Updated Wallet", description="Updated description", metadata={"key": "updated_value"}
        )

    @pytest.fixture
    def sample_wallet_fund_request(self):
        return WalletFundRequest(
            transaction=Transaction(
                siacoin_inputs=[],
                siacoin_outputs=[],
                file_contracts=[],
                file_contract_revisions=[],
                storage_proofs=[],
                siafund_inputs=[],
                siafund_outputs=[],
                miner_fees=[],
                arbitrary_data=[],
                signatures=[],
            ),
            amount=Currency("1000000"),
            change_address=Address("addr:changeaddress123456789"),
        )

    @pytest.fixture
    def sample_fund_response(self):
        return WalletFundResponse(
            transaction=Transaction(
                siacoin_inputs=[],
                siacoin_outputs=[],
                file_contracts=[],
                file_contract_revisions=[],
                storage_proofs=[],
                siafund_inputs=[],
                siafund_outputs=[],
                miner_fees=[],
                arbitrary_data=[],
                signatures=[],
            ),
            to_sign=[Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")],
            depends_on=[],
        )

    async def test_add_wallet(self, wallet_mutations, mock_client, sample_wallet, sample_wallet_update_request):
        mock_client.post_add_wallet.return_value = sample_wallet
        mock_info = self.create_mock_info(mock_client, Wallet)

        result = await wallet_mutations.add_wallet(info=mock_info, wallet=sample_wallet_update_request)

        assert isinstance(result, Wallet)
        assert result.name == sample_wallet.name
        assert result.description == sample_wallet.description

        mock_client.post_add_wallet.assert_called_once_with(wallet_update=sample_wallet_update_request)

    async def test_update_wallet(self, wallet_mutations, mock_client, sample_wallet, sample_wallet_update_request):
        mock_client.post_update_wallet.return_value = sample_wallet
        mock_info = self.create_mock_info(mock_client, Wallet)

        result = await wallet_mutations.update_wallet(
            info=mock_info, wallet_id="1", wallet=sample_wallet_update_request
        )

        assert isinstance(result, Wallet)
        assert result.name == sample_wallet.name
        assert result.description == sample_wallet.description

        mock_client.post_update_wallet.assert_called_once_with(
            wallet_id="1", wallet_update=sample_wallet_update_request
        )

    async def test_delete_wallet(self, wallet_mutations, mock_client):
        mock_client.delete_wallet.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await wallet_mutations.delete_wallet(info=mock_info, wallet_id="1")

        assert result is True
        mock_client.delete_wallet.assert_called_once_with(wallet_id="1")

    async def test_add_wallet_address(self, wallet_mutations, mock_client, sample_address):
        mock_client.add_wallet_address.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await wallet_mutations.add_wallet_address(info=mock_info, wallet_id="1", address=sample_address)

        assert result is True
        mock_client.add_wallet_address.assert_called_once_with(wallet_id="1", address=sample_address)

    async def test_remove_wallet_address(self, wallet_mutations, mock_client, sample_address):
        mock_client.delete_wallet_address.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await wallet_mutations.remove_wallet_address(
            info=mock_info, wallet_id="1", address=str(sample_address)
        )

        assert result is True
        mock_client.delete_wallet_address.assert_called_once_with(wallet_id="1", address=str(sample_address))

    async def test_fund_transaction(
        self, wallet_mutations, mock_client, sample_wallet_fund_request, sample_fund_response
    ):
        mock_client.post_wallet_fund.return_value = sample_fund_response
        mock_info = self.create_mock_info(mock_client, WalletFundResponse)

        result = await wallet_mutations.fund_transaction(
            info=mock_info, wallet_id="1", request=sample_wallet_fund_request
        )

        assert isinstance(result, WalletFundResponse)
        assert isinstance(result.transaction, Transaction)
        assert len(result.to_sign) == len(sample_fund_response.to_sign)

        mock_client.post_wallet_fund.assert_called_once_with(wallet_id="1", fund_request=sample_wallet_fund_request)
