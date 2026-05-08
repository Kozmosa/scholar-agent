import { useState } from 'react';
import type { MessageItem } from '../../types';

function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString();
}

export function SystemEventBlock({ message }: { message: MessageItem }) {
  const content = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);
  return (
    <div className="my-2 text-center text-xs text-gray-500">
      <span className="rounded-full bg-gray-800 px-3 py-1">{content}</span>
      <span className="ml-2 text-gray-600">{formatTime(message.metadata.timestamp)}</span>
    </div>
  );
}

export function UserMessage({ message }: { message: MessageItem }) {
  const content = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);
  return (
    <div className="my-2 flex justify-end">
      <div className="max-w-[80%] rounded-2xl rounded-tr-sm bg-blue-600/20 px-4 py-2 text-sm text-blue-100">
        <pre className="whitespace-pre-wrap font-sans">{content}</pre>
      </div>
    </div>
  );
}

export function AssistantMessage({ message }: { message: MessageItem }) {
  const content = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);
  return (
    <div className="my-2 flex justify-start">
      <div className="max-w-[80%] rounded-2xl rounded-tl-sm bg-white/[0.03] px-4 py-2 text-sm text-gray-100">
        <pre className="whitespace-pre-wrap font-sans">{content}</pre>
      </div>
    </div>
  );
}

export function ThinkingBlock({ message }: { message: MessageItem }) {
  const [isOpen, setIsOpen] = useState(false);
  const content = typeof message.content === 'string' ? message.content : '';
  return (
    <div className="my-1 flex justify-start">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="rounded-lg border border-white/10 bg-white/[0.02] px-3 py-1.5 text-xs text-gray-400 transition hover:bg-white/[0.05]"
      >
        {isOpen ? '▾' : '▸'} Thinking...
      </button>
      {isOpen && (
        <div className="mt-1 max-w-[80%] rounded-lg border border-white/10 bg-white/[0.02] px-3 py-2 text-xs text-gray-400">
          <pre className="whitespace-pre-wrap font-sans">{content || ''}</pre>
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
    <div className="my-1 flex justify-start">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="rounded-lg border border-white/10 bg-white/[0.02] px-3 py-1.5 text-xs text-gray-400 transition hover:bg-white/[0.05]"
      >
        {isOpen ? '▾' : '▸'} Tool: {name}
      </button>
      {isOpen && (
        <div className="mt-1 max-w-[80%] rounded-lg border border-white/10 bg-white/[0.02] px-3 py-2 text-xs text-gray-400">
          <pre className="whitespace-pre-wrap font-mono">{JSON.stringify(content, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export function ToolResultBlock({ message }: { message: MessageItem }) {
  const [isOpen, setIsOpen] = useState(false);
  const content = typeof message.content === 'object' ? message.content : {};
  return (
    <div className="my-1 flex justify-start pl-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="rounded-lg border border-white/10 bg-white/[0.02] px-3 py-1.5 text-xs text-gray-500 transition hover:bg-white/[0.05]"
      >
        {isOpen ? '▾' : '▸'} Result
      </button>
      {isOpen && (
        <div className="mt-1 max-w-[80%] rounded-lg border border-white/10 bg-white/[0.02] px-3 py-2 text-xs text-gray-500">
          <pre className="whitespace-pre-wrap font-mono">{JSON.stringify(content, null, 2)}</pre>
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
