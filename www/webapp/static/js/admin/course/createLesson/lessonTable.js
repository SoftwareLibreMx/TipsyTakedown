export class FormController {
    customCallbacksAdded = false;

    constructor(course, stepNumber, globalStepId) {
        this.course = course;
        this.stepNumber = stepNumber;
        this.stepsElement = document.querySelector(`#${globalStepId}`);
        this.formElement = document.querySelector("#lessonForm");

        this.stepsElement.addEventListener(
            "stepsControllerLoaded",
            this.addEventListenerToNextStepButton.bind(this)
        );
    }

    addEventListenerToNextStepButton() {
        if (this.initializeNextStep) {
            return;
        }

        this.stepsController = globalThis.stepsController;

        this.stepsController.runBeforeNextStep(this.onClickSave.bind(this));
        this.stepsController.runAfterNextStep(
            this.changeButtonIfCurrentStep.bind(this)
        );
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

        if (!lessonMap.has("lesson_name")) {
            alert("At least one lesson is required");
            return 'Error saving lessons';
        }

        const lessons = [];
        lessonMap.get("lesson_name").forEach((name, index) => {
            if (!name) {
                alert("Lesson name is required");
                return 'Error saving lessons';
            }

            const lessonKey = lessonMap.get("lesson_key")[index];
            const materials = lessonMap.get(`material_id_${lessonKey}`);

            if (!materials) {
                alert(`At least one Material is required, remove or add a material to ${name}`);
                return 'Error saving lessons';
            }

            lessons.push({
                id: lessonMap.get("lesson_id")[index],
                name,
                materials
            });
        });
        
        const response = await fetch(`/api/admin/course/${this.course.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `${sessionStorage.getItem("token")}`,
            },
            body: JSON.stringify({ lessons }),
        });

        if (!response.ok) {
            alert("Error saving lessons");
            return "Error saving lessons";
        }

        window.location.href = `/admin/`;
    }

    changeButtonIfCurrentStep() {
        if (!this.stepsController.isCurrentStep(this.stepNumber)) {
            this.stepsController.nextStep.textContent = "Next Step";
            return;
        }

        this.stepsController.nextStep.textContent = "Save";
        this.stepsController.nextStep.disabled = false;
    }

    beforePrevStep() {
        if (!this.stepsController.isCurrentStep(this.stepNumber)) {
            return;
        }

        this.stepsController.nextStep.textContent = "Next Step";
    }
}

export class LessonTable {
    initializeNextStep = false;
    dragedElement = null;

    constructor(
        stepNumberTitle,
        newLessonTemplate,
        newMaterialTemplate,
        globalStepId,
        courseStr
    ) {
        this.stepNumber = parseInt(stepNumberTitle) - 1;
        this.course = JSON.parse(courseStr || sessionStorage.getItem("course"));

        this.newLesson = document.querySelector("#addLesson");
        this.container = document.querySelector("#lessonsContainer");

        this.newLessonTemplate = newLessonTemplate;
        this.newMaterialTemplate = newMaterialTemplate;

        this.newLesson.addEventListener("click", this.addLesson.bind(this));
        this.stepsButton = new FormController(
            this.course,
            this.stepNumber,
            globalStepId
        );
        this.initialize();
    }

    initialize() {
        if (this.course === null) {
            return;
        }
        this.course.lessons.forEach((lesson) => {
            const lessonElement = this.addLesson();

            lessonElement.setInput("id", lesson.id);
            lessonElement.setInput("name", lesson.name);
            // TODO: Add material to lesson
            
            lesson.materials.forEach((material) => {
                lessonElement.addMaterial(material);
            });
        });
    }

    addLesson() {
        const [lessonTrElement, materialTrElement] = this.newLessonTemplate(
            this.startDrag.bind(this),
            this.dragOver.bind(this)
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

        if (
            children.indexOf(parentNode) > children.indexOf(this.dragedElement)
        ) {
            parentNode.nextSibling.after(this.dragedElement);
            this.dragedElement.after(nextSibling);
        } else {
            parentNode.before(this.dragedElement);
            this.dragedElement.after(nextSibling);
        }
    }
}

export class Lesson {
    dragedElement = null;

    constructor(container, lessonTrElement, materialTrElement) {
        this.key = self.crypto.randomUUID();
        this.container = container;
        this.materialContainer = materialTrElement.querySelector(
            "#materialsContainer"
        );

        this.lessonTrElement = lessonTrElement;
        this.materialTrElement = materialTrElement;

        this.newMaterialTemplate = container.newMaterialTemplate;
        this.materialIds = new Set();

        this.lessonId = this.lessonTrElement.querySelector("#lessonId");
        this.lessonName = this.lessonTrElement.querySelector("#lessonName");
        this.removeLessonButton =
            this.lessonTrElement.querySelector("#remove-lesson");
        this.addMaterialButton =
            this.lessonTrElement.querySelector("#add-material");

        this.removeLessonButton.addEventListener(
            "click",
            this.removeLesson.bind(this)
        );
        this.addMaterialButton.addEventListener(
            "click",
            this.selectMaterialCallback.bind(this)
        );

        const lessonKey = this.lessonTrElement.querySelector("#lessonKey");
        lessonKey.value = this.key;
    }

    removeLesson() {
        this.materialTrElement.remove();
        this.lessonTrElement.remove();
    }

    selectMaterialCallback() {
        const materialSelector = globalThis.materialSelector;

        materialSelector.setSaveCallback((material) => 
            this.addMaterial(material));
    }

    addMaterial(material) {
        if (this.materialIds.has(material.id)) {
            alert("Material already added");
            return;
        }

        this.materialIds.add(material.id);
        new MaterialTable(
            this.key,
            this.materialTrElement,
            this.newMaterialTemplate,
            material,
            this.startDrag.bind(this),
            this.dragOver.bind(this)
        );
    }

    setInput(key, value) {
        this.inputs = {
            name: this.lessonName,
            id: this.lessonId,
        };

        if (!this.inputs[key]) {
            return;
        }

        this.inputs[key].value = value;
    }

    startDrag(event) {
        this.dragedElement = event.target;
    }

    dragOver(event) {
        event.preventDefault();
        
        const children = Array.from(this.materialContainer.children);
        const parentNode = event.target.parentNode;

        if (
            children.indexOf(parentNode) > children.indexOf(this.dragedElement)
        ) {
            parentNode.after(this.dragedElement);
        } else {
            parentNode.before(this.dragedElement);
        }
    }
}

export class MaterialTable {
    constructor(
        lessonKey,
        container,
        newMaterialTemplate,
        material,
        startDrag,
        dragOver
    ) {
        this.lessonKey = lessonKey;
        this.container = container.querySelector("#materialsContainer");

        this.newMaterialTemplate = newMaterialTemplate;

        this.removePlaceholder();
        this.addMaterial(material, startDrag, dragOver);
    }

    removePlaceholder() {
        const placeholder = this.container.querySelector("#placeHolder");

        if (placeholder) {
            placeholder.remove();
        }
    }

    addMaterial(material, startDrag, dragOver) {
        this.container.appendChild(this.newMaterialTemplate(
            this.lessonKey, material, startDrag, dragOver
        ));
    }
}
