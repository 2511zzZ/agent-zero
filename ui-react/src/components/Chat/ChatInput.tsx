import React, { useState, useRef, type KeyboardEvent } from 'react';
import { Button, Input, Space, Tooltip, Upload, message as antMessage } from 'antd';
import { SendOutlined, PaperClipOutlined, StopOutlined } from '@ant-design/icons';
import type { UploadFile } from 'antd';

const { TextArea } = Input;

interface ChatInputProps {
  onSendMessage: (message: string, files?: UploadFile[]) => void;
  onStop?: () => void;
  loading?: boolean;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
  allowAttachments?: boolean;
  className?: string;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  onStop,
  loading = false,
  disabled = false,
  placeholder = '输入消息...',
  maxLength = 4000,
  allowAttachments = true,
  className = ''
}) => {
  const [message, setMessage] = useState('');
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const textAreaRef = useRef<any>(null);

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage && fileList.length === 0) {
      return;
    }

    onSendMessage(trimmedMessage, fileList.length > 0 ? fileList : undefined);
    setMessage('');
    setFileList([]);
    
    // 重新聚焦到输入框
    setTimeout(() => {
      textAreaRef.current?.focus();
    }, 100);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Ctrl+Enter 或 Cmd+Enter 发送消息
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
    // Shift+Enter 换行（默认行为）
  };

  const handleStop = () => {
    if (onStop) {
      onStop();
    }
  };

  const handleFileChange = ({ fileList: newFileList }: { fileList: UploadFile[] }) => {
    // 限制文件数量
    if (newFileList.length > 5) {
      antMessage.warning('最多只能上传 5 个文件');
      return;
    }

    // 限制文件大小 (10MB)
    const maxSize = 10 * 1024 * 1024;
    const validFiles = newFileList.filter(file => {
      if (file.size && file.size > maxSize) {
        antMessage.error(`文件 ${file.name} 超过 10MB 限制`);
        return false;
      }
      return true;
    });

    setFileList(validFiles);
  };

  const canSend = message.trim() || fileList.length > 0;

  return (
    <div className={`border-t border-gray-200 bg-white p-4 ${className}`}>
      <div className="max-w-4xl mx-auto">
        <div className="flex flex-col space-y-3">
          {/* 文件附件显示 */}
          {fileList.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {fileList.map((file) => (
                <div
                  key={file.uid}
                  className="flex items-center bg-blue-50 border border-blue-200 rounded px-2 py-1 text-sm"
                >
                  <PaperClipOutlined className="mr-1 text-blue-500" />
                  <span className="text-blue-700">{file.name}</span>
                  <Button
                    type="text"
                    size="small"
                    className="ml-1 p-0 h-auto text-blue-500 hover:text-blue-700"
                    onClick={() => setFileList(prev => prev.filter(f => f.uid !== file.uid))}
                  >
                    ×
                  </Button>
                </div>
              ))}
            </div>
          )}

          {/* 输入区域 */}
          <div className="flex items-end space-x-2">
            <div className="flex-1">
              <TextArea
                ref={textAreaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                maxLength={maxLength}
                showCount
                autoSize={{ minRows: 1, maxRows: 6 }}
                disabled={disabled}
                className="resize-none"
              />
            </div>

            <Space>
              {/* 文件上传按钮 */}
              {allowAttachments && (
                <Upload
                  fileList={fileList}
                  onChange={handleFileChange}
                  beforeUpload={() => false} // 阻止自动上传
                  multiple
                  showUploadList={false}
                  disabled={disabled || loading}
                >
                  <Tooltip title="添加附件">
                    <Button
                      type="text"
                      icon={<PaperClipOutlined />}
                      disabled={disabled || loading}
                      className="text-gray-500 hover:text-gray-700"
                    />
                  </Tooltip>
                </Upload>
              )}

              {/* 发送/停止按钮 */}
              {loading ? (
                <Tooltip title="停止生成">
                  <Button
                    type="primary"
                    danger
                    icon={<StopOutlined />}
                    onClick={handleStop}
                    disabled={!onStop}
                  >
                    停止
                  </Button>
                </Tooltip>
              ) : (
                <Tooltip title="发送消息 (Ctrl+Enter)">
                  <Button
                    type="primary"
                    icon={<SendOutlined />}
                    onClick={handleSend}
                    disabled={disabled || !canSend}
                  >
                    发送
                  </Button>
                </Tooltip>
              )}
            </Space>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInput; 