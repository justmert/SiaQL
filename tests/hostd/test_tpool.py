# tests/hostd/test_tpool.py
import pytest
from typing import Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.tpool import TPoolQueries
from siaql.graphql.schemas.types import Currency
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestTPoolQueries(BaseHostdTest):
    @pytest.fixture
    def tpool_queries(self):
        return TPoolQueries()

    @pytest.fixture
    def sample_fee(self):
        return Currency("1000000")  # Example transaction fee

    async def test_get_tpool_fee(self, tpool_queries, mock_client, sample_fee):
        mock_client.get_tpool_fee.return_value = sample_fee
        mock_info = self.create_mock_info(mock_client, Currency)

        result = await tpool_queries.tpool_fee(info=mock_info)
        assert result == sample_fee
        mock_client.get_tpool_fee.assert_called_once()

    async def test_get_tpool_fee_zero(self, tpool_queries, mock_client):
        zero_fee = Currency("0")
        mock_client.get_tpool_fee.return_value = zero_fee
        mock_info = self.create_mock_info(mock_client, Currency)

        result = await tpool_queries.tpool_fee(info=mock_info)

        assert result == zero_fee
        mock_client.get_tpool_fee.assert_called_once()

    async def test_get_tpool_fee_empty(self, tpool_queries, mock_client):
        mock_client.get_tpool_fee.return_value = None
        mock_info = self.create_mock_info(mock_client, Currency)

        result = await tpool_queries.tpool_fee(info=mock_info)

        assert result is None
        mock_client.get_tpool_fee.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="value", operator=FilterOperator.GTE, value="1000"), None, None),
            (None, SortInput(field="value", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_tpool_fee_with_filters(
        self, tpool_queries, mock_client, sample_fee, filter_input, sort_input, pagination_input
    ):
        mock_client.get_tpool_fee.return_value = sample_fee
        mock_info = self.create_mock_info(mock_client, Currency)

        result = await tpool_queries.tpool_fee(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert result == sample_fee
        mock_client.get_tpool_fee.assert_called_once()

    async def test_get_tpool_fee_large_value(self, tpool_queries, mock_client):
        large_fee = Currency("1" + "0" * 24)  # 1 Siacoin (10^24 Hastings)
        mock_client.get_tpool_fee.return_value = large_fee
        mock_info = self.create_mock_info(mock_client, Currency)

        result = await tpool_queries.tpool_fee(info=mock_info)

        assert result == large_fee
        mock_client.get_tpool_fee.assert_called_once()

    async def test_get_tpool_fee_error(self, tpool_queries, mock_client):
        mock_client.get_tpool_fee.side_effect = Exception("Failed to get transaction pool fee")
        mock_info = self.create_mock_info(mock_client, Currency)

        with pytest.raises(Exception):
            await tpool_queries.tpool_fee(info=mock_info)
