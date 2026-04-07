interface Props {
  size?: 'sm' | 'md' | 'lg';
  message?: string;
}

function LoadingSpinner({ size = 'md', message }: Props) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className="flex flex-col items-center justify-center gap-2">
      <div
        className={`${sizeClasses[size]} border-2 border-gray-300 border-t-[var(--accent)] rounded-full animate-spin`}
      />
      {message && <span className="text-sm text-gray-500">{message}</span>}
    </div>
  );
}

export default LoadingSpinner;