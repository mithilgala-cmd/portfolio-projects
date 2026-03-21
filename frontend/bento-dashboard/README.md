# Bento Dashboard

A finance dashboard UI built with **React + Vite**. Features a bento-style layout with a collapsible sidebar, stat cards, transaction history, live activity chart, quick transfer, wallet, analytics, admin panel, and settings.

---

## Features

- 📊 **Stat cards** — portfolio value, P&L, daily change, active positions
- 📈 **Activity chart** — weekly/monthly performance via Recharts
- 💳 **Transaction list** — recent activity with expandable history
- 🔄 **Quick transfer** — send money to saved contacts
- 👛 **Wallet view** — card management interface
- 📉 **Analytics view** — deeper performance breakdowns
- 🛠️ **Settings** — 2FA, push alerts, and account preferences
- 🔐 **Login page** — authentication entry point
- 🧭 **Sidebar navigation** — smooth animated collapsible sidebar

---

## Project Structure

```
bento-dashboard/
├── src/
│   ├── components/
│   │   ├── ActivityChart.jsx     # Recharts line chart
│   │   ├── AddTransactionModal.jsx
│   │   ├── QuickTransfer.jsx
│   │   ├── Sidebar.jsx
│   │   ├── StatCard.jsx
│   │   └── TransactionList.jsx
│   ├── views/
│   │   ├── AdminPanel.jsx
│   │   ├── Analytics.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Login.jsx
│   │   ├── Settings.jsx
│   │   └── Wallet.jsx
│   ├── App.jsx
│   └── index.css
├── package.json
└── vite.config.js
```

---

## Quick Start

```bash
cd frontend/bento-dashboard
npm install
npm run dev
```

Visit `http://localhost:5173`.

---

## Tech Stack

- **React 19** + **Vite 8**
- **Recharts** — activity chart visualisation
- **Lucide React** — icon library
- **Vanilla CSS** — custom dark-theme design system

---

## Stack

![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![Recharts](https://img.shields.io/badge/Recharts-FF6384?style=flat)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=flat&logo=css3&logoColor=white)
