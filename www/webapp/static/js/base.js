window.onload = function() {
    if (window.matchMedia('(prefers-color-scheme: light)').matches) {
        const body = document.body;

        body.setAttribute('data-bs-theme', 'light');
    }

};
