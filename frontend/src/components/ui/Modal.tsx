import { useCallback, useEffect, useState, type ReactNode } from 'react';
import { X } from 'lucide-react';
import useFocusTrap from '../../hooks/useFocusTrap';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  title?: string | null;
  children: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showCloseButton?: boolean;
  closeOnBackdropClick?: boolean;
}

const sizeClasses: Record<NonNullable<Props['size']>, string> = {
  sm: 'max-w-sm',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
};

export default function Modal({
  isOpen,
  onClose,
  title = null,
  children,
  size = 'md',
  showCloseButton = true,
  closeOnBackdropClick = true,
}: Props) {
  const [isClosing, setIsClosing] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const dialogRef = useFocusTrap<HTMLDivElement>(isOpen && isVisible);

  // Handle open/close with animation
  useEffect(() => {
    if (isOpen) {
      setIsClosing(false);
      // Small delay to allow the DOM to mount before starting the enter transition
      const showTimeout = setTimeout(() => setIsVisible(true), 10);
      return () => clearTimeout(showTimeout);
    }
  }, [isOpen]);

  // Handle escape key
  useEffect(() => {
    if (!isOpen) {
      return;
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        handleClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  const handleClose = useCallback(() => {
    setIsClosing(true);
    setIsVisible(false);
  }, []);

  const handleTransitionEnd = useCallback(() => {
    if (isClosing) {
      onClose();
      setIsClosing(false);
    }
  }, [isClosing, onClose]);

  const handleBackdropClick = useCallback(
    (event: React.MouseEvent<HTMLDivElement>) => {
      if (closeOnBackdropClick && event.target === event.currentTarget) {
        handleClose();
      }
    },
    [closeOnBackdropClick, handleClose]
  );

  if (!isOpen && !isClosing) {
    return null;
  }

  const backdropOpacity = isVisible && !isClosing ? 'opacity-100' : 'opacity-0';
  const dialogTransform = isVisible && !isClosing ? 'scale-100 opacity-100' : 'scale-[0.96] opacity-0';

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/45 transition-opacity duration-150 ${backdropOpacity}`}
      onClick={handleBackdropClick}
      onTransitionEnd={handleTransitionEnd}
      role="presentation"
    >
      <div
        ref={dialogRef}
        className={`w-full ${sizeClasses[size]} max-h-[90vh] overflow-auto rounded-2xl border border-[var(--border)] bg-[var(--surface)] shadow-2xl transition-all duration-200 ease-out ${dialogTransform}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? 'modal-title' : undefined}
        onClick={(e) => e.stopPropagation()}
      >
        {title !== null && (
          <div className="flex items-center justify-between border-b border-[var(--border)] px-6 py-4">
            <h2 id="modal-title" className="text-lg font-semibold text-[var(--text)]">
              {title}
            </h2>
            {showCloseButton && (
              <button
                type="button"
                onClick={handleClose}
                className="rounded-lg p-1 text-[var(--muted-foreground)] transition hover:bg-[var(--bg-secondary)] hover:text-[var(--text)]"
                aria-label="Close"
              >
                <X size={20} />
              </button>
            )}
          </div>
        )}
        {title === null && showCloseButton && (
          <div className="flex justify-end px-6 pt-4">
            <button
              type="button"
              onClick={handleClose}
              className="rounded-lg p-1 text-[var(--muted-foreground)] transition hover:bg-[var(--bg-secondary)] hover:text-[var(--text)]"
              aria-label="Close"
            >
              <X size={20} />
            </button>
          </div>
        )}
        <div className="px-6 py-4">{children}</div>
      </div>
    </div>
  );
}
