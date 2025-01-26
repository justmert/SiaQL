# SiaQL

A GraphQL interface for Sia network components: [walletd](https://sia.tech/software/walletd), [renterd](https://sia.tech/software/renterd), [hostd](https://sia.tech/software/hostd).

[![Python](https://img.shields.io/badge/python-^3.9-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-package-blueviolet.svg)](https://python-poetry.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://siaql-docs.netlify.app)
  
## Overview

SiaQL provides a unified GraphQL API layer for interacting with various Sia network components. It simplifies the process of querying and managing Sia nodes by providing:

📚 See GraphQL documentation: [siaql-docs.netlify.app](https://siaql-docs.netlify.app)

## Features

- **Unified API**: Access walletd, renterd, and hostd through a single GraphQL endpoint
- **Type Safety**: Fully typed schema with TypeScript/Python type definitions
- **Flexible Queries**: Built-in support for filtering, sorting, and pagination
- **Interactive Documentation and Playground**: GraphiQL interface with schema exploration
- **CLI Tool**: Easy setup and management through command-line interface

## Installation

Install SiaQL using pip:

```bash
pip install siaql
```

## Quick Start

1. Start the SiaQL server:

```bash
siaql
```

2. Access the GraphiQL interface at `http://localhost:9090/graphql` by default.

3. Start querying your Sia components!

## Configuration

SiaQL can be configured through environment variables (`.env` file), command-line arguments:

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | 127.0.0.1 | Server host address |
| `PORT` | 9090 | Server port |
| `ENABLE_RENTERD` | true | Enable/disable renterd integration |
| `RENTERD_URL` | <http://localhost:9981> | Renterd API URL |
| `RENTERD_PASSWORD` | None | Renterd API password |
| `ENABLE_WALLETD` | true | Enable/disable walletd integration |
| `WALLETD_URL` | <http://localhost:9982> | Walletd API URL |
| `WALLETD_PASSWORD` | None | Walletd API password |
| `ENABLE_HOSTD` | true | Enable/disable hostd integration |
| `HOSTD_URL` | <http://localhost:9983> | Hostd API URL |
| `HOSTD_PASSWORD` | None | Hostd API password |

### Command Line Arguments

The same configuration options are available as command-line arguments:

```bash
siaql --host 127.0.0.1 --port 9090
```

> **Note**: SiaQL can be started without any configuration, in which case it will ask for the API URLs and passwords interactively.

### Compatibility

SiaQL is compatible with following versions of Sia components:

| Component | Version |
|----------|---------|
| Walletd | [v0.8.0](https://github.com/SiaFoundation/walletd/releases/tag/v0.8.0) |
| Renterd | [v1.1.1](https://github.com/SiaFoundation/renterd/releases/tag/v1.1.1) |
| Hostd | [v2.0.2](https://github.com/SiaFoundation/hostd/releases/tag/v2.0.2) |

## Example Queries

All [queries](http://localhost:3000/#group-Operations-Queries) are written as its respective Sia component. For example `renterd_Contracts` for  Renterd  [contracts](https://api.sia.tech/renterd#3aca247e-0dd0-449a-abab-d15494b77c37) endpoint.

1. Get Sorted Contracts
```graphql
query GetSortedContracts {
  renterdContracts(
    sort: {
      field: "size"
      direction: DESC
    }
  ) {
    id
    size
    hostKey
    state
    totalCost
    spending {
      uploads
      downloads
      fundAccount
      deletions
      sectorRoots
    }
  }
}
```

2. Get Reliable Hosts
```graphql
query GetReliableHosts {
  renterdGetHosts(
    filter: {
      field: "interactions.successfulInteractions"
      operator: GT
      value: "100"
    }
    sort: {
      field: "interactions.uptime"
      direction: DESC
    }
    pagination: {
      offset: 0
      limit: 20
    }
  ) {
    publicKey
    netAddress
    interactions {
      successfulInteractions
      uptime
      lastScan
    }
  }
}
```

## Development

### Setup Development Environment

```bash
# Create a virtual environment if needed
# python3.9 -m venv venv

# Clone the repository
git clone https://github.com/justmert/siaql.git && cd siaql

# Tested with poetry 2.0.1
# pip install --upgrade poetry==2.0.1

# Install dependencies
poetry install

# Run tests
poetry run pytest

```

## Acknowledgments

- [Sia](https://sia.tech/) - The decentralized storage network
- [Strawberry GraphQL](https://strawberry.rocks/) - GraphQL library for Python
- [Typer](https://typer.tiangolo.com/) - CLI library for Python

## Disclaimer

This repository is a community effort and is not officially supported by the Sia Network.
