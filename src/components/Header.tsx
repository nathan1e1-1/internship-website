import { ThemeToggle } from './ThemeToggle';

interface HeaderProps {
  lastUpdated: string;
}

export function Header({ lastUpdated }: HeaderProps) {
  return (
    <header className="py-8 px-4 flex items-start justify-between gap-4">
      <div>
        <h1 className="text-3xl font-bold text-foreground tracking-tight">Internship Board</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Aggregated opportunities for students · Updated {lastUpdated}
        </p>
      </div>
      <ThemeToggle />
    </header>
  );
}
