import TerminalBenchCardView from './TerminalBenchCardView';
import { useTerminalBenchSession } from './useTerminalBenchSession';

function TerminalBenchCard() {
  const state = useTerminalBenchSession();

  return <TerminalBenchCardView {...state} />;
}

export default TerminalBenchCard;
