# tests/walletd/test_events.py
import pytest
from datetime import datetime, timezone
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.events import EventQueries
from siaql.graphql.schemas.types import WalletEvent, ChainIndex, BlockID, Hash256, Address


class TestEventQueries(BaseWalletdTest):
    @pytest.fixture
    def event_queries(self):
        return EventQueries()

    @pytest.fixture
    def sample_event(self):
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

    async def test_get_event(self, event_queries, mock_client, sample_event):
        mock_client.get_event.return_value = sample_event
        mock_info = self.create_mock_info(mock_client, WalletEvent)

        result = await event_queries.event(info=mock_info, event_id=sample_event.id)

        assert isinstance(result, WalletEvent)
        assert result.id == sample_event.id
        assert result.type == sample_event.type
        assert result.maturity_height == sample_event.maturity_height
        assert result.timestamp == sample_event.timestamp
        assert result.relevant == sample_event.relevant

        mock_client.get_event.assert_called_once_with(event_id=sample_event.id)

    async def test_get_event_not_found(self, event_queries, mock_client):
        mock_client.get_event.return_value = None
        mock_info = self.create_mock_info(mock_client, WalletEvent)
        event_id = Hash256("0000000000000000000000000000000000000000000000000000000000000000")

        result = await event_queries.event(info=mock_info, event_id=event_id)

        assert result is None
        mock_client.get_event.assert_called_once_with(event_id=event_id)
