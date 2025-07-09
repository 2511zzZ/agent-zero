import React from 'react';
import { BulbOutlined } from '@ant-design/icons';
import BaseNode from './BaseNode';

interface PlanNodeProps {
  data: {
    title: string;
    content: string;
    status?: 'pending' | 'in_progress' | 'completed';
    priority?: 'low' | 'medium' | 'high';
  };
}

const PlanNode: React.FC<PlanNodeProps> = ({ data }) => {
  return (
    <BaseNode
      data={data}
      color="#3b82f6"
      icon={<BulbOutlined />}
      className="plan-node"
    />
  );
};

export default PlanNode; 