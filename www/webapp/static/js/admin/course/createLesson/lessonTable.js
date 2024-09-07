export class FormController {
    customCallbacksAdded = false;

    constructor(course, stepNumber, globalStepId) {
        this.course = course;
        this.stepNumber = stepNumber;
        this.stepsElement = document.querySelector(`#${globalStepId}`);
        this.formElement = document.querySelector('#lessonForm');

        this.stepsElement.addEventListener(
            'stepsControllerLoaded',
            this.addEventListenerToNextStepButton.bind(this)
        );
    }


    addEventListenerToNextStepButton() {
        if (this.initializeNextStep) {
            return;
        }

        this.stepsController = globalThis.stepsController;
    
        this.stepsController.runBeforeNextStep(this.onClickSave.bind(this));
        this.stepsController.runAfterNextStep(this.changeButtonIfCurrentStep.bind(this));
        this.stepsController.runBeforePrevStep(this.beforePrevStep.bind(this));
        this.initializeNextStep = true;
    }

    async onClickSave() {
        if (!this.stepsController.isCurrentStep(this.stepNumber)) {
            return;
        } 

        const formData = new FormData(this.formElement);
        
        const lessonMap = new Map();
        for (let [key, value] of formData.entries()) {
            if (lessonMap.has(key)) {
                lessonMap.get(key).push(value);
                continue;
            }

            lessonMap.set(key, [value]);
        }

        const lessons = [];
        lessonMap.get('lesson_name').forEach((name, index) => {
            lessons.push({
                id: lessonMap.get('lesson_id')[index],
                name,
            });
        });

        const response = await fetch(`/api/admin/course/${this.course.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `${sessionStorage.getItem('token')}`
            },
            body: JSON.stringify({ lessons })
        });

        if (!response.ok) {
            alert('Error saving lessons');
            return 'Error saving lessons';
        }
        
        window.location.href = `/admin/`;
    }

    changeButtonIfCurrentStep() {
        if (!this.stepsController.isCurrentStep(this.stepNumber)) {
            this.stepsController.nextStep.textContent = 'Next Step';
            return;
        } 

        this.stepsController.nextStep.textContent = 'Save';
        this.stepsController.nextStep.disabled = false;
    }

    beforePrevStep() {
        if (!this.stepsController.isCurrentStep(this.stepNumber)) {
            return;
        }

        this.stepsController.nextStep.textContent = 'Next Step';
    }
}

export class LessonTable {
    initializeNextStep = false;
    dragedElement = null;

    constructor(stepNumberTitle, newLessonTemplate, globalStepId, courseStr) {
        this.stepNumber = parseInt(stepNumberTitle) - 1;
        this.course = JSON.parse(courseStr || sessionStorage.getItem('course'));
        
        this.newLesson = document.querySelector('#addLesson');
        this.container = document.querySelector('#lessonsContainer');


        this.newLessonTemplate = newLessonTemplate;

        this.newLesson.addEventListener('click', this.addLesson.bind(this));
        this.stepsButton = new FormController(this.course, this.stepNumber, globalStepId);
        this.initialize();
    }

    initialize() {
        if(this.course === null) {
            return;
        }
        this.course.lessons.forEach(lesson => {
            const lessonElement = this.addLesson();
            
            lessonElement.setInput('id', lesson.id);
            lessonElement.setInput('name', lesson.name);
            // TODO: Add material to lesson
        }); 
    }

    addLesson() {
        const [lessonTrElement, materialTrElement] = this.newLessonTemplate(
            this.startDrag.bind(this), this.dragOver.bind(this)
        );
        
        const lesson = new Lesson(this, lessonTrElement, materialTrElement);

        this.container.appendChild(lessonTrElement);
        this.container.appendChild(materialTrElement);

        return lesson;
    }

    startDrag(event) {
        this.dragedElement = event.target;
    }

    dragOver(event) {
        event.preventDefault();

        const children = Array.from(this.container.children);
        const parentNode = event.target.parentNode;
        const nextSibling = this.dragedElement.nextSibling;
    
        if (children.indexOf(parentNode) > children.indexOf(this.dragedElement)) {
            parentNode.nextSibling.after(this.dragedElement);
            this.dragedElement.after(nextSibling);
        } else {
            parentNode.before(this.dragedElement);
            this.dragedElement.after(nextSibling);
        }
    }
}

export class Lesson {
    constructor(container, lessonTrElement, materialTrElement) {
        this.container = container;
        
        this.lessonTrElement =lessonTrElement;
        this.materialTrElement = materialTrElement; 
        
        this.lessonId = this.lessonTrElement.querySelector('#lessonId');
        this.lessonName = this.lessonTrElement.querySelector('#lessonName');
        this.removeLessonButton = this.lessonTrElement.querySelector('#remove-lesson');
        this.addMaterialButton = this.lessonTrElement.querySelector('#add-material');

        this.removeLessonButton.addEventListener('click', this.removeLesson.bind(this));
        this.addMaterialButton.addEventListener('click', this.selectMaterialCallback.bind(this));
    }

    removeLesson() {
        this.materialTrElement.remove();
        this.lessonTrElement.remove();
    }

    selectMaterialCallback() {
        const that = this;
        const materialSelector = globalThis.materialSelector;

        materialSelector.setSaveCallback((material) => {
            that.addMaterial(material);
        })
    }

    addMaterial(material) {
        const materialElement = document.createElement('div');
        materialElement.style = 'min-width: 50%;';
        materialElement.innerHTML = this.container.newLessonTemplate(material);

        this.materialTrElement.appendChild(materialElement);
    }

    setInput(key, value) {
        this.inputs = {
            'name': this.lessonName,
            'id': this.lessonId,
        }

        if (!this.inputs[key]) {
            return;
        }

        this.inputs[key].value = value;
    }
}
