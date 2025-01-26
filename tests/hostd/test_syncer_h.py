# tests/hostd/test_syncer.py
import pytest
from typing import List, Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.syncer import SyncerQueries, SyncerMutations
from siaql.graphql.schemas.types import Peer
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


@pytest.fixture
def sample_address():
    return "127.0.0.1:9981"


@pytest.fixture
def sample_peer(make_timestamp):
    return Peer(
        address="127.0.0.1:9981",
        inbound=False,
        version="1.5.4",
        first_seen=make_timestamp,
        connected_since=make_timestamp,
        synced_blocks=100000,
        sync_duration=3600000000000,  # 1 hour in nanoseconds
    )


@pytest.fixture
def sample_peers(make_timestamp):
    return [
        Peer(
            address="127.0.0.1:9981",
            inbound=False,
            version="1.5.4",
            first_seen=make_timestamp,
            connected_since=make_timestamp,
            synced_blocks=100000,
            sync_duration=3600000000000,
        ),
        Peer(
            address="127.0.0.1:9982",
            inbound=True,
            version="1.5.4",
            first_seen=make_timestamp,
            connected_since=make_timestamp,
            synced_blocks=90000,
            sync_duration=1800000000000,
        ),
    ]


class TestSyncerQueries(BaseHostdTest):
    @pytest.fixture
    def syncer_queries(self):
        return SyncerQueries()

    async def test_get_syncer_address(self, syncer_queries, mock_client, sample_address):
        mock_client.get_syncer_address.return_value = sample_address
        mock_info = self.create_mock_info(mock_client, str)

        result = await syncer_queries.syncer_address(info=mock_info)

        assert isinstance(result, str)
        assert result == sample_address
        mock_client.get_syncer_address.assert_called_once()

    async def test_get_syncer_peers(self, syncer_queries, mock_client, sample_peers):
        mock_client.get_syncer_peers.return_value = sample_peers
        mock_info = self.create_mock_info(mock_client, List[Peer])

        result = await syncer_queries.syncer_peers(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Peer)
        assert result[0].address == sample_peers[0].address
        assert result[0].inbound == sample_peers[0].inbound
        assert result[0].version == sample_peers[0].version
        assert result[0].synced_blocks == sample_peers[0].synced_blocks
        mock_client.get_syncer_peers.assert_called_once()

    async def test_get_syncer_peers_empty(self, syncer_queries, mock_client):
        mock_client.get_syncer_peers.return_value = []
        mock_info = self.create_mock_info(mock_client, List[Peer])

        result = await syncer_queries.syncer_peers(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 0
        mock_client.get_syncer_peers.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (None, SortInput(field="syncedBlocks", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_syncer_peers_with_filters(
        self, syncer_queries, mock_client, sample_peers, filter_input, sort_input, pagination_input
    ):
        mock_client.get_syncer_peers.return_value = sample_peers
        mock_info = self.create_mock_info(mock_client, List[Peer])

        result = await syncer_queries.syncer_peers(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Peer)
        mock_client.get_syncer_peers.assert_called_once()


class TestSyncerMutations(BaseHostdTest):
    @pytest.fixture
    def syncer_mutations(self):
        return SyncerMutations()

    @pytest.fixture
    def sample_address(self):
        return "127.0.0.1:9981"

    async def test_connect_peer(self, syncer_mutations, mock_client, sample_address):
        mock_client.put_syncer_peer.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await syncer_mutations.connect_peer(info=mock_info, address=sample_address)

        assert result is True
        mock_client.put_syncer_peer.assert_called_once_with(address=sample_address)

    async def test_connect_peer_invalid_address(self, syncer_mutations, mock_client):
        mock_client.put_syncer_peer.side_effect = Exception("Invalid peer address")
        mock_info = self.create_mock_info(mock_client, bool)

        with pytest.raises(Exception):
            await syncer_mutations.connect_peer(info=mock_info, address="invalid:address")
