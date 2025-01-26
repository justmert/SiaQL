# tests/walletd/test_syncer.py
import pytest
from datetime import datetime, timezone
from typing import List
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.syncer import SyncerQueries, SyncerMutations
from siaql.graphql.schemas.types import (
    GatewayPeer,
    Block,
    BlockID,
    SiacoinOutput,
    Transaction,
    Currency,
    Address,
    TransactionSignature,
    FileContractRevision,
    FileContract,
    V2Transaction,
    V2BlockData,
    Hash256,
)


class TestSyncerQueries(BaseWalletdTest):
    @pytest.fixture
    def syncer_queries(self):
        return SyncerQueries()

    @pytest.fixture
    def sample_peers(self):
        return [
            GatewayPeer(
                addr="peer1.example.com:9981",
                inbound=False,
                version="1.0.0",
                first_seen=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
                connected_since=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
                synced_blocks=1000,
                sync_duration=3600000000000,  # 1 hour in nanoseconds
            ),
            GatewayPeer(
                addr="peer2.example.com:9981",
                inbound=True,
                version="1.0.1",
                first_seen=datetime(2025, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
                connected_since=datetime(2025, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
                synced_blocks=2000,
                sync_duration=7200000000000,  # 2 hours in nanoseconds
            ),
        ]

    async def test_get_syncer_peers(self, syncer_queries, mock_client, sample_peers):
        mock_client.get_syncer_peers.return_value = sample_peers
        mock_info = self.create_mock_info(mock_client, List[GatewayPeer])

        result = await syncer_queries.syncer_peers(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(peer, GatewayPeer) for peer in result)
        assert result[0].addr == sample_peers[0].addr
        assert result[1].addr == sample_peers[1].addr

        mock_client.get_syncer_peers.assert_called_once()


class TestSyncerMutations(BaseWalletdTest):
    @pytest.fixture
    def syncer_mutations(self):
        return SyncerMutations()

    @pytest.fixture
    def sample_block(self):
        return Block(
            parent_id=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            nonce=12345,
            timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            miner_payouts=[SiacoinOutput(value=Currency("1000000"), address=Address("addr:testaddress123456789"))],
            transactions=[],
            v2=V2BlockData(
                height=100000,
                commitment=Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                transactions=[],
            ),
        )

    async def test_syncer_connect(self, syncer_mutations, mock_client):
        mock_client.post_syncer_connect.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)
        addr = "peer.example.com:9981"

        result = await syncer_mutations.syncer_connect(info=mock_info, addr=addr)

        assert result is True
        mock_client.post_syncer_connect.assert_called_once_with(addr=addr)

    async def test_syncer_broadcast_block(self, syncer_mutations, mock_client, sample_block):
        mock_client.post_syncer_broadcast_block.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await syncer_mutations.syncer_broadcast_block(info=mock_info, block=sample_block)

        assert result is True
        mock_client.post_syncer_broadcast_block.assert_called_once_with(block=sample_block)

    async def test_syncer_connect_invalid_address(self, syncer_mutations, mock_client):
        mock_client.post_syncer_connect.side_effect = Exception("Invalid address")
        mock_info = self.create_mock_info(mock_client, bool)
        addr = "invalid-address"

        with pytest.raises(Exception):
            await syncer_mutations.syncer_connect(info=mock_info, addr=addr)

        mock_client.post_syncer_connect.assert_called_once_with(addr=addr)

    async def test_syncer_broadcast_block_invalid(self, syncer_mutations, mock_client, sample_block):
        mock_client.post_syncer_broadcast_block.side_effect = Exception("Invalid block")
        mock_info = self.create_mock_info(mock_client, bool)

        with pytest.raises(Exception):
            await syncer_mutations.syncer_broadcast_block(info=mock_info, block=sample_block)

        mock_client.post_syncer_broadcast_block.assert_called_once_with(block=sample_block)
