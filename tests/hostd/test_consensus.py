# tests/hostd/test_consensus.py
import pytest
from typing import Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.consensus import ConsensusQueries
from siaql.graphql.schemas.types import (
    ChainIndex,
    Network,
    ConsensusState,
    BlockID,
    HardforkDevAddr,
    HardforkTax,
    HardforkStorageProof,
    HardforkOak,
    HardforkASIC,
    HardforkFoundation,
    HardforkV2,
    Address,
    Currency,
    Duration,
)
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestConsensusQueries(BaseHostdTest):
    @pytest.fixture
    def consensus_queries(self):
        return ConsensusQueries()

    @pytest.fixture
    def sample_chain_index(self):
        return ChainIndex(
            height=123456, id=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
        )

    @pytest.fixture
    def sample_network(self, make_timestamp):
        return Network(
            name="mainnet",
            initial_coinbase=Currency("300000"),
            minimum_coinbase=Currency("30000"),
            initial_target=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            block_interval=Duration(600000000000),  # 10 minutes in nanoseconds
            maturity_delay=144,
            hardfork_dev_addr=HardforkDevAddr(
                height=10000, old_address=Address("addr:old12345"), new_address=Address("addr:new12345")
            ),
            hardfork_tax=HardforkTax(height=20000),
            hardfork_storage_proof=HardforkStorageProof(height=30000),
            hardfork_oak=HardforkOak(height=40000, fix_height=45000, genesis_timestamp=make_timestamp),
            hardfork_asic=HardforkASIC(
                height=50000,
                oak_time=Duration(600000000000),
                oak_target=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            ),
            hardfork_foundation=HardforkFoundation(
                height=60000,
                primary_address=Address("addr:primary12345"),
                failsafe_address=Address("addr:failsafe12345"),
            ),
            hardfork_v2=HardforkV2(allow_height=70000, require_height=75000),
        )

    @pytest.fixture
    def sample_consensus_state(self, make_timestamp):
        return ConsensusState(block_height=123456, last_block_time=make_timestamp, synced=True)

    async def test_get_consensus_tip(self, consensus_queries, mock_client, sample_chain_index):
        mock_client.get_consensus_tip.return_value = sample_chain_index
        mock_info = self.create_mock_info(mock_client, ChainIndex)

        result = await consensus_queries.consensus_tip(info=mock_info)

        assert isinstance(result, ChainIndex)
        assert result.height == sample_chain_index.height
        assert result.id == sample_chain_index.id
        mock_client.get_consensus_tip.assert_called_once()

    async def test_get_consensus_tip_state(self, consensus_queries, mock_client, sample_consensus_state):
        mock_client.get_consensus_tip_state.return_value = sample_consensus_state
        mock_info = self.create_mock_info(mock_client, ConsensusState)

        result = await consensus_queries.consensus_tip_state(info=mock_info)

        assert isinstance(result, ConsensusState)
        assert result.block_height == sample_consensus_state.block_height
        assert result.last_block_time == sample_consensus_state.last_block_time
        assert result.synced == sample_consensus_state.synced
        mock_client.get_consensus_tip_state.assert_called_once()

    async def test_get_consensus_network(self, consensus_queries, mock_client, sample_network):
        mock_client.get_consensus_network.return_value = sample_network
        mock_info = self.create_mock_info(mock_client, Network)

        result = await consensus_queries.consensus_network(info=mock_info)

        assert isinstance(result, Network)
        assert result.name == sample_network.name
        assert result.initial_coinbase == sample_network.initial_coinbase
        assert result.minimum_coinbase == sample_network.minimum_coinbase
        assert result.initial_target == sample_network.initial_target
        assert result.block_interval == sample_network.block_interval
        assert result.maturity_delay == sample_network.maturity_delay
        mock_client.get_consensus_network.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="blockHeight", operator=FilterOperator.GTE, value=100000), None, None),
            (None, SortInput(field="blockHeight", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_consensus_tip_with_filters(
        self, consensus_queries, mock_client, sample_chain_index, filter_input, sort_input, pagination_input
    ):
        mock_client.get_consensus_tip.return_value = sample_chain_index
        mock_info = self.create_mock_info(mock_client, ChainIndex)

        result = await consensus_queries.consensus_tip(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, ChainIndex)
        assert result.height == sample_chain_index.height
        assert result.id == sample_chain_index.id
        mock_client.get_consensus_tip.assert_called_once()

    async def test_get_consensus_tip_empty(self, consensus_queries, mock_client):
        mock_client.get_consensus_tip.return_value = None
        mock_info = self.create_mock_info(mock_client, ChainIndex)

        result = await consensus_queries.consensus_tip(info=mock_info)

        assert result is None
        mock_client.get_consensus_tip.assert_called_once()
