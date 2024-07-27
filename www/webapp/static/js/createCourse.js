const saveButton = document.getElementById('saveBtn');
const addMaterialButton = document.getElementById('addMaterialBtn');

function createTextFormGroup(id, label, type, placeholder='') {
    const input = document.createElement('input');
    input.setAttribute('type', type);
    input.classList.add('form-control');
    input.setAttribute('placeholder', placeholder);
    input.setAttribute('name', id);

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
    file.setAttribute('name', id);
    file.classList.add('form-control');

    const labelElement = document.createElement('label');
    labelElement.setAttribute('for', id);
    labelElement.textContent = label;
    labelElement.classList.add('form-label');

    const formGroup = document.createElement('div');
    formGroup.classList.add('mt-2');
    
    formGroup.appendChild(labelElement);
    formGroup.appendChild(file);

    return formGroup;
}

function materialVideoForm() {
    const title = createTextFormGroup(`videoTitle`, 'Title', 'text');
    const description = createTextFormGroup(
        `videoDescription`, 'Description', 'text'
    );
    const video = createFileFormGroup(`videoFile`, 'Video');
    
    const titleDecriptionRow = document.createElement('div');
    title.classList.add('flex-grow', 'me-2');
    description.classList.add('flex-grow');
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

saveButton.addEventListener('click', () => {
    const form = document.getElementById('courseForm');
    const formData = new FormData(form);
    
    console.log(formData.entries().toArray());
    // fetch('/api/courses', {
    //     method: 'POST',
    //     body: formData
    // }).then(response => {
    //     if (response.status === 201) {
    //         window.location.href = '/courses';
    //     }
    // });
});
