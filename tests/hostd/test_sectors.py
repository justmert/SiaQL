# tests/hostd/test_sectors.py
import pytest
from typing import Optional, Dict
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.sectors import SectorQueries, SectorMutations
from siaql.graphql.schemas.types import VerifySectorResponse, Hash256
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestSectorQueries(BaseHostdTest):
    @pytest.fixture
    def sector_queries(self):
        return SectorQueries()

    @pytest.fixture
    def sample_verify_sector_response(self):
        return VerifySectorResponse(
            sector_ref={
                "contract_id": "fcid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                "sector_index": 1,
            },
            error=None,
        )

    @pytest.fixture
    def sample_root(self):
        return Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")

    async def test_verify_sector(self, sector_queries, mock_client, sample_verify_sector_response, sample_root):
        mock_client.get_verify_sector.return_value = sample_verify_sector_response
        mock_info = self.create_mock_info(mock_client, VerifySectorResponse)

        result = await sector_queries.verify_sector(info=mock_info, root=sample_root)

        assert isinstance(result, VerifySectorResponse)
        assert result.sector_ref == sample_verify_sector_response.sector_ref
        assert result.error == sample_verify_sector_response.error
        mock_client.get_verify_sector.assert_called_once_with(root=sample_root)

    async def test_verify_sector_with_error(self, sector_queries, mock_client, sample_root):
        error_response = VerifySectorResponse(sector_ref=None, error="Sector not found")
        mock_client.get_verify_sector.return_value = error_response
        mock_info = self.create_mock_info(mock_client, VerifySectorResponse)

        result = await sector_queries.verify_sector(info=mock_info, root=sample_root)

        assert isinstance(result, VerifySectorResponse)
        assert result.sector_ref is None
        assert result.error == "Sector not found"
        mock_client.get_verify_sector.assert_called_once_with(root=sample_root)

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="error", operator=FilterOperator.EQ, value=None), None, None),
            (None, SortInput(field="sectorRef.sectorIndex", direction=SortDirection.ASC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_verify_sector_with_filters(
        self,
        sector_queries,
        mock_client,
        sample_verify_sector_response,
        sample_root,
        filter_input,
        sort_input,
        pagination_input,
    ):
        mock_client.get_verify_sector.return_value = sample_verify_sector_response
        mock_info = self.create_mock_info(mock_client, VerifySectorResponse)

        result = await sector_queries.verify_sector(
            info=mock_info, root=sample_root, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, VerifySectorResponse)
        assert result.sector_ref == sample_verify_sector_response.sector_ref
        mock_client.get_verify_sector.assert_called_once_with(root=sample_root)


class TestSectorMutations(BaseHostdTest):
    @pytest.fixture
    def sector_mutations(self):
        return SectorMutations()

    @pytest.fixture
    def sample_root(self):
        return Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")

    async def test_delete_sector(self, sector_mutations, mock_client, sample_root):
        mock_client.delete_sector.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await sector_mutations.delete_sector(info=mock_info, root=sample_root)

        assert result is True
        mock_client.delete_sector.assert_called_once_with(root=sample_root)
