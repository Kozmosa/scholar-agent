import { FitAddon } from '@xterm/addon-fit';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';
import { useEffect, useRef, useState } from 'react';
import type { TerminalSessionStatus } from '../../types';

type SocketStatus = 'idle' | 'connecting' | 'connected' | 'disconnected' | 'error';

interface Props {
  sessionId: string | null;
  terminalWsUrl: string | null;
  status: TerminalSessionStatus;
  onDisconnected?: () => void;
}

interface SocketOutputMessage {
  type: 'output';
  data: string;
}

interface SocketStatusMessage {
  type: 'status';
  status: 'exited';
  return_code: number;
}

type SocketMessage = SocketOutputMessage | SocketStatusMessage;

function resolveWebSocketUrl(url: string): string {
  const resolved = new URL(url, window.location.origin);
  if (resolved.protocol === 'http:') {
    resolved.protocol = 'ws:';
  } else if (resolved.protocol === 'https:') {
    resolved.protocol = 'wss:';
  }
  return resolved.toString();
}

function isSocketMessage(value: unknown): value is SocketMessage {
  if (!value || typeof value !== 'object') {
    return false;
  }

  const record = value as Record<string, unknown>;
  if (record.type === 'output') {
    return typeof record.data === 'string';
  }

  if (record.type === 'status') {
    return record.status === 'exited' && typeof record.return_code === 'number';
  }

  return false;
}

function TerminalSessionConsole({ sessionId, terminalWsUrl, status, onDisconnected }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const onDisconnectedRef = useRef(onDisconnected);
  const disconnectNotifiedRef = useRef(false);
  const [socketStatus, setSocketStatus] = useState<SocketStatus>('idle');
  const displaySocketStatus =
    status !== 'running' || terminalWsUrl === null
      ? 'idle'
      : socketStatus === 'idle'
        ? 'connecting'
        : socketStatus;

  useEffect(() => {
    onDisconnectedRef.current = onDisconnected;
  }, [onDisconnected]);

  useEffect(() => {
    if (status !== 'running' || terminalWsUrl === null || containerRef.current === null) {
      disconnectNotifiedRef.current = false;
      return;
    }

    const terminal = new Terminal({
      convertEol: true,
      cursorBlink: true,
      fontFamily: 'var(--mono)',
      fontSize: 13,
      scrollback: 2000,
      theme: {
        background: '#0b1020',
        foreground: '#e5eefc',
        cursor: '#c084fc',
        selectionBackground: '#334155',
      },
    });
    const fitAddon = new FitAddon();
    terminal.loadAddon(fitAddon);
    terminal.open(containerRef.current);
    terminal.focus();

    const socket = new WebSocket(resolveWebSocketUrl(terminalWsUrl));
    let disposed = false;

    const resizeDisposable = terminal.onResize(({ cols, rows }) => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'resize', cols, rows }));
      }
    });

    const inputDisposable = terminal.onData((data) => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'input', data }));
      }
    });

    const fitTerminal = () => {
      try {
        fitAddon.fit();
      } catch {
        // ignore fit failures while the container is hidden or resizing
      }
    };

    const notifyDisconnected = () => {
      if (disconnectNotifiedRef.current) {
        return;
      }
      disconnectNotifiedRef.current = true;
      onDisconnectedRef.current?.();
    };

    const handleWindowResize = () => {
      fitTerminal();
    };

    socket.onopen = () => {
      if (disposed) {
        return;
      }
      setSocketStatus('connected');
      fitTerminal();
      socket.send(JSON.stringify({ type: 'resize', cols: terminal.cols, rows: terminal.rows }));
    };

    socket.onmessage = (event) => {
      if (disposed || typeof event.data !== 'string') {
        return;
      }

      try {
        const payload: unknown = JSON.parse(event.data) as unknown;
        if (!isSocketMessage(payload)) {
          terminal.write(event.data);
          return;
        }

        if (payload.type === 'output') {
          terminal.write(payload.data);
          return;
        }

        if (payload.type === 'status' && payload.status === 'exited') {
          terminal.writeln('');
          terminal.writeln(`Session exited with code ${payload.return_code}`);
          setSocketStatus('disconnected');
          notifyDisconnected();
        }
        return;
      } catch {
        terminal.write(event.data);
      }
    };

    socket.onerror = () => {
      if (!disposed) {
        setSocketStatus('error');
      }
    };

    socket.onclose = () => {
      if (!disposed) {
        setSocketStatus((current) => (current === 'connected' ? 'disconnected' : current));
        notifyDisconnected();
      }
    };

    window.addEventListener('resize', handleWindowResize);
    fitTerminal();

    return () => {
      disposed = true;
      window.removeEventListener('resize', handleWindowResize);
      resizeDisposable.dispose();
      inputDisposable.dispose();
      socket.close();
      terminal.dispose();
      disconnectNotifiedRef.current = false;
    };
  }, [sessionId, status, terminalWsUrl]);

  if (status !== 'running' || terminalWsUrl === null) {
    return (
      <div className="rounded-2xl border border-dashed border-gray-300 bg-gray-50 p-6 text-sm text-gray-500">
        Start a terminal session to open the xterm console.
      </div>
    );
  }

  return (
    <section className="space-y-3 rounded-2xl border border-gray-200 bg-gray-50 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="space-y-1">
          <h3 className="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--accent)]">
            Interactive terminal
          </h3>
          <p className="text-sm text-gray-600">
            WebSocket session: <code className="rounded bg-gray-100 px-1.5 py-0.5">{sessionId ?? 'n/a'}</code>
          </p>
        </div>
        <div className="rounded-full border border-gray-200 bg-white px-3 py-1 text-xs font-medium text-gray-700">
          Connection: {displaySocketStatus}
        </div>
      </div>

      <div
        ref={containerRef}
        className="min-h-[480px] overflow-hidden rounded-2xl border border-gray-800 bg-[#0b1020]"
      />
    </section>
  );
}

export default TerminalSessionConsole;
