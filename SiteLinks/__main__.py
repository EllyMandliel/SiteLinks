from SiteLinks.urlfetcher import main
import selectors
import asyncio

if __name__ == '__main__':
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()
