

/* ==========================================
   SELECT ELEMENTS
========================================== */

const filterButtons = document.querySelectorAll(".filter-btn");
const projectCards = document.querySelectorAll(".project-card");

const searchInput = document.getElementById("searchProjects");

const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");
const closeLightbox = document.querySelector(".close-lightbox");


/* ==========================================
   FILTER PROJECTS
========================================== */

if (filterButtons.length > 0) {

    filterButtons.forEach(button => {

        button.addEventListener("click", () => {

            filterButtons.forEach(btn => btn.classList.remove("active"));

            button.classList.add("active");

            const filter = button.dataset.filter;

            projectCards.forEach(card => {

                if (filter === "all" || card.classList.contains(filter)) {

                    card.classList.remove("hide");

                } else {

                    card.classList.add("hide");

                }

            });

        });

    });

}


/* ==========================================
   SEARCH PROJECTS
========================================== */

if (searchInput) {

    searchInput.addEventListener("keyup", () => {

        const value = searchInput.value.toLowerCase().trim();

        projectCards.forEach(card => {

            const text = card.textContent.toLowerCase();

            if (text.includes(value)) {

                card.classList.remove("hide");

            } else {

                card.classList.add("hide");

            }

        });

    });

}


/* ==========================================
   LIGHTBOX
========================================== */

if (lightbox && lightboxImg && closeLightbox) {

    document.querySelectorAll(".project-image img").forEach(image => {

        image.style.cursor = "zoom-in";

        image.addEventListener("click", () => {

            lightbox.classList.add("active");

            lightboxImg.src = image.src;

            lightboxImg.alt = image.alt;

        });

    });

    closeLightbox.addEventListener("click", () => {

        lightbox.classList.remove("active");

    });

    lightbox.addEventListener("click", (e) => {

        if (e.target === lightbox) {

            lightbox.classList.remove("active");

        }

    });

    document.addEventListener("keydown", (e) => {

        if (e.key === "Escape") {

            lightbox.classList.remove("active");

        }

    });

}