(() => {
    const rows = document.querySelectorAll('[data-record-url]');

    for (const row of rows) {
        const url = row.dataset.recordUrl;
        row.onclick = () => {
            window.location.assign(url);
        }
    }
})();
