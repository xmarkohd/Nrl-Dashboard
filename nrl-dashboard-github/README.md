# 🏉 NRL Live Dashboard

A real-time NRL analytics dashboard with live ladder, fixtures, and historical data.

## 🚀 Deployment Options

### Option 1: GitHub Pages (Free - Easiest)

1. **Fork or create a new repository**
2. **Upload files:**
   - `index.html` (rename from NRL_Dashboard_2026.html)
   - `data/` folder
3. **Enable GitHub Pages:**
   - Go to Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`
4. **Your site is live at:** `https://yourusername.github.io/nrl-dashboard/`

### Option 2: Netlify (Free - Auto-deploys)

1. Go to [netlify.com](https://netlify.com)
2. Drag and drop your project folder
3. Done! Get a free `.netlify.app` URL
4. Optional: Connect to GitHub for auto-deploys

### Option 3: Vercel (Free - Best for React/Next.js)

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Deploy automatically on every push

### Option 4: Cloudflare Pages (Free - Fast CDN)

1. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
2. Connect GitHub repository
3. Deploy with global CDN

---

## 🔄 Live Data Options

### A. Daily Auto-Updates (Free via GitHub Actions)

The included GitHub Action (`.github/workflows/update-data.yml`) automatically:
- Runs at 6 AM AEST daily
- Fetches latest ladder, fixtures, and results
- Regenerates the dashboard
- Commits and deploys changes

**Setup:**
1. Enable GitHub Actions in your repository
2. The workflow runs automatically

### B. Real-Time Updates (Requires Backend)

For live scores during games, you need a backend service:

#### Option B1: Cloudflare Workers (Free tier: 100k requests/day)

```javascript
// worker.js - Deploy to Cloudflare Workers
export default {
  async fetch(request) {
    const nrlData = await fetch('https://www.nrl.com/api/...');
    return new Response(JSON.stringify(await nrlData.json()), {
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }
}
```

#### Option B2: Vercel Serverless Functions

```javascript
// api/live-scores.js
export default async function handler(req, res) {
  const data = await fetch('https://nrl-data-source.com/api/scores');
  res.json(await data.json());
}
```

#### Option B3: AWS Lambda + API Gateway

More complex but highly scalable for production use.

### C. Third-Party APIs

| Provider | Cost | Features |
|----------|------|----------|
| [SportRadar](https://sportradar.com) | $$$ | Official NRL data partner |
| [API-Football](https://api-football.com) | $20/mo | Rugby league coverage |
| [TheSportsDB](https://thesportsdb.com) | Free tier | Basic data |

---

## 📁 Project Structure

```
nrl-dashboard/
├── index.html              # Main dashboard (rename from NRL_Dashboard_2026.html)
├── data/
│   ├── matches.json        # Historical match data
│   ├── fixtures.json       # Upcoming fixtures
│   ├── ladder.json         # Current ladder
│   └── live_scores.json    # Live game scores
├── scripts/
│   ├── fetch_nrl_data.py   # Data fetching script
│   └── generate_dashboard.py
├── .github/
│   └── workflows/
│       └── update-data.yml # Auto-update workflow
└── README.md
```

---

## 🔧 Making the Dashboard Load External Data

To switch from embedded data to external JSON files, modify the dashboard:

```javascript
// Replace embedded data with fetch calls
async function loadData() {
  const [matches, fixtures, ladder] = await Promise.all([
    fetch('data/matches.json').then(r => r.json()),
    fetch('data/fixtures.json').then(r => r.json()),
    fetch('data/ladder.json').then(r => r.json())
  ]);
  
  return { matches, fixtures, ladder };
}

// Then in your app initialization:
loadData().then(data => {
  MATCHES = data.matches;
  FIXTURES_2026 = data.fixtures;
  // ... render app
});
```

---

## ⚡ Real-Time Updates with WebSockets

For live score updates during games:

```javascript
// Connect to a WebSocket service
const ws = new WebSocket('wss://your-backend.com/nrl-live');

ws.onmessage = (event) => {
  const liveData = JSON.parse(event.data);
  updateLiveScores(liveData);
};

function updateLiveScores(data) {
  // Update UI with live scores
  document.getElementById('live-scores').innerHTML = renderLiveScores(data);
}
```

---

## 📊 Data Sources

| Source | Data Type | Update Frequency |
|--------|-----------|------------------|
| [AusSportsBetting](https://aussportsbetting.com/data/) | Historical results + odds | Weekly |
| [Rugby League Project](https://rugbyleagueproject.org) | Historical data | After each round |
| [NRL.com](https://nrl.com/draw/) | Fixtures, ladder, live | Real-time |
| [Zero Tackle](https://zerotackle.com) | News, team logos | Daily |
| [Live Ladders](https://liveladders.com/nrl/) | Live ladder | During games |

---

## 🛠 Development

### Run Locally

```bash
# Simple HTTP server
python -m http.server 8000

# Or with Node.js
npx serve .
```

Then open `http://localhost:8000`

### Update Data Manually

```bash
cd scripts
python fetch_nrl_data.py
python generate_dashboard.py
```

---

## 📱 Mobile App Version

To convert to a mobile app:

1. **PWA (Progressive Web App)** - Add a manifest.json and service worker
2. **Capacitor** - Wrap in native iOS/Android container
3. **React Native** - Rebuild with React Native components

---

## 🔐 Environment Variables

For API keys and secrets, use GitHub Secrets:

```yaml
# In your workflow
env:
  NRL_API_KEY: ${{ secrets.NRL_API_KEY }}
  SPORTSRADAR_KEY: ${{ secrets.SPORTSRADAR_KEY }}
```

---

## 📄 License

Data © NRL. Logos © respective clubs. Code is MIT licensed.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📞 Support

- Create an issue for bugs
- Discussions for feature requests
