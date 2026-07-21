/*======================================
SCROLL ANIMATION
======================================*/

const animatedSections = document.querySelectorAll(".animate");

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

}, {

    threshold: 0.15

});

animatedSections.forEach(section => {

    section.classList.add("hidden");

    observer.observe(section);

});