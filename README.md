# SiaQL

A GraphQL interface for Sia network components (hostd, renterd, and walletd).

## Overview

SiaQL provides a unified GraphQL layer on top of Sia's core REST APIs, making it easier to interact with Sia components. This project aims to simplify data querying and reduce over-fetching by providing a flexible GraphQL interface.

## Features

- GraphQL interface for Sia's core components
- Built-in GraphiQL editor for API exploration
- Secure authentication handling
- Efficient API integration
- Type-safe queries and responses

## Installation

### Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/justmert/siaql.git
cd siaql
```

2. Install dependencies:
```bash
poetry install
```

## Usage

### Starting the Server

Start the GraphQL server using one of these methods:

1. With password prompt (recommended):
```bash
poetry run siaql
```

2. With password as command line argument:
```bash
poetry run siaql --walletd-password your_password
```

3. With password as environment variable:
```bash
export SIAQL_WALLETD_PASSWORD=your_password
poetry run siaql
```

Additional configuration options:
```bash
poetry run siaql --help
```

### Using the GraphQL Interface

Once the server is running, open GraphiQL at `http://localhost:8000/graphql`. Here are some example queries:

```graphql
# Get address balance
{
  addressBalance(address: "your_sia_address") {
    siacoins
    immatureSiacoins
    siafunds
  }
}

# Get address events
{
  addressEvents(address: "your_sia_address", limit: 5) {
    id
    timestamp
    type
    maturityHeight
  }
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
