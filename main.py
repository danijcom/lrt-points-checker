import os.path
import traceback
import asyncio
import aiohttp
import config

renzo_headers = {
    "authority": "app.renzoprotocol.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://app.renzoprotocol.com/portfolio",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


async def renzo_points(session: aiohttp.ClientSession, address: str, proxy: str | None, attempt=0):
    try:
        async with session.get(
            f"https://app.renzoprotocol.com/api/points/{address}?chainId=1",
            proxy=f"http://{proxy}" if proxy else None,
            headers=renzo_headers,
            ssl=False,
            timeout=25,
        ) as response:
            if response.status == 200:
                response = await response.json()
                # print(response)
                if response["success"]:
                    return True, address, response["data"]["totals"]
                else:
                    return False, address, response
            else:
                return False, address, f"Status code is {response.status}"
    except Exception as ex:
        # print(ex)
        if attempt == config.max_attempts:
            return False, address, f"Exception: {traceback.format_exc()}"
        else:
            return await renzo_points(session, address, proxy, attempt=attempt + 1)


etherfi_headers = {
    "authority": "app.ether.fi",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://app.ether.fi",
    "referer": "https://app.ether.fi/portfolio",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


async def etherfi_points(session: aiohttp.ClientSession, address: str, proxy: str | None, attempt=0):
    try:
        async with session.get(
            f"https://app.ether.fi/api/portfolio/v3/{address}",
            proxy=f"http://{proxy}" if proxy else None,
            headers=etherfi_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()

                loyaltyPoints = 0
                eigenlayerPoints = 0

                if "referrals" in response:
                    loyaltyPoints += response["referrals"]["total"]
                    # print("Referrals: ", response["referrals"]["total"])

                if "totalIntegrationLoyaltyPoints" in response:
                    loyaltyPoints += response["totalIntegrationLoyaltyPoints"]

                for badge in response["badges"]:
                    if "points" in badge:
                        # print("Badge: ", badge["name"], " Points: ", badge["points"])
                        loyaltyPoints += float(badge["points"])

                if "totalIntegrationEigenLayerPoints" in response:
                    eigenlayerPoints = response["totalIntegrationEigenLayerPoints"]
                if "bonusEigenLayerPoints" in response:
                    eigenlayerPoints += response["bonusEigenLayerPoints"]

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
        if attempt == config.max_attempts:
            return False, address, f"Exception: {traceback.format_exc()}"
        else:
            return await etherfi_points(session, address, proxy, attempt=attempt + 1)


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


async def puffer_points(session: aiohttp.ClientSession, address: str, proxy: str | None, attempt=0):
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
                        if "latest_points" in response["data"][defi]:
                            loyality_points += float(response["data"][defi]["latest_points"])

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
        if attempt == config.max_attempts:
            return False, address, f"Exception: {traceback.format_exc()}"
        else:
            return await puffer_points(session, address, proxy, attempt=attempt + 1)


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


async def kelp_points(session: aiohttp.ClientSession, address: str, proxy: str | None, attempt=0):
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
        if attempt == config.max_attempts:
            return False, address, f"Exception: {traceback.format_exc()}"
        else:
            return await kelp_points(session, address, proxy, attempt=attempt + 1)


zircuit_headers = {
    "authority": "stake.zircuit.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,uk;q=0.6,hr;q=0.5,fr;q=0.4",
    "referer": "https://stake.zircuit.com/points",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}


async def zircuit_points(session: aiohttp.ClientSession, address: str, proxy: str | None, attempt=0):
    try:
        async with session.get(
            f"https://stake.zircuit.com/api/points/{address}",
            proxy=f"http://{proxy}" if proxy else None,
            headers=zircuit_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()
                points = 0

                if isinstance(response, dict) and "totalPoints" in response:
                    points = float(response["totalPoints"])

                return (
                    True,
                    address,
                    {"zircuitPoints": points},
                )
            else:
                return False, address, f"Status code is {response.status}"
    except Exception as ex:
        if attempt == config.max_attempts:
            return False, address, f"Exception: {traceback.format_exc()}"
        else:
            return await zircuit_points(session, address, proxy, attempt=attempt + 1)


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


async def swell_points(session: aiohttp.ClientSession, address: str, proxy: str | None, attempt=0):
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
        if attempt == config.max_attempts:
            return False, address, f"Exception: {traceback.format_exc()}"
        else:
            return await swell_points(session, address, proxy, attempt=attempt + 1)


ethena_headers = {
    "authority": "app.ethena.fi",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,uk;q=0.6,hr;q=0.5,fr;q=0.4",
    "cookie": "termsAccepted=true; added_USDe_to_wallet=true",
    "referer": "https://app.ethena.fi/join",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122""',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}


async def ethena_points(session: aiohttp.ClientSession, address: str, proxy: str | None, attempt=0):
    try:
        async with session.get(
            f"https://app.ethena.fi/api/referral/get-referree?address={address}",
            proxy=f"http://{proxy}" if proxy else None,
            headers=ethena_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()
                if isinstance(response, dict) and "queryWallet" in response:
                    if len(response["queryWallet"]) == 1:
                        if "accumulatedTotalShardsEarned" in response["queryWallet"][0]:
                            if isinstance(response["queryWallet"][0]["accumulatedTotalShardsEarned"], float):
                                return (
                                    True,
                                    address,
                                    {"ethenaPoints": response["queryWallet"][0]["accumulatedTotalShardsEarned"]},
                                )
                    return (
                        True,
                        address,
                        {"ethenaPoints": 0},
                    )
                else:
                    return False, address, response
            else:
                return False, address, f"Status code is {response.status}"
    except Exception as ex:
        if attempt == config.max_attempts:
            return False, address, f"Exception: {traceback.format_exc()}"
        else:
            return await ethena_points(session, address, proxy, attempt=attempt + 1)


karak_headers = {
    "Accept": "*/*",
    "Accept-Language": "ru,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Origin": "https://app.karak.network",
    "Referer": "https://app.karak.network/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


async def karak_points(session: aiohttp.ClientSession, address: str, proxy: str | None, attempt=0):
    try:
        async with session.get(
            f"https://restaking-backend.karak.network/getXP,getTvl?batch=1&input=%7B%220%22%3A%7B%22wallet%22%3A%22{address}%22%7D%7D",
            proxy=f"http://{proxy}" if proxy else None,
            headers=karak_headers,
            ssl=False,
            timeout=15,
        ) as response:
            if response.status == 200:
                response = await response.json()
                if isinstance(response, list) and len(response) > 0:
                    response = response[0]
                    if "result" in response:
                        if "data" in response["result"] and response["result"]["data"].isdigit():
                            return True, address, {"karakPoints": float(response["result"]["data"])}
                    return True, address, {"karakPoints": 0}
                else:
                    return False, address, response
            else:
                if response.status == 207:
                    return True, address, {"karakPoints": 0}
                return False, address, f"Status code is {response.status}"
    except Exception as ex:
        if attempt == config.max_attempts:
            return False, address, f"Exception: {traceback.format_exc()}"
        else:
            return await karak_points(session, address, proxy, attempt=attempt + 1)


async def get_points(addresses: list, proxies: list, without_proxies=False):
    async with aiohttp.ClientSession() as session:
        renzo_tasks = []
        etherfi_tasks = []
        puffer_tasks = []
        kelp_tasks = []
        swell_tasks = []
        zircuit_tasks = []
        ethena_tasks = []
        karak_tasks = []

        for i in range(len(addresses)):
            if config.protocols["renzo"]:
                renzo_tasks.append(
                    renzo_points(
                        session,
                        addresses[i],
                        proxies[i] if not without_proxies else None,
                    )
                )
            if config.protocols["etherfi"]:
                etherfi_tasks.append(
                    etherfi_points(
                        session,
                        addresses[i],
                        proxies[i] if not without_proxies else None,
                    )
                )
            if config.protocols["puffer"]:
                puffer_tasks.append(
                    puffer_points(
                        session,
                        addresses[i],
                        proxies[i] if not without_proxies else None,
                    )
                )
            if config.protocols["kelp"]:
                kelp_tasks.append(
                    kelp_points(
                        session,
                        addresses[i],
                        proxies[i] if not without_proxies else None,
                    )
                )
            if config.protocols["swell"]:
                swell_tasks.append(
                    swell_points(
                        session,
                        addresses[i],
                        proxies[i] if not without_proxies else None,
                    )
                )
            if config.protocols["zircuit"]:
                zircuit_tasks.append(
                    zircuit_points(
                        session,
                        addresses[i],
                        proxies[i] if not without_proxies else None,
                    )
                )
            if config.protocols["ethena"]:
                ethena_tasks.append(
                    ethena_points(
                        session,
                        addresses[i],
                        proxies[i] if not without_proxies else None,
                    )
                )
            if config.protocols["karak"]:
                karak_tasks.append(
                    karak_points(
                        session,
                        addresses[i],
                        proxies[i] if not without_proxies else None,
                    )
                )

        print("🔄 Getting points:", end="")

        renzo_results = []
        etherfi_results = []
        puffer_results = []
        kelp_results = []
        swell_results = []
        zircuit_results = []
        ethena_results = []
        karak_results = []

        if config.protocols["renzo"]:
            renzo_results = await asyncio.gather(*renzo_tasks)
            print(" Renzo", end="")
        if config.protocols["etherfi"]:
            etherfi_results = await asyncio.gather(*etherfi_tasks)
            print(" EtherFi", end="")
        if config.protocols["puffer"]:
            puffer_results = await asyncio.gather(*puffer_tasks)
            print(" Puffer", end="")
        if config.protocols["kelp"]:
            kelp_results = await asyncio.gather(*kelp_tasks)
            print(" Kelp", end="")
        if config.protocols["swell"]:
            swell_results = await asyncio.gather(*swell_tasks)
            print(" Swell", end="")
        if config.protocols["zircuit"]:
            zircuit_results = await asyncio.gather(*zircuit_tasks)
            print(" Zircuit", end="")
        if config.protocols["ethena"]:
            ethena_results = await asyncio.gather(*ethena_tasks)
            print(" Ethena", end="")
        if config.protocols["karak"]:
            karak_results = await asyncio.gather(*karak_tasks)
            print(" Karak", end="")

        print()

        return (
            renzo_results,
            etherfi_results,
            puffer_results,
            kelp_results,
            swell_results,
            zircuit_results,
            ethena_results,
            karak_results,
        )


async def print_points(addresses: list, proxies: list, without_proxies=False):
    (
        renzo_results,
        etherfi_results,
        puffer_results,
        kelp_results,
        swell_results,
        zircuit_results,
        ethena_results,
        karak_results,
    ) = await get_points(addresses, proxies, without_proxies)

    total_renzo_points = 0
    total_etherfi_points = 0
    total_puffer_points = 0
    total_kelp_points = 0
    total_swell_points = 0
    total_zircuit_points = 0
    total_eigen_points = 0
    total_ethena_points = 0
    total_karak_points = 0

    for i in range(len(addresses)):
        eigen_points = 0

        print("\n{}".format(addresses[i]))

        if renzo_results:
            status, address, data = renzo_results[i]
            if status:
                if data["renzoPoints"] > 0:
                    print(
                        " 💚 Renzo: {:,.0f} pts | EL {:,.0f} pts".format(data["renzoPoints"], data["eigenLayerPoints"])
                    )
                    total_renzo_points += data["renzoPoints"]
                eigen_points += data["eigenLayerPoints"]
            else:
                print(" ⛔️ Renzo: {}".format(data))

        if etherfi_results:
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

        if puffer_results:
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

        if kelp_results:
            status, address, data = kelp_results[i]
            if status:
                if data["kelpMiles"] > 0:
                    print(" 🩶 Kelp: {:,.0f} pts | EL {:,.0f} pts".format(data["kelpMiles"], data["eigenlayerPoints"]))
                    total_kelp_points += data["kelpMiles"]
                eigen_points += data["eigenlayerPoints"]
            else:
                print(" ⛔️ Kelp: {}".format(data))

        if swell_results:
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
            else:
                print(" ⛔️ Swell: {}".format(data))

        if zircuit_results:
            status, address, data = zircuit_results[i]
            if status:
                if data["zircuitPoints"] > 0:
                    print(" 🐱 Zircuit: {:,.0f} pts".format(data["zircuitPoints"]))
                    total_zircuit_points += data["zircuitPoints"]
            else:
                print(" ⛔️ Zircuit: {}".format(data))

        if ethena_results:
            status, address, data = ethena_results[i]
            if status:
                if data["ethenaPoints"] > 0:
                    print(" 🧊 Ethena: {:,.0f} pts".format(data["ethenaPoints"]))
                    total_ethena_points += data["ethenaPoints"]
            else:
                print(" ⛔️ Ethena: {}".format(data))

        if karak_results:
            status, address, data = karak_results[i]
            if status:
                if data["karakPoints"] > 0:
                    print(" 🌟 Karak: {:,.0f} pts".format(data["karakPoints"]))
                    total_karak_points += data["karakPoints"]
            else:
                print(" ⛔️ Karak: {}".format(data))

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
    if total_zircuit_points:
        print(" 🐱 Total Zircuit Points: {:,.0f}".format(total_zircuit_points))
    if total_ethena_points:
        print(" 🧊 Total Ethena Points: {:,.0f}".format(total_ethena_points))
    if total_karak_points:
        print(" 🌟 Total Karak Points: {:,.0f}".format(total_karak_points))
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
    if not os.path.isfile("proxies.txt"):
        print("⛔️ File 'proxies.txt' not found")
    elif not os.path.isfile("addresses.txt"):
        print("⛔️ File 'addresses.txt' not found")
    else:
        proxies = read_proxies()
        addresses = read_addresses()

        if len(addresses) > len(proxies):
            print("⛔️ Not enough proxies ({}) for all addresses ({})".format(len(proxies), len(addresses)))
            result = input("❔ Continue without proxies? (y/n): ")
            if result.lower() != "y":
                print("❌ Aborted")
            else:
                print("📶 Loaded {} addresses".format(len(addresses)))
                asyncio.run(print_points(addresses, proxies, without_proxies=True))
        else:
            print("📶 Loaded {} proxies and {} addresses".format(len(proxies), len(addresses)))
            asyncio.run(print_points(addresses, proxies))

    print()
    input("❔ Press ENTER key to exit")
