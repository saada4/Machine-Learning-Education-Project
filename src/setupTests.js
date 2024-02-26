// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

it('renders welcome message', () => {
    render(<App />);
    expect(screen.getByText('Learn React')).toBeInTheDocument();
});

describe('App-logo', () => {
    test('App-logo must have src = "/logo.svg" and alt = "logo"', () => {
        render(<App />);
        const logo = screen.getByRole('img');
        expect(logo).toHaveAttribute('src', 'logo.svg');
        expect(logo).toHaveAttribute('alt', 'logo');
    });
});

it('expects link to work', () => {
    render(<App />);
    expect(screen.getByRole('link')).toHaveAttribute('href', 'https://reactjs.org');
});


