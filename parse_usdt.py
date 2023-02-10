import asyncio
import aiohttp

XRPUSDT = 'https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT'
HTTP_OK = 200


async def get_xrp_usdt_price():
    async with aiohttp.ClientSession() as session:
        async with session.get(XRPUSDT) as response:
            if response.status == HTTP_OK:
                data = await response.json()
                price = float(data['price'])
                return price
            else:
                raise Exception(
                    'Не удалось получить цену XRP/USDT от Binance.')


async def main():
    try:
        with open('max_price.txt', 'r') as f:
            max_price = float(f.read().strip())
    except FileNotFoundError:
        max_price = 0.0

    while True:
        try:
            xrp_usdt_price = await get_xrp_usdt_price()
            if xrp_usdt_price > max_price:
                max_price = xrp_usdt_price
                with open('max_price.txt', 'w') as f:
                    f.write(str(max_price))
            dif_price = xrp_usdt_price < max_price * 0.99
            if dif_price:
                print(
                    'Цена XRP/USDT упала на 1% от '
                    f'максимальной цены за последний час: {max_price}')
                max_price = 0.0
            diff = round((max_price/xrp_usdt_price - 1) * 100, 2)
            print(
                f'Максимальная цена {max_price}, '
                f'текущая {xrp_usdt_price} %{diff}')
            await asyncio.sleep(10)
        except Exception as e:
            print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход из программы...")
