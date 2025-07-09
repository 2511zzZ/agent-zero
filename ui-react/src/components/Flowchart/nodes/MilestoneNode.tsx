import React from 'react';
import { TrophyOutlined } from '@ant-design/icons';
import BaseNode from './BaseNode';

interface MilestoneNodeProps {
  data: {
    title: string;
    content: string;
    status?: 'pending' | 'in_progress' | 'completed';
    priority?: 'low' | 'medium' | 'high';
  };
}

const MilestoneNode: React.FC<MilestoneNodeProps> = ({ data }) => {
  return (
    <BaseNode
      data={data}
      color="#f59e0b"
      icon={<TrophyOutlined />}
      className="milestone-node"
    />
  );
};

export default MilestoneNode; 