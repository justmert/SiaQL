# tests/renterd/test_bus.py
import pytest
from typing import List, Optional, Dict
from tests.conftest import BaseRenterdTest
from siaql.graphql.schemas.renterd.bus import BusQueries, BusMutations
from siaql.graphql.schemas.types import (
    Account,
    Alert,
    AlertsOpts,
    AlertsResponse,
    BusStateResponse,
    ConsensusState,
    ContractSpending,
    Network,
    ChainIndex,
    BlockID,
    Hash256,
    ContractMetadata,
    ContractPruneRequest,
    ContractPruneResponse,
    ContractSetUpdateRequest,
    ContractRenewRequest,
    ContractRenewedRequest,
    FileContractID,
    Currency,
    PublicKey,
    Address,
    ContractSpendingRecord,
    UpdateAllowlistRequest,
    UpdateBlocklistRequest,
    HostsPriceTablesRequest,
    HostsScanRequest,
    WalletResponse,
    Block,
    Transaction,
    TransactionID,
    SearchHostsRequest,
    ObjectMetadata,
    GougingParams,
    UploadParams,
    AddObjectRequest,
    CopyObjectsRequest,
    MultipartCreateRequest,
    MultipartCreateResponse,
    MultipartAbortRequest,
    MultipartCompleteRequest,
    MultipartCompleteResponse,
    MultipartAddPartRequest,
)
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


@pytest.fixture
def sample_state(make_timestamp):
    return BusStateResponse(
        version="1.0.0",
        commit="abcdef123456",
        os="linux",
        build_time=make_timestamp,
        start_time=make_timestamp,
        network="mainnet",
    )


@pytest.fixture
def sample_account():
    return Account(
        id=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
        clean_shutdown=True,
        balance=Currency("1000000"),
        host_key=PublicKey("ed25519:abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678"),
        drift=0,
        owner="bus-1",
        requires_sync=False,
    )


