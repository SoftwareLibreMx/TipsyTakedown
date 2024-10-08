const fileToVideoType = {
    'video/mp4': 'VIDEO',
    'video/quicktime': 'VIDEO',
    'video/avi': 'VIDEO',
    'video/mpeg': 'VIDEO',
    'application/pdf': 'PDF',
};

class Material {
    constructor(material, materialElement, saveBtn) {
        this.material = material;
        this.saveBtn = saveBtn;
        this.materialElement = materialElement;
        this.loader = materialElement.querySelector('#loader');
        this.deleteBtn = materialElement.querySelector('#delete-btn');
        this.setDeleteEventListener();
    }

    toggleLoading() {
        this.loader.classList.toggle('d-none');
        this.deleteBtn.classList.toggle('d-none');
    }

    async setDeleteEventListener() {
        this.deleteBtn.addEventListener('click', async () => {
            const response = await fetch(`/api/admin/material/${this.material.id}/`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                this.saveBtn.setAlert('Failed to delete');
                return;
            }

            this.saveBtn.removeMaterial(this);
        });
    }
}

export class SaveButton {
    constructor(document, materialTemplate) {
        this.button = document.getElementById('saveMaterialBtn');
        this.text = document.getElementById('saveText');
        this.spinner = document.getElementById('spinner');
        this.materialTemplate = materialTemplate;
        this.materialsContainer = document.getElementById('materials-container');
        this.errorAlert = document.getElementById('errorAlert');
        this.materialType = document.getElementById('material_type');
    }

    toggleLoading() {
        this.text.classList.toggle('d-none');
        this.spinner.classList.toggle('d-none');
    }

    addMaterial(material) {
        const materialElement = document.createElement('div');
        materialElement.style = 'min-width: 50%;';
        materialElement.innerHTML = this.materialTemplate(material);

        this.materialsContainer.appendChild(materialElement);

        const materialObj = new Material(material, materialElement, this);

        return materialObj;
    }

    setAlert(message) {
        this.errorAlert.innerHTML = message;
        this.errorAlert.classList.remove('d-none');
        setTimeout(() => {
            this.errorAlert.classList.add('d-none');
        }, 2000);
    }

    setMaterialType(type) {
        this.materialType.value = type;
    }

    toggleDisable() {
        this.button.disabled = !this.button.disabled;
    }

    removeMaterial(material) {
        this.materialsContainer.removeChild(material.materialElement);
    }
}

function getFormValidateAndSetType(form, saveBtn) {
    const formData = new FormData(form);
    const material = Object.fromEntries(formData.entries());

    if (!material.name) {
        saveBtn.setAlert('Title is required');
        return;
    }
    
    if (!material.file?.size) {
        saveBtn.setAlert('File is required');
        return;
    }
    
    const materialType = fileToVideoType[material.file.type];
    if(!materialType) {
        saveBtn.setAlert('Invalid file type');
        return;
    }

    saveBtn.setMaterialType(materialType);

    return new FormData(form);
}

export async function onClickSaveButton(document, saveBtn) {
    const form = document.getElementById('videoUploadForm');
    const formData = getFormValidateAndSetType(form, saveBtn);
    
    if (!formData) {
        return;
    }

    const formDataJson = Object.fromEntries(formData.entries());

    const material = saveBtn.addMaterial(formDataJson);
    saveBtn.toggleDisable();
    
    const response = await fetch('/api/admin/material/', {
        method: 'POST',
        body: formData,
    });

    saveBtn.toggleDisable();
    material.toggleLoading();

    if (!response.ok) {
        saveBtn.setAlert('Failed to upload');
        saveBtn.removeMaterial(material);
        return;
    }

    const materialJson = await response.json();

    material.material.id = materialJson.id;

}

export function initSaveButton(document, materialTemplate) {
    const saveButton = new SaveButton(document, materialTemplate);

    saveButton.button.addEventListener('click', async () => {
        await onClickSaveButton(document, saveButton);
    });
}
