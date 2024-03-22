import traceback
import asyncio
import aiohttp

renzo_headers = {
    "authority": "app.renzoprotocol.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://app.renzoprotocol.com/portfolio",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


async def renzo_points(session: aiohttp.ClientSession, address: str, proxy: str | None):
    try:
        async with session.get(
            f"https://app.renzoprotocol.com/api/points/{address}",
            proxy=f"http://{proxy}" if proxy else None,
            headers=renzo_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()
                if response["success"]:
                    return True, address, response["data"]["totals"]
                else:
                    return False, address, response
            else:
                return False, address, f"Status code is {response.status}"
    except Exception as ex:
        return False, address, f"Exception: {traceback.format_exc()}"


etherfi_headers = {
    "authority": "app.ether.fi",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://app.ether.fi",
    "referer": "https://app.ether.fi/portfolio",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


async def etherfi_points(
    session: aiohttp.ClientSession, address: str, proxy: str | None
):
    try:
        async with session.get(
            f"https://app.ether.fi/api/portfolio/v2/{address}",
            proxy=f"http://{proxy}" if proxy else None,
            headers=etherfi_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()

                loyaltyPoints = response["loyaltyPoints"]
                eigenlayerPoints = response["eigenlayerPoints"]

                for defi in response:
                    if defi == "pendle":
                        continue
                    if isinstance(response[defi], dict):
                        if "loyaltyPoints" in response[defi]:
                            loyaltyPoints += response[defi]["loyaltyPoints"]
                        if "eigenlayerPoints" in response[defi]:
                            loyaltyPoints += response[defi]["eigenlayerPoints"]
                # for bage in response["badges"]:
                #    if "points" in bage:
                #        loyaltyPoints += float(bage["points"])

                return (
                    True,
                    address,
                    {
                        "loyaltyPoints": loyaltyPoints,
                        "eigenlayerPoints": eigenlayerPoints,
                    },
                )
            else:
                return False, address, f"Status code is {response.status}"
    except Exception as ex:
        return False, address, f"Exception: {traceback.format_exc()}"


puffer_headers = {
    "authority": "quest-api.puffer.fi",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,uk;q=0.6,hr;q=0.5,fr;q=0.4",
    "origin": "https://quest.puffer.fi",
    "referer": "https://quest.puffer.fi/",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}


async def puffer_points(
    session: aiohttp.ClientSession, address: str, proxy: str | None
):
    try:
        headers = puffer_headers.copy()
        headers["address"] = address
        async with session.get(
            f"https://quest-api.puffer.fi/puffer-quest/chapter3/deposit_info",
            proxy=f"http://{proxy}" if proxy else None,
            headers=headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()

                loyality_points = 0
                for defi in response["data"]:
                    if defi == "eigenlayer_points":
                        continue
                    if isinstance(response["data"][defi], int):
                        loyality_points += response["data"][defi]
                    if isinstance(response["data"][defi], float):
                        loyality_points += response["data"][defi]
                    if isinstance(response["data"][defi], dict):
                        if "balance" in response["data"][defi]:
                            loyality_points += float(response["data"][defi]["balance"])

                eigenlayer_points = response["data"]["eigenlayer_points"]

                return (
                    True,
                    address,
                    {
                        "loyaltyPoints": loyality_points,
                        "eigenlayerPoints": eigenlayer_points,
                    },
                )
            else:
                return False, address, f"Status code is {response.status}"
    except Exception as ex:
        return False, address, f"Exception: {traceback.format_exc()}"


kelp_headers = {
    "authority": "common.kelpdao.xyz",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,uk;q=0.6,hr;q=0.5,fr;q=0.4",
    "origin": "https://kelpdao.xyz",
    "referer": "https://kelpdao.xyz/",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}


async def kelp_points(session: aiohttp.ClientSession, address: str, proxy: str | None):
    try:
        async with session.get(
            f"https://common.kelpdao.xyz/km-el-points/user/{address}",
            proxy=f"http://{proxy}" if proxy else None,
            headers=kelp_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()

                return (
                    True,
                    address,
                    {
                        "kelpMiles": float(response["value"]["kelpMiles"]),
                        "eigenlayerPoints": float(response["value"]["elPoints"]),
                    },
                )
            else:
                return False, address, f"Status code is {response.status}"
    except Exception as ex:
        return False, address, f"Exception: {traceback.format_exc()}"


swell_headers = {
    "authority": "v3-lrt.svc.swellnetwork.io",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,uk;q=0.6,hr;q=0.5,fr;q=0.4",
    "origin": "https://app.swellnetwork.io",
    "referer": "https://app.swellnetwork.io/portfolio",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}


async def swell_points(session: aiohttp.ClientSession, address: str, proxy: str | None):
    try:
        loyality_points = 0
        eigenlayer_points = 0

        async with session.get(
            f"https://v3.svc.swellnetwork.io/swell.v3.VoyageService/VoyageUser?connect=v1&encoding=json&message=%7B%22address%22%3A%22{address}%22%7D",
            proxy=f"http://{proxy}" if proxy else None,
            headers=swell_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()
                if "points" in response:
                    loyality_points = response["points"]
            else:
                return False, address, f"Status code is {response.status}"

        async with session.get(
            f"https://v3-lrt.svc.swellnetwork.io/swell.v3.EigenPointsService/EigenPointsUser?connect=v1&encoding=json&message=%7B%22address%22%3A%22{address}%22%7D",
            proxy=f"http://{proxy}" if proxy else None,
            headers=swell_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()
                if "points" in response:
                    eigenlayer_points = response["points"]
            else:
                return False, address, f"Status code is {response.status}"

        return (
            True,
            address,
            {
                "loyaltyPoints": loyality_points,
                "eigenlayerPoints": eigenlayer_points,
            },
        )
    except Exception as ex:
        return False, address, f"Exception: {traceback.format_exc()}"


async def get_points(addresses: list, proxies: list, without_proxies=False):
    async with aiohttp.ClientSession() as session:
        renzo_tasks = []
        etherfi_tasks = []
        puffer_tasks = []
        kelp_tasks = []
        swell_tasks = []

        for i in range(len(addresses)):
            renzo_tasks.append(
                renzo_points(
                    session, addresses[i], proxies[i] if not without_proxies else None
                )
            )
            etherfi_tasks.append(
                etherfi_points(
                    session, addresses[i], proxies[i] if not without_proxies else None
                )
            )
            puffer_tasks.append(
                puffer_points(
                    session, addresses[i], proxies[i] if not without_proxies else None
                )
            )
            kelp_tasks.append(
                kelp_points(
                    session, addresses[i], proxies[i] if not without_proxies else None
                )
            )
            swell_tasks.append(
                swell_points(
                    session, addresses[i], proxies[i] if not without_proxies else None
                )
            )

        renzo_results = await asyncio.gather(*renzo_tasks)
        etherfi_results = await asyncio.gather(*etherfi_tasks)
        puffer_results = await asyncio.gather(*puffer_tasks)
        kelp_results = await asyncio.gather(*kelp_tasks)
        swell_results = await asyncio.gather(*swell_tasks)

        return (
            renzo_results,
            etherfi_results,
            puffer_results,
            kelp_results,
            swell_results,
        )


async def print_points(addresses: list, proxies: list, without_proxies=False):
    renzo_results, etherfi_results, puffer_results, kelp_results, swell_results = (
        await get_points(addresses, proxies, without_proxies)
    )

    total_renzo_points = 0
    total_etherfi_points = 0
    total_puffer_points = 0
    total_kelp_points = 0
    total_swell_points = 0
    total_eigen_points = 0

    for i in range(len(addresses)):
        eigen_points = 0

        print("\n{}".format(addresses[i]))

        status, address, data = renzo_results[i]
        if status:
            if data["renzoPoints"] > 0:
                print(
                    " 💚 Renzo: {:,.0f} pts | EL {:,.0f} pts".format(
                        data["renzoPoints"], data["eigenLayerPoints"]
                    )
                )
                total_renzo_points += data["renzoPoints"]
            eigen_points += data["eigenLayerPoints"]
        else:
            print(" ⛔️ Renzo: {}".format(data))

        status, address, data = etherfi_results[i]
        if status:
            if data["loyaltyPoints"] > 0:
                print(
                    " 💜 EtherFi: {:,.0f} pts | EL {:,.0f} pts".format(
                        data["loyaltyPoints"], data["eigenlayerPoints"]
                    )
                )
                total_etherfi_points += data["loyaltyPoints"]
            eigen_points += data["eigenlayerPoints"]
        else:
            print(" ⛔️ EtherFi: {}".format(data))

        status, address, data = puffer_results[i]
        if status:
            if data["loyaltyPoints"] > 0:
                print(
                    " 🐡 Puffer: {:,.0f} pts | EL {:,.0f} pts".format(
                        data["loyaltyPoints"], data["eigenlayerPoints"]
                    )
                )
                total_puffer_points += data["loyaltyPoints"]
            eigen_points += data["eigenlayerPoints"]
        else:
            print(" ⛔️ Puffer: {}".format(data))

        status, address, data = kelp_results[i]
        if status:
            if data["kelpMiles"] > 0:
                print(
                    " 🩶 Kelp: {:,.0f} pts | EL {:,.0f} pts".format(
                        data["kelpMiles"], data["eigenlayerPoints"]
                    )
                )
                total_kelp_points += data["kelpMiles"]
            eigen_points += data["eigenlayerPoints"]
        else:
            print(" ⛔️ Kelp: {}".format(data))

        status, address, data = swell_results[i]
        if status:
            if data["loyaltyPoints"] > 0:
                print(
                    " 🩵 Swell: {:,.0f} pts | EL {:,.0f} pts".format(
                        data["loyaltyPoints"], data["eigenlayerPoints"]
                    )
                )
                total_swell_points += data["loyaltyPoints"]
            eigen_points += data["eigenlayerPoints"]

        total_eigen_points += eigen_points

    print("\n📊 Totals:")
    if total_renzo_points:
        print(" 💚 Total Renzo Points: {:,.0f}".format(total_renzo_points))
    if total_etherfi_points:
        print(" 💜 Total EtherFi Points: {:,.0f}".format(total_etherfi_points))
    if total_puffer_points:
        print(" 🐡 Total Puffer Points: {:,.0f}".format(total_puffer_points))
    if total_kelp_points:
        print(" 🩶 Total Kelp Points: {:,.0f}".format(total_kelp_points))
    if total_swell_points:
        print(" 🩵 Total Swell Points: {:,.0f}".format(total_swell_points))
    if total_eigen_points:
        print(" 💙 Total EigenLayer Points: {:,.0f}".format(total_eigen_points))


def read_proxies():
    proxies = []

    with open("proxies.txt", "r") as file:
        for line in file:
            if not "@" in line:
                line = line.replace("\n", "")
                ip, port, user, password = line.split(":")
                proxies.append(f"{ip}:{port}@{user}:{password}")
            else:
                proxies.append(line.replace("\n", ""))

    return proxies


def read_addresses():
    addresses = []

    with open("addresses.txt", "r") as file:
        for line in file:
            addresses.append(line.replace("\n", ""))

    return addresses


if __name__ == "__main__":
    proxies = read_proxies()
    addresses = read_addresses()

    if len(addresses) > len(proxies):
        print(
            "⛔️ Not enough proxies ({}) for all addresses ({})".format(
                len(proxies), len(addresses)
            )
        )
        result = input("❔ Continue without proxies? (y/n): ")
        if result.lower() != "y":
            print("❌ Aborted")
        else:
            print("📶 Loaded {} addresses".format(len(addresses)))
            asyncio.run(print_points(addresses, proxies, without_proxies=True))
    else:
        print(
            "📶 Loaded {} proxies and {} addresses".format(len(proxies), len(addresses))
        )
        asyncio.run(print_points(addresses, proxies))
