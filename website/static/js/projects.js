document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       PROJECT FILTER + SEARCH
    ===================================================== */

    const filterButtons = document.querySelectorAll(".filter-btn");
    const searchInput = document.getElementById("searchProjects");

    // Only get cards from the main projects section
    const projectCards = document.querySelectorAll(
        ".projects-section .project-card"
    );

    let currentFilter = "all";


    /* =====================================================
       FILTER + SEARCH FUNCTION
    ===================================================== */

    function filterProjects() {

        const searchValue = searchInput
            ? searchInput.value.toLowerCase().trim()
            : "";

        projectCards.forEach(function (card) {

            const category = (
                card.dataset.category || ""
            )
                .toLowerCase()
                .trim();

            const searchText = (
                card.dataset.search ||
                card.textContent ||
                ""
            )
                .toLowerCase();

            /* FILTER */

            const matchesFilter =
                currentFilter === "all" ||
                category === currentFilter;

            /* SEARCH */

            const matchesSearch =
                searchValue === "" ||
                searchText.includes(searchValue);

            /* SHOW / HIDE */

            if (matchesFilter && matchesSearch) {

                card.style.display = "";

            } else {

                card.style.display = "none";

            }

        });

    }


    /* =====================================================
       FILTER BUTTONS
    ===================================================== */

    filterButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            /* Remove active state */

            filterButtons.forEach(function (btn) {
                btn.classList.remove("active");
            });

            /* Add active state */

            this.classList.add("active");

            /* Get filter */

            currentFilter = (
                this.dataset.filter || "all"
            )
                .toLowerCase()
                .trim();

            console.log(
                "Selected filter:",
                currentFilter
            );

            /* Apply filter */

            filterProjects();

        });

    });


    /* =====================================================
       SEARCH
    ===================================================== */

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            filterProjects();

        });

    }


    /* =====================================================
       INITIAL FILTER
    ===================================================== */

    filterProjects();


    /* =====================================================
       PROJECT LIGHTBOX
    ===================================================== */

    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    const closeLightbox = document.querySelector(".close-lightbox");

    const projectImages = document.querySelectorAll(
        ".projects-section .project-image img"
    );


    if (
        lightbox &&
        lightboxImg &&
        closeLightbox &&
        projectImages.length
    ) {

        projectImages.forEach(function (image) {

            image.style.cursor = "zoom-in";

            image.addEventListener("click", function () {

                lightboxImg.src = image.src;
                lightboxImg.alt = image.alt;

                lightbox.classList.add("active");

                document.body.style.overflow = "hidden";

            });

        });


        /* CLOSE BUTTON */

        closeLightbox.addEventListener("click", function () {

            lightbox.classList.remove("active");

            document.body.style.overflow = "";

        });


        /* CLICK OUTSIDE IMAGE */

        lightbox.addEventListener("click", function (event) {

            if (event.target === lightbox) {

                lightbox.classList.remove("active");

                document.body.style.overflow = "";

            }

        });


        /* ESCAPE KEY */

        document.addEventListener("keydown", function (event) {

            if (event.key === "Escape") {

                lightbox.classList.remove("active");

                document.body.style.overflow = "";

            }

        });

    }


    /* =====================================================
       PROJECT SCROLL ANIMATIONS
    ===================================================== */

    const animatedItems = document.querySelectorAll(
        `
        .projects-section .project-card,
        .project-hero,
        .project-overview,
        .project-gallery,
        .project-process,
        .project-navigation,
        .related-projects,
        .project-cta,
        .overview-card,
        .gallery-card,
        .process-step,
        .related-card
        `
    );


    if ("IntersectionObserver" in window) {

        const observer = new IntersectionObserver(
            function (entries) {

                entries.forEach(function (entry) {

                    if (entry.isIntersecting) {

                        entry.target.classList.add("show");

                        observer.unobserve(entry.target);

                    }

                });

            },
            {
                threshold: 0.15
            }
        );


        animatedItems.forEach(function (item) {

            item.classList.add("hidden");

            observer.observe(item);

        });

    } else {

        animatedItems.forEach(function (item) {

            item.classList.add("show");

        });

    }


    /* =====================================================
       STAGGERED ANIMATIONS
    ===================================================== */

    document.querySelectorAll(".overview-card").forEach(
        function (card, index) {

            card.style.transitionDelay =
                `${index * 120}ms`;

        }
    );


    document.querySelectorAll(".gallery-card").forEach(
        function (card, index) {

            card.style.transitionDelay =
                `${index * 100}ms`;

        }
    );


    document.querySelectorAll(".process-step").forEach(
        function (card, index) {

            card.style.transitionDelay =
                `${index * 150}ms`;

        }
    );


    document.querySelectorAll(".related-card").forEach(
        function (card, index) {

            card.style.transitionDelay =
                `${index * 120}ms`;

        }
    );

});