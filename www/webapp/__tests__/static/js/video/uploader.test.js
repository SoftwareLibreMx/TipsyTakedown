import { jest } from '@jest/globals';

let mockFetch = jest.fn();
jest.spyOn(global, 'fetch').mockImplementation(mockFetch);

let mockFormData = jest.fn();
jest.spyOn(global, 'FormData').mockImplementation(mockFormData);

import { SaveButton, onClickSaveButton, initSaveButton } from '@static/js/video/uploader';

describe('uploader', () => {
    let document = {
        getElementById: jest.fn(),
    };

    afterEach(() => {
        jest.clearAllMocks();
    });

    describe('SaveButton', () => {
        it('should toggle loading', () => {
            const saveBtn = jest.fn();
            const saveText = {
                classList: {
                    toggle: jest.fn(),
                },
            };
            const spinner = {
                classList: {
                    toggle: jest.fn(),
                },
            };

            document.getElementById.mockImplementation((id) => {
                return {
                    saveBtn,
                    saveText,
                    spinner,
                }[id];
            });

            const saveButton = new SaveButton(document);

            saveButton.toggleLoading();
           
            expect(saveText.classList.toggle).toHaveBeenCalledWith('d-none');
            expect(spinner.classList.toggle).toHaveBeenCalledWith('d-none');
        });
    });

    describe('onClickSaveButton', () => {
        it('should toggle loading', async () => {
            const saveBtn = {
                toggleLoading: jest.fn(),
            };
            const form = {
                id: 'videoUploadForm',
            };
            const response = {
                ok: true,
            };

            document.getElementById.mockImplementation((id) => {
                return {
                    videoUploadForm: form,
                }[id];
            });

            fetch.mockResolvedValue(response);

            await onClickSaveButton(document, saveBtn);

            expect(saveBtn.toggleLoading).toHaveBeenCalledTimes(2);
            expect(fetch).toHaveBeenCalledWith('/api/video/', {
                method: 'POST',
                body: new FormData(form),
            });
        });

        it('should show error alert', async () => {
            const saveBtn = {
                toggleLoading: jest.fn(),
            };
            const form = {
                id: 'videoUploadForm',
            };
            const response = {
                ok: false,
            };
            const errorAlert = {
                classList: {
                    remove: jest.fn(),
                },
            };

            document.getElementById.mockImplementation((id) => {
                return {
                    videoUploadForm: form,
                    errorAlert,
                }[id];
            });

            fetch.mockResolvedValue(response);

            await onClickSaveButton(document, saveBtn);

            expect(errorAlert.classList.remove).toHaveBeenCalledWith('d-none');
        });
    });

    describe('initSaveButton', () => {
        it('should add event listener', () => {
            const getElementByIdResponse = {
                addEventListener: jest.fn(),
            };
            
            document.getElementById.mockReturnValue(getElementByIdResponse);

            initSaveButton(document);

            expect(getElementByIdResponse.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
        });
    });
});
