import { render, screen } from '@testing-library/react';
import { InternshipList } from '../InternshipList';
import { Internship } from '@/lib/types';

const mockList: Internship[] = [
  {
    id: 'test-1',
    title: 'SWE Intern',
    company: 'Acme',
    type: 'internship',
    category: 'general',
    url: 'https://acme.com',
    location: 'Remote',
    work_type: 'remote',
    date_posted: '2025-07-01',
    date_scraped: '2025-07-24',
  },
];

describe('InternshipList', () => {
  it('renders list of internships', () => {
    render(<InternshipList internships={mockList} />);
    expect(screen.getByText('SWE Intern')).toBeInTheDocument();
    expect(screen.getByText(/@ Acme/)).toBeInTheDocument();
  });

  it('shows empty state when no internships', () => {
    render(<InternshipList internships={[]} />);
    expect(screen.getByText(/no internships found/i)).toBeInTheDocument();
  });
});
