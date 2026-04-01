#!/usr/bin/env python3

import aiohttp
import asyncio

from .ELEX import ELEX
from .const import UOM_EUR_PER_KWH

# Safe, rate-limited token for public GitHub testing for BE market area.
DEMO_TOKEN = "elex_demo_token"

async def main():
    async with aiohttp.ClientSession() as session:
        print("\n=== Testing ELEX Spot Prices ===")
        
        # Test with Belgium (BE) using the demo token
        service = ELEX.Elex(
            market_area="BE", 
            api_key=DEMO_TOKEN, 
            duration=15, 
            session=session
        )

        await service.fetch()
        md = service.marketdata
        
        print(f"Success! Fetched {len(md)} entries from ELEX:")
        print("-" * 30)
        
        for e in md:
            print(f"{e.start_time}: {e.market_price_per_kwh:.4f} {UOM_EUR_PER_KWH}")

if __name__ == "__main__":
    asyncio.run(main())