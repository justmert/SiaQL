# tests/hostd/test_settings.py
import pytest
from typing import Optional
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.settings import SettingsQueries, SettingsMutations
from siaql.graphql.schemas.types import HostSettings, PinnedSettings, Currency, DNSSettings, Pin, Duration
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


@pytest.fixture
def sample_host_settings():
    return HostSettings(
        accepting_contracts=True,
        net_address="test.host:9981",
        max_contract_duration=144 * 30 * 3,  # 3 months in blocks
        window_size=144 * 3,  # 3 days in blocks
        # Pricing
        contract_price=Currency("100000"),
        base_rpc_price=Currency("1000"),
        sector_access_price=Currency("1000"),
        collateral_multiplier=1.5,
        max_collateral=Currency("10000000"),
        storage_price=Currency("2000"),
        egress_price=Currency("1000"),
        ingress_price=Currency("1000"),
        price_table_validity=Duration(600000000000),  # 10 minutes
        # Registry
        max_registry_entries=1000,
        # RHP3
        account_expiry=Duration(86400000000000),  # 24 hours
        max_account_balance=Currency("1000000"),
        # Bandwidth
        ingress_limit=1000000,  # 1MB/s
        egress_limit=1000000,  # 1MB/s
        # DNS
        ddns=DNSSettings(
            provider="cloudflare", ipv4=True, ipv6=False, options={"token": "test-token", "zone_id": "test-zone"}
        ),
        sector_cache_size=1000,
        revision=1,
    )


@pytest.fixture
def sample_pinned_settings():
    return PinnedSettings(
        currency="USD",
        threshold=0.1,
        storage=Pin(pinned=True, value=2.0),
        ingress=Pin(pinned=True, value=0.1),
        egress=Pin(pinned=True, value=0.1),
        max_collateral=Pin(pinned=True, value=100.0),
    )


class TestSettingsQueries(BaseHostdTest):
    @pytest.fixture
    def settings_queries(self):
        return SettingsQueries()

    async def test_get_settings(self, settings_queries, mock_client, sample_host_settings):
        mock_client.get_settings.return_value = sample_host_settings
        mock_info = self.create_mock_info(mock_client, HostSettings)

        result = await settings_queries.settings(info=mock_info)

        assert isinstance(result, HostSettings)
        assert result.accepting_contracts == sample_host_settings.accepting_contracts
        assert result.net_address == sample_host_settings.net_address
        assert result.max_contract_duration == sample_host_settings.max_contract_duration
        assert result.contract_price == sample_host_settings.contract_price
        assert result.storage_price == sample_host_settings.storage_price
        assert result.ddns.provider == sample_host_settings.ddns.provider
        mock_client.get_settings.assert_called_once()

    async def test_get_pinned_settings(self, settings_queries, mock_client, sample_pinned_settings):
        mock_client.get_pinned_settings.return_value = sample_pinned_settings
        mock_info = self.create_mock_info(mock_client, PinnedSettings)

        result = await settings_queries.pinned_settings(info=mock_info)

        assert isinstance(result, PinnedSettings)
        assert result.currency == sample_pinned_settings.currency
        assert result.threshold == sample_pinned_settings.threshold
        assert result.storage.pinned == sample_pinned_settings.storage.pinned
        assert result.storage.value == sample_pinned_settings.storage.value
        mock_client.get_pinned_settings.assert_called_once()

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="accepting_contracts", operator=FilterOperator.EQ, value=True), None, None),
            (None, SortInput(field="revision", direction=SortDirection.DESC), None),
            (None, None, PaginationInput(offset=0, limit=10)),
        ],
    )
    async def test_get_settings_with_filters(
        self, settings_queries, mock_client, sample_host_settings, filter_input, sort_input, pagination_input
    ):
        mock_client.get_settings.return_value = sample_host_settings
        mock_info = self.create_mock_info(mock_client, HostSettings)

        result = await settings_queries.settings(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )

        assert isinstance(result, HostSettings)
        assert result.accepting_contracts == sample_host_settings.accepting_contracts
        mock_client.get_settings.assert_called_once()


class TestSettingsMutations(BaseHostdTest):
    @pytest.fixture
    def settings_mutations(self):
        return SettingsMutations()

    async def test_update_settings(self, settings_mutations, mock_client, sample_host_settings):
        mock_client.patch_settings.return_value = sample_host_settings
        mock_info = self.create_mock_info(mock_client, HostSettings)

        result = await settings_mutations.update_settings(info=mock_info, settings=sample_host_settings)

        assert isinstance(result, HostSettings)
        assert result.accepting_contracts == sample_host_settings.accepting_contracts
        assert result.net_address == sample_host_settings.net_address
        mock_client.patch_settings.assert_called_once_with(settings=sample_host_settings)

    async def test_update_pinned_settings(self, settings_mutations, mock_client, sample_pinned_settings):
        mock_client.put_pinned_settings.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await settings_mutations.update_pinned_settings(info=mock_info, settings=sample_pinned_settings)

        assert result is True
        mock_client.put_pinned_settings.assert_called_once_with(settings=sample_pinned_settings)

    async def test_announce(self, settings_mutations, mock_client):
        mock_client.post_announce.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await settings_mutations.announce(info=mock_info)

        assert result is True
        mock_client.post_announce.assert_called_once()

    async def test_update_ddns(self, settings_mutations, mock_client):
        mock_client.put_ddns_update.return_value = None
        mock_info = self.create_mock_info(mock_client, bool)

        result = await settings_mutations.update_ddns(info=mock_info, force=True)

        assert result is True
        mock_client.put_ddns_update.assert_called_once_with(force=True)
