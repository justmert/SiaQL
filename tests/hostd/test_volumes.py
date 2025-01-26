# tests/hostd/test_volumes.py
import pytest
from typing import List, Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.volumes import VolumeQueries, VolumeMutations
from siaql.graphql.schemas.types import Volume, VolumeMeta, AddVolumeRequest, UpdateVolumeRequest, ResizeVolumeRequest
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


@pytest.fixture
def sample_volume_meta():
    return VolumeMeta(
        id=1,
        local_path="/test/volume/path",
        used_sectors=1000,
        total_sectors=10000,
        read_only=False,
        available=True,
        failed_reads=0,
        failed_writes=0,
        successful_reads=1000,
        successful_writes=500,
        status="ready",
        errors=[],
    )


@pytest.fixture
def sample_volumes():
    return [
        VolumeMeta(
            id=1,
            local_path="/test/volume/path1",
            used_sectors=1000,
            total_sectors=10000,
            read_only=False,
            available=True,
            failed_reads=0,
            failed_writes=0,
            successful_reads=1000,
            successful_writes=500,
            status="ready",
            errors=[],
        ),
        VolumeMeta(
            id=2,
            local_path="/test/volume/path2",
            used_sectors=2000,
            total_sectors=10000,
            read_only=True,
            available=True,
            failed_reads=5,
            failed_writes=2,
            successful_reads=2000,
            successful_writes=1000,
            status="ready",
            errors=[],
        ),
    ]


class TestVolumeQueries(BaseHostdTest):
    @pytest.fixture
    def volume_queries(self):
        return VolumeQueries()

    async def test_get_volumes(self, volume_queries, mock_client, sample_volumes):
        mock_client.get_volumes.return_value = sample_volumes
        mock_info = self.create_mock_info(mock_client, List[VolumeMeta])

        result = await volume_queries.volumes(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], VolumeMeta)
        assert result[0].id == sample_volumes[0].id
        assert result[0].local_path == sample_volumes[0].local_path
        assert result[0].status == sample_volumes[0].status
        mock_client.get_volumes.assert_called_once()

    async def test_get_volume(self, volume_queries, mock_client, sample_volume_meta):
        mock_client.get_volume.return_value = sample_volume_meta
        mock_info = self.create_mock_info(mock_client, VolumeMeta)

        result = await volume_queries.volume(info=mock_info, id=1)

        assert isinstance(result, VolumeMeta)
        assert result.id == sample_volume_meta.id
        assert result.local_path == sample_volume_meta.local_path
        assert result.status == sample_volume_meta.status
        mock_client.get_volume.assert_called_once_with(id=1)

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="usedSectors", operator=FilterOperator.LTE, value=1000), None, None),
        ],
    )
    async def test_get_volumes_with_filters(
        self, volume_queries, mock_client, sample_volumes, filter_input, sort_input, pagination_input
    ):
        mock_client.get_volumes.return_value = sample_volumes
        mock_info = self.create_mock_info(mock_client, List[VolumeMeta])

        result = await volume_queries.volumes(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, list)
        assert len(result) == 1
        mock_client.get_volumes.assert_called_once()


class TestVolumeMutations(BaseHostdTest):
    @pytest.fixture
    def volume_mutations(self):
        return VolumeMutations()

    @pytest.fixture
    def sample_add_volume_request(self):
        return AddVolumeRequest(local_path="/test/new/volume", max_sectors=10000)

    @pytest.fixture
    def sample_update_volume_request(self):
        return UpdateVolumeRequest(read_only=True)

    @pytest.fixture
    def sample_resize_volume_request(self):
        return ResizeVolumeRequest(max_sectors=20000)

    async def test_add_volume(self, volume_mutations, mock_client, sample_add_volume_request, sample_volume_meta):
        mock_client.post_volume.return_value = sample_volume_meta
        mock_info = self.create_mock_info(mock_client, Volume)

        result = await volume_mutations.add_volume(info=mock_info, req=sample_add_volume_request)

        assert isinstance(result, Volume)
        assert result.local_path == sample_volume_meta.local_path
        assert result.total_sectors == sample_volume_meta.total_sectors
        mock_client.post_volume.assert_called_once_with(req=sample_add_volume_request)

    async def test_update_volume(self, volume_mutations, mock_client, sample_update_volume_request):
        mock_client.put_volume.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await volume_mutations.update_volume(info=mock_info, id=1, req=sample_update_volume_request)

        assert result is True
        mock_client.put_volume.assert_called_once_with(id=1, req=sample_update_volume_request)

    async def test_delete_volume(self, volume_mutations, mock_client):
        mock_client.delete_volume.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await volume_mutations.delete_volume(info=mock_info, id=1, force=True)

        assert result is True
        mock_client.delete_volume.assert_called_once_with(id=1, force=True)

    async def test_resize_volume(self, volume_mutations, mock_client, sample_resize_volume_request):
        mock_client.put_volume_resize.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await volume_mutations.resize_volume(info=mock_info, id=1, req=sample_resize_volume_request)

        assert result is True
        mock_client.put_volume_resize.assert_called_once_with(id=1, req=sample_resize_volume_request)

    async def test_cancel_volume_operation(self, volume_mutations, mock_client):
        mock_client.delete_volume_cancel_op.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await volume_mutations.cancel_volume_operation(info=mock_info, id=1)

        assert result is True
        mock_client.delete_volume_cancel_op.assert_called_once_with(id=1)

    async def test_add_volume_error(self, volume_mutations, mock_client, sample_add_volume_request):
        mock_client.post_volume.side_effect = Exception("Invalid volume path")
        mock_info = self.create_mock_info(mock_client, Volume)

        with pytest.raises(Exception):
            await volume_mutations.add_volume(info=mock_info, req=sample_add_volume_request)
