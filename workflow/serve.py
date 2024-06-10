from datetime import timedelta
import asyncio
from prefect import serve
from workflow.flows.analyze_bitcoin_prices import analyze_bitcoin_prices
from workflow.flows.trending_coins import trending_coins_market_data


async def run_serve():
    analyze_bitcoin_prices_deploy = await analyze_bitcoin_prices.to_deployment(
        name="analyze_bitcoin_prices_scheduled_job", interval=timedelta(minutes=1)
    )
    trending_coins_market_data_deploy = await trending_coins_market_data.to_deployment(
        name="trending_coins_market_data_scheduled_job", interval=timedelta(minutes=30)
    )
    await serve(trending_coins_market_data_deploy, analyze_bitcoin_prices_deploy)


if __name__ == "__main__":

    asyncio.run(run_serve())
