const materials = 0;
const addMaterialButton = document.getElementById('addMaterialBtn');

function createTextFormGroup(id, label, type, placeholder='') {
    const input = document.createElement('input');
    input.setAttribute('type', type);
    input.setAttribute('id', id);
    input.classList.add('form-control');
    input.setAttribute('placeholder', placeholder);

    const labelElement = document.createElement('label');
    labelElement.setAttribute('for', id);
    labelElement.textContent = label;

    const formGroup = document.createElement('div');
    formGroup.classList.add('form-group', 'mt-2');

    formGroup.appendChild(labelElement);
    formGroup.appendChild(input);

    return formGroup;
}

function createFileFormGroup(id, label) {
    const file = document.createElement('input');
    file.setAttribute('type', 'file');
    file.setAttribute('id', id);
    file.classList.add('custom-file-input');

    const labelElement = document.createElement('label');
    labelElement.setAttribute('for', id);
    labelElement.textContent = label;
    labelElement.classList.add('custom-file-label');

    const formGroup = document.createElement('div');
    formGroup.classList.add('custom-file', 'mt-2');

    formGroup.appendChild(labelElement);
    formGroup.appendChild(file);

    const inputGroup = document.createElement('div');
    inputGroup.classList.add('input-group');

    inputGroup.appendChild(formGroup);

    return inputGroup;
}

function materialVideoForm() {
    const title = createTextFormGroup(`title${materials}`, 'Title', 'text');
    const description = createTextFormGroup(
        `description${materials}`, 'Description', 'text'
    );
    const video = createFileFormGroup(`video${materials}`, 'Video');
    
    const titleDecriptionRow = document.createElement('div');
    titleDecriptionRow.classList.add('d-flex', 'flex-row');
    titleDecriptionRow.appendChild(title);
    titleDecriptionRow.appendChild(description);

    const material = document.createElement('div');
    material.classList.add('mt-2');
    
    material.appendChild(titleDecriptionRow);
    material.appendChild(video);

    return material;
}

addMaterialButton.addEventListener('click', () => {
    const materials = document.getElementById('materials');

    const material = materialVideoForm();

    materials.appendChild(material);
});
