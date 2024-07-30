export class SaveButton {
    constructor(document) {
        this.button = document.getElementById('saveBtn');
        this.text = document.getElementById('saveText');
        this.spinner = document.getElementById('spinner');
    }

    toggleLoading() {
        this.text.classList.toggle('d-none');
        this.spinner.classList.toggle('d-none');
    }
}

export async function onClickSaveButton(document, saveBtn) {
    saveBtn.toggleLoading();

    const form = document.getElementById('videoUploadForm');
    const formData = new FormData(form);

    const response = await fetch('/api/video/', {
        method: 'POST',
        body: formData,
    });

    saveBtn.toggleLoading();

    if (!response.ok) {
        const errorAlert = document.getElementById('errorAlert');
        errorAlert.classList.remove('d-none');
        return;
    }

     // window.location.href = `/video/`;
}

export function initSaveButton(document) {
    const saveButton = new SaveButton(document);

    saveButton.button.addEventListener('click', async () => {
        await onClickSaveButton(document, saveButton);
    });
}
