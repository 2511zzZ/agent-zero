import React from 'react';
import { FileTextOutlined } from '@ant-design/icons';
import BaseNode from './BaseNode';

interface DeliverableNodeProps {
  data: {
    title: string;
    content: string;
    status?: 'pending' | 'in_progress' | 'completed';
    priority?: 'low' | 'medium' | 'high';
  };
}

const DeliverableNode: React.FC<DeliverableNodeProps> = ({ data }) => {
  return (
    <BaseNode
      data={data}
      color="#10b981"
      icon={<FileTextOutlined />}
      className="deliverable-node"
    />
  );
};

export default DeliverableNode; 