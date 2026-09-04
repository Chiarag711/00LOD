// ---------------------------------
// Mobile navigation
// ---------------------------------

const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector("#site-nav");

if (menuToggle && siteNav) {
    // Open or close the mobile navigation
    menuToggle.addEventListener("click", () => {
        const isOpen = siteNav.classList.toggle("open");

        menuToggle.setAttribute("aria-expanded", isOpen);
        menuToggle.setAttribute(
            "aria-label",
            isOpen ? "Close navigation" : "Open navigation"
        );
    });

    // Close the navigation after selecting a page
    siteNav.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            siteNav.classList.remove("open");

            menuToggle.setAttribute("aria-expanded", "false");
            menuToggle.setAttribute("aria-label", "Open navigation");
        });
    });
}


// ---------------------------------
// Dossier setup
// ---------------------------------

// Collect dossiers in Mission File order
const dossiers = Array.from(
    document.querySelectorAll(".dossier")
);


// Return the dossier currently selected by the URL hash
const getActiveDossier = () => {
    if (!window.location.hash) {
        return null;
    }

    const id = window.location.hash.slice(1);
    const target = document.getElementById(id);

    if (target && target.classList.contains("dossier")) {
        return target;
    }

    return null;
};


// Return a dossier from a hash such as #james_bond
const getDossierFromHash = hash => {
    if (!hash || !hash.startsWith("#")) {
        return null;
    }

    const id = hash.slice(1);
    const target = document.getElementById(id);

    if (target && target.classList.contains("dossier")) {
        return target;
    }

    return null;
};


// Extract the three-digit Mission File number
const getDossierNumber = dossier => {
    const fileNumber =
        dossier.querySelector(".file-number")?.textContent || "";

    const match = fileNumber.match(/\d{3}/);

    return match ? match[0] : "";
};


// Extract the dossier title
const getDossierTitle = dossier => {
    return (
        dossier
            .querySelector(".dossier-heading h3")
            ?.textContent.trim() ||
        "Dossier"
    );
};


// ---------------------------------
// Previous / next navigation
// ---------------------------------

const buildDossierNavigation = () => {
    if (dossiers.length < 2) {
        return;
    }

    dossiers.forEach((dossier, index) => {
        const panel = dossier.querySelector(".dossier-panel");

        // Avoid duplicate navigation controls
        if (
            !panel ||
            panel.querySelector(".dossier-navigation")
        ) {
            return;
        }

        // Circular navigation:
        // 001 goes back to 014 and 014 continues to 001
        const previousDossier =
            dossiers[
                (index - 1 + dossiers.length) %
                dossiers.length
            ];

        const nextDossier =
            dossiers[
                (index + 1) %
                dossiers.length
            ];

        const previousNumber =
            getDossierNumber(previousDossier);

        const nextNumber =
            getDossierNumber(nextDossier);

        const previousTitle =
            getDossierTitle(previousDossier);

        const nextTitle =
            getDossierTitle(nextDossier);


        // Navigation container
        const navigation =
            document.createElement("nav");

        navigation.className =
            "dossier-navigation";

        navigation.setAttribute(
            "aria-label",
            "Mission File navigation"
        );


        // Previous Mission File
        const previousLink =
            document.createElement("a");

        previousLink.className =
            "dossier-nav-link dossier-nav-prev";

        previousLink.href =
            `#${previousDossier.id}`;

        previousLink.setAttribute(
            "aria-label",
            `Previous Mission File: ${previousTitle}`
        );


        const previousNumberElement =
            document.createElement("span");

        previousNumberElement.className =
            "dossier-nav-number";

        previousNumberElement.textContent =
            `← ${previousNumber}`;


        const previousTitleElement =
            document.createElement("span");

        previousTitleElement.className =
            "dossier-nav-title";

        previousTitleElement.textContent =
            previousTitle;


        previousLink.append(
            previousNumberElement,
            previousTitleElement
        );


        // Next Mission File
        const nextLink =
            document.createElement("a");

        nextLink.className =
            "dossier-nav-link dossier-nav-next";

        nextLink.href =
            `#${nextDossier.id}`;

        nextLink.setAttribute(
            "aria-label",
            `Next Mission File: ${nextTitle}`
        );


        const nextNumberElement =
            document.createElement("span");

        nextNumberElement.className =
            "dossier-nav-number";

        nextNumberElement.textContent =
            `${nextNumber} →`;


        const nextTitleElement =
            document.createElement("span");

        nextTitleElement.className =
            "dossier-nav-title";

        nextTitleElement.textContent =
            nextTitle;


        nextLink.append(
            nextNumberElement,
            nextTitleElement
        );


        navigation.append(
            previousLink,
            nextLink
        );

        panel.appendChild(navigation);
    });
};


// ---------------------------------
// Dossier state
// ---------------------------------

