# tests/walletd/test_rescan.py
import pytest
from datetime import datetime, timezone
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.rescan import RescanQueries, RescanMutations
from siaql.graphql.schemas.types import RescanResponse, ChainIndex, BlockID


class TestRescanQueries(BaseWalletdTest):
    @pytest.fixture
    def rescan_queries(self):
        return RescanQueries()

    @pytest.fixture
    def sample_rescan_response(self):
        return RescanResponse(
            start_index=ChainIndex(
                height=1000, id=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
            ),
            index=ChainIndex(
                height=2000, id=BlockID("block:abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678")
            ),
            start_time=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            error=None,
        )

    async def test_get_rescan_status(self, rescan_queries, mock_client, sample_rescan_response):
        mock_client.get_rescan_status.return_value = sample_rescan_response
        mock_info = self.create_mock_info(mock_client, RescanResponse)

        result = await rescan_queries.rescan_status(info=mock_info)

        assert isinstance(result, RescanResponse)
        assert result.start_index.height == sample_rescan_response.start_index.height
        assert result.start_index.id == sample_rescan_response.start_index.id
        assert result.index.height == sample_rescan_response.index.height
        assert result.index.id == sample_rescan_response.index.id
        assert result.start_time == sample_rescan_response.start_time
        assert result.error == sample_rescan_response.error

        mock_client.get_rescan_status.assert_called_once()


class TestRescanMutations(BaseWalletdTest):
    @pytest.fixture
    def rescan_mutations(self):
        return RescanMutations()

    async def test_start_rescan(self, rescan_mutations, mock_client):
        mock_client.start_rescan.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)
        height = 100000

        result = await rescan_mutations.start_rescan(info=mock_info, height=height)

        assert result is True
        mock_client.start_rescan.assert_called_once_with(height=height)

    async def test_start_rescan_with_zero_height(self, rescan_mutations, mock_client):
        mock_client.start_rescan.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)
        height = 0

        result = await rescan_mutations.start_rescan(info=mock_info, height=height)

        assert result is True
        mock_client.start_rescan.assert_called_once_with(height=height)
