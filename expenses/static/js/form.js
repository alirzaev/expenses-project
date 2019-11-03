(() => {
    document.getElementById('category').onchange = event => {
        const value = event.target.value;

        const other = document.getElementById('otherCategory');

        if (value === '') {
            other.setAttribute('required', '');
            other.setAttribute('name', 'otherCategory');
            other.hidden = false;
        } else {
            other.removeAttribute('required');
            other.removeAttribute('name');
            other.hidden = true;
        }
    };
})();
