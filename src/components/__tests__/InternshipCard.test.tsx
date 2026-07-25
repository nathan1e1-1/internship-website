import { render, screen } from '@testing-library/react';
import { InternshipCard } from '../InternshipCard';
import { Internship } from '@/lib/types';

const mockInternship: Internship = {
  id: 'test-1',
  title: 'SWE Intern',
  company: 'Acme',
  type: 'internship',
  category: 'general',
  url: 'https://acme.com',
  location: 'Remote',
  work_type: 'remote',
  date_posted: '2025-07-01',
  deadline: '2025-08-15',
  date_scraped: '2025-07-24',
};

describe('InternshipCard', () => {
  it('renders title, company, location, and apply button', () => {
    render(<InternshipCard internship={mockInternship} />);
    expect(screen.getByText('SWE Intern')).toBeInTheDocument();
    expect(screen.getByText(/@ Acme/)).toBeInTheDocument();
    expect(screen.getByText('Remote')).toBeInTheDocument();
    expect(screen.getByText('Apply')).toHaveAttribute('href', 'https://acme.com');
  });
});
