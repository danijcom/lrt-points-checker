# Ethereum LRT protocols points checker
 Small script to gather all your Ethereum LRT points from different wallets. 
 
 Currently, only [ether.fi](https://app.ether.fi/portfolio), [renzo](https://app.renzoprotocol.com/portfolio), [puffer](https://quest.puffer.fi/), and [kelp](https://kelpdao.xyz/dashboard/) are supported

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
- put your proxies in format user:password@IP:PORT to proxies.txt

# 📊 Output example
<img width="306" alt="Screenshot_95" src="https://github.com/danijcom/lrt-points-checker/assets/46953160/8bc6aa7e-5c1a-473a-be40-5ed9dd24d603">


* A bit inspired by [this](https://github.com/Jcomper/etherfidailycollector)https://github.com/Jcomper/etherfidailycollector script
