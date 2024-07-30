class SaveButton {
    constructor() {
        this.button = document.getElementById('saveBtn');
        this.text = document.getElementById('saveText');
        this.spinner = document.getElementById('spinner');
    }

    toggleLoading() {
        this.text.classList.toggle('d-none');
        this.spinner.classList.toggle('d-none');
    }
}

const saveButton = new SaveButton();
const errorAlert = document.getElementById('errorAlert');

saveButton.button.addEventListener('click', async () => {
    saveButton.toggleLoading();

    const form = document.getElementById('videoUploadForm');
    const formData = new FormData(form);

    const response = await fetch('/api/video/', {
        method: 'POST',
        body: formData,
    });

    saveButton.toggleLoading();

    if (!response.ok) {
        errorAlert.classList.remove('d-none');
        return;
    }

    // window.location.href = `/video/`;
});
