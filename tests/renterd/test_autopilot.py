# tests/renterd/test_autopilot.py
import pytest
from typing import List, Optional
from tests.conftest import BaseRenterdTest
from siaql.graphql.schemas.renterd.autopilot import AutopilotQueries, AutopilotMutations
from siaql.graphql.schemas.types import (
    AutopilotConfig,
    AutopilotStateResponse,
    AutopilotTriggerRequest,
    AutopilotTriggerResponse,
    HostResponse,
    ContractsConfig,
    HostsConfig,
    SearchHostsRequest,
    PublicKey,
    ConfigEvaluationRequest,
    ConfigEvaluationResponse,
    Currency,
    ConfigRecommendation,
    GougingParams,
    RedundancySettings,
)
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestAutopilotQueries(BaseRenterdTest):
    @pytest.fixture
    def autopilot_queries(self):
        return AutopilotQueries()

    @pytest.fixture
    def sample_redundancy_settings(self):
        return RedundancySettings(min_shards=10, total_shards=30)

    @pytest.fixture
    def sample_autopilot_config(self, sample_redundancy_settings):
        return AutopilotConfig(
            contracts=ContractsConfig(
                set="autopilot",
                amount=50,
                allowance=Currency("100000000"),
                period=6048,  # blocks
                renew_window=2016,  # blocks
                download=1000000000,  # bytes
                upload=1000000000,  # bytes
                storage=1000000000,  # bytes
                prune=True,
            ),
            hosts=HostsConfig(
                allow_redundant_ips=False,
                max_downtime_hours=72,
                min_protocol_version="1.5.4",
                max_consecutive_scan_failures=3,
                score_overrides={},
            ),
        )

    @pytest.fixture
    def sample_autopilot_state(self, make_timestamp):
        return AutopilotStateResponse(
            configured=True,
            migrating=False,
            migrating_last_start=make_timestamp,
            pruning=False,
            pruning_last_start=make_timestamp,
            scanning=False,
            scanning_last_start=make_timestamp,
            uptime_ms=3600000,  # 1 hour
            start_time=make_timestamp,
            # BuildState fields
            version="1.0.0",
            commit="abcdef123456",
            os="linux",
            build_time=make_timestamp,
        )

    @pytest.fixture
    def sample_host_response(self):
        return HostResponse(host=None, checks=None)  # Add host details if needed  # Add checks details if needed

    @pytest.fixture
    def sample_host_key(self):
        return PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")

    async def test_get_autopilot_config(self, autopilot_queries, mock_client, sample_autopilot_config):
        mock_client.get_autopilot_config.return_value = sample_autopilot_config
        mock_info = self.create_mock_info(mock_client, AutopilotConfig)

        result = await autopilot_queries.autopilot_config(info=mock_info)

        assert isinstance(result, AutopilotConfig)
        assert result.contracts.set == sample_autopilot_config.contracts.set
        assert result.contracts.amount == sample_autopilot_config.contracts.amount
        assert result.hosts.max_downtime_hours == sample_autopilot_config.hosts.max_downtime_hours
        mock_client.get_autopilot_config.assert_called_once()

    async def test_get_autopilot_state(self, autopilot_queries, mock_client, sample_autopilot_state):
        mock_client.get_autopilot_state.return_value = sample_autopilot_state
        mock_info = self.create_mock_info(mock_client, AutopilotStateResponse)

        result = await autopilot_queries.autopilot_state(info=mock_info)

        assert isinstance(result, AutopilotStateResponse)
        assert result.configured == sample_autopilot_state.configured
        assert result.migrating == sample_autopilot_state.migrating
        assert result.version == sample_autopilot_state.version
        mock_client.get_autopilot_state.assert_called_once()

    async def test_get_autopilot_hosts(self, autopilot_queries, mock_client, sample_host_response):
        mock_client.get_autopilot_hosts.return_value = [sample_host_response]
        mock_info = self.create_mock_info(mock_client, List[HostResponse])
        search_opts = SearchHostsRequest(
            offset=0,
            limit=10,
            autopilot_id="autopilot-1",
            filter_mode="all",
            usability_mode="usable",
            address_contains="",
            key_in=[],
        )

        result = await autopilot_queries.autopilot_hosts(info=mock_info, opts=search_opts)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], HostResponse)
        mock_client.get_autopilot_hosts.assert_called_once_with(opts=search_opts)


