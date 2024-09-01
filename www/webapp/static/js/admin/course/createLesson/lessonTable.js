class LessonTable {
    constructor(lessonTrElement, materialTrElement) {
        this.lessonTrElement = lessonTrElement;
        this.materialTrElement = materialTrElement; 

        this.removeLessonButton = this.lessonTrElement.querySelector('#remove-lesson');

        this.removeLessonButton.addEventListener('click', this.removeLesson.bind(this));
    }

    removeLesson() {
        this.materialTrElement.remove();
        this.lessonTrElement.remove();
    }
}
