import React, { useEffect, useRef } from 'react';
import { Empty, Spin } from 'antd';
import ChatMessage from './ChatMessage';
import type { ChatMessage as ChatMessageType } from '@/types';

interface ChatMessageListProps {
  messages: ChatMessageType[];
  loading?: boolean;
  onCopyMessage?: (content: string) => void;
  className?: string;
}

const ChatMessageList: React.FC<ChatMessageListProps> = ({
  messages,
  loading = false,
  onCopyMessage,
  className = ''
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleCopyMessage = (content: string) => {
    if (onCopyMessage) {
      onCopyMessage(content);
    } else {
      navigator.clipboard.writeText(content);
    }
  };

  if (messages.length === 0 && !loading) {
    return (
      <div className={`flex items-center justify-center h-full ${className}`}>
        <Empty
          description="暂无对话消息"
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        />
      </div>
    );
  }

  return (
    <div 
      ref={containerRef}
      className={`flex flex-col h-full overflow-hidden ${className}`}
    >
      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto px-4 py-2">
        <div className="space-y-2">
          {messages.map((message) => (
            <ChatMessage
              key={message.id}
              message={message}
              onCopy={handleCopyMessage}
            />
          ))}
          
          {/* 加载指示器 */}
          {loading && (
            <div className="flex justify-center py-4">
              <Spin size="small" />
            </div>
          )}
          
          {/* 滚动锚点 */}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  );
};

export default ChatMessageList; 