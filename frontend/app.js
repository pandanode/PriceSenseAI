/* ═══════════════════════════════════════════
   PRICESENSEAI — app.js
   All JavaScript logic
═══════════════════════════════════════════ */

const API = "http://127.0.0.1:8000";
// State
let currentProduct = null;
let currentBestPrice = null;
let patienceTimer = null;

/* ═══════════════════════════════════════════
   SPLASH → APP TRANSITION
═══════════════════════════════════════════ */
function enterApp() {
  const btn = document.getElementById("enterBtn");
  btn.innerHTML = `<span class="btn-text">LOADING</span> <span class="btn-arrow">⏳</span>`;
  btn.disabled = true;

  setTimeout(() => {
    document.getElementById("splash").classList.add("fade-out");
    setTimeout(() => {
      document.getElementById("splash").style.display = "none";
      document.getElementById("app").classList.add("visible");
      window.scrollTo(0, 0);
    }, 900);
  }, 500);
}

/* ═══════════════════════════════════════════
   SEARCH
═══════════════════════════════════════════ */
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("searchInput").addEventListener("keydown", e => {
    if (e.key === "Enter") doSearch();
  });

  document.getElementById("alertPopup").addEventListener("click", e => {
    if (e.target.id === "alertPopup") closeAlertPopup();
  });
});

function quickSearch(term) {
  document.getElementById("searchInput").value = term;
  doSearch();
}

