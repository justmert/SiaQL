# tests/walletd/test_state.py
import pytest
from datetime import datetime, timezone
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.state import StateQueries
from siaql.graphql.schemas.types import StateResponse, IndexMode


class TestStateQueries(BaseWalletdTest):
    @pytest.fixture
    def state_queries(self):
        return StateQueries()

    @pytest.fixture
    def sample_state_response(self):
        return StateResponse(
            version="1.0.0",
            commit="abc123",
            os="linux",
            build_time=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            start_time=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            index_mode=IndexMode.FULL,
        )

    async def test_get_state(self, state_queries, mock_client, sample_state_response):
        mock_client.get_state.return_value = sample_state_response
        mock_info = self.create_mock_info(mock_client, StateResponse)

        result = await state_queries.state(info=mock_info)

        assert isinstance(result, StateResponse)
        assert result.version == sample_state_response.version
        assert result.commit == sample_state_response.commit
        assert result.os == sample_state_response.os
        assert result.build_time == sample_state_response.build_time
        assert result.start_time == sample_state_response.start_time
        assert result.index_mode == sample_state_response.index_mode

        mock_client.get_state.assert_called_once()

    @pytest.mark.parametrize("index_mode", [IndexMode.PERSONAL, IndexMode.FULL, IndexMode.NONE])
    async def test_get_state_different_modes(self, state_queries, mock_client, sample_state_response, index_mode):
        sample_state_response.index_mode = index_mode
        mock_client.get_state.return_value = sample_state_response
        mock_info = self.create_mock_info(mock_client, StateResponse)

        result = await state_queries.state(info=mock_info)

        assert isinstance(result, StateResponse)
        assert result.index_mode == index_mode
        mock_client.get_state.assert_called_once()
