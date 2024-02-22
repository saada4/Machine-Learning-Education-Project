import { render, screen } from '@testing-library/react';
import App from './App';

test('Checks if "Learn React" is on the page. DUMMY CASE', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
