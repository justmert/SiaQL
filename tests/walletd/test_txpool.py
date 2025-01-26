# tests/walletd/test_txpool.py
import pytest
from datetime import datetime, timezone
from typing import List
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.txpool import TxpoolQueries, TxpoolMutations
from siaql.graphql.schemas.types import (
    Transaction,
    V2Transaction,
    Currency,
    Address,
    SiacoinInput,
    SiacoinOutput,
    SiafundInput,
    SiafundOutput,
    FileContract,
    FileContractRevision,
    StorageProof,
    TransactionSignature,
    Hash256,
    TxpoolBroadcastRequest,
    TxpoolTransactionsResponse,
)


@pytest.fixture
def sample_transaction():
    return Transaction(
        siacoin_inputs=[
            SiacoinInput(
                parent_id=Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                unlock_conditions=None,
            )
        ],
        siacoin_outputs=[SiacoinOutput(value=Currency("1000000"), address=Address("addr:testaddress123456789"))],
        file_contracts=[],
        file_contract_revisions=[],
        storage_proofs=[],
        siafund_inputs=[],
        siafund_outputs=[],
        miner_fees=[Currency("1000")],
        arbitrary_data=[],
        signatures=[],
    )


@pytest.fixture
def sample_v2_transaction():
    return V2Transaction(
        siacoin_inputs=[],
        siacoin_outputs=[],
        siafund_inputs=[],
        siafund_outputs=[],
        file_contracts=[],
        file_contract_revisions=[],
        file_contract_resolutions=[],
        attestations=[],
        arbitrary_data=[],
        miner_fee=Currency("1000"),
        new_foundation_address=Address("addr:testaddress123456789"),
    )


class TestTxpoolQueries(BaseWalletdTest):
    @pytest.fixture
    def txpool_queries(self):
        return TxpoolQueries()

    @pytest.fixture
    def sample_txpool_transactions(self, sample_transaction, sample_v2_transaction):
        return TxpoolTransactionsResponse(transactions=[sample_transaction], v2transactions=[sample_v2_transaction])

    async def test_get_txpool_parents(self, txpool_queries, mock_client, sample_transaction):
        parent_transactions = [sample_transaction]
        mock_client.get_txpool_parents.return_value = parent_transactions
        mock_info = self.create_mock_info(mock_client, List[Transaction])

        result = await txpool_queries.txpool_parents(info=mock_info, transaction=sample_transaction)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Transaction)
        assert result[0].siacoin_inputs == sample_transaction.siacoin_inputs
        assert result[0].siacoin_outputs == sample_transaction.siacoin_outputs

        mock_client.get_txpool_parents.assert_called_once_with(transaction=sample_transaction)

    async def test_get_txpool_transactions(self, txpool_queries, mock_client, sample_txpool_transactions):
        mock_client.get_txpool_transactions.return_value = sample_txpool_transactions
        mock_info = self.create_mock_info(mock_client, TxpoolTransactionsResponse)

        result = await txpool_queries.txpool_transactions(info=mock_info)

        assert isinstance(result, TxpoolTransactionsResponse)
        assert len(result.transactions) == 1
        assert len(result.v2transactions) == 1
        assert isinstance(result.transactions[0], Transaction)
        assert isinstance(result.v2transactions[0], V2Transaction)

        mock_client.get_txpool_transactions.assert_called_once()

    async def test_get_txpool_fee(self, txpool_queries, mock_client):
        expected_fee = Currency("1000")
        mock_client.get_txpool_fee.return_value = expected_fee
        mock_info = self.create_mock_info(mock_client, Currency)

        result = await txpool_queries.txpool_fee(info=mock_info)
        assert result == expected_fee

        mock_client.get_txpool_fee.assert_called_once()


class TestTxpoolMutations(BaseWalletdTest):
    @pytest.fixture
    def txpool_mutations(self):
        return TxpoolMutations()

    @pytest.fixture
    def sample_broadcast_request(self, sample_transaction, sample_v2_transaction):
        return TxpoolBroadcastRequest(transactions=[sample_transaction], v2transactions=[sample_v2_transaction])

    async def test_txpool_broadcast(self, txpool_mutations, mock_client, sample_broadcast_request):
        mock_client.txpool_broadcast.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await txpool_mutations.txpool_broadcast(info=mock_info, req=sample_broadcast_request)

        assert result is True
        mock_client.txpool_broadcast.assert_called_once_with(req=sample_broadcast_request)

    async def test_txpool_broadcast_invalid_transaction(self, txpool_mutations, mock_client, sample_broadcast_request):
        mock_client.txpool_broadcast.side_effect = Exception("Invalid transaction")
        mock_info = self.create_mock_info(mock_client, bool)

        with pytest.raises(Exception):
            await txpool_mutations.txpool_broadcast(info=mock_info, req=sample_broadcast_request)

        mock_client.txpool_broadcast.assert_called_once_with(req=sample_broadcast_request)
