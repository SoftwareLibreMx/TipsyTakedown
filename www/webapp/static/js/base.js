window.onload = function() {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        const body = document.body;
        
        body.setAttribute('data-bs-theme', 'dark');
    }
};