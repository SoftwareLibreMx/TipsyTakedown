export class StepsController {
    initialized = false;
    beforeNextStepCallbacks = [];
    beforePrevStepCallbacks = [];
    afterNextStepCallbacks = [];
    afterPrevStepCallbacks = [];

    constructor(currentStep, steps) {
        this.prevStep = document.querySelector('#prevStep');
        this.nextStep = document.querySelector('#nextStep');
        this.currentStep = currentStep;
        
        this.steps = steps.split(',').map(step => {
            step = step.trim();
            return document.getElementById(step)
        });

        this.steps[currentStep].classList.remove('d-none');
    }

    runBeforeNextStep(callback) {
        this.beforeNextStepCallbacks.push(callback)
    }

    runBeforePrevStep(callback) {
        this.beforePrevStepCallbacks.push(callback)
    }

    runAfterNextStep(callback) {
        this.afterNextStepCallbacks.push(callback)
    }

    runAfterPrevStep(callback) {
        this.afterPrevStepCallbacks.push(callback)
    }

    initialize() {
        if (this.initialized) return;

        this.prevStep.addEventListener('click', this.prevStepHandler.bind(this));
        this.nextStep.addEventListener('click', this.nextStepHandler.bind(this));
        
        this.initialized = true;
    }

    async prevStepHandler() {
        for (let callback of this.beforePrevStepCallbacks) {
            const error = await callback();

            if (error) {
                throw new Error(error);
            }
        }

        this.steps[this.currentStep].classList.add('d-none');
        this.steps[this.currentStep - 1].classList.remove('d-none');
        this.currentStep--;
        this.nextStep.disabled = false;
        if (this.currentStep === 0) {
            this.prevStep.disabled = true;
        }

        for (let callback of this.afterPrevStepCallbacks) {
            callback();
        }
    }

    async nextStepHandler() {
        for (let callback of this.beforeNextStepCallbacks) {
            const error = await callback();

            if (error) {
                throw new Error(error);
            }
        }

        this.steps[this.currentStep].classList.add('d-none');
        this.steps[this.currentStep + 1].classList.remove('d-none');
        this.currentStep++;
        this.prevStep.disabled = false;
        if (this.currentStep === this.steps.length - 1) {
            this.nextStep.disabled = true;
        }

        for (let callback of this.afterNextStepCallbacks) {
            callback();
        }
    }

    isCurrentStep(step) {
        return step === this.currentStep;
    }
}
