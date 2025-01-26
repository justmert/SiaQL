# tests/hostd/test_index.py
import pytest
from typing import Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.index import IndexQueries
from siaql.graphql.schemas.types import ChainIndex, BlockID
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestIndexQueries(BaseHostdTest):
    @pytest.fixture
    def index_queries(self):
        return IndexQueries()

    @pytest.fixture
    def sample_chain_index(self):
        return ChainIndex(
            height=123456, id=BlockID("block:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
        )

    async def test_get_index_tip(self, index_queries, mock_client, sample_chain_index):
        mock_client.get_index_tip.return_value = sample_chain_index
        mock_info = self.create_mock_info(mock_client, ChainIndex)

        result = await index_queries.index_tip(info=mock_info)

        assert isinstance(result, ChainIndex)
        assert result.height == sample_chain_index.height
        assert result.id == sample_chain_index.id
        mock_client.get_index_tip.assert_called_once()

    async def test_get_index_tip_empty(self, index_queries, mock_client):
        mock_client.get_index_tip.return_value = None
        mock_info = self.create_mock_info(mock_client, ChainIndex)

        result = await index_queries.index_tip(info=mock_info)

        assert result is None
        mock_client.get_index_tip.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="height", operator=FilterOperator.GTE, value=100000), None, None),
            (None, SortInput(field="height", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_index_tip_with_filters(
        self, index_queries, mock_client, sample_chain_index, filter_input, sort_input, pagination_input
    ):
        mock_client.get_index_tip.return_value = sample_chain_index
        mock_info = self.create_mock_info(mock_client, ChainIndex)

        result = await index_queries.index_tip(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, ChainIndex)
        assert result.height == sample_chain_index.height
        assert result.id == sample_chain_index.id
        mock_client.get_index_tip.assert_called_once()
