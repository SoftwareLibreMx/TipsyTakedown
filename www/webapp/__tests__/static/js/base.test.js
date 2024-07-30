/**
 * @jest-environment jsdom
 */
import { jest } from '@jest/globals';

let mockMatchMedia = jest.fn();
global.window.matchMedia = mockMatchMedia;

import * as base from '@static/js/base.js';

describe('Base', () => {
    it('should set dark theme', () => {
        mockMatchMedia.mockReturnValue({ matches: true });
        const setAttribute = jest.fn();
        document.body.setAttribute = setAttribute;

        global.window.onload();

        expect(setAttribute).toHaveBeenCalledWith('data-bs-theme', 'dark');
    });

    it('should not set dark theme', () => {
        mockMatchMedia.mockReturnValue({ matches: false });
        const setAttribute = jest.fn();
        document.body.setAttribute = setAttribute;

        global.window.onload();

        expect(setAttribute).not.toHaveBeenCalled();
    });
});