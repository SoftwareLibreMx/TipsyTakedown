let materials = 0;
const addMaterialButton = document.getElementById('addMaterialBtn');
const saveButton = document.getElementById('saveBtn');
const form = document.getElementById('courseForm');

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
    const title = createTextFormGroup(`title${materials}`, 'Title', 'text');
    const description = createTextFormGroup(
        `description${materials}`, 'Description', 'text'
    );
    const video = createFileFormGroup(`videoFile${materials}`, 'Video');
    
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
    
    materials++;
    return material;
}

addMaterialButton.addEventListener('click', () => {
    const materials = document.getElementById('materials');

    const material = materialVideoForm();

    materials.appendChild(material);
});

document.body.addEventListener('htmx:configRequest', (event) => {
  if (event.target.tagName === "FORM") {
    const formData = new FormData(event.target); // this triggers a formdata event, which is handled by shoelace

    console.log(formData);

    // add the form data as request parameters
    for (const pair of formData.entries()) {
      const name = pair[0];
      const value = pair[1];

      const parameters = event.detail.parameters;

      // for multivalued form fields, FormData.entries() may contain multiple entries with the same name
      if (parameters[name] == null) {
        parameters[name] = [value]; // single element array
      } else if (Array.isArray(parameters[name]) && !parameters[name].includes(value)) {
        parameters[name].push(value);
      }
    }
  }
});
