# 🛢️ Hordstake — Oil & Gas Equipment Rental Platform

## ⚡ Local Development

```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py create_superuser
python manage.py runserver
```

Open: http://127.0.0.1:8000/

**Admin login:** username `Admin2` / password `12345678`
**Admin dashboard:** http://127.0.0.1:8000/admin_dashboard/

---

## 🚀 Render.com Deployment (EXACT STEPS)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Hordstake deploy"
git remote add origin https://github.com/YOUR_USERNAME/hordstake.git
git push -u origin main
```

### Step 2 — Create Web Service on Render
1. Go to https://render.com → **New** → **Web Service**
2. Connect your GitHub repo
3. Set these values:
   - **Name:** hordstake
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn hordstake.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### Step 3 — Environment Variables (REQUIRED on Render)
Go to your service → **Environment** tab → Add these:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Any random 50-char string (generate at https://djecrety.ir/) |
| `DEBUG` | `False` |
| `PYTHON_VERSION` | `3.11.0` |

### Step 4 — Database (Choose one)
**Option A - Keep SQLite (simple, free):**
No extra setup needed. SQLite file persists on Render disk.

**Option B - PostgreSQL (recommended for production):**
1. Render Dashboard → **New** → **PostgreSQL**
2. Copy the **Internal Database URL**
3. Add env variable: `DATABASE_URL` = (paste the URL)

### Step 5 — Deploy
Click **Deploy** and watch the build logs.

---

## 💬 Adding Smartsupp Live Chat

When users click a bank for wire transfer, they get a modal that opens your live chat.

1. Sign up at https://smartsupp.com
2. Get your key from Settings → Chat box → Code
3. Open `core/templates/core/base.html`
4. Find the Smartsupp section (near bottom) and uncomment it:
   ```html
   <script type="text/javascript">
   var _smartsupp = _smartsupp || {};
   _smartsupp.key = 'YOUR_KEY_HERE';   ← replace this
   ...
   ```

---

## 🔧 Setting Wallet Addresses

After deploying, go to:
`/admin_dashboard/wallet-settings/`

Enter your real USDT, BTC, ETH, and SOL wallet addresses.
These show up on the deposit page for users.

---

## 📋 Features
- Equipment rental + sell listings
- Crypto deposits (BTC/ETH/USDT/SOL) with admin confirmation
- Bank wire transfer → opens live chat support
- KYC verification system
- Invoice/receipt generator
- Investment plans (8/16/24% ROI)
- Admin dashboard with full user/KYC/listing management
- Referral system ($50 per referral)
- Mobile-responsive design
