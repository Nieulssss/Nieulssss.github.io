const buttonScroll = document.querySelector('.scroll');
const nav = document.querySelector('nav');
const header = document.querySelector('header');

const h2header = header.querySelector('h2');
let typingTimeout = null; // Variable pour stocker l'ID du timer et pouvoir l'annuler
let currentTxt = 'Développeur'; // Variable globale pour le texte

const typingDelay = 120;
const pauseAfter = 800;

function startTypingAnimation(text) {
    // Si on fournit un nouveau texte, on met à jour la variable globale
    if (text) currentTxt = text;

    // IMPORTANT : Si une animation est déjà en cours, on la tue pour éviter les bugs
    if (typingTimeout) clearTimeout(typingTimeout);

    if (!h2header) return;

    function typeForward(i = 0) {
        h2header.textContent = currentTxt.slice(0, i);
        if (i < currentTxt.length) {
            typingTimeout = setTimeout(() => typeForward(i + 1), typingDelay);
        } else {
            // Mot complet affiché, pause avant d'effacer
            typingTimeout = setTimeout(() => typeBackward(currentTxt.length - 1), pauseAfter);
        }
    }

    function typeBackward(i) {
        h2header.textContent = currentTxt.slice(0, i);
        if (i > 0) {
            typingTimeout = setTimeout(() => typeBackward(i - 1), typingDelay);
        } else {
            // Mot effacé, on recommence à écrire
            typingTimeout = setTimeout(() => typeForward(1), typingDelay);
        }
    }

    // Lancement initial
    typeForward(1);
}

// Lancement au chargement de la page avec le texte initial
if (h2header) {
    // On prend le texte déjà présent dans le HTML ou une valeur par défaut
    startTypingAnimation(h2header.textContent || 'Développeur');
}

// Gérer le scroll sur le click de la flèche
buttonScroll.addEventListener('click', _ => {
    document.querySelector('#Moi').scrollIntoView({ behavior: 'smooth' });
});

// Gère les clics dans la navigation
nav.querySelectorAll('button[data-target]').forEach(button => {
    button.addEventListener('click', () => {
        document.querySelector(button.dataset.target).scrollIntoView({ behavior: 'smooth' });
    });
});

// Contrôler l'apparition de la navbar fixe
const observerOptions = {
    rootMargin: '-100px 0px 0px 0px' // Déclenche quand le header est presque sorti de la vue
};

const headerObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        nav.classList.toggle('visible', !entry.isIntersecting);
    });
}, observerOptions);

headerObserver.observe(header);



// Télécharger le CV
const cvButton = document.querySelector('button#CV');
cvButton.addEventListener('click', _ => {
    if (document.documentElement.lang === 'en') {
        window.open('CV/CV Niels-int.pdf', '_blank');
    } else if (document.documentElement.lang === 'fr') {
        window.open('CV/CV Niels-fr.pdf', '_blank');
    }
});



// Gérer le changement de langue
const langFRButton = document.querySelector('#langFR');
const langENButton = document.querySelector('#langEN');

function applyTranslations(lang) {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (translations[lang] && translations[lang][key]) {
            el.innerHTML = translations[lang][key];
        }
    });
}

function changeLang(lang) {
    document.documentElement.lang = lang;
    localStorage.setItem('preferredLang', lang);
    applyTranslations(lang);

    // Basculer la classe active
    if (langFRButton) langFRButton.classList.toggle('active', lang === 'fr');
    if (langENButton) langENButton.classList.toggle('active', lang === 'en');

    // Mettre à jour l'animation de texte
    if (translations[lang] && translations[lang]['subtitle']) {
        startTypingAnimation(translations[lang]['subtitle']);
    }
}

// Menu burger (mobile)
const hamburger = document.querySelector('.hamburger');
const navUl = document.querySelector('nav ul');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        nav.classList.toggle('open');
    });
}

// Fermer le menu burger (mobile) quand on clique sur un lien
nav.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
        if (nav.classList.contains('open')) {
            nav.classList.remove('open');
        }
    });
});

// Initialiser la langue au chargement
const savedLang = localStorage.getItem('preferredLang') || 'fr';
changeLang(savedLang);

if (langFRButton) langFRButton.addEventListener('click', () => changeLang('fr'));
if (langENButton) langENButton.addEventListener('click', () => changeLang('en'));

// Filtrer le portfolio par technologie
const filterSelect = document.querySelector('#filter-tech');
const portfolioItems = document.querySelectorAll('#Portfolio ul li');

filterSelect.addEventListener('change', (e) => {
    const selectedTech = e.target.value;

    portfolioItems.forEach(item => {
        const techParagraph = item.querySelector('p.tech');
        const techText = techParagraph.textContent.toLowerCase();

        if (selectedTech === 'all') {
            item.style.display = 'grid';
        } else if (techText.includes(selectedTech.toLowerCase())) {
            item.style.display = 'grid';
        } else {
            item.style.display = 'none';
        }
    });
});

// Animation des barres de compétences au scroll
const skillsSection = document.querySelector('.skills');
const progressBars = document.querySelectorAll('.progress');

const skillsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            progressBars.forEach(bar => {
                const width = bar.getAttribute('data-width');
                bar.style.width = width;
            });
            // On arrête d'observer une fois l'animation lancée
            skillsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.2 });

if (skillsSection) {
    skillsObserver.observe(skillsSection);
}