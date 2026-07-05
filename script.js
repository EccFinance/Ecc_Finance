const marketThemes = [
  ["MASI", "+ watchlist"],
  ["Banking", "+ earnings"],
  ["Bonds", "- duration"],
  ["FX MAD", "+ macro"],
  ["M&A", "+ carrières"],
  ["Quant", "+ Python"],
  ["Commodities", "- volatility"],
  ["EcoTALKS", "+ research"],
];

const partners = {
  alumneye: {
    kicker: "Partenaire actif",
    title: "AlumnEye",
    text: "Un partenariat 2026/2027 autour des processus de recrutement en banque et MSc Finance, avec conférence, accès JOBTALK, réductions formation et workshop annuel.",
    bullets: [
      "Conférence ouverte aux étudiants de Centrale Casablanca",
      "Accès aux événements métiers: M&A, Trading et autres formats",
      "Workshop annuel et avantages formation pour les membres",
    ],
  },
  ecofinance: {
    kicker: "Partenaire éducatif",
    title: "EcoFinance Analytics",
    text: "Une collaboration autour d'un compte certifié sur EcoTALKS pour publier des analyses macroéconomiques, études sectorielles et contenus pédagogiques gratuits.",
    bullets: [
      "Compte certifié pour renforcer la crédibilité éditoriale",
      "Liberté de sujets: macro, secteurs et décryptages académiques",
      "Mise en valeur des publications auprès d'une communauté finance",
    ],
  },
  future: {
    kicker: "Opportunité",
    title: "Votre structure",
    text: "Banque, cabinet, fintech, société de bourse, fonds, alumni ou média spécialisé: ECC Finance peut transformer votre expertise en expérience utile pour les étudiants.",
    bullets: [
      "Intervention campus ou format hybride",
      "Workshop technique, panel métier ou challenge analytique",
      "Pipeline clair vers stages, projets et visibilité marque employeur",
    ],
  },
};

function initTicker() {
  const ticker = document.querySelector("[data-ticker]");
  if (!ticker) return;

  const items = [...marketThemes, ...marketThemes]
    .map(([label, value]) => {
      const direction = value.trim().startsWith("+") ? "up" : "down";
      return `<span class="ticker-item"><strong>${label}</strong><span class="${direction}">${value}</span></span>`;
    })
    .join("");

  ticker.innerHTML = items;
}

function initHeader() {
  const header = document.querySelector("[data-header]");
  const progress = document.querySelector(".scroll-progress");
  const nav = document.querySelector("#site-nav");
  const toggle = document.querySelector(".nav-toggle");

  const sync = () => {
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = maxScroll > 0 ? window.scrollY / maxScroll : 0;
    header?.classList.toggle("scrolled", window.scrollY > 28);
    if (progress) progress.style.width = `${Math.min(ratio * 100, 100)}%`;
  };

  toggle?.addEventListener("click", () => {
    const isOpen = nav?.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(Boolean(isOpen)));
    toggle.setAttribute("aria-label", isOpen ? "Fermer le menu" : "Ouvrir le menu");
  });

  nav?.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("open");
      toggle?.setAttribute("aria-expanded", "false");
      toggle?.setAttribute("aria-label", "Ouvrir le menu");
    });
  });

  window.addEventListener("scroll", sync, { passive: true });
  sync();
}

function initReveal() {
  const elements = document.querySelectorAll(".reveal");

  if (!("IntersectionObserver" in window)) {
    elements.forEach((element) => element.classList.add("visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );

  elements.forEach((element) => observer.observe(element));
}

function initFilters() {
  const buttons = document.querySelectorAll(".filter-button");
  const posts = document.querySelectorAll("[data-category]");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      buttons.forEach((item) => item.classList.toggle("active", item === button));

      posts.forEach((post) => {
        const shouldShow = filter === "all" || post.dataset.category === filter;
        post.classList.toggle("is-hidden", !shouldShow);
      });
    });
  });
}

function initPartners() {
  const buttons = document.querySelectorAll("[data-partner]");
  const panel = document.querySelector("[data-partner-panel]");
  if (!panel) return;

  const render = (key) => {
    const partner = partners[key];
    if (!partner) return;
    panel.innerHTML = `
      <p class="spotlight-kicker">${partner.kicker}</p>
      <h3>${partner.title}</h3>
      <p class="spotlight-text">${partner.text}</p>
      <ul class="spotlight-list">
        ${partner.bullets.map((bullet) => `<li>${bullet}</li>`).join("")}
      </ul>
      <div class="spotlight-actions">
        <a class="button button-primary" href="mailto:club.finance@centrale-casablanca.ma?subject=Partenariat%20ECC%20Finance">Construire un partenariat</a>
        <a class="button button-secondary" href="assets/partner-pack-ecc-finance.pdf" download>Télécharger le dossier partenaire</a>
      </div>
    `;
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.classList.toggle("active", item === button));
      render(button.dataset.partner);
    });
  });
}

function initJoinForm() {
  const form = document.querySelector("[data-join-form]");
  const status = document.querySelector("[data-form-status]");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const name = data.get("name")?.toString().trim();
    const track = data.get("track")?.toString().trim();
    const year = data.get("year")?.toString().trim();
    const domain = data.get("domain")?.toString().trim();
    const motivation = data.get("motivation")?.toString().trim();

    const body = [
      "Bonjour ECC Finance,",
      "",
      "Je souhaite rejoindre le club / candidater au Research Desk.",
      "",
      `Nom: ${name}`,
      `Filière: ${track}`,
      `Année: ${year}`,
      `Je veux rejoindre: ${domain}`,
      "",
      "Motivation:",
      motivation,
    ].join("\n");

    const subject = encodeURIComponent(`Candidature ECC Finance - ${name}`);
    window.location.href = `mailto:club.finance@centrale-casablanca.ma?subject=${subject}&body=${encodeURIComponent(body)}`;

    if (status) {
      status.textContent = "Votre client mail va s'ouvrir avec une candidature préremplie.";
    }
  });
}

initTicker();
initHeader();
initReveal();
initFilters();
initPartners();
initJoinForm();