async function doSearch() {
  const q = document.getElementById("searchInput").value.trim();
  if (!q) {
    shakeSearchBox();
    return;
  }

  currentProduct = q;
  hideAll();
  showPatience(q);
  document.getElementById("searchBtn").disabled = true;

  try {
    const res = await fetch(`${API}/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();

    stopPatience();

    if (!res.ok) throw new Error(data.detail || "No results found");

    await renderResults(data);
    showSection("resultsSection");
    scrollToResults();

  } catch (err) {
    stopPatience();
    document.getElementById("errorMsg").textContent =
      err.message || "Something went wrong. Is the server running?";
    showSection("errorBox");
  } finally {
    document.getElementById("searchBtn").disabled = false;
  }
}

function shakeSearchBox() {
  const box = document.getElementById("searchBox");
  box.style.animation = "none";
  box.offsetHeight;
  box.style.animation = "shake 0.4s ease";
  box.addEventListener("animationend", () => { box.style.animation = ""; }, { once: true });
}

function hideAll() {
  document.getElementById("resultsSection").classList.remove("active");
  document.getElementById("errorBox").classList.remove("active");
  document.getElementById("patienceScreen").classList.remove("active");
}

function showSection(id) {
  document.getElementById(id).classList.add("active");
}

function scrollToResults() {
  setTimeout(() => {
    document.getElementById("resultsSection").scrollIntoView({ behavior: "smooth", block: "start" });
  }, 100);
}

function resetSearch() {
  hideAll();
  document.getElementById("searchInput").value = "";
  document.getElementById("searchInput").focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ═══════════════════════════════════════════
   PATIENCE SCREEN
═══════════════════════════════════════════ */
const patienceMessages = [
  "It will take a few moments, have patience! 😊",
  "Great deals are worth the wait! ⏳",
  "Scanning the best prices for you... 🔍",
  "Almost there, hang tight! 💪",
  "Checking Amazon, Flipkart & Snapdeal... 🛒",
  "Our AI is hard at work! 🤖",
  "Finding you the best deal... 💰",
];

const stepIds = ["step1", "step2", "step3", "step4", "step5"];
const stepProgress = [10, 30, 55, 75, 95];
let msgIndex = 0;

function showPatience(query) {
  stepIds.forEach(id => {
    const el = document.getElementById(id);
    el.classList.remove("active", "done");
  });
  document.getElementById("patienceBar").style.width = "0%";
  msgIndex = 0;
  document.getElementById("patienceText").textContent = patienceMessages[0];
  showSection("patienceScreen");

  let stepIndex = 0;

  function advanceStep() {
    if (stepIndex < stepIds.length) {
      if (stepIndex > 0) {
        const prev = document.getElementById(stepIds[stepIndex - 1]);
        prev.classList.remove("active");
        prev.classList.add("done");
        prev.textContent = prev.textContent.replace("🟡", "✅");
      }
      const current = document.getElementById(stepIds[stepIndex]);
      current.classList.add("active");
      current.textContent = current.textContent.replace("⚪", "🟡");
      document.getElementById("patienceBar").style.width = stepProgress[stepIndex] + "%";
      stepIndex++;
    }
    msgIndex = (msgIndex + 1) % patienceMessages.length;
    document.getElementById("patienceText").textContent = patienceMessages[msgIndex];
  }

  advanceStep();
  patienceTimer = setInterval(advanceStep, 5000);
}

function stopPatience() {
  if (patienceTimer) { clearInterval(patienceTimer); patienceTimer = null; }
  document.getElementById("patienceScreen").classList.remove("active");
  document.getElementById("patienceBar").style.width = "100%";
  stepIds.forEach(id => {
    const el = document.getElementById(id);
    el.classList.remove("active");
    el.classList.add("done");
  });
}

/* ═══════════════════════════════════════════
   RENDER RESULTS
═══════════════════════════════════════════ */
async function renderResults(data) {
  // Header
  document.getElementById("queryLabel").textContent = `"${data.query.toUpperCase()}"`;
  document.getElementById("resultsCount").textContent =
    `${data.results.length} PLATFORM${data.results.length !== 1 ? "S" : ""} FOUND`;

  const best = data.best_deal;
  currentBestPrice = best.price;

  // Best banner
  document.getElementById("bestTitle").textContent = best.title;
  document.getElementById("bestPrice").textContent = `₹${formatPrice(best.price)}`;
  document.getElementById("bestPlatform").textContent = `ON ${best.platform.toUpperCase()}`;
  document.getElementById("bestLink").href = best.url;

  if (data.savings > 0) {
    document.getElementById("bestSaving").innerHTML =
      `YOU SAVE <strong>₹${formatPrice(data.savings)}</strong> VS HIGHEST PRICE`;
  } else {
    document.getElementById("bestSaving").textContent = "BEST AVAILABLE PRICE ACROSS ALL PLATFORMS";
  }

  // Platform Cards
  const grid = document.getElementById("cardsGrid");
  grid.innerHTML = "";
  const sorted = [...data.results].sort((a, b) => a.price - b.price);

  sorted.forEach((r, i) => {
    const isBest = r.platform === best.platform && r.price === best.price;
    const card = document.createElement("div");
    card.className = `price-card${isBest ? " best-card" : ""}`;
    card.style.animationDelay = `${i * 0.1}s`;
    card.style.opacity = "0";

    const dotClass = `dot-${r.platform.toLowerCase()}`;

    card.innerHTML = `
      ${isBest ? '<div class="card-best-badge">★ BEST</div>' : ""}
      <div class="card-platform-row">
        <div class="platform-dot ${dotClass}"></div>
        <div class="platform-label">${r.platform.toUpperCase()}</div>
      </div>
      <div class="card-title">${r.title}</div>
      <div class="card-price-val"><small>₹</small>${formatPrice(Math.floor(r.price))}</div>
      <a class="card-url" href="${r.url}" target="_blank" title="${r.url}">
        ${r.url.length > 45 ? r.url.slice(0, 45) + "..." : r.url}
      </a>
    `;
    grid.appendChild(card);
  });

  // ✅ Real LSTM Predictions
  await renderPredictions(best.price, data.results);

  // Pre-fill alert popup
  document.getElementById("popupPrice").value = Math.floor(best.price * 0.88);
  document.getElementById("popupSub").textContent =
    `Book: "${data.query}" | Current best: ₹${formatPrice(best.price)}`;
}

/* ═══════════════════════════════════════════
   AI PRICE PREDICTION — Real LSTM API
═══════════════════════════════════════════ */
async function renderPredictions(currentPrice, results) {
  const container = document.getElementById("predictionCards");
  container.innerHTML = `
    <div style="color:var(--muted);font-family:var(--mono);font-size:0.8rem;padding:1rem;grid-column:1/-1;">
      🤖 Loading AI predictions...
    </div>`;

  try {
    const res = await fetch(
      `${API}/predict?q=${encodeURIComponent(currentProduct)}&platform=Amazon`
    );
    const data = await res.json();

    if (!res.ok) throw new Error("Prediction failed");

    container.innerHTML = "";

    const periods = [
      { key: "next_week",     label: "NEXT WEEK",  icon: "📅" },
      { key: "next_month",    label: "NEXT MONTH", icon: "📆" },
      { key: "next_3_months", label: "3 MONTHS",   icon: "🗓️" },
    ];

    const allPrices = periods.map(p => data[p.key].price);
    const lowestPredicted = Math.min(...allPrices);
    const bestPeriodLabel = periods[allPrices.indexOf(lowestPredicted)].label;

    // Render 3 period cards
    periods.forEach(p => {
      const pred = data[p.key];
      const isDown = pred.trend === "down";
      const isUp   = pred.trend === "up";
      const isBestPrice = pred.price === lowestPredicted;

      const card = document.createElement("div");
      card.className = "pred-card";
      if (isBestPrice) card.style.borderColor = "var(--green)";

      card.innerHTML = `
        <div class="pred-period">${p.icon} ${p.label}</div>
        <div class="pred-price">₹${formatPrice(Math.floor(pred.price))}</div>
        <div class="pred-trend ${isDown ? "trend-down" : isUp ? "trend-up" : "trend-same"}">
          ${isDown ? "↓" : isUp ? "↑" : "→"} ${pred.change_pct}%
        </div>
      `;
      container.appendChild(card);
    });

    // Best time to buy card
    const bestCard = document.createElement("div");
    bestCard.className = "pred-card";
    bestCard.style.borderColor = "var(--green)";
    bestCard.style.background = "#f0fff4";
    bestCard.innerHTML = `
      <div class="pred-period">💡 BEST TIME TO BUY</div>
      <div class="pred-price">₹${formatPrice(Math.floor(lowestPredicted))}</div>
      <div class="pred-trend trend-down">BUY IN ${bestPeriodLabel}</div>
    `;
    container.appendChild(bestCard);

  } catch (err) {
    container.innerHTML = `
      <div style="color:var(--muted);font-family:var(--mono);font-size:0.8rem;
                  padding:1rem;grid-column:1/-1;">
        ⚠️ AI predictions unavailable right now
      </div>`;
  }
}

/* ═══════════════════════════════════════════
   ALERT POPUP
═══════════════════════════════════════════ */
function openAlertPopup() {
  document.getElementById("popupStep1").style.display = "block";
  document.getElementById("popupStep2").classList.remove("active");
  document.getElementById("alertPopup").classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeAlertPopup() {
  document.getElementById("alertPopup").classList.remove("active");
  document.body.style.overflow = "";
}

async function submitAlert() {
  const email = document.getElementById("popupEmail").value.trim();
  const price = parseFloat(document.getElementById("popupPrice").value);

  if (!email || !email.includes("@")) {
    shakeInput("popupEmail");
    return;
  }
  if (!price || price <= 0) {
    shakeInput("popupPrice");
    return;
  }

  const btn = document.querySelector(".popup-submit-btn");
  btn.textContent = "SETTING ALERT...";
  btn.disabled = true;

  try {
    const res = await fetch(`${API}/alert`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        product_name: currentProduct,
        target_price: price
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed");

    // Show success screen
    document.getElementById("popupStep1").style.display = "none";
    document.getElementById("successMsg").textContent =
      `We'll email ${email} when "${currentProduct}" drops below ₹${formatPrice(price)}!`;
    document.getElementById("popupStep2").classList.add("active");

  } catch (err) {
    btn.textContent = "SET ALERT →";
    btn.disabled = false;
    alert("Failed to set alert: " + (err.message || "Unknown error"));
  }
}

function shakeInput(id) {
  const el = document.getElementById(id);
  el.style.borderColor = "#e74c3c";
  el.style.animation = "none";
  el.offsetHeight;
  el.style.animation = "shake 0.4s ease";
  setTimeout(() => {
    el.style.borderColor = "";
    el.style.animation = "";
  }, 1000);
}

/* ═══════════════════════════════════════════
   UTILITIES
═══════════════════════════════════════════ */
function formatPrice(num) {
  return Math.round(num).toLocaleString("en-IN");
}

// Shake keyframe
const shakeStyle = document.createElement("style");
shakeStyle.textContent = `
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%       { transform: translateX(-8px); }
    40%       { transform: translateX(8px); }
    60%       { transform: translateX(-5px); }
    80%       { transform: translateX(5px); }
  }
`;
document.head.appendChild(shakeStyle);