// Mobile navigation
const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector("#site-nav");

if (menuToggle && siteNav) {
    menuToggle.addEventListener("click", () => {
        const open = siteNav.classList.toggle("open");
        menuToggle.setAttribute("aria-expanded", open);
        menuToggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
    });

    siteNav.addEventListener("click", event => {
        if (!event.target.closest("a")) return;

        siteNav.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.setAttribute("aria-label", "Open navigation");
    });
}


// Mission File dossiers
const dossiers = [...document.querySelectorAll(".dossier")];

if (dossiers.length) {
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    let transitionRunning = false;

    const dossierFromHash = hash => {
        if (!hash?.startsWith("#")) return null;

        const target = document.getElementById(hash.slice(1));
        return target?.classList.contains("dossier") ? target : null;
    };

    const activeDossier = () => dossierFromHash(window.location.hash);

    const dossierInfo = dossier => ({
        number: dossier.querySelector(".file-number")?.textContent.match(/\d{3}/)?.[0] || "",
        title: dossier.querySelector(".dossier-heading h3")?.textContent.trim() || "Dossier"
    });

    // Add circular previous / next controls
    dossiers.forEach((dossier, index) => {
        const panel = dossier.querySelector(".dossier-panel");

        if (!panel || panel.querySelector(".dossier-navigation")) return;

        const previous = dossiers[(index - 1 + dossiers.length) % dossiers.length];
        const next = dossiers[(index + 1) % dossiers.length];

        const prevInfo = dossierInfo(previous);
        const nextInfo = dossierInfo(next);

        panel.insertAdjacentHTML("beforeend", `
            <nav class="dossier-navigation" aria-label="Mission File navigation">
                <a class="dossier-nav-link dossier-nav-prev" href="#${previous.id}" aria-label="Previous Mission File: ${prevInfo.title}">
                    <span class="dossier-nav-number">← ${prevInfo.number}</span>
                    <span class="dossier-nav-title">${prevInfo.title}</span>
                </a>

                <a class="dossier-nav-link dossier-nav-next" href="#${next.id}" aria-label="Next Mission File: ${nextInfo.title}">
                    <span class="dossier-nav-number">${nextInfo.number} →</span>
                    <span class="dossier-nav-title">${nextInfo.title}</span>
                </a>
            </nav>
        `);
    });

    const syncDossierState = () => {
        document.body.classList.toggle("dossier-open", Boolean(activeDossier()));
    };

    const switchDossier = (target, direction = 1) => {
        const current = activeDossier();

        if (!target || target === current || transitionRunning) return;

        if (!current || reducedMotion.matches) {
            window.location.hash = target.id;
            return;
        }

        transitionRunning = true;

        current.classList.add(direction < 0 ? "is-switching-prev" : "is-switching-next");

        window.setTimeout(() => {
            window.location.hash = target.id;

            current.classList.remove(
                "is-switching-prev",
                "is-switching-next"
            );

            transitionRunning = false;
        }, 180);
    };

    const navigateDossier = direction => {
        const current = activeDossier();

        if (!current) return;

        const index = dossiers.indexOf(current);
        const target = dossiers[(index + direction + dossiers.length) % dossiers.length];

        switchDossier(target, direction);
    };

    // One handler covers previous / next and dossier links
    document.addEventListener("click", event => {
        const link = event.target.closest('a[href^="#"]');

        if (!link) return;

        const target = dossierFromHash(link.getAttribute("href"));
        const current = activeDossier();

        if (!target || !current || target === current) return;

        event.preventDefault();

        let direction = 1;

        if (link.classList.contains("dossier-nav-prev")) {
            direction = -1;
        } else if (!link.classList.contains("dossier-nav-next")) {
            const currentIndex = dossiers.indexOf(current);
            const previousIndex =
                (currentIndex - 1 + dossiers.length) %
                dossiers.length;

            if (dossiers.indexOf(target) === previousIndex) {
                direction = -1;
            }
        }

        switchDossier(target, direction);
    });

    window.addEventListener("hashchange", syncDossierState);
    syncDossierState();

    // Keyboard controls
    document.addEventListener("keydown", event => {
        if (!activeDossier()) return;

        const activeElement = document.activeElement;
        const tag = activeElement?.tagName;

        if (["INPUT", "TEXTAREA", "SELECT"].includes(tag) || activeElement?.isContentEditable) return;

        if (event.key === "Escape") {
            window.location.hash = "mission-files";
        } else if (event.key === "ArrowLeft") {
            event.preventDefault();
            navigateDossier(-1);
        } else if (event.key === "ArrowRight") {
            event.preventDefault();
            navigateDossier(1);
        }
    });
}