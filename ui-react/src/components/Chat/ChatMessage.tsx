import React from 'react';
import { Avatar, Typography, Card, Tag, Tooltip, Button } from 'antd';
import { CopyOutlined, UserOutlined, RobotOutlined, ToolOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import type { ChatMessage as ChatMessageType } from '@/types';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

const { Text, Paragraph } = Typography;

interface ChatMessageProps {
  message: ChatMessageType;
  onCopy?: (content: string) => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onCopy }) => {
  const { type, content, timestamp } = message;

  const getMessageIcon = () => {
    switch (type) {
      case 'user':
        return <UserOutlined className="text-blue-500" />;
      case 'agent':
        return <RobotOutlined className="text-green-500" />;
      case 'tool':
        return <ToolOutlined className="text-orange-500" />;
      case 'error':
        return <ExclamationCircleOutlined className="text-red-500" />;
      case 'system':
        return <RobotOutlined className="text-gray-500" />;
      default:
        return <UserOutlined />;
    }
  };

  const getMessageColor = () => {
    switch (type) {
      case 'user':
        return 'blue';
      case 'agent':
        return 'green';
      case 'tool':
        return 'orange';
      case 'error':
        return 'red';
      case 'system':
        return 'default';
      default:
        return 'default';
    }
  };

  const getMessageTitle = () => {
    switch (type) {
      case 'user':
        return '用户';
      case 'agent':
        return 'Agent';
      case 'tool':
        return '工具执行';
      case 'error':
        return '错误';
      case 'system':
        return '系统';
      default:
        return '未知';
    }
  };

  const handleCopy = () => {
    if (onCopy) {
      onCopy(content);
    } else {
      navigator.clipboard.writeText(content);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const renderMarkdown = (content: string) => {
    return (
      <ReactMarkdown
        components={{
          code({ inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '');
            const language = match ? match[1] : '';

            if (!inline && language) {
              return (
                <SyntaxHighlighter
                  style={oneLight}
                  language={language}
                  PreTag="div"
                  {...props}
                >
                  {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
              );
            }

            return (
              <code className="bg-gray-100 px-1 py-0.5 rounded text-sm" {...props}>
                {children}
              </code>
            );
          },
          p: ({ children }: any) => <Paragraph className="mb-2 last:mb-0">{children}</Paragraph>,
          h1: ({ children }: any) => <Typography.Title level={1}>{children}</Typography.Title>,
          h2: ({ children }: any) => <Typography.Title level={2}>{children}</Typography.Title>,
          h3: ({ children }: any) => <Typography.Title level={3}>{children}</Typography.Title>,
          h4: ({ children }: any) => <Typography.Title level={4}>{children}</Typography.Title>,
          h5: ({ children }: any) => <Typography.Title level={5}>{children}</Typography.Title>,
          ul: ({ children }: any) => <ul className="list-disc list-inside ml-4 mb-2">{children}</ul>,
          ol: ({ children }: any) => <ol className="list-decimal list-inside ml-4 mb-2">{children}</ol>,
          li: ({ children }: any) => <li className="mb-1">{children}</li>,
          blockquote: ({ children }: any) => (
            <blockquote className="border-l-4 border-blue-500 pl-4 py-2 bg-blue-50 rounded-r">
              {children}
            </blockquote>
          ),
          table: ({ children }: any) => (
            <div className="overflow-x-auto">
              <table className="min-w-full border-collapse border border-gray-300">
                {children}
              </table>
            </div>
          ),
          th: ({ children }: any) => (
            <th className="border border-gray-300 px-4 py-2 bg-gray-100 font-semibold">
              {children}
            </th>
          ),
          td: ({ children }: any) => (
            <td className="border border-gray-300 px-4 py-2">{children}</td>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    );
  };

  return (
    <div className={`mb-4 flex ${type === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[80%] ${type === 'user' ? 'order-2' : 'order-1'}`}>
        <Card
          className={`${
            type === 'user' 
              ? 'bg-blue-50 border-blue-200' 
              : type === 'error'
              ? 'bg-red-50 border-red-200'
              : 'bg-white border-gray-200'
          }`}
          size="small"
          bodyStyle={{ padding: '12px 16px' }}
        >
          {/* 消息头部 */}
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <Avatar 
                size="small" 
                icon={getMessageIcon()} 
                className={`bg-${getMessageColor()}-100`}
              />
              <Tag color={getMessageColor()}>
                {getMessageTitle()}
              </Tag>
              <Text type="secondary" className="text-xs">
                {formatTimestamp(timestamp)}
              </Text>
            </div>
            <Tooltip title="复制消息">
              <Button 
                type="text" 
                size="small" 
                icon={<CopyOutlined />}
                onClick={handleCopy}
                className="text-gray-400 hover:text-gray-600"
              />
            </Tooltip>
          </div>

          {/* 消息内容 */}
          <div className="message-content">
            {type === 'user' ? (
              <Paragraph className="mb-0 whitespace-pre-wrap">
                {content}
              </Paragraph>
            ) : (
              renderMarkdown(content)
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ChatMessage; 