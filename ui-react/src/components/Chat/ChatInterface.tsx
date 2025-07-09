import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Button, Input, Upload, message as antMessage, Tooltip, Alert } from 'antd';
import { 
  SendOutlined, 
  PaperClipOutlined, 
  AudioOutlined,
  PauseOutlined,
  PlayCircleOutlined,
  SettingOutlined,
  FolderOutlined,
  HistoryOutlined,
  ReloadOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import { chatAPI, systemAPI } from '@/services/api';
import ChatMessageList from './ChatMessageList';
import type { ChatMessage, MessageType } from '@/types';
import './ChatInterface.css';

const { TextArea } = Input;

interface ChatInterfaceProps {
  contextId?: string;
  onContextChange?: (contextId: string) => void;
}

// 临时信息消息接口
interface TempInfoMessage {
  id: string;
  content: string;
  timestamp: string;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ 
  contextId: propContextId, 
  onContextChange 
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [contextId, setContextId] = useState(propContextId || '');
  const [attachments, setAttachments] = useState<File[]>([]);
  const [isPaused, setIsPaused] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true);
  const [pollingActive, setPollingActive] = useState(false);
  // 新增：临时信息消息状态
  const [tempInfoMessage, setTempInfoMessage] = useState<TempInfoMessage | null>(null);
  
  // 参考 index.js 的实现：添加日志版本管理
  const [lastLogVersion, setLastLogVersion] = useState(0);
  const [lastLogGuid, setLastLogGuid] = useState('');
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const tempInfoTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // 生成唯一ID
  function generateGUID() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
      var r = (Math.random() * 16) | 0;
      var v = c === "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  // 自动滚动到底部
  const scrollToBottom = useCallback(() => {
    if (autoScroll && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [autoScroll]);

  // 显示临时信息消息
  const showTempInfoMessage = useCallback((content: string) => {
    // 清除之前的定时器
    if (tempInfoTimeoutRef.current) {
      clearTimeout(tempInfoTimeoutRef.current);
    }

    setTempInfoMessage({
      id: "",
      content,
      timestamp: new Date().toISOString()
    });

    // 5秒后自动清除临时消息
    tempInfoTimeoutRef.current = setTimeout(() => {
      setTempInfoMessage(null);
    }, 5000);
  }, []);

  // 检查消息类型是否应该显示在聊天历史中
  const shouldShowInChatHistory = (messageType: string): boolean => {
    return ['user', 'agent', 'response'].includes(messageType);
  };

  // 参考 index.js 实现：根据消息 ID 设置或更新消息
  const setMessage = useCallback((id: string, type: string, heading: string, content: string, temp: boolean, kvps: any = null) => {
    setMessages(prevMessages => {
      // 查找现有消息
      const existingIndex = prevMessages.findIndex(msg => msg.id === id);
      console.log('existingIndex', existingIndex);
      
      const messageData: ChatMessage = {
        id: id,
        type: type as MessageType,
        content: content || '',
        heading: heading || '',
        timestamp: new Date().toISOString(),
        temp: temp || false,
        kvps: kvps || {},
        role: type === 'user' ? 'user' : 'assistant'
      };

      if (existingIndex >= 0) {
        // 对于用户消息，不重新渲染
        if (type === 'user') {
          return prevMessages;
        }
        // 更新现有消息
        const newMessages = [...prevMessages];
        newMessages[existingIndex] = messageData;
        return newMessages;
      } else {
        // 添加新消息
        return [...prevMessages, messageData];
      }
    });
  }, []);

  // 轮询获取消息更新 - 参考 index.js 的实现
  const poll = useCallback(async () => {
    if (!contextId || !pollingActive) return false;

    try {
      // 获取时区信息
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

      const response = await chatAPI.poll({ 
        context: contextId,
        log_from: lastLogVersion, // 使用版本号而不是索引
        timezone: timezone || 'UTC'
      });
      
      // 检查响应是否有效
      if (!response) {
        console.error('Invalid response from poll endpoint');
        return false;
      }

      // 如果 log_guid 改变，清空聊天历史（参考 index.js）
      if (lastLogGuid !== '' && lastLogGuid !== response.log_guid) {
        setMessages([]);
        setLastLogVersion(0);
      }

      // 只有当 log_version 改变时才处理新的日志
      if (lastLogVersion !== response.log_version) {
        if (response.logs && Array.isArray(response.logs)) {
          response.logs.forEach((log: any) => {
            const messageType = log.type;

            // 处理不同类型的消息
            if (messageType === 'info') {
              // info 类型消息显示为临时消息
              if (log.content) {
                showTempInfoMessage(log.content);
              }
              return; // 不添加到聊天历史
            }

            if (messageType === 'util') {
              // util 类型消息不显示
              return;
            }

            // 只处理允许显示的消息类型
            if (!shouldShowInChatHistory(messageType)) {
              return;
            }

            const messageId = log.id || log.no; // 完全使用后端返回的 ID，不自己生成
            console.log('messageId', messageId);
            setMessage(
              messageId,
              log.type,
              log.heading || '',
              log.content || '',
              log.temp || false,
              log.kvps
            );
          });
        }

        // 更新版本信息
        setLastLogVersion(response.log_version);
        setTimeout(scrollToBottom, 100);
      }

      setLastLogGuid(response.log_guid);
      return true;
    } catch (error) {
      console.error('轮询失败:', error);
      return false;
    }
  }, [contextId, pollingActive, lastLogVersion, lastLogGuid, scrollToBottom, showTempInfoMessage, setMessage]);

  // 启动轮询
  const startPolling = useCallback(() => {
    if (pollingRef.current) return;
    
    setPollingActive(true);
    pollingRef.current = setInterval(poll, 250); // 使用 250ms 间隔，与 index.js 保持一致
  }, [poll]);

  // 停止轮询
  const stopPolling = useCallback(() => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
    setPollingActive(false);
  }, []);

  // 发送消息
  const sendMessage = async () => {
    if ((!inputValue.trim() && attachments.length === 0) || loading) return;

    const messageText = inputValue.trim();
    const messageId = generateGUID();
    
    setInputValue('');
    setAttachments([]);
    setLoading(true);

    try {
      let result: any;
      
      if (attachments.length > 0) {
        // 带附件的消息使用 FormData
        const formData = new FormData();
        formData.append('text', messageText);
        formData.append('context', contextId);
        formData.append('message_id', messageId);
        
        attachments.forEach((file) => {
          formData.append('attachments', file);
        });

        const response = await fetch('/api/message_async', {
          method: 'POST',
          body: formData,
        });
        
        result = await response.json();
      } else {
        // 纯文本消息
        result = await chatAPI.sendMessage({
          text: messageText,
          context: contextId,
          message_id: messageId
        });
      }

      if (result?.context) {
        setContextId(result.context);
        onContextChange?.(result.context);
      }

      // 启动轮询获取所有消息（包括刚发送的用户消息和AI回复）
      startPolling();
      
    } catch (error) {
      console.error('发送消息失败:', error);
      antMessage.error('发送消息失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 重置聊天
  const resetChat = async () => {
    try {
      if (contextId) {
        await chatAPI.resetChat(contextId);
      }
      setMessages([]);
      setContextId('');
      setTempInfoMessage(null);
      // 重置版本跟踪变量
      setLastLogVersion(0);
      setLastLogGuid('');
      stopPolling();
      onContextChange?.('');
      antMessage.success('聊天已重置');
    } catch (error) {
      console.error('重置聊天失败:', error);
      antMessage.error('重置聊天失败');
    }
  };

  // 暂停/恢复 Agent
  const togglePause = async () => {
    try {
      await systemAPI.togglePause();
      setIsPaused(!isPaused);
      antMessage.success(isPaused ? 'Agent 已恢复' : 'Agent 已暂停');
    } catch (error) {
      console.error('切换暂停状态失败:', error);
      antMessage.error('操作失败');
    }
  };

  // 处理附件上传
  const handleFileChange = (fileList: File[]) => {
    setAttachments(fileList);
  };

  // 处理键盘事件
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // 加载聊天历史
  const loadHistory = useCallback(async () => {
    if (!contextId) return;
    
    try {
      const history = await chatAPI.getChatHistory(contextId);
      const formattedMessages: ChatMessage[] = history
        .filter((item: any) => shouldShowInChatHistory(item.type)) // 过滤只显示允许的消息类型
        .map((item: any) => ({
          id: item.id || item.no, // 完全使用后端返回的 ID
          type: item.type as MessageType,
          content: item.content || '',
          heading: item.heading || '',
          role: item.type === 'user' ? 'user' : 'assistant',
          timestamp: item.timestamp ? new Date(item.timestamp).toISOString() : new Date().toISOString(),
          temp: item.temp || false,
          kvps: item.kvps || {}
        }));
      
      setMessages(formattedMessages.sort((a, b) => {
        const idA = parseInt(a.id.replace(/\D/g, '')) || 0;
        const idB = parseInt(b.id.replace(/\D/g, '')) || 0;
        return idA - idB;
      }));
      
      // 重置版本跟踪变量，准备开始增量轮询
      setLastLogVersion(0);
      setLastLogGuid('');
      
      setTimeout(scrollToBottom, 100);
    } catch (error) {
      console.error('加载历史失败:', error);
    }
  }, [contextId, scrollToBottom]);

  // 监听 contextId 变化，加载对应的聊天历史
  useEffect(() => {
    if (contextId) {
      // 重置状态
      setLastLogVersion(0);
      setLastLogGuid('');
      setTempInfoMessage(null);
      
      loadHistory();
      startPolling();
    } else {
      setMessages([]);
      setTempInfoMessage(null);
      setLastLogVersion(0);
      setLastLogGuid('');
      stopPolling();
    }

    return () => {
      stopPolling();
    };
  }, [contextId, loadHistory, startPolling, stopPolling]);

  // 组件卸载时清理轮询和定时器
  useEffect(() => {
    return () => {
      stopPolling();
      if (tempInfoTimeoutRef.current) {
        clearTimeout(tempInfoTimeoutRef.current);
      }
    };
  }, [stopPolling]);

  return (
    <div className="chat-interface">
      {/* 顶部工具栏 */}
      <div className="chat-toolbar">
        <div className="toolbar-left">
          <Button 
            type="primary" 
            icon={<ReloadOutlined />} 
            onClick={resetChat}
            size="small"
          >
            重置聊天
          </Button>
          <Button 
            icon={isPaused ? <PlayCircleOutlined /> : <PauseOutlined />} 
            onClick={togglePause}
            size="small"
          >
            {isPaused ? '恢复 Agent' : '暂停 Agent'}
          </Button>
        </div>
        <div className="toolbar-right">
          <Tooltip title="设置">
            <Button icon={<SettingOutlined />} size="small" />
          </Tooltip>
          <Tooltip title="文件管理">
            <Button icon={<FolderOutlined />} size="small" />
          </Tooltip>
          <Tooltip title="历史记录">
            <Button icon={<HistoryOutlined />} size="small" />
          </Tooltip>
        </div>
      </div>

      {/* 消息区域 */}
      <div className="chat-messages" ref={chatContainerRef}>
        <ChatMessageList 
          messages={messages} 
          loading={loading}
        />
        <div ref={messagesEndRef} />
      </div>

      {/* 输入区域 */}
      <div className="chat-input-area">
        {/* 临时信息消息显示区域 */}
        {tempInfoMessage && (
          <div className="temp-info-message">
            <Alert
              message={tempInfoMessage.content}
              type="info"
              icon={<InfoCircleOutlined />}
              closable
              onClose={() => setTempInfoMessage(null)}
              style={{ marginBottom: 8 }}
            />
          </div>
        )}

        {/* 附件预览 */}
        {attachments.length > 0 && (
          <div className="attachments-preview">
            {attachments.map((file, index) => (
              <div key={index} className="attachment-item">
                <span>{file.name}</span>
                <Button 
                  type="text" 
                  size="small"
                  onClick={() => setAttachments(prev => prev.filter((_, i) => i !== index))}
                >
                  ×
                </Button>
              </div>
            ))}
          </div>
        )}

        {/* 输入框和按钮 */}
        <div className="input-controls">
          <Upload
            multiple
            showUploadList={false}
            beforeUpload={(file) => {
              setAttachments(prev => [...prev, file]);
              return false;
            }}
          >
            <Button 
              icon={<PaperClipOutlined />} 
              type="text"
              className="attach-button"
            />
          </Upload>

          <TextArea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="输入您的消息..."
            autoSize={{ minRows: 1, maxRows: 6 }}
            className="message-input"
          />

          <div className="send-buttons">
            <Button 
              icon={<AudioOutlined />} 
              type="text"
              className="voice-button"
            />
            <Button 
              type="primary" 
              icon={<SendOutlined />}
              onClick={sendMessage}
              loading={loading}
              className="send-button"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 