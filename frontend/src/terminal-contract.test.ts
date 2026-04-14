import {
  createTerminalSession,
  deleteTerminalSession,
  getCodeServerStatus,
  getTerminalSession,
} from './api/endpoints';
import {
  mockCreateTerminalSession,
  mockDeleteTerminalSession,
  mockGetCodeServerStatus,
  mockGetTerminalSession,
} from './api/mock';
import type { CodeServerStatus, TerminalSession } from './types';

type TerminalSessionLoader = () => Promise<TerminalSession>;
type MockTerminalSessionLoader = () => TerminalSession;
type CodeServerStatusLoader = () => Promise<CodeServerStatus>;
type MockCodeServerStatusLoader = () => CodeServerStatus;

const _getTerminalSession: TerminalSessionLoader = getTerminalSession;
const _createTerminalSession: TerminalSessionLoader = createTerminalSession;
const _deleteTerminalSession: TerminalSessionLoader = deleteTerminalSession;
const _mockGetTerminalSession: MockTerminalSessionLoader = mockGetTerminalSession;
const _mockCreateTerminalSession: MockTerminalSessionLoader = mockCreateTerminalSession;
const _mockDeleteTerminalSession: MockTerminalSessionLoader = mockDeleteTerminalSession;
const _getCodeServerStatus: CodeServerStatusLoader = getCodeServerStatus;
const _mockGetCodeServerStatus: MockCodeServerStatusLoader = mockGetCodeServerStatus;

const _terminalSessionStatusValues: TerminalSession['status'][] = [
  'idle',
  'starting',
  'running',
  'stopping',
  'failed',
];

const _terminalSessionContract: TerminalSession = {
  session_id: 'term-1',
  provider: 'ttyd',
  target_kind: 'daemon-host',
  status: 'running',
  created_at: '2026-04-13T16:00:00Z',
  started_at: '2026-04-13T16:00:01Z',
  closed_at: null,
  terminal_url: 'http://127.0.0.1:7681',
  detail: null,
};

const _codeServerStatuses: CodeServerStatus['status'][] = ['starting', 'ready', 'unavailable'];

const _codeServerContract: CodeServerStatus = {
  status: 'ready',
  workspace_dir: '/workspace/project-a',
  detail: null,
  managed: true,
};

void [
  _getTerminalSession,
  _createTerminalSession,
  _deleteTerminalSession,
  _mockGetTerminalSession,
  _mockCreateTerminalSession,
  _mockDeleteTerminalSession,
  _getCodeServerStatus,
  _mockGetCodeServerStatus,
  _terminalSessionStatusValues,
  _terminalSessionContract,
  _codeServerStatuses,
  _codeServerContract,
];
