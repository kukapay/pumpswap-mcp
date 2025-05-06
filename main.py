import asyncio
from typing import Optional
from solders.pubkey import Pubkey
from mcp.server.fastmcp import FastMCP, Context
from pumpswap_sdk import PumpSwapSDK
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(".env.private")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY not found in environment variables. Please set it in .env file.")

# Initialize PumpSwap SDK
pumpswap_sdk = PumpSwapSDK()

# Initialize MCP server
mcp = FastMCP("PumpSwap MCP")

@mcp.tool()
async def buy_token(
    mint: str,
    sol_amount: float,
    user_private_key: str = PRIVATE_KEY,
    ctx: Context = None
) -> str:
    """Buy tokens from PumpSwap DEX using SOL
    
    Args:
        mint: The token mint address
        sol_amount: Amount of SOL to spend
        user_private_key: User's private key for transaction signing (defaults to PRIVATE_KEY from .env)
    
    Returns:
        Transaction result as string, including txid, amount, and token price on success, or error message on failure
    """
    try:
        ctx.info(f"Initiating buy for {sol_amount} SOL of token {mint}")
        result = await pumpswap_sdk.buy(mint, sol_amount, user_private_key)
        
        if result.get("status", False):
            data = result.get("data", {})
            txid = data.get("txid", "N/A")
            amount = data.get("amount", "N/A")
            token_price_sol = data.get("token_price_sol", "N/A")
            ctx.info(f"Buy transaction completed: txid={txid}")
            return (
                f"Buy successful for {sol_amount} SOL of token {mint}\n"
                f"Transaction ID: {txid}\n"
                f"Amount: {amount}\n"
                f"Token Price (SOL): {token_price_sol}"
            )
        else:
            message = result.get("message", "Unknown error")
            ctx.error(f"Buy failed: {message}")
            return f"Buy failed: {message}"
            
    except Exception as e:
        ctx.error(f"Buy failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
async def sell_token(
    mint: str,
    token_amount: float,
    user_private_key: str = PRIVATE_KEY,
    ctx: Context = None
) -> str:
    """Sell tokens on PumpSwap DEX
    
    Args:
        mint: The token mint address
        token_amount: Amount of tokens to sell
        user_private_key: User's private key for transaction signing (defaults to PRIVATE_KEY from .env)
    
    Returns:
        Transaction result as string, including txid, amount, and token price on success, or error message on failure
    """
    try:
        ctx.info(f"Initiating sell of {token_amount} tokens for {mint}")
        result = await pumpswap_sdk.sell(mint, token_amount, user_private_key)
        
        if result.get("status", False):
            data = result.get("data", {})
            txid = data.get("txid", "N/A")
            amount = data.get("amount", "N/A")
            token_price_sol = data.get("token_price_sol", "N/A")
            ctx.info(f"Sell transaction completed: txid={txid}")
            return (
                f"Sell successful for {token_amount} tokens of {mint}\n"
                f"Transaction ID: {txid}\n"
                f"Amount: {amount}\n"
                f"Token Price (SOL): {token_price_sol}"
            )
        else:
            message = result.get("message", "Unknown error")
            ctx.error(f"Sell failed: {message}")
            return f"Sell failed: {message}"
            
    except Exception as e:
        ctx.error(f"Sell failed: {str(e)}")
        return f"Error: {str(e)}"
        
@mcp.tool()
async def get_token_price(
    mint: str,
    ctx: Context
) -> float:
    """Get current token price from PumpSwap DEX
    
    Args:
        mint: The token mint address
    
    Returns:
        Current token price as float
    """
    try:
        ctx.info(f"Fetching price for token {mint}")
        price = await pumpswap_sdk.get_token_price(mint)
        ctx.info(f"Price retrieved: {price}")
        return price
    except Exception as e:
        ctx.error(f"Price fetch failed: {str(e)}")
        raise ValueError(f"Error fetching price: {str(e)}")

@mcp.tool()
async def get_pool_data(
    mint: str,
    ctx: Context
) -> str:
    """Get pool data for a specific token from PumpSwap DEX in textual format
    
    Args:
        mint: The token mint address
    
    Returns:
        Formatted string containing pool data
    """
    try:
        ctx.info(f"Fetching pool data for token {mint}")
        pool_data = await pumpswap_sdk.get_pool_data(mint)
        ctx.info("Pool data retrieved")
        
        # Format PumpPool data into a readable string
        formatted_data = (
            f"PumpPool Data for mint {mint}:\n"
            f"Pool Bump: {pool_data.pool_bump}\n"
            f"Index: {pool_data.index}\n"
            f"Creator: {pool_data.creator}\n"
            f"Base Mint: {pool_data.base_mint}\n"
            f"Quote Mint: {pool_data.quote_mint}\n"
            f"LP Mint: {pool_data.lp_mint}\n"
            f"Pool Base Token Account: {pool_data.pool_base_token_account}\n"
            f"Pool Quote Token Account: {pool_data.pool_quote_token_account}\n"
            f"LP Supply: {pool_data.lp_supply}"
        )
        return formatted_data
    except Exception as e:
        ctx.error(f"Pool data fetch failed: {str(e)}")
        return f"Error: {str(e)}"
        
# Run the server
if __name__ == "__main__":
    mcp.run()
