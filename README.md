# ZEC-PRO V4 Enterprise

Python FastAPI + Vue3 + Docker 的量化终端重构版。

## 安全说明

默认只开启 Paper Trading，真实交易锁关闭。不要把交易所密钥提交到 GitHub。

## 服务器部署

```bash
sudo -i
cd /opt
rm -rf zec-pro-v4
git clone https://github.com/hyw88838/zec-pro-v4.git zec-pro-v4
cd zec-pro-v4
chmod +x scripts/*.sh
./scripts/install.sh
```

访问：

```text
http://服务器IP:8000
```

## 更新

```bash
cd /opt/zec-pro-v4
./scripts/update.sh
```

## 查看日志

```bash
docker compose logs -f api
```
