# Ethereum LRT protocols points checker
 Small script to gather all your Ethereum LRT points from different wallets. 
 
 Currently, only [ether.fi](https://app.ether.fi/portfolio), [renzo](https://app.renzoprotocol.com/portfolio), [puffer](https://quest.puffer.fi/), [swell](https://app.swellnetwork.io/) and [kelp](https://kelpdao.xyz/dashboard/) are supported

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
- put your proxies in format user:password@IP:PORT to proxies.txt (or you can leave the proxy.txt file empty, and confirm the script will run without a proxy after launch, if you want. I don't know what the consequences might be) 

# 📊 Output example

<img width="316" alt="Screenshot_96" src="https://github.com/danijcom/lrt-points-checker/assets/46953160/e6e37011-2496-4ed4-bce5-d06e0a591f23">


* A bit inspired by [this](https://github.com/Jcomper/etherfidailycollector) script
