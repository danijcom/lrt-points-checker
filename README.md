# Ethereum LRT protocols points checker
 Small script to gather all your Ethereum LRT points from different addresses (no private keys required). 
 
 Currently, only [ether.fi](https://app.ether.fi/portfolio), [renzo](https://app.renzoprotocol.com/portfolio), [puffer](https://quest.puffer.fi/), [swell](https://app.swellnetwork.io/), [zircuit](https://stake.zircuit.com/), [Ethena](https://www.ethena.fi/), [Karak](https://app.karak.network/) and [kelp](https://kelpdao.xyz/dashboard/) are supported
 
 +Bonus: 📜Scroll marks checker (turn it off in the config.py if you do not need it)

 __Ether.fi points are not 100% accurate, their API is so strange, I'm getting like 10% less than the actual amount__

<h2>🚀 Installation</h2>

```
git clone https://github.com/danijcom/lrt-points-checker

cd lrt-points-checker

pip install -r requirements.txt

python main.py
```

# ⚙️ Before you start:
- rename addresses_EXAMPLE.txt -> addresses.txt
- put your addresses (NOT PRIVATE KEYS) to addresses.txt
- rename proxies_EXAMPLE.txt -> proxies.txt
- put your proxies in format user:password@IP:PORT to proxies.txt (or you can leave the proxy.txt file empty, and confirm the script will run without a proxy after launch if you want. I don't know what the consequences might be)
- [optional] You can turn off not-needed protocols in the config.py by changing True to False.

# 📊 Output example

<img width="305" alt="Screenshot_97" src="https://github.com/danijcom/lrt-points-checker/assets/46953160/3704d1cc-f4f7-4098-ba83-55ecc7d4b784">


* A bit inspired by [this](https://github.com/Jcomper/etherfidailycollector) script
