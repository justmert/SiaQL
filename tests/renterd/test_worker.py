# tests/renterd/test_worker.py
import pytest
from typing import List, Optional
from tests.conftest import BaseRenterdTest
from siaql.graphql.schemas.renterd.worker import WorkerQueries, WorkerMutations
from siaql.graphql.schemas.types import (
    Account,
    ContractsResponse,
    DownloadStatsResponse,
    GetObjectOptions,
    GetObjectResponse,
    HeadObjectOptions,
    HeadObjectResponse,
    HostPriceTable,
    MemoryResponse,
    MigrateSlabResponse,
    MultipartAbortRequest,
    MultipartAddPartRequest,
    MultipartCompleteRequest,
    MultipartCompleteResponse,
    MultipartCreateRequest,
    MultipartCreateResponse,
    RHPPriceTableRequest,
    RHPScanRequest,
    RHPScanResponse,
    Slab,
    UploadObjectOptions,
    UploadObjectResponse,
    UploadStatsResponse,
    WebhookEvent,
    WorkerStateResponse,
    PublicKey,
    Hash256,
    FileContractID,
    Currency,
    Contract,
)
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestWorkerQueries(BaseRenterdTest):
    @pytest.fixture
    def worker_queries(self):
        return WorkerQueries()

    @pytest.fixture
    def sample_worker_state(self, make_timestamp):
        return WorkerStateResponse(
            id="worker-1",
            start_time=make_timestamp,
            version="1.0.0",
            commit="abcdef123456",
            os="linux",
            build_time=make_timestamp,
        )

    @pytest.fixture
    def sample_memory_response(self):
        return MemoryResponse(
            download={"available": 1000000000, "total": 2000000000},
            upload={"available": 1500000000, "total": 2000000000},
        )

    @pytest.fixture
    def sample_account(self):
        return Account(
            id=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            clean_shutdown=True,
            balance=Currency("1000000"),
            host_key=PublicKey("ed25519:abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678"),
            drift=0,
            owner="worker-1",
            requires_sync=False,
        )

    @pytest.fixture
    def sample_download_stats(self):
        return DownloadStatsResponse(
            avg_download_speed_mbps=10.5,
            avg_overdrive_pct=20.0,
            healthy_downloaders=5,
            num_downloaders=6,
            downloaders_stats=[
                {
                    "avgSectorDownloadSpeedMbps": 10.5,
                    "hostKey": "ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    "numDownloads": 100,
                }
            ],
        )

    @pytest.fixture
    def sample_upload_stats(self):
        return UploadStatsResponse(
            avg_slab_upload_speed_mbps=8.5,
            avg_overdrive_pct=15.0,
            healthy_uploaders=4,
            num_uploaders=5,
            uploaders_stats=[
                {
                    "avgSectorUploadSpeedMbps": 8.5,
                    "hostKey": "ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                }
            ],
        )

    async def test_worker_state(self, worker_queries, mock_client, sample_worker_state):
        mock_client.get_worker_state.return_value = sample_worker_state
        mock_info = self.create_mock_info(mock_client, WorkerStateResponse)

        result = await worker_queries.worker_state(info=mock_info)

        assert isinstance(result, WorkerStateResponse)
        assert result.id == sample_worker_state.id
        assert result.version == sample_worker_state.version
        assert result.start_time == sample_worker_state.start_time
        mock_client.get_worker_state.assert_called_once()

    async def test_worker_memory(self, worker_queries, mock_client, sample_memory_response):
        mock_client.get_worker_memory.return_value = sample_memory_response
        mock_info = self.create_mock_info(mock_client, MemoryResponse)

        result = await worker_queries.worker_memory(info=mock_info)

        assert isinstance(result, MemoryResponse)
        assert result.download["available"] == sample_memory_response.download["available"]
        assert result.upload["available"] == sample_memory_response.upload["available"]
        mock_client.get_worker_memory.assert_called_once()

    async def test_worker_id(self, worker_queries, mock_client):
        worker_id = "worker-1"
        mock_client.get_worker_id.return_value = worker_id
        mock_info = self.create_mock_info(mock_client, str)

        result = await worker_queries.worker_id(info=mock_info)

        assert isinstance(result, str)
        assert result == worker_id
        mock_client.get_worker_id.assert_called_once()

    async def test_worker_accounts(self, worker_queries, mock_client, sample_account):
        mock_client.get_worker_accounts.return_value = [sample_account]
        mock_info = self.create_mock_info(mock_client, List[Account])

        result = await worker_queries.worker_accounts(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Account)
        assert result[0].id == sample_account.id
        assert result[0].balance == sample_account.balance
        mock_client.get_worker_accounts.assert_called_once()

    async def test_download_stats(self, worker_queries, mock_client, sample_download_stats):
        mock_client.get_worker_downloads_stats.return_value = sample_download_stats
        mock_info = self.create_mock_info(mock_client, DownloadStatsResponse)

        result = await worker_queries.download_stats(info=mock_info)

        assert isinstance(result, DownloadStatsResponse)
        assert result.avg_download_speed_mbps == sample_download_stats.avg_download_speed_mbps
        assert result.healthy_downloaders == sample_download_stats.healthy_downloaders
        mock_client.get_worker_downloads_stats.assert_called_once()

    async def test_upload_stats(self, worker_queries, mock_client, sample_upload_stats):
        mock_client.get_worker_uploads_stats.return_value = sample_upload_stats
        mock_info = self.create_mock_info(mock_client, UploadStatsResponse)

        result = await worker_queries.upload_stats(info=mock_info)

        assert isinstance(result, UploadStatsResponse)
        assert result.avg_slab_upload_speed_mbps == sample_upload_stats.avg_slab_upload_speed_mbps
        assert result.healthy_uploaders == sample_upload_stats.healthy_uploaders
        mock_client.get_worker_uploads_stats.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="id", operator=FilterOperator.EQ, value="worker-1"), None, None),
            (None, SortInput(field="startTime", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_worker_state_with_filters(
        self, worker_queries, mock_client, sample_worker_state, filter_input, sort_input, pagination_input
    ):
        mock_client.get_worker_state.return_value = sample_worker_state
        mock_info = self.create_mock_info(mock_client, WorkerStateResponse)

        result = await worker_queries.worker_state(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, WorkerStateResponse)
        assert result.id == sample_worker_state.id
        mock_client.get_worker_state.assert_called_once()


class TestWorkerMutations(BaseRenterdTest):
    @pytest.fixture
    def worker_mutations(self):
        return WorkerMutations()

    @pytest.fixture
    def sample_scan_request(self):
        return RHPScanRequest(
            host_key=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            host_ip="127.0.0.1",
            timeout=5000,  # milliseconds
        )

    @pytest.fixture
    def sample_scan_response(self):
        return RHPScanResponse(ping=100, scan_error=None, settings=None, price_table=None)

    async def test_rhp_scan(self, worker_mutations, mock_client, sample_scan_request, sample_scan_response):
        mock_client.rhp_scan.return_value = sample_scan_response
        mock_info = self.create_mock_info(mock_client, RHPScanResponse)

        result = await worker_mutations.rhp_scan(info=mock_info, req=sample_scan_request)

        assert isinstance(result, RHPScanResponse)
        assert result.ping == sample_scan_response.ping
        assert result.scan_error == sample_scan_response.scan_error
        mock_client.rhp_scan.assert_called_once_with(req=sample_scan_request)
