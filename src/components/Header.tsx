interface HeaderProps {
  lastUpdated: string;
}

export function Header({ lastUpdated }: HeaderProps) {
  return (
    <header className="py-8 px-4">
      <h1 className="text-3xl font-bold text-gray-900">Internship Board</h1>
      <p className="text-sm text-gray-500 mt-1">
        Aggregated opportunities for students · Updated {lastUpdated}
      </p>
    </header>
  );
}
