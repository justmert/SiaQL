# tests/walletd/test_outputs.py
import pytest
from tests.conftest import BaseWalletdTest
from siaql.graphql.schemas.walletd.outputs import OutputsQueries
from siaql.graphql.schemas.types import (
    SiacoinElement,
    SiafundElement,
    Currency,
    Address,
    SiacoinOutputID,
    SiafundOutputID,
    SiafundOutput,
)


class TestOutputsQueries(BaseWalletdTest):
    @pytest.fixture
    def outputs_queries(self):
        return OutputsQueries()

    @pytest.fixture
    def sample_siacoin_output(self):
        return SiacoinElement(
            id=SiacoinOutputID("scoid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            value=Currency("1000000"),
            address=Address("addr:testaddress123456789"),
            maturity_height=100,
        )

    @pytest.fixture
    def sample_siafund_output(self):
        return SiafundElement(
            id=SiafundOutputID("sfoid:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),
            state_element=None,
            siafund_output=SiafundOutput(value=5, address=Address("addr:testaddress123456789")),
            claim_start=Currency("0"),
        )

    async def test_get_siacoin_output(self, outputs_queries, mock_client, sample_siacoin_output):
        mock_client.get_siacoin_output.return_value = sample_siacoin_output
        mock_info = self.create_mock_info(mock_client, SiacoinElement)

        result = await outputs_queries.get_siacoin_output(info=mock_info, id=str(sample_siacoin_output.id))

        assert isinstance(result, SiacoinElement)
        assert result.id == sample_siacoin_output.id
        assert result.value == sample_siacoin_output.value
        assert result.address == sample_siacoin_output.address
        assert result.maturity_height == sample_siacoin_output.maturity_height

        mock_client.get_siacoin_output.assert_called_once_with(id=str(sample_siacoin_output.id))

    async def test_get_siafund_output(self, outputs_queries, mock_client, sample_siafund_output):
        mock_client.get_siafund_output.return_value = sample_siafund_output
        mock_info = self.create_mock_info(mock_client, SiafundElement)

        result = await outputs_queries.get_siafund_output(info=mock_info, id=str(sample_siafund_output.id))

        assert isinstance(result, SiafundElement)
        assert result.id == sample_siafund_output.id
        assert result.siafund_output.value == sample_siafund_output.siafund_output.value
        assert result.siafund_output.address == sample_siafund_output.siafund_output.address
        assert result.claim_start == sample_siafund_output.claim_start

        mock_client.get_siafund_output.assert_called_once_with(id=str(sample_siafund_output.id))

    async def test_get_siacoin_output_not_found(self, outputs_queries, mock_client):
        mock_client.get_siacoin_output.return_value = None
        mock_info = self.create_mock_info(mock_client, SiacoinElement)
        output_id = "scoid:0000000000000000000000000000000000000000000000000000000000000000"

        result = await outputs_queries.get_siacoin_output(info=mock_info, id=output_id)

        assert result is None
        mock_client.get_siacoin_output.assert_called_once_with(id=output_id)

    async def test_get_siafund_output_not_found(self, outputs_queries, mock_client):
        mock_client.get_siafund_output.return_value = None
        mock_info = self.create_mock_info(mock_client, SiafundElement)
        output_id = "sfoid:0000000000000000000000000000000000000000000000000000000000000000"

        result = await outputs_queries.get_siafund_output(info=mock_info, id=output_id)

        assert result is None
        mock_client.get_siafund_output.assert_called_once_with(id=output_id)
