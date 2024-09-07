export class QuerySelector {
    previewsQuery = null;
    previewsResponse = [];
    callback = null;
    emptyResponse = false;

    constructor(getItems, modalId = "#querySelectorModal") {
        this.getItems = getItems;

        this.modal = document.querySelector(`#${modalId}`);
        this.searchBar = this.modal.querySelector("#searchInput");
        this.datalist = this.modal.querySelector(`#${modalId}Options`);
        this.saveButton = this.modal.querySelector("#saveButton");
        this.closeButton = this.modal.querySelector("#closeButton");
        
        this.modal.addEventListener("shown.bs.modal", () => this.searchBar.focus());
        this.modal.addEventListener("hidden.bs.modal", () => this.clearSearchBar());
        this.searchBar.addEventListener("input", (e) => this.updateItems(e.target.value));
        this.saveButton.addEventListener("click", this.save.bind(this));
    }

    async updateItems(query) {
        const emptyPreviewsQuery = (
            query.startsWith(this.previewsQuery)
            && this.previewsResponse.length === 0
        );
        if (query.length < 3 || emptyPreviewsQuery) {
            return;
        }
        
        const items = await this.getItems(query);

        if (items.length === 0) {
            this.emptyResponse = true;
            return;
        }

        this.previewsResponse = items;
        this.previewsQuery = query;

        this.datalist.innerHTML = "";
        items.forEach((item) => {
            const option = document.createElement("option");

            option.innerText = item.name;
            option.value = item.id;

            this.datalist.appendChild(option);
        });
    }

    setSaveCallback(callback) {
        this.callback = callback;
    }

    save() {
        const selectedValue = this.previewsResponse.find(
            (item) => item.id === this.searchBar.value
        );

        if (this.callback) {
            this.callback(selectedValue);
        }

        this.callback = null;
        this.closeButton.click();
    }

    clearSearchBar() {
        this.searchBar.value = "";
        this.datalist.innerHTML = "";
        this.previousQuery = "";
        this.previousResponse = [];
    }
}
