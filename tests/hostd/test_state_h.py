# tests/hostd/test_state.py
import pytest
from typing import Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.state import StateQueries
from siaql.graphql.schemas.types import HostdState, Announcement, ChainIndex, BlockID, PublicKey, ExplorerState, Address
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestStateQueries(BaseHostdTest):
    @pytest.fixture
    def state_queries(self):
        return StateQueries()

    @pytest.fixture
    def sample_announcement(self, make_timestamp):
        return Announcement(
            index=ChainIndex(
                height=100000, id=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
            ),
            address="test.host:9981",
        )

    @pytest.fixture
    def sample_hostd_state(self, make_timestamp, sample_announcement):
        return HostdState(
            name="test-host",
            public_key=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            last_announcement=sample_announcement,
            start_time=make_timestamp,
            explorer=ExplorerState(enabled=True, url="https://explorer.sia.tech"),
            # Include BuildState fields
            version="1.0.0",
            commit="abcdef123456",
            os="linux",
            build_time=make_timestamp,
        )

    async def test_get_state(self, state_queries, mock_client, sample_hostd_state):
        mock_client.get_state.return_value = sample_hostd_state
        mock_info = self.create_mock_info(mock_client, HostdState)

        result = await state_queries.state(info=mock_info)

        assert isinstance(result, HostdState)
        assert result.name == sample_hostd_state.name
        assert result.public_key == sample_hostd_state.public_key
        assert result.version == sample_hostd_state.version
        assert result.commit == sample_hostd_state.commit
        assert result.os == sample_hostd_state.os
        assert result.build_time == sample_hostd_state.build_time
        assert result.start_time == sample_hostd_state.start_time
        assert result.explorer.enabled == sample_hostd_state.explorer.enabled
        assert result.explorer.url == sample_hostd_state.explorer.url
        assert isinstance(result.last_announcement, Announcement)
        assert result.last_announcement.address == sample_hostd_state.last_announcement.address
        mock_client.get_state.assert_called_once()

    async def test_get_state_empty(self, state_queries, mock_client):
        mock_client.get_state.return_value = None
        mock_info = self.create_mock_info(mock_client, HostdState)

        result = await state_queries.state(info=mock_info)

        assert result is None
        mock_client.get_state.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="name", operator=FilterOperator.EQ, value="test-host"), None, None),
            (None, SortInput(field="buildTime", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_state_with_filters(
        self, state_queries, mock_client, sample_hostd_state, filter_input, sort_input, pagination_input
    ):
        mock_client.get_state.return_value = sample_hostd_state
        mock_info = self.create_mock_info(mock_client, HostdState)

        result = await state_queries.state(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, HostdState)
        assert result.name == sample_hostd_state.name
        assert result.public_key == sample_hostd_state.public_key
        assert result.version == sample_hostd_state.version
        mock_client.get_state.assert_called_once()
