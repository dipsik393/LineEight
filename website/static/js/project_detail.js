/*=========================================
SCROLL ANIMATION
=========================================*/

const animatedItems = document.querySelectorAll(

`
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

const observer = new IntersectionObserver((entries)=>{

    entries.forEach((entry)=>{

        if(entry.isIntersecting){

            entry.target.classList.add("show");

        }

    });

},{
    threshold:.15
});

animatedItems.forEach(item=>{

    item.classList.add("hidden");

    observer.observe(item);

});

document.querySelectorAll(".overview-card").forEach((card,index)=>{

    card.style.transitionDelay=`${index*120}ms`;

});

document.querySelectorAll(".gallery-card").forEach((card,index)=>{

    card.style.transitionDelay=`${index*100}ms`;

});

document.querySelectorAll(".process-step").forEach((card,index)=>{

    card.style.transitionDelay=`${index*150}ms`;

});

document.querySelectorAll(".related-card").forEach((card,index)=>{

    card.style.transitionDelay=`${index*120}ms`;

});

/* ==========================
GALLERY LIGHTBOX
========================== */

const galleryImages = document.querySelectorAll(".gallery-card img");

const lightbox = document.querySelector(".lightbox");
const lightboxImage = document.querySelector(".lightbox-image");

const closeButton = document.querySelector(".lightbox-close");
const prevButton = document.querySelector(".lightbox-prev");
const nextButton = document.querySelector(".lightbox-next");

let currentIndex = 0;

// Only initialize if the lightbox exists
if (
    galleryImages.length &&
    lightbox &&
    lightboxImage &&
    closeButton &&
    prevButton &&
    nextButton
) {

    galleryImages.forEach((image, index) => {

        image.addEventListener("click", () => {

            currentIndex = index;

            showImage();

            lightbox.classList.add("active");

            document.body.style.overflow = "hidden";

        });

    });

    function showImage() {

        lightboxImage.src = galleryImages[currentIndex].src;

        lightboxImage.alt = galleryImages[currentIndex].alt;

    }

    nextButton.addEventListener("click", () => {

        currentIndex++;

        if (currentIndex >= galleryImages.length) {

            currentIndex = 0;

        }

        showImage();

    });

    prevButton.addEventListener("click", () => {

        currentIndex--;

        if (currentIndex < 0) {

            currentIndex = galleryImages.length - 1;

        }

        showImage();

    });

    function closeLightbox() {

        lightbox.classList.remove("active");

        document.body.style.overflow = "";

    }

    closeButton.addEventListener("click", closeLightbox);

    lightbox.addEventListener("click", (e) => {

        if (e.target === lightbox) {

            closeLightbox();

        }

    });

    document.addEventListener("keydown", (e) => {

        if (!lightbox.classList.contains("active")) return;

        if (e.key === "Escape") {

            closeLightbox();

        }

        if (e.key === "ArrowRight") {

            nextButton.click();

        }

        if (e.key === "ArrowLeft") {

            prevButton.click();

        }

    });

}