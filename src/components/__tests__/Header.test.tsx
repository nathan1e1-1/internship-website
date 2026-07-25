import { render, screen } from '@testing-library/react';
import { Header } from '../Header';

describe('Header', () => {
  it('renders title and subtitle', () => {
    render(<Header lastUpdated="2025-07-24" />);
    expect(screen.getByText('Internship Board')).toBeInTheDocument();
    expect(screen.getByText(/updated/i)).toBeInTheDocument();
  });
});
