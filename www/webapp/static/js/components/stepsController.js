export class StepsController {
    initialized = false;
    nextStepCallbacks = [];

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
        this.nextStepCallbacks.push(callback)
    }

    initialize() {
        if (this.initialized) return;

        this.prevStep.addEventListener('click', () => { this.prevStepHandler() });
        this.nextStep.addEventListener('click', async () => { await this.nextStepHandler() });
        
        this.initialized = true;
    }

    prevStepHandler() {
        this.steps[this.currentStep].classList.add('d-none');
        this.steps[this.currentStep - 1].classList.remove('d-none');
        this.currentStep--;
        this.nextStep.disabled = false;
        if (this.currentStep === 0) {
            this.prevStep.disabled = true;
        }
    }

    async nextStepHandler() {
        for (let callback of this.nextStepCallbacks) {
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
    }
}
