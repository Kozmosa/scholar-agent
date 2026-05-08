import { useState } from 'react';
import type { MessageItem } from '../../types';

function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString();
}

export function SystemEventBlock({ message }: { message: MessageItem }) {
  const content = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);
  return (
    <div className="my-2 flex justify-center">
      <div className="flex items-center gap-2 rounded-lg border-l-2 border-[var(--apple-blue)] bg-[var(--bg-secondary)] px-3 py-1.5">
        <span className="text-xs text-[var(--text-secondary)]">{content}</span>
        <span className="text-xs text-[var(--text-tertiary)]">{formatTime(message.metadata.timestamp)}</span>
      </div>
    </div>
  );
}

export function UserMessage({ message }: { message: MessageItem }) {
  const content = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);
  return (
    <div className="my-2 flex justify-end">
      <div className="max-w-[80%] rounded-2xl rounded-tr-sm border border-[var(--apple-blue)]/20 bg-[var(--apple-blue)]/10 px-4 py-2">
        <pre className="whitespace-pre-wrap break-words font-sans text-sm text-[var(--apple-blue)]">{content}</pre>
        <div className="mt-1 text-right text-[10px] text-[var(--text-tertiary)]">{formatTime(message.metadata.timestamp)}</div>
      </div>
    </div>
  );
}

export function AssistantMessage({ message }: { message: MessageItem }) {
  const content = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);
  return (
    <div className="my-2 flex justify-start">
      <div className="max-w-[80%] rounded-2xl rounded-tl-sm bg-[var(--bg-secondary)] px-4 py-2">
        <pre className="whitespace-pre-wrap break-words font-sans text-sm text-[var(--text)]">{content}</pre>
        <div className="mt-1 text-right text-[10px] text-[var(--text-tertiary)]">{formatTime(message.metadata.timestamp)}</div>
      </div>
    </div>
  );
}

export function ThinkingBlock({ message }: { message: MessageItem }) {
  const [isOpen, setIsOpen] = useState(false);
  const content = typeof message.content === 'string' ? message.content : '';
  return (
    <div className="my-1 flex flex-col items-start">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1 rounded-lg border-l-2 border-[var(--text-tertiary)] bg-[var(--bg-secondary)] px-3 py-1.5 text-xs text-[var(--text-secondary)] transition hover:bg-[var(--border)]"
      >
        {isOpen ? '▾' : '▸'} Thinking...
      </button>
      {isOpen && (
        <div className="mt-1 w-full rounded-lg border-l-2 border-[var(--text-tertiary)] bg-[var(--bg-secondary)] px-3 py-2">
          <pre className="whitespace-pre-wrap break-words font-sans text-xs text-[var(--text-secondary)]">{content || ''}</pre>
        </div>
      )}
    </div>
  );
}

export function ToolCallBlock({ message }: { message: MessageItem }) {
  const [isOpen, setIsOpen] = useState(false);
  const content = typeof message.content === 'object' ? message.content : {};
  const name = String((content as Record<string, unknown>).name || 'unknown');
  return (
    <div className="my-1 flex flex-col items-start">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1 rounded-lg border-l-2 border-[var(--apple-blue)] bg-[var(--bg-secondary)] px-3 py-1.5 text-xs text-[var(--text-secondary)] transition hover:bg-[var(--border)]"
      >
        {isOpen ? '▾' : '▸'} Tool: {name}
      </button>
      {isOpen && (
        <div className="mt-1 w-full rounded-lg border-l-2 border-[var(--apple-blue)] bg-[var(--bg-secondary)] px-3 py-2">
          <pre className="whitespace-pre-wrap break-words font-mono text-xs text-[var(--text-secondary)]">{JSON.stringify(content, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export function ToolResultBlock({ message }: { message: MessageItem }) {
  const [isOpen, setIsOpen] = useState(false);
  const content = typeof message.content === 'object' ? message.content : {};
  return (
    <div className="my-1 flex flex-col items-start pl-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1 rounded-lg border-l-2 border-[#22c55e] bg-[var(--bg-secondary)] px-3 py-1.5 text-xs text-[var(--text-secondary)] transition hover:bg-[var(--border)]"
      >
        {isOpen ? '▾' : '▸'} Result
      </button>
      {isOpen && (
        <div className="mt-1 w-full rounded-lg border-l-2 border-[#22c55e] bg-[var(--bg-secondary)] px-3 py-2">
          <pre className="whitespace-pre-wrap break-words font-mono text-xs text-[var(--text-secondary)]">{JSON.stringify(content, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export function MessageBlock({ message }: { message: MessageItem }) {
  switch (message.type) {
    case 'system_event':
      return <SystemEventBlock message={message} />;
    case 'user':
      return <UserMessage message={message} />;
    case 'assistant':
      return <AssistantMessage message={message} />;
    case 'thinking':
      return <ThinkingBlock message={message} />;
    case 'tool_call':
      return <ToolCallBlock message={message} />;
    case 'tool_result':
      return <ToolResultBlock message={message} />;
    default:
      return <AssistantMessage message={message} />;
  }
}
