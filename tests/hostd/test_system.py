# tests/hostd/test_system.py
import pytest
from typing import List, Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.system import SystemQueries, SystemMutations
from siaql.graphql.schemas.types import SystemDirResponse
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestSystemQueries(BaseHostdTest):
    @pytest.fixture
    def system_queries(self):
        return SystemQueries()

    @pytest.fixture
    def sample_dir_response(self):
        return SystemDirResponse(
            path="/test/path", total_bytes=1000000, free_bytes=500000, directories=["dir1", "dir2", "dir3"]
        )

    async def test_get_system_dir(self, system_queries, mock_client, sample_dir_response):
        mock_client.get_system_dir.return_value = sample_dir_response
        mock_info = self.create_mock_info(mock_client, SystemDirResponse)
        path = "/test/path"

        result = await system_queries.system_dir(info=mock_info, path=path)

        assert isinstance(result, SystemDirResponse)
        assert result.path == sample_dir_response.path
        assert result.total_bytes == sample_dir_response.total_bytes
        assert result.free_bytes == sample_dir_response.free_bytes
        assert result.directories == sample_dir_response.directories
        mock_client.get_system_dir.assert_called_once_with(path=path)

    async def test_get_system_dir_empty(self, system_queries, mock_client):
        mock_client.get_system_dir.return_value = None
        mock_info = self.create_mock_info(mock_client, SystemDirResponse)
        path = "/nonexistent/path"

        result = await system_queries.system_dir(info=mock_info, path=path)

        assert result is None
        mock_client.get_system_dir.assert_called_once_with(path=path)

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="totalBytes", operator=FilterOperator.GTE, value=1000000), None, None),
            (None, SortInput(field="path", direction=SortDirection.ASC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_system_dir_with_filters(
        self, system_queries, mock_client, sample_dir_response, filter_input, sort_input, pagination_input
    ):
        mock_client.get_system_dir.return_value = sample_dir_response
        mock_info = self.create_mock_info(mock_client, SystemDirResponse)
        path = "/test/path"

        result = await system_queries.system_dir(
            info=mock_info, path=path, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, SystemDirResponse)
        assert result.path == sample_dir_response.path
        mock_client.get_system_dir.assert_called_once_with(path=path)


class TestSystemMutations(BaseHostdTest):
    @pytest.fixture
    def system_mutations(self):
        return SystemMutations()

    async def test_create_dir(self, system_mutations, mock_client):
        mock_client.put_system_dir.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)
        path = "/test/new/path"

        result = await system_mutations.create_dir(info=mock_info, path=path)

        assert result is True
        mock_client.put_system_dir.assert_called_once_with(path=path)

    async def test_backup_sqlite3(self, system_mutations, mock_client):
        mock_client.post_system_sqlite3_backup.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)
        path = "/test/backup/path"

        result = await system_mutations.backup_sqlite3(info=mock_info, path=path)

        assert result is True
        mock_client.post_system_sqlite3_backup.assert_called_once_with(path=path)

    async def test_create_dir_error(self, system_mutations, mock_client):
        mock_client.put_system_dir.side_effect = Exception("Permission denied")
        mock_info = self.create_mock_info(mock_client, bool)
        path = "/protected/path"

        with pytest.raises(Exception):
            await system_mutations.create_dir(info=mock_info, path=path)

    async def test_backup_sqlite3_error(self, system_mutations, mock_client):
        mock_client.post_system_sqlite3_backup.side_effect = Exception("Backup failed")
        mock_info = self.create_mock_info(mock_client, bool)
        path = "/invalid/backup/path"

        with pytest.raises(Exception):
            await system_mutations.backup_sqlite3(info=mock_info, path=path)
