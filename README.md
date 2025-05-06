# PumpSwap MCP Server

An MCP server that enables AI agents to interact with [PumpSwap](https://swap.pump.fun/) for real-time token swaps and automated on-chain trading.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)


## Features

- **Buy Tokens**: Purchase tokens using SOL with customizable slippage and priority fees.
- **Sell Tokens**: Sell tokens for SOL with configurable parameters.
- **Token Price Query**: Retrieve current token prices in SOL.
- **Pool Data Retrieval**: Fetch and display detailed pool information for a given token mint.

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management and script execution
- Solana RPC endpoint (e.g., `https://api.mainnet-beta.solana.com`)
- A valid Solana private key for transaction signing

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/pumpswap-mcp.git
   cd pumpswap-mcp
   ```

2. **Install uv**:
   If `uv` is not installed, follow the official [uv installation guide](https://github.com/astral-sh/uv#installation). For example:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set Up Dependencies**:
   Use `uv` to install dependencies:
   ```bash
   uv sync
   ```

4. **Configure Environment Variables**:
   Create a `.env.private` filein the project root with the following variables:
   ```plaintext
   HTTPS_RPC_ENDPOINT=https://api.mainnet-beta.solana.com
   BUY_SLIPPAGE=0.3
   SELL_SLIPPAGE=0.1
   SWAP_PRIORITY_FEE=1500000
   PRIVATE_KEY=your-solana-private-key
   ```

   Replace `your-solana-private-key` with your actual Solana private key. 
   
## Usage

### Run the MCP Server
   Use `uv` to run the server:
   ```bash
   uv run main.py
   ```

   The server will listen for MCP commands and expose the following tools:
   - `buy_token(mint: str, sol_amount: float, user_private_key: str)`: Buy tokens with SOL.
   - `sell_token(mint: str, token_amount: float, user_private_key: str)`: Sell tokens for SOL.
   - `get_token_price(mint: str)`: Fetch the current token price in SOL.
   - `get_pool_data(mint: str)`: Retrieve formatted pool data for a token.

### Buy Tokens

**Prompt**:
```
Buy 0.1 SOL worth of tokens with mint address FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump.
```

This triggers `buy_token("FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump", 0.1)`.

**Expected Output**:
```
Buy successful for 0.1 SOL of token FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump
Transaction ID: <transaction-id>
Amount: <token-amount>
Token Price (SOL): <price>
```

### Sell Tokens
**Prompt**:
```
Sell 1000 tokens of FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump.
```

This triggers `sell_token("FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump", 1000)`.

**Expected Output**:
```
Sell successful for 1000 tokens of FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump
Transaction ID: <transaction-id>
Amount: <sol-amount>
Token Price (SOL): <price>
```

### Get Token Price
**Prompt**:
```
What is the current price of the token with mint FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump?
```
This triggers `get_token_price("FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump")`.

**Expected Output**:
```
The current price of token FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump is <price> SOL.
```

### Get Pool Data
**Prompt**:
```
Show me the pool data for the token with mint FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump.
```
This triggers `get_pool_data("FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump")`.

**Expected Output**:
```
PumpPool Data for mint FC988ZAKRPc26wefDAxcYWB8kgbJTH4Tg3qDvf7xpump:
Pool Bump: <bump>
Index: <index>
Creator: <creator-pubkey>
Base Mint: <base-mint>
Quote Mint: <quote-mint>
LP Mint: <lp-mint>
Pool Base Token Account: <base-account>
Pool Quote Token Account: <quote-account>
LP Supply: <supply>
```

## Environment Variables

The server uses the following environment variables, loaded from `.env.private`:

| Variable              | Description                                      | Default Value                       |
|-----------------------|--------------------------------------------------|-------------------------------------|
| `HTTPS_RPC_ENDPOINT`  | Solana RPC endpoint URL                          | https://api.mainnet-beta.solana.com |
| `BUY_SLIPPAGE`        | Slippage tolerance for buy transactions          | 0.3 (30%)                           |
| `SELL_SLIPPAGE`       | Slippage tolerance for sell transactions         | 0.1 (10%)                           |
| `SWAP_PRIORITY_FEE`   | Priority fee for transactions (in lamports)      | 1500000                             |
| `PRIVATE_KEY`         | Solana private key for signing transactions      | None (required)                     |

Ensure `PRIVATE_KEY` is set, as the server will raise an error if it's missing.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This software interacts with decentralized finance (DeFi) protocols and handles sensitive data like private keys. Use it at your own risk. Ensure your `.env.private` file is secure and never share your private key. The authors are not responsible for any financial losses or security issues arising from the use of this software.

