import React from 'react';
import { Spin, Typography, Tag, Button, Image } from 'antd';
import { CopyOutlined, InfoCircleOutlined, WarningOutlined, CloseCircleOutlined } from '@ant-design/icons';
import type { ChatMessage } from '@/types';
import './ChatInterface.css';

const { Text, Paragraph } = Typography;

interface ChatMessageListProps {
  messages: ChatMessage[];
  loading?: boolean;
}

interface MessageItemProps {
  message: ChatMessage;
}

// 允许在聊天历史中显示的消息类型
const ALLOWED_MESSAGE_TYPES = ['user', 'agent', 'response'];

// 消息类型对应的颜色和图标
const getMessageStyle = (type: string) => {
  switch (type) {
    case 'user':
      return { color: '#1890ff', icon: null, bg: '#f0f8ff' };
    case 'agent':
    case 'response':
      return { color: '#52c41a', icon: null, bg: '#f6ffed' };
    default:
      return { color: '#595959', icon: null, bg: '#fafafa' };
  }
};

// 渲染键值对数据
const renderKvps = (kvps: Record<string, any>) => {
  if (!kvps || Object.keys(kvps).length === 0) return null;

  return (
    <div className="message-kvps">
      {Object.entries(kvps).map(([key, value]) => {
        if (key === 'attachments' && Array.isArray(value)) {
          return (
            <div key={key} className="kvp-row">
              <Text strong className="kvp-key">附件:</Text>
              <div className="attachment-list">
                {value.map((file: any, index: number) => (
                  <div key={index} className="attachment-preview">
                    {file.type === 'image' && file.url ? (
                      <Image
                        src={file.url}
                        alt={file.name}
                        style={{ maxWidth: 200, maxHeight: 150 }}
                      />
                    ) : (
                      <div className="file-attachment">
                        <span>{file.name}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          );
        }

        if (typeof value === 'object') {
          return (
            <div key={key} className="kvp-row">
              <Text strong className="kvp-key">{key}:</Text>
              <pre className="kvp-value">{JSON.stringify(value, null, 2)}</pre>
            </div>
          );
        }

        return (
          <div key={key} className="kvp-row">
            <Text strong className="kvp-key">{key}:</Text>
            <Text className="kvp-value">{String(value)}</Text>
          </div>
        );
      })}
    </div>
  );
};

// 复制文本到剪贴板
const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    console.error('复制失败:', err);
  }
};

// 简单的 Markdown 文本处理
const formatText = (text: string) => {
  // 处理代码块
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  const inlineCodeRegex = /`([^`]+)`/g;
  
  let formatted = text
    .replace(codeBlockRegex, (match, lang, code) => {
      return `<pre class="code-block"><code>${code.trim()}</code></pre>`;
    })
    .replace(inlineCodeRegex, '<code class="inline-code">$1</code>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');

  return formatted;
};

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const { type, content, heading, kvps, timestamp, temp } = message;
  
  // 确保只显示允许的消息类型
  if (!ALLOWED_MESSAGE_TYPES.includes(type)) {
    return null;
  }

  const style = getMessageStyle(type);
  const hasError = kvps?.error;

  const renderContent = () => {
    if (!content || content.trim().length === 0) return null;

    // 根据消息类型决定渲染方式
    switch (type) {
      case 'user':
      case 'agent':
      case 'response':
        // 支持简单格式化的消息类型
        return (
          <div 
            className="message-content markdown-content"
            dangerouslySetInnerHTML={{ __html: formatText(content) }}
          />
        );
      
      default:
        // 其他类型使用纯文本（虽然不应该到达这里）
        return (
          <div className="message-content text-content">
            <Paragraph style={{ marginBottom: 0, whiteSpace: 'pre-wrap' }}>
              {content}
            </Paragraph>
          </div>
        );
    }
  };

  // 构建CSS类名
  const classNames = [
    'message-item',
    `message-${type}`,
    temp && 'message-temp',
    hasError && 'message-error'
  ].filter(Boolean).join(' ');

  return (
    <div 
      className={classNames}
      style={{ borderLeftColor: style.color }}
    >
      {/* 消息头部 */}
      <div className="message-header">
        <div className="message-type">
          {style.icon && <span className="message-icon">{style.icon}</span>}
          <Tag color={style.color} className="message-tag">
            {type.toUpperCase()}
          </Tag>
          {heading && <Text strong className="message-heading">{heading}</Text>}
        </div>
        <div className="message-actions">
          <Button
            type="text"
            size="small"
            icon={<CopyOutlined />}
            onClick={() => copyToClipboard(content)}
            title="复制内容"
          />
          <Text type="secondary" className="message-time">
            {new Date(timestamp).toLocaleTimeString()}
          </Text>
        </div>
      </div>

      {/* 错误信息 */}
      {hasError && (
        <div className="mb-2 p-2 bg-red-50 border border-red-200 rounded text-red-600 text-sm">
          <span className="font-medium">发送失败: </span>
          {kvps.error}
        </div>
      )}

      {/* 键值对数据 */}
      {renderKvps(kvps || {})}

      {/* 消息内容 */}
      {renderContent()}
    </div>
  );
};

const ChatMessageList: React.FC<ChatMessageListProps> = ({ messages, loading }) => {
  // 过滤出允许显示的消息类型
  const filteredMessages = messages.filter(message => 
    ALLOWED_MESSAGE_TYPES.includes(message.type)
  );

  if (filteredMessages.length === 0 && !loading) {
    return (
      <div className="empty-messages">
        <Text type="secondary">开始对话吧！向 AI Agent 发送消息...</Text>
      </div>
    );
  }

  return (
    <div className="chat-message-list">
      {filteredMessages.map((message) => (
        <MessageItem key={message.id} message={message} />
      ))}
      
      {loading && (
        <div className="loading-message">
          <Spin size="small" />
          <Text type="secondary" style={{ marginLeft: 8 }}>
            AI 正在思考中...
          </Text>
        </div>
      )}
    </div>
  );
};

export default ChatMessageList; 