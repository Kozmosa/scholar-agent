import { useRef, useEffect } from 'react';
import type { MessageItem } from '../../types';
import { MessageBlock } from './MessageBlocks';

interface Props {
  messages: MessageItem[];
}

export default function MessageStream({ messages }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-gray-400">
        No messages yet
      </div>
    );
  }

  return (
    <div className="flex flex-col px-4 py-2">
      {messages.map((msg) => (
        <MessageBlock key={msg.id} message={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
