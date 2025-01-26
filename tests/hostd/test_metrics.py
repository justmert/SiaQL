# tests/hostd/test_metrics.py
import pytest
from typing import List
from datetime import datetime, timezone
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.metrics import MetricsQueries
from siaql.graphql.schemas.types import (
    Metrics,
    MetricsInterval,
    Revenue,
    RHPData,
    DataMetrics,
    Contracts,
    Accounts,
    Pricing,
    Registry,
    Storage,
    RevenueMetrics,
    WalletMetrics,
    Currency,
)
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestMetricsQueries(BaseHostdTest):
    @pytest.fixture
    def metrics_queries(self):
        return MetricsQueries()

    @pytest.fixture
    def sample_metrics(self, make_timestamp):
        return Metrics(
            accounts=Accounts(active=100, balance=Currency("1000000")),
            revenue=RevenueMetrics(
                potential=Revenue(
                    rpc=Currency("100000"),
                    storage=Currency("500000"),
                    ingress=Currency("200000"),
                    egress=Currency("200000"),
                    registry_read=Currency("50000"),
                    registry_write=Currency("50000"),
                ),
                earned=Revenue(
                    rpc=Currency("80000"),
                    storage=Currency("400000"),
                    ingress=Currency("150000"),
                    egress=Currency("150000"),
                    registry_read=Currency("40000"),
                    registry_write=Currency("40000"),
                ),
            ),
            pricing=Pricing(
                contract_price=Currency("100000"),
                ingress_price=Currency("1000"),
                egress_price=Currency("1000"),
                base_rpc_price=Currency("100"),
                sector_access_price=Currency("1000"),
                storage_price=Currency("2000"),
                collateral_multiplier=1.5,
            ),
            contracts=Contracts(
                active=50,
                rejected=5,
                failed=2,
                renewed=10,
                successful=33,
                locked_collateral=Currency("5000000"),
                risked_collateral=Currency("2500000"),
            ),
            storage=Storage(
                total_sectors=1000,
                physical_sectors=900,
                lost_sectors=10,
                contract_sectors=800,
                temp_sectors=100,
                reads=5000,
                writes=2000,
                sector_cache_hits=4000,
                sector_cache_misses=1000,
            ),
            registry=Registry(entries=200, max_entries=1000, reads=1500, writes=500),
            data=DataMetrics(rhp=RHPData(ingress=1000000, egress=500000)),
            wallet=WalletMetrics(balance=Currency("10000000"), immature_balance=Currency("1000000")),
            timestamp=make_timestamp,
        )

    async def test_get_metrics(self, metrics_queries, mock_client, sample_metrics, make_timestamp):
        mock_client.get_metrics.return_value = sample_metrics
        mock_info = self.create_mock_info(mock_client, Metrics)

        result = await metrics_queries.metrics(info=mock_info, timestamp=make_timestamp)

        assert isinstance(result, Metrics)
        assert result.accounts.active == sample_metrics.accounts.active
        assert result.accounts.balance == sample_metrics.accounts.balance
        assert result.revenue.potential.rpc == sample_metrics.revenue.potential.rpc
        assert result.revenue.earned.storage == sample_metrics.revenue.earned.storage
        assert result.contracts.active == sample_metrics.contracts.active
        assert result.storage.total_sectors == sample_metrics.storage.total_sectors
        assert result.wallet.balance == sample_metrics.wallet.balance
        mock_client.get_metrics.assert_called_once_with(timestamp=make_timestamp)

    async def test_get_metrics_empty(self, metrics_queries, mock_client, make_timestamp):
        mock_client.get_metrics.return_value = None
        mock_info = self.create_mock_info(mock_client, Metrics)

        result = await metrics_queries.metrics(info=mock_info, timestamp=make_timestamp)

        assert result is None
        mock_client.get_metrics.assert_called_once_with(timestamp=make_timestamp)

    async def test_get_period_metrics(self, metrics_queries, mock_client, sample_metrics, make_timestamp):
        mock_client.get_period_metrics.return_value = [sample_metrics]
        mock_info = self.create_mock_info(mock_client, List[Metrics])

        result = await metrics_queries.period_metrics(
            info=mock_info, start=make_timestamp, periods=1, interval=MetricsInterval.HOURLY
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Metrics)
        assert result[0].accounts.active == sample_metrics.accounts.active
        mock_client.get_period_metrics.assert_called_once_with(
            start=make_timestamp, periods=1, interval=MetricsInterval.HOURLY
        )

    @pytest.mark.parametrize(
        "interval",
        [
            MetricsInterval.FIVE_MINUTES,
            MetricsInterval.FIFTEEN_MINUTES,
            MetricsInterval.HOURLY,
            MetricsInterval.DAILY,
            MetricsInterval.WEEKLY,
            MetricsInterval.MONTHLY,
            MetricsInterval.YEARLY,
        ],
    )
    async def test_get_period_metrics_different_intervals(
        self, metrics_queries, mock_client, sample_metrics, make_timestamp, interval
    ):
        mock_client.get_period_metrics.return_value = [sample_metrics]
        mock_info = self.create_mock_info(mock_client, List[Metrics])

        result = await metrics_queries.period_metrics(
            info=mock_info, start=make_timestamp, periods=1, interval=interval
        )

        assert isinstance(result, list)
        assert len(result) == 1
        mock_client.get_period_metrics.assert_called_once_with(start=make_timestamp, periods=1, interval=interval)

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="accounts.active", operator=FilterOperator.GTE, value=50), None, None),
            (None, SortInput(field="timestamp", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_metrics_with_filters(
        self, metrics_queries, mock_client, sample_metrics, make_timestamp, filter_input, sort_input, pagination_input
    ):
        mock_client.get_metrics.return_value = sample_metrics
        mock_info = self.create_mock_info(mock_client, Metrics)

        result = await metrics_queries.metrics(
            info=mock_info, timestamp=make_timestamp, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, Metrics)
        assert result.accounts.active == sample_metrics.accounts.active
        mock_client.get_metrics.assert_called_once_with(timestamp=make_timestamp)