const syncDossierState = () => {
    const activeDossier =
        getActiveDossier();

    // Prevent the page behind an open dossier from scrolling
    document.body.classList.toggle(
        "dossier-open",
        Boolean(activeDossier)
    );
};


// ---------------------------------
// Dossier transitions
// ---------------------------------

let dossierTransitionRunning = false;


// Open another dossier with a directional transition
const switchDossier = (targetDossier, direction) => {
    const activeDossier =
        getActiveDossier();

    if (
        !targetDossier ||
        targetDossier === activeDossier ||
        dossierTransitionRunning
    ) {
        return;
    }

    // If no dossier is currently open, open the target normally
    if (!activeDossier) {
        window.location.hash =
            targetDossier.id;

        return;
    }


    // Respect reduced-motion preferences
    const prefersReducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

    if (prefersReducedMotion) {
        window.location.hash =
            targetDossier.id;

        return;
    }


    dossierTransitionRunning = true;


    // Animate the current dossier out
    activeDossier.classList.add(
        direction > 0
            ? "is-switching-next"
            : "is-switching-prev"
    );


    window.setTimeout(() => {
        // Change the active dossier
        window.location.hash =
            targetDossier.id;


        // Remove the outgoing animation class
        activeDossier.classList.remove(
            "is-switching-next",
            "is-switching-prev"
        );


        // Allow the new :target styles to render
        window.requestAnimationFrame(() => {
            window.requestAnimationFrame(() => {
                dossierTransitionRunning = false;
            });
        });
    }, 180);
};


// Move backward or forward through the Mission Files
const navigateDossier = direction => {
    const activeDossier =
        getActiveDossier();

    if (!activeDossier) {
        return;
    }

    const currentIndex =
        dossiers.indexOf(activeDossier);

    if (currentIndex === -1) {
        return;
    }

    const targetIndex =
        (
            currentIndex +
            direction +
            dossiers.length
        ) % dossiers.length;

    switchDossier(
        dossiers[targetIndex],
        direction
    );
};


// Determine the direction between two dossiers
const getNavigationDirection = (
    activeDossier,
    targetDossier
) => {
    const currentIndex =
        dossiers.indexOf(activeDossier);

    const targetIndex =
        dossiers.indexOf(targetDossier);

    if (
        currentIndex === -1 ||
        targetIndex === -1
    ) {
        return 1;
    }


    // Previous dossier in the circular sequence
    const previousIndex =
        (
            currentIndex - 1 + dossiers.length
        ) % dossiers.length;

    if (targetIndex === previousIndex) {
        return -1;
    }


    // All other dossier links move forward
    return 1;
};


// ---------------------------------
// Initialise dossier navigation
// ---------------------------------

buildDossierNavigation();
syncDossierState();


// Update state whenever the URL hash changes
window.addEventListener(
    "hashchange",
    syncDossierState
);


// ---------------------------------
// Dossier link transitions
// ---------------------------------

// Previous controls
document
    .querySelectorAll(".dossier-nav-prev")
    .forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault();

            navigateDossier(-1);
        });
    });


// Next controls
document
    .querySelectorAll(".dossier-nav-next")
    .forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault();

            navigateDossier(1);
        });
    });


// Apply the same transition to links between entities inside dossiers
document
    .querySelectorAll(".dossier-content a[href^='#']")
    .forEach(link => {
        link.addEventListener("click", event => {
            const targetDossier =
                getDossierFromHash(
                    link.getAttribute("href")
                );

            const activeDossier =
                getActiveDossier();

            // Normal behaviour for links that do not target another dossier
            if (
                !targetDossier ||
                !activeDossier
            ) {
                return;
            }

            event.preventDefault();

            const direction =
                getNavigationDirection(
                    activeDossier,
                    targetDossier
                );

            switchDossier(
                targetDossier,
                direction
            );
        });
    });


// ---------------------------------
// Keyboard dossier controls
// ---------------------------------

document.addEventListener("keydown", event => {
    const activeDossier =
        getActiveDossier();

    if (!activeDossier) {
        return;
    }


    // Do not intercept keys while the user is typing
    const activeElement =
        document.activeElement;

    const isTyping =
        activeElement &&
        (
            activeElement.tagName === "INPUT" ||
            activeElement.tagName === "TEXTAREA" ||
            activeElement.tagName === "SELECT" ||
            activeElement.isContentEditable
        );

    if (isTyping) {
        return;
    }


    // Escape returns to the Mission Files
    if (event.key === "Escape") {
        event.preventDefault();

        window.location.hash =
            "mission-files";

        return;
    }


    // Left arrow opens the previous Mission File
    if (event.key === "ArrowLeft") {
        event.preventDefault();

        navigateDossier(-1);

        return;
    }


    // Right arrow opens the next Mission File
    if (event.key === "ArrowRight") {
        event.preventDefault();

        navigateDossier(1);
    }
});