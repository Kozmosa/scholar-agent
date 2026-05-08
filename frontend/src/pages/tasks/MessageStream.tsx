import { useRef, useEffect, useCallback } from 'react';
import type { MessageItem } from '../../types';
import { MessageBlock } from './MessageBlocks';

interface Props {
  messages: MessageItem[];
}

export default function MessageStream({ messages }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const shouldScrollRef = useRef(true);

  const handleScroll = useCallback(() => {
    const container = containerRef.current;
    if (!container) return;
    const threshold = 80;
    const distanceFromBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight;
    shouldScrollRef.current = distanceFromBottom < threshold;
  }, []);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  useEffect(() => {
    if (shouldScrollRef.current) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-gray-400">
        No messages yet
      </div>
    );
  }

  return (
    <div ref={containerRef} className="flex flex-col overflow-auto px-4 py-2">
      {messages.map((msg) => (
        <MessageBlock key={msg.id} message={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
