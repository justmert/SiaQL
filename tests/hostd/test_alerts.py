# tests/hostd/test_alerts.py
import pytest
from typing import List
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.alerts import AlertQueries, AlertMutations
from siaql.graphql.schemas.types import Alert, Hash256, Severity
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


@pytest.fixture
def sample_alerts(make_timestamp):
    return [
        Alert(
            id=Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            severity=Severity.WARNING,
            message="Test alert message",
            data={"key": "value"},
            timestamp=make_timestamp,
        ),
        Alert(
            id=Hash256("abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"),
            severity=Severity.WARNING,
            message="Another test alert",
            data={"key2": "value2"},
            timestamp=make_timestamp,
        ),
    ]


class TestAlertQueries(BaseHostdTest):
    @pytest.fixture
    def alert_queries(self):
        return AlertQueries()

    async def test_get_alerts(self, alert_queries, mock_client, sample_alerts):
        mock_client.get_alerts.return_value = sample_alerts
        mock_info = self.create_mock_info(mock_client, List[Alert])

        result = await alert_queries.alerts(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Alert)
        assert result[0].id == sample_alerts[0].id
        assert result[0].severity == sample_alerts[0].severity
        assert result[0].message == sample_alerts[0].message
        assert result[1].id == sample_alerts[1].id
        assert result[1].severity == sample_alerts[1].severity

        mock_client.get_alerts.assert_called_once()

    async def test_get_alerts_empty(self, alert_queries, mock_client):
        mock_client.get_alerts.return_value = []
        mock_info = self.create_mock_info(mock_client, List[Alert])

        result = await alert_queries.alerts(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 0
        mock_client.get_alerts.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input,sort_input,pagination_input",
        [
            (None, None, None),
            (None, SortInput(field="timestamp", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_alerts_with_filters(
        self, alert_queries, mock_client, sample_alerts, filter_input, sort_input, pagination_input
    ):
        mock_client.get_alerts.return_value = sample_alerts
        mock_info = self.create_mock_info(mock_client, List[Alert])

        result = await alert_queries.alerts(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, list)
        assert len(result) == 2
        mock_client.get_alerts.assert_called_once()


class TestAlertMutations(BaseHostdTest):
    @pytest.fixture
    def alert_mutations(self):
        return AlertMutations()

    async def test_dismiss_alerts(self, alert_mutations, mock_client):
        mock_client.post_alerts_dismiss.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)
        alert_ids = [
            Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            Hash256("abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"),
        ]

        result = await alert_mutations.dismiss_alerts(info=mock_info, ids=alert_ids)

        assert result is True
        mock_client.post_alerts_dismiss.assert_called_once_with(ids=alert_ids)

    async def test_dismiss_alerts_empty(self, alert_mutations, mock_client):
        mock_client.post_alerts_dismiss.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await alert_mutations.dismiss_alerts(info=mock_info, ids=[])

        assert result is True
        mock_client.post_alerts_dismiss.assert_called_once_with(ids=[])
