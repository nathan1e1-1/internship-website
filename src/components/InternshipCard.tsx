import { Internship } from '@/lib/types';

interface InternshipCardProps {
  internship: Internship;
}

export function InternshipCard({ internship }: InternshipCardProps) {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-semibold text-lg">{internship.title}</h3>
          <p className="text-gray-600">{internship.company}</p>
        </div>
        <span className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-600">
          {internship.work_type}
        </span>
      </div>
      <div className="mt-2 text-sm text-gray-500">
        <p>{internship.location}</p>
        {internship.date_posted && <p>Posted: {internship.date_posted}</p>}
        {internship.deadline ? (
          <p>Deadline: {internship.deadline}</p>
        ) : (
          <p>Deadline: TBD</p>
        )}
      </div>
      <a
        href={internship.url}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-3 inline-block px-4 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
      >
        Apply
      </a>
    </div>
  );
}
