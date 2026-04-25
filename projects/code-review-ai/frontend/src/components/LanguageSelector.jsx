import { ChevronDown } from 'lucide-react';

const LANGUAGES = [
  { value: 'python',     label: 'Python',      monaco: 'python' },
  { value: 'javascript', label: 'JavaScript',   monaco: 'javascript' },
  { value: 'typescript', label: 'TypeScript',   monaco: 'typescript' },
  { value: 'java',       label: 'Java',         monaco: 'java' },
  { value: 'c',          label: 'C',            monaco: 'c' },
  { value: 'cpp',        label: 'C++',          monaco: 'cpp' },
  { value: 'csharp',     label: 'C#',           monaco: 'csharp' },
  { value: 'go',         label: 'Go',           monaco: 'go' },
  { value: 'rust',       label: 'Rust',         monaco: 'rust' },
  { value: 'swift',      label: 'Swift',        monaco: 'swift' },
  { value: 'kotlin',     label: 'Kotlin',       monaco: 'kotlin' },
  { value: 'ruby',       label: 'Ruby',         monaco: 'ruby' },
  { value: 'php',        label: 'PHP',          monaco: 'php' },
  { value: 'sql',        label: 'SQL',          monaco: 'sql' },
  { value: 'bash',       label: 'Bash/Shell',   monaco: 'shell' },
];

export { LANGUAGES };

export default function LanguageSelector({ value, onChange }) {
  return (
    <div className="lang-select-wrapper">
      <select
        className="lang-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.value} value={lang.value}>
            {lang.label}
          </option>
        ))}
      </select>
      <ChevronDown size={13} className="lang-select-chevron" />
    </div>
  );
}
