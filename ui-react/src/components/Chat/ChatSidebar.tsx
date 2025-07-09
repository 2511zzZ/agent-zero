import React, { useEffect, useState } from 'react';
import { Button, Space, Typography, Dropdown, message } from 'antd';
import { 
  MessageOutlined, 
  PlusOutlined, 
  MoreOutlined, 
  DeleteOutlined,
  SyncOutlined
} from '@ant-design/icons';
import ChatMessageList from './ChatMessageList';
import ChatInput from './ChatInput';
import { useChatStore } from '@/stores/useChatStore';
import type { UploadFile } from 'antd';

const { Title, Text } = Typography;

interface ChatSidebarProps {
  projectId: string;
  className?: string;
}

const ChatSidebar: React.FC<ChatSidebarProps> = ({
  projectId,
  className = ''
}) => {
  const {
    messages,
    loading,
    sendMessage,
    startPolling,
    stopPolling,
    clearMessages,
    createNewChat,
    setCurrentContext
  } = useChatStore();

  const [contextId, setContextId] = useState<string>(`project_${projectId}`);

  useEffect(() => {
    // 当项目 ID 变化时更新上下文 ID
    const newContextId = `project_${projectId}`;
    setContextId(newContextId);
    
    // 设置当前上下文并开始轮询
    setCurrentContext(newContextId);
    startPolling();

    // 组件卸载时停止轮询
    return () => {
      stopPolling();
    };
  }, [projectId, startPolling, stopPolling, setCurrentContext]);

  const handleSendMessage = async (text: string, _files?: UploadFile[]) => {
    try {
      await sendMessage({
        text,
        context: contextId,
        projectId,
        // TODO: 添加文件附件支持
      });
    } catch (error) {
      console.error('Failed to send message:', error);
      message.error('发送消息失败，请重试');
    }
  };

  const handleNewChat = () => {
    try {
      createNewChat(contextId);
      message.success('已创建新对话');
    } catch (error) {
      console.error('Failed to create new chat:', error);
      message.error('创建新对话失败');
    }
  };

  const handleClearMessages = () => {
    try {
      clearMessages();
      message.success('已清空对话记录');
    } catch (error) {
      console.error('Failed to clear messages:', error);
      message.error('清空对话失败');
    }
  };

  const handleRefresh = () => {
    try {
      // 重新开始轮询来刷新消息
      stopPolling();
      setTimeout(() => {
        startPolling();
      }, 100);
      message.success('已刷新对话');
    } catch (error) {
      console.error('Failed to refresh chat:', error);
      message.error('刷新对话失败');
    }
  };

  const moreMenuItems = [
    {
      key: 'refresh',
      label: '刷新对话',
      icon: <SyncOutlined />,
      onClick: handleRefresh
    },
    {
      key: 'clear',
      label: '清空对话',
      icon: <DeleteOutlined />,
      onClick: handleClearMessages,
      danger: true
    }
  ];

  return (
    <div className={`flex flex-col h-full bg-white border-l border-gray-200 ${className}`}>
      {/* 聊天头部 */}
      <div className="flex-shrink-0 p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <MessageOutlined className="text-blue-500" />
            <Title level={4} className="mb-0">
              Agent 对话
            </Title>
          </div>
          
          <Space>
            <Button
              type="primary"
              size="small"
              icon={<PlusOutlined />}
              onClick={handleNewChat}
            >
              新对话
            </Button>
            
            <Dropdown
              menu={{ items: moreMenuItems }}
              trigger={['click']}
              placement="bottomRight"
            >
              <Button type="text" size="small" icon={<MoreOutlined />} />
            </Dropdown>
          </Space>
        </div>
        
        <Text type="secondary" className="text-sm">
          与 Agent 进行实时对话，讨论项目进展
        </Text>
      </div>

      {/* 消息列表区域 */}
      <div className="flex-1 flex flex-col min-h-0">
        <ChatMessageList
          messages={messages}
          loading={loading.isLoading}
        />
      </div>

      {/* 输入区域 */}
      <div className="flex-shrink-0">
        <ChatInput
          onSendMessage={handleSendMessage}
          loading={loading.isLoading}
          placeholder="向 Agent 提问或描述需求..."
          allowAttachments={false} // 暂时禁用文件上传
        />
      </div>
    </div>
  );
};

export default ChatSidebar; 