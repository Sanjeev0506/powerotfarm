/* =====================================================================
==           WEBSITE JAVASCRIPT LOGIC - GLOBAL FEATURES           ==
=====================================================================
*/

document.addEventListener('DOMContentLoaded', function() {

    // --- Initialize Lucide Icons ---
    lucide.createIcons();
    
    // --- Sticky Header on Scroll ---
    const header = document.getElementById('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // --- Mobile Menu Toggle ---
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const navLinks = document.getElementById('nav-links');
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = menuToggle.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.setAttribute('data-lucide', 'x');
            } else {
                icon.setAttribute('data-lucide', 'menu');
            }
            lucide.createIcons();
        });

        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    menuToggle.querySelector('i').setAttribute('data-lucide', 'menu');
                    lucide.createIcons();
                }
            });
        });
    }

    // --- Media Modal Logic (MODIFIED) ---
    const mediaModal = document.getElementById('media-modal');
    const modalVideoPlayer = document.getElementById('modal-video-player');
    const modalImageViewer = document.getElementById('modal-image-viewer');
    const modalYoutubePlayer = document.getElementById('modal-youtube-player');
    const closeModalBtn = document.getElementById('close-modal');
    const mediaThumbnails = document.querySelectorAll('.media-thumbnail');

    if (mediaModal && closeModalBtn) {
        mediaThumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', () => {
                const mediaSrc = thumbnail.getAttribute('data-src');
                const mediaType = thumbnail.getAttribute('data-type');
                
                modalVideoPlayer.style.display = 'none';
                modalImageViewer.style.display = 'none';
                modalYoutubePlayer.style.display = 'none';
                
                // Reset sources
                modalVideoPlayer.querySelector('source').setAttribute('src', '');
                modalVideoPlayer.load();
                modalImageViewer.setAttribute('src', '');
                modalYoutubePlayer.setAttribute('src', '');

                if (mediaSrc) {
                    if (mediaType === 'video') {
                        modalVideoPlayer.querySelector('source').setAttribute('src', mediaSrc);
                        modalVideoPlayer.load();
                        modalVideoPlayer.style.display = 'block';
                        mediaModal.classList.add('active');
                        modalVideoPlayer.play();
                    } else if (mediaType === 'image') {
                        modalImageViewer.setAttribute('src', mediaSrc);
                        modalImageViewer.style.display = 'block';
                        mediaModal.classList.add('active');
                    } else if (mediaType === 'youtube') {
                        modalYoutubePlayer.setAttribute('src', mediaSrc);
                        modalYoutubePlayer.style.display = 'block';
                        mediaModal.classList.add('active');
                    }
                }
            });
        });

        const closeModal = () => {
            mediaModal.classList.remove('active');
            modalVideoPlayer.pause();
            modalVideoPlayer.querySelector('source').setAttribute('src', '');
            modalImageViewer.setAttribute('src', '');
            modalYoutubePlayer.setAttribute('src', '');
        };

        closeModalBtn.addEventListener('click', closeModal);
        mediaModal.addEventListener('click', (e) => {
            if (e.target === mediaModal) {
                closeModal();
            }
        });
    }
    
    // --- Contact Form Submission ---
    const contactForm = document.getElementById('contact-form');
    const formMessage = document.getElementById('form-message');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            formMessage.textContent = 'Thank you! Your message has been sent successfully.';
            contactForm.reset();
            setTimeout(() => {
                formMessage.textContent = '';
            }, 5000);
        });
    }

    // --- Scroll Reveal Animations ---
    const revealElements = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        threshold: 0.1
    });

    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
    
    // --- Active Navigation Link on Scroll ---
    const sections = document.querySelectorAll('section[id]');
    const navLinksList = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', () => {
        let currentSectionId = '';
        const offset = header ? header.offsetHeight + 10 : 70; 

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - offset) {
                currentSectionId = section.getAttribute('id');
            }
        });

        navLinksList.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href.includes('#') && href.substring(href.indexOf('#') + 1) === currentSectionId) {
                link.classList.add('active');
            } else if (!href.includes('#') && href.includes(window.location.pathname.split('/').pop()) && currentSectionId === '') {
                link.classList.add('active');
            }
            if (currentSectionId === 'hero' && link.getAttribute('href') === 'index.html') {
                link.classList.add('active');
            }
        });
    });


    // --- Dynamic Year in Footer ---
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // --- Services Page: Toggle Price Tables ---
    const toggleButtons = document.querySelectorAll('.toggle-details-btn');
    if (toggleButtons.length > 0) {
        toggleButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('data-target');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    targetElement.classList.toggle('active');
                    if (targetElement.classList.contains('active')) {
                        this.textContent = 'Hide Prices';
                    } else {
                        this.textContent = 'View Prices';
                    }
                }
            });
        });
    }
});