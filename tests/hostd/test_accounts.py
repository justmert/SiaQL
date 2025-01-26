# tests/hostd/test_accounts.py
import pytest
from typing import List
from tests.conftest import BaseHostdTest
from siaql.graphql.schemas.hostd.accounts import AccountQueries
from siaql.graphql.schemas.types import HostdAccount, FundingSource, Currency, PublicKey, FileContractID
from siaql.graphql.resolvers.filter import FilterInput, FilterOperator, SortInput, SortDirection, PaginationInput


class TestAccountQueries(BaseHostdTest):
    @pytest.fixture
    def account_queries(self):
        return AccountQueries()

    @pytest.fixture
    def sample_hostd_account(self, make_timestamp):
        return HostdAccount(
            id=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            balance=Currency("1000000"),
            expiration=make_timestamp,
        )

    @pytest.fixture
    def sample_hostd_accounts(self, make_timestamp):
        return [
            HostdAccount(
                id=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                balance=Currency("1000000"),
                expiration=make_timestamp,
            ),
            HostdAccount(
                id=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                balance=Currency("2000000"),
                expiration=make_timestamp,
            ),
            HostdAccount(
                id=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                balance=Currency("10"),
                expiration=make_timestamp,
            ),
        ]

    @pytest.fixture
    def sample_funding_sources(self):
        return [
            FundingSource(
                contract_id=FileContractID("fcid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                account_id=PublicKey("ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
                amount=1000000,
            ),
            FundingSource(
                contract_id=FileContractID("fcid:abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678"),
                account_id=PublicKey("ed25519:abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678"),
                amount=2000000,
            ),
        ]

    async def test_get_accounts(self, account_queries, mock_client, sample_hostd_account):
        mock_client.get_accounts.return_value = [sample_hostd_account]
        mock_info = self.create_mock_info(mock_client, List[HostdAccount])

        result = await account_queries.accounts(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], HostdAccount)
        assert result[0].id == sample_hostd_account.id
        assert result[0].balance == sample_hostd_account.balance
        assert result[0].expiration == sample_hostd_account.expiration

        mock_client.get_accounts.assert_called_once()

    async def test_get_accounts_empty(self, account_queries, mock_client):
        mock_client.get_accounts.return_value = []
        mock_info = self.create_mock_info(mock_client, List[HostdAccount])

        result = await account_queries.accounts(info=mock_info)

        assert isinstance(result, list)
        assert len(result) == 0
        mock_client.get_accounts.assert_called_once()

    async def test_get_account_funding(self, account_queries, mock_client, sample_funding_sources):
        mock_client.get_account_funding.return_value = sample_funding_sources
        mock_info = self.create_mock_info(mock_client, List[FundingSource])
        account_id = "ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        result = await account_queries.account_funding(info=mock_info, account=account_id)

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], FundingSource)
        assert result[0].contract_id == sample_funding_sources[0].contract_id
        assert result[0].account_id == sample_funding_sources[0].account_id
        assert result[0].amount == sample_funding_sources[0].amount

        mock_client.get_account_funding.assert_called_once_with(account=account_id)

    async def test_get_account_funding_empty(self, account_queries, mock_client):
        mock_client.get_account_funding.return_value = []
        mock_info = self.create_mock_info(mock_client, List[FundingSource])
        account_id = "ed25519:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        result = await account_queries.account_funding(info=mock_info, account=account_id)

        assert isinstance(result, list)
        assert len(result) == 0
        mock_client.get_account_funding.assert_called_once_with(account=account_id)

    @pytest.mark.parametrize(
        "filter_input, sort_input, pagination_input",
        [
            (FilterInput(field="balance", operator=FilterOperator.GTE, value=1000000), None, None),
        ],
    )
    async def test_get_accounts_with_filters(
        self, account_queries, mock_client, sample_hostd_accounts, filter_input, sort_input, pagination_input
    ):
        mock_client.get_accounts.return_value = sample_hostd_accounts
        mock_info = self.create_mock_info(mock_client, List[HostdAccount])

        result = await account_queries.accounts(
            info=mock_info, filter=filter_input, sort=sort_input, pagination=pagination_input
        )
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], HostdAccount)
        mock_client.get_accounts.assert_called_once()
