import TerminalBenchCardView from './TerminalBenchCardView';
import { useTerminalBenchSession } from './useTerminalBenchSession';
import type { EnvironmentRecord } from '../../types';

interface Props {
  selectedEnvironment: EnvironmentRecord | null;
}

function TerminalBenchCard({ selectedEnvironment }: Props) {
  const state = useTerminalBenchSession();

  return (
    <TerminalBenchCardView
      {...state}
      selectedEnvironmentSummary={
        selectedEnvironment ? `${selectedEnvironment.alias} · ${selectedEnvironment.display_name}` : null
      }
      canStart={state.canStart && selectedEnvironment !== null}
    />
  );
}

export default TerminalBenchCard;
