import aioschedule
import asyncio
import limits
import mono


async def autolimit_daily():
    await limits.autolimit(mono.get_balance())


# Запуск планировщика
async def scheduler():
    try:
        aioschedule.every().day.at("23:00").do(autolimit_daily)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)

    except Exception as e:
        print(e)


# Создание планировщика
async def on_startup():
    asyncio.create_task(scheduler())
