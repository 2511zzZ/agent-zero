import React from 'react';
import { Handle, Position } from 'reactflow';
import { Card, Typography, Tag } from 'antd';

const { Text } = Typography;

interface BaseNodeProps {
  data: {
    title: string;
    content: string;
    status?: 'pending' | 'in_progress' | 'completed';
    priority?: 'low' | 'medium' | 'high';
  };
  className?: string;
  color?: string;
  icon?: React.ReactNode;
}

const BaseNode: React.FC<BaseNodeProps> = ({ 
  data, 
  className = '', 
  color = '#3b82f6',
  icon 
}) => {
  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'in_progress': return 'processing';
      case 'pending': return 'default';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <div className={`min-w-48 ${className}`}>
      <Handle type="target" position={Position.Top} />
      
      <Card
        size="small"
        className="shadow-md border-l-4"
        style={{ borderLeftColor: color }}
        bodyStyle={{ padding: '12px' }}
      >
        <div className="flex items-start space-x-2">
          {icon && (
            <div className="flex-shrink-0 mt-1" style={{ color }}>
              {icon}
            </div>
          )}
          
          <div className="flex-1 min-w-0">
            <div className="font-medium text-sm text-gray-900 mb-1 truncate">
              {data.title || '无标题'}
            </div>
            
            {data.content && (
              <Text type="secondary" className="text-xs leading-relaxed">
                {data.content.length > 100 
                  ? `${data.content.substring(0, 100)}...` 
                  : data.content
                }
              </Text>
            )}
            
            <div className="flex items-center justify-between mt-2">
              <div className="flex space-x-1">
                {data.status && (
                  <Tag color={getStatusColor(data.status)}>
                    {data.status === 'pending' ? '待处理' :
                     data.status === 'in_progress' ? '进行中' : '已完成'}
                  </Tag>
                )}
                
                {data.priority && (
                  <Tag 
                    style={{ 
                      borderColor: getPriorityColor(data.priority),
                      color: getPriorityColor(data.priority)
                    }}
                  >
                    {data.priority === 'high' ? '高' :
                     data.priority === 'medium' ? '中' : '低'}
                  </Tag>
                )}
              </div>
            </div>
          </div>
        </div>
      </Card>
      
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default BaseNode; 