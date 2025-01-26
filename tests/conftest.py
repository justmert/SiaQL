# tests/conftest.py
import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, PropertyMock
from strawberry.types import Info
from siaql.api.renterd import RenterdClient
from siaql.api.walletd import WalletdClient
from siaql.api.hostd import HostdClient
from typing import List, Optional, Type
import strawberry
from siaql.graphql.schemas.types import Wallet, Balance, Address, Currency


class MockField:
    def __init__(self, type_: Type):
        self.type = type_


class WalletdMockInfo:
    def __init__(self, client, field_type):
        self.context = {"walletd_client": client}
        self._field = MockField(field_type)


class HostdMockInfo:
    def __init__(self, client, field_type):
        self.context = {"hostd_client": client}
        self._field = MockField(field_type)


class RenterddMockInfo:
    def __init__(self, client, field_type):
        self.context = {"renterd_client": client}
        self._field = MockField(field_type)


class BaseWalletdTest:
    """Base class for walletd schema tests"""

    @pytest.fixture
    def mock_client(self):
        """Create a mock WalletdClient for testing"""
        client = AsyncMock(spec=WalletdClient)
        client.base_url = "http://localhost:9980/api"
        return client

    def create_mock_info(self, client, field_type):
        """Create a mock Info object with proper field type"""
        return WalletdMockInfo(client, field_type)


class BaseHostdTest:
    """Base class for hostd schema tests"""

    @pytest.fixture
    def mock_client(self):
        """Create a mock HostdClient for testing"""
        client = AsyncMock(spec=HostdClient)
        client.base_url = "http://localhost:9980/api"
        return client

    def create_mock_info(self, client, field_type):
        """Create a mock Info object with proper field type"""
        return HostdMockInfo(client, field_type)


class BaseRenterdTest:
    """Base class for renterd schema tests"""

    @pytest.fixture
    def mock_client(self):
        """Create a mock RenterdClient for testing"""
        client = AsyncMock(spec=RenterdClient)
        client.base_url = "http://localhost:9980/api"
        return client

    def create_mock_info(self, client, field_type):
        """Create a mock Info object with proper field type"""
        return RenterddMockInfo(client, field_type)


@pytest.fixture
def make_timestamp():
    """Create a sample timestamp for testing"""
    return datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


# Global fixtures that can be used across all tests
@pytest.fixture
def mock_walletd_client():
    """Create a mock WalletdClient for testing"""
    client = AsyncMock(spec=WalletdClient)
    client.base_url = "http://localhost:9980/api"
    return client


# Global fixtures that can be used across all tests
@pytest.fixture
def mock_renterd_client():
    """Create a mock RenterdClient for testing"""
    client = AsyncMock(spec=RenterdClient)
    client.base_url = "http://localhost:9980/api"
    return client


# Global fixtures that can be used across all tests
@pytest.fixture
def mock_hostd_client():
    """Create a mock HostdClient for testing"""
    client = AsyncMock(spec=HostdClient)
    client.base_url = "http://localhost:9980/api"
    return client
