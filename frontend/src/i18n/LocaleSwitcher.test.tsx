import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it } from 'vitest';
import LocaleSwitcher from '../components/common/LocaleSwitcher';
import { LocaleProvider, useI18n, useT } from './index';

function LocaleHarness() {
  const { locale } = useI18n();
  const t = useT();

  return (
    <div>
      <LocaleSwitcher />
      <p data-testid="locale-value">{locale}</p>
      <p data-testid="terminal-label">{t('navigation.terminal.label')}</p>
    </div>
  );
}

describe('LocaleSwitcher', () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it('switches between English and Chinese and persists the selection', async () => {
    const user = userEvent.setup();

    render(
      <LocaleProvider initialLocale="en">
        <LocaleHarness />
      </LocaleProvider>
    );

    expect(screen.getByRole('button', { name: 'English' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByTestId('terminal-label')).toHaveTextContent('Terminal');

    await user.click(screen.getByRole('button', { name: '中文' }));

    expect(screen.getByTestId('locale-value')).toHaveTextContent('zh');
    expect(screen.getByTestId('terminal-label')).toHaveTextContent('终端');
    expect(window.localStorage.getItem('scholar-agent:locale')).toBe('zh');
  });

  it('restores the stored locale on mount', () => {
    window.localStorage.setItem('scholar-agent:locale', 'zh');

    render(
      <LocaleProvider>
        <LocaleHarness />
      </LocaleProvider>
    );

    expect(screen.getByTestId('locale-value')).toHaveTextContent('zh');
    expect(screen.getByTestId('terminal-label')).toHaveTextContent('终端');
  });
});