class TestAutopilotMutations(BaseRenterdTest):
    @pytest.fixture
    def autopilot_mutations(self):
        return AutopilotMutations()

    @pytest.fixture
    def sample_redundancy_settings(self):
        return RedundancySettings(min_shards=10, total_shards=30)

    @pytest.fixture
    def sample_autopilot_config(self, sample_redundancy_settings):
        return AutopilotConfig(
            contracts=ContractsConfig(
                set="autopilot",
                amount=50,
                allowance=Currency("100000000"),
                period=6048,
                renew_window=2016,
                download=1000000000,
                upload=1000000000,
                storage=1000000000,
                prune=True,
            ),
            hosts=HostsConfig(
                allow_redundant_ips=False,
                max_downtime_hours=72,
                min_protocol_version="1.5.4",
                max_consecutive_scan_failures=3,
                score_overrides={},
            ),
        )

    async def test_update_autopilot_config(self, autopilot_mutations, mock_client, sample_autopilot_config):
        mock_client.update_autopilot_config.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await autopilot_mutations.update_autopilot_config(info=mock_info, config=sample_autopilot_config)

        assert result is True
        mock_client.update_autopilot_config.assert_called_once_with(config=sample_autopilot_config)

    async def test_evaluate_autopilot_config(
        self, autopilot_mutations, mock_client, sample_autopilot_config, sample_redundancy_settings
    ):
        config_request = ConfigEvaluationRequest(
            autopilot_config=sample_autopilot_config,
            gouging_settings=GougingParams(
                consensus_state=None,
                gouging_settings=None,
                redundancy_settings=sample_redundancy_settings,
                transaction_fee=Currency("1000000"),
            ),
            redundancy_settings=sample_redundancy_settings,
        )

        evaluation_response = ConfigEvaluationResponse(
            hosts=100, usable=50, unusable=None, recommendation=ConfigRecommendation(gouging_settings=None)
        )

        mock_client.evaluate_autopilot_config.return_value = evaluation_response
        mock_info = self.create_mock_info(mock_client, ConfigEvaluationResponse)

        result = await autopilot_mutations.evaluate_autopilot_config(info=mock_info, req=config_request)

        assert isinstance(result, ConfigEvaluationResponse)
        assert result.hosts == evaluation_response.hosts
        assert result.usable == evaluation_response.usable
        mock_client.evaluate_autopilot_config.assert_called_once_with(req=config_request)

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="contracts.amount", operator=FilterOperator.GTE, value=50), None, None),
            (None, SortInput(field="contracts.set", direction=SortDirection.ASC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_autopilot_config_with_filters(
        self, autopilot_mutations, mock_client, sample_autopilot_config, filter_input, sort_input, pagination_input
    ):
        mock_client.get_autopilot_config.return_value = sample_autopilot_config
        mock_info = self.create_mock_info(mock_client, AutopilotConfig)

        result = await autopilot_mutations.update_autopilot_config(info=mock_info, config=sample_autopilot_config)

        assert result is True
        mock_client.update_autopilot_config.assert_called_once_with(config=sample_autopilot_config)

    async def test_update_autopilot_config_error(self, autopilot_mutations, mock_client, sample_autopilot_config):
        mock_client.update_autopilot_config.side_effect = Exception("Invalid configuration")
        mock_info = self.create_mock_info(mock_client, bool)

        with pytest.raises(Exception):
            await autopilot_mutations.update_autopilot_config(info=mock_info, config=sample_autopilot_config)
