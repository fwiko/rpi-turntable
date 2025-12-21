import asyncio

from recognition_service import RecognitionService, Config


async def main():
    config = Config()
    service = RecognitionService(config)
    
    await service.run()


if __name__ == "__main__":
    asyncio.run(main())
