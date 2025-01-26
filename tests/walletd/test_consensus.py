# tests/walletd/test_consensus.py
import pytest
from datetime import datetime, timezone
from typing import List, Union
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.consensus import ConsensusQueries
from siaql.graphql.schemas.types import (
    ConsensusUpdatesResponse,
    Network,
    ChainIndex,
    ConsensusState,
    Block,
    Currency,
    BlockID,
    Address,
    ApplyUpdate,
    RevertUpdate,
    Hash256,
    HardforkDevAddr,
    HardforkTax,
    HardforkStorageProof,
    HardforkOak,
    HardforkASIC,
    HardforkFoundation,
    HardforkV2,
    SiacoinOutput,
    V2BlockData,
)


class TestConsensusQueries(BaseWalletdTest):
    @pytest.fixture
    def consensus_queries(self):
        return ConsensusQueries()

    @pytest.fixture
    def sample_network(self):
        return Network(
            name="mainnet",
            initial_coinbase=Currency("300000000000000000000000000000"),
            minimum_coinbase=Currency("300000000000000000000000000000"),
            initial_target=BlockID("0x0000000000000000000000000000000000000000000000000000000000000000"),
            block_interval=60000000000,  # Duration in nanoseconds
            maturity_delay=144,
            hardfork_dev_addr=HardforkDevAddr(
                height=1000, old_address=Address("old_addr"), new_address=Address("new_addr")
            ),
            hardfork_tax=HardforkTax(height=2000),
            hardfork_storage_proof=HardforkStorageProof(height=3000),
            hardfork_oak=HardforkOak(
                height=4000, fix_height=4100, genesis_timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc)
            ),
            hardfork_asic=HardforkASIC(height=5000, oak_time=60000000000, oak_target=BlockID("target_hash")),
            hardfork_foundation=HardforkFoundation(
                height=6000, primary_address=Address("primary_addr"), failsafe_address=Address("failsafe_addr")
            ),
            hardfork_v2=HardforkV2(allow_height=7000, require_height=7100),
        )

    @pytest.fixture
    def sample_chain_index(self):
        return ChainIndex(
            height=100000, id=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
        )

    @pytest.fixture
    def sample_consensus_state(self):
        return ConsensusState(
            block_height=100000, last_block_time=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc), synced=True
        )

    @pytest.fixture
    def sample_block(self):
        return Block(
            parent_id=BlockID("parent:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            nonce=12345,
            timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            miner_payouts=[SiacoinOutput(value=Currency("1000000000"), address=Address("miner_addr"))],
            transactions=[],
        )

    @pytest.fixture
    def sample_consensus_updates(self):
        block = Block(
            parent_id=BlockID("parent:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            nonce=12345,
            timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            miner_payouts=[],
            transactions=[],
            v2=V2BlockData(
                height=100000,
                commitment=Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                transactions=[],
            ),
        )
        return {
            "applied": [
                ApplyUpdate(
                    update={"type": "apply", "data": {}}, state={"type": "consensus_state", "data": {}}, block=block
                )
            ],
            "reverted": [
                RevertUpdate(
                    update={"type": "revert", "data": {}}, state={"type": "consensus_state", "data": {}}, block=block
                )
            ],
        }

    async def test_consensus_network(self, consensus_queries, mock_client, sample_network):
        mock_client.get_consensus_network.return_value = sample_network
        mock_info = self.create_mock_info(mock_client, Network)

        result = await consensus_queries.consensus_network(info=mock_info)

        assert isinstance(result, Network)
        assert result.name == sample_network.name
        assert result.initial_coinbase == sample_network.initial_coinbase
        assert result.minimum_coinbase == sample_network.minimum_coinbase
        assert result.initial_target == sample_network.initial_target

        mock_client.get_consensus_network.assert_called_once()

    async def test_consensus_tip(self, consensus_queries, mock_client, sample_chain_index):
        mock_client.get_consensus_tip.return_value = sample_chain_index
        mock_info = self.create_mock_info(mock_client, ChainIndex)

        result = await consensus_queries.consensus_tip(info=mock_info)

        assert isinstance(result, ChainIndex)
        assert result.height == sample_chain_index.height
        assert result.id == sample_chain_index.id

        mock_client.get_consensus_tip.assert_called_once()

    async def test_consensus_tip_state(self, consensus_queries, mock_client, sample_consensus_state):
        mock_client.get_consensus_tip_state.return_value = sample_consensus_state
        mock_info = self.create_mock_info(mock_client, ConsensusState)

        result = await consensus_queries.consensus_tip_state(info=mock_info)

        assert isinstance(result, ConsensusState)
        assert result.block_height == sample_consensus_state.block_height
        assert result.last_block_time == sample_consensus_state.last_block_time
        assert result.synced == sample_consensus_state.synced

        mock_client.get_consensus_tip_state.assert_called_once()

    async def test_consensus_index(self, consensus_queries, mock_client, sample_chain_index):
        mock_client.get_consensus_index.return_value = sample_chain_index
        mock_info = self.create_mock_info(mock_client, ChainIndex)

        result = await consensus_queries.consensus_index(info=mock_info, height=100000)

        assert isinstance(result, ChainIndex)
        assert result.height == sample_chain_index.height
        assert result.id == sample_chain_index.id

        mock_client.get_consensus_index.assert_called_once_with(height=100000)

    async def test_consensus_updates(
        self, consensus_queries, mock_client, sample_chain_index, sample_consensus_updates
    ):
        mock_client.get_consensus_updates.return_value = sample_consensus_updates
        mock_info = self.create_mock_info(mock_client, ConsensusUpdatesResponse)

        result = await consensus_queries.consensus_updates(info=mock_info, index=sample_chain_index, limit=10)

        assert isinstance(result, ConsensusUpdatesResponse)

        mock_client.get_consensus_updates.assert_called_once_with(index=sample_chain_index, limit=10)
