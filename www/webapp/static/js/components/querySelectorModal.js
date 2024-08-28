export class QuerySelector {
    previewsQuery = "";
    previewsResponse = [];

    constructor(getItems, modalId = "#querySelectorModal") {
        this.getItems = getItems;
        this.modal = document.querySelector(`#${modalId}`);
        this.searchBar = document.querySelector("#searchInput");
        this.datalist = document.querySelector("#datalist");

        
        this.modal.addEventListener("shown.bs.modal", () => this.searchBar.focus());
        this.modal.addEventListener("hidden.bs.modal", () => this.clearSearchBar());
        this.searchBar.addEventListener("input", (e) => this.updateItems(e.target.value));
    }

    async updateItems(query) {
        const emptyPreviousQuery = (
            query.startsWith(this.previousQuery)
            && this.previousResponse.length === 0
        );

        if (query.length < 3 || emptyPreviousQuery) {
            return;
        }

        const items = await this.getItems(query);

        this.previousResponse = items;
        this.previousQuery = query;

        this.datalist.innerHTML = "";
        items.forEach((item) => {
            const option = document.createElement("option");
            option.value = item.name;
            this.datalist.appendChild(option);
        });
    }

    clearSearchBar() {
        this.searchBar.value = "";
        this.datalist.innerHTML = "";
        this.previousQuery = "";
        this.previousResponse = [];
    }
}