@pytest.fixture
def sample_alert(make_timestamp):
    return Alert(
        id=Hash256("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
        severity=2,  # WARNING
        message="Test alert",
        data={"key": "value"},
        timestamp=make_timestamp,
    )


@pytest.fixture
def sample_alerts_response(sample_alert):
    return AlertsResponse(
        alerts=[sample_alert], has_more=False, totals={"info": 1, "warning": 1, "error": 0, "critical": 0}
    )


@pytest.fixture
def sample_contract_metadata(make_timestamp):
    return ContractMetadata(
        id=FileContractID("fcid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
        host_ip="127.0.0.1:9981",
        host_key=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
        siamux_addr="127.0.0.1:9981",  # Added missing field
        proof_height=150000,
        revision_height=140000,
        revision_number=1,
        size=1000000,
        start_height=100000,
        state="active",
        window_start=145000,
        window_end=150000,
        contract_price=Currency("1000000"),
        renewed_from=None,  # Added missing field
        spending=ContractSpending(  # Added missing field
            downloads=Currency("100000"),
            uploads=Currency("200000"),
            fund_account=Currency("300000"),
            deletions=Currency("50000"),
            sector_roots=Currency("150000"),
        ),
        total_cost=Currency("5000000"),
        contract_sets=["default"],  # Added missing field
    )


class TestBusQueries(BaseRenterdTest):
    @pytest.fixture
    def bus_queries(self):
        return BusQueries()

    async def test_get_state(self, bus_queries, mock_client, sample_state):
        mock_client.get_state.return_value = sample_state
        mock_info = self.create_mock_info(mock_client, BusStateResponse)

        result = await bus_queries.get_state(info=mock_info)

        assert isinstance(result, BusStateResponse)
        assert result.version == sample_state.version
        assert result.network == sample_state.network
        mock_client.get_state.assert_called_once()

    async def test_get_accounts(self, bus_queries, mock_client, sample_account):
        mock_client.get_accounts.return_value = [sample_account]
        mock_info = self.create_mock_info(mock_client, List[Account])

        result = await bus_queries.accounts(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Account)
        assert result[0].id == sample_account.id
        assert result[0].balance == sample_account.balance
        mock_client.get_accounts.assert_called_once()

    async def test_get_alerts(self, bus_queries, mock_client, sample_alerts_response):
        mock_client.get_alerts.return_value = sample_alerts_response
        mock_info = self.create_mock_info(mock_client, AlertsResponse)
        opts = AlertsOpts(offset=0, limit=10, severity=2)

        result = await bus_queries.alerts(info=mock_info, opts=opts)

        assert isinstance(result, AlertsResponse)
        assert len(result.alerts) == 1
        assert isinstance(result.alerts[0], Alert)
        mock_client.get_alerts.assert_called_once_with(opts=opts)

    async def test_get_contracts(self, bus_queries, mock_client, sample_contract_metadata):
        mock_client.get_contracts.return_value = [sample_contract_metadata]
        mock_info = self.create_mock_info(mock_client, List[ContractMetadata])
        contract_set = "default"

        result = await bus_queries.contracts(info=mock_info, contract_set=contract_set)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ContractMetadata)
        assert result[0].id == sample_contract_metadata.id
        mock_client.get_contracts.assert_called_once_with(contract_set=contract_set)

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="balance", operator=FilterOperator.GTE, value="1000000"), None, None),
            (None, SortInput(field="id", direction=SortDirection.ASC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_accounts_with_filters(
        self, bus_queries, mock_client, sample_account, filter_input, sort_input, pagination_input
    ):
        mock_client.get_accounts.return_value = [sample_account]
        mock_info = self.create_mock_info(mock_client, List[Account])

        result = await bus_queries.accounts(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Account)
        mock_client.get_accounts.assert_called_once()


class TestBusMutations(BaseRenterdTest):
    @pytest.fixture
    def bus_mutations(self):
        return BusMutations()

    @pytest.fixture
    def sample_contract_spending_record(self):
        return ContractSpendingRecord(
            contract_id=FileContractID("fcid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            revision_number=1,
            size=1000000,
            missed_host_payout=Currency("1000000"),
            valid_renter_payout=Currency("5000000"),
            downloads=Currency("100000"),
            uploads=Currency("200000"),
            fund_account=Currency("300000"),
            deletions=Currency("50000"),
            sector_roots=Currency("150000"),
        )

    async def test_record_contract_spending(self, bus_mutations, mock_client, sample_contract_spending_record):
        mock_client.record_contract_spending.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await bus_mutations.record_contract_spending(info=mock_info, records=[sample_contract_spending_record])

        assert result is True
        mock_client.record_contract_spending.assert_called_once_with(records=[sample_contract_spending_record])

    async def test_update_hosts_allowlist(self, bus_mutations, mock_client):
        req = UpdateAllowlistRequest(
            add=[PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")],
            remove=[],
            clear=False,
        )
        mock_client.update_hosts_allowlist.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await bus_mutations.update_hosts_allowlist(info=mock_info, req=req)

        assert result is True
        mock_client.update_hosts_allowlist.assert_called_once_with(req=req)

    # Add more test cases for contract operations
    async def test_renew_contract(self, bus_mutations, mock_client, sample_contract_metadata):
        req = ContractRenewRequest(
            end_height=200000,
            expected_new_storage=1000000,
            max_fund_amount=Currency("10000000"),
            min_new_collateral=Currency("5000000"),
            renter_funds=Currency("8000000"),
        )
        mock_client.renew_contract.return_value = sample_contract_metadata
        mock_info = self.create_mock_info(mock_client, ContractMetadata)
        contract_id = FileContractID("fcid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")

        result = await bus_mutations.renew_contract(info=mock_info, id=contract_id, req=req)

        assert isinstance(result, ContractMetadata)
        assert result.id == sample_contract_metadata.id
        mock_client.renew_contract.assert_called_once_with(id=contract_id, req=req)

    async def test_delete_contract(self, bus_mutations, mock_client):
        contract_id = FileContractID("fcid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
        mock_client.delete_contract.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await bus_mutations.delete_contract(info=mock_info, id=contract_id)

        assert result is True
        mock_client.delete_contract.assert_called_once_with(id=contract_id)

    async def test_prune_contract(self, bus_mutations, mock_client):
        contract_id = FileContractID("fcid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
        req = ContractPruneRequest(timeout=5000)
        response = ContractPruneResponse(contract_size=1000000, pruned=500000, remaining=500000, error=None)
        mock_client.prune_contract.return_value = response
        mock_info = self.create_mock_info(mock_client, ContractPruneResponse)

        result = await bus_mutations.prune_contract(info=mock_info, id=contract_id, req=req)

        assert isinstance(result, ContractPruneResponse)
        assert result.contract_size == response.contract_size
        assert result.pruned == response.pruned
        mock_client.prune_contract.assert_called_once_with(id=contract_id, req=req)
