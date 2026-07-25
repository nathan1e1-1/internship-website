import { render, screen, fireEvent } from '@testing-library/react';
import { FilterBar } from '../FilterBar';

const filters = {
  companies: ['Acme', 'Beta'],
  locations: ['Remote', 'NYC'],
  types: ['internship', 'fellowship'],
  workTypes: ['remote', 'hybrid', 'in-person'],
};

describe('FilterBar', () => {
  it('renders all filter dropdowns', () => {
    render(<FilterBar filters={filters} onChange={() => {}} onClear={() => {}} />);
    expect(screen.getByLabelText(/company/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/location/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^Type$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/work type/i)).toBeInTheDocument();
  });

  it('calls onChange when a filter is selected', () => {
    const onChange = jest.fn();
    render(<FilterBar filters={filters} onChange={onChange} onClear={() => {}} />);
    fireEvent.change(screen.getByLabelText(/company/i), { target: { value: 'Acme' } });
    expect(onChange).toHaveBeenCalledWith(expect.objectContaining({ company: 'Acme' }));
  });
});
