# ATLAS Menu

---

## 🚀 Prerequisites

- Python 3.x
- Django 4.2.x (installed via `pip`)
- Cloudflared (installed and authenticated to your Cloudflare account)
- A domain set up in Cloudflare
- `.env` file configured for your project

---

## ⚡ Running locally with Cloudflare Tunnel

### 1️⃣ Start Cloudflare Tunnel

Expose your local server (running on port 8000):

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

This will generate sub domain like: 
```https://your-random-subdomain.trycloudflare.com````

After, copy that sub domain to `.env` file var.

Finally run the django project in same `localhost`!