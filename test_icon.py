"""Test the catalog-based icon resolution via the library.

Set BRING_EMAIL and BRING_PASSWORD environment variables before running.
"""
import asyncio
import aiohttp
import os
import sys
sys.path.insert(0, 'src')
from python_bring_api.bring import Bring

MAIL = os.environ['BRING_EMAIL']
PASSWORD = os.environ['BRING_PASSWORD']

async def main():
    async with aiohttp.ClientSession() as session:
        bring = Bring(MAIL, PASSWORD, sessionAsync=session)
        await bring.loginAsync()
        print("Logged in")

        lists = await bring.loadListsAsync()
        list_uuid = lists['lists'][0]['listUuid']
        print(f"Using list: {lists['lists'][0]['name']}")

        # Load catalog for icon support
        await bring.loadCatalogAsync('en-US')
        print(f"Catalog loaded: {len(bring._catalog)} entries")

        # Save item using English name - should auto-resolve and show icon
        await bring.saveItemAsync(list_uuid, 'Pineapple', 'via catalog')
        print("Saved 'Pineapple'")

        # Read back - should return English names
        items = await bring.getItemsAsync(list_uuid)
        for p in items.get('purchase', []):
            print(f"  Item: {p['name']} ({p['specification']})")

        # Clean up
        await asyncio.sleep(5)
        await bring.removeItemAsync(list_uuid, 'Pineapple')
        print("Removed 'Pineapple'")

asyncio.run(main())
