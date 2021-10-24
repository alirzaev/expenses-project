(() => {
    const Form = {
        data() {
            const mixin = document.querySelector('#django-mixin');
            const categories = JSON.parse(mixin.textContent) ?? [];

            return {
                categories: categories,
                selected: categories.length > 0 ? categories[0].name : ''
            };
        },
        computed: {
            noCategories() {
                return this.categories.length === 0;
            },
            customSelected() {
                return this.selected === '';
            }
        }
    };

    const app = Vue.createApp(Form);
    app.config.compilerOptions.delimiters = ['${', '}$'];

    app.mount('#vue-form');
})();
