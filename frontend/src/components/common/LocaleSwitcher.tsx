import { Globe } from 'lucide-react';
import { useLocaleSwitcher, useT } from '../../i18n';

function LocaleSwitcher() {
  const t = useT();
  const { locale, setLocale } = useLocaleSwitcher();

  return (
    <div className="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white px-2 py-1 shadow-sm">
      <Globe size={16} className="text-gray-500" />
      <span className="sr-only">{t('common.language')}</span>
      <button
        type="button"
        onClick={() => setLocale('en')}
        aria-pressed={locale === 'en'}
        className={[
          'rounded-full px-3 py-1 text-xs font-semibold transition',
          locale === 'en'
            ? 'bg-[var(--accent)] text-white'
            : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900',
        ].join(' ')}
      >
        {t('common.english')}
      </button>
      <button
        type="button"
        onClick={() => setLocale('zh')}
        aria-pressed={locale === 'zh'}
        className={[
          'rounded-full px-3 py-1 text-xs font-semibold transition',
          locale === 'zh'
            ? 'bg-[var(--accent)] text-white'
            : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900',
        ].join(' ')}
      >
        {t('common.chinese')}
      </button>
    </div>
  );
}

export default LocaleSwitcher;
