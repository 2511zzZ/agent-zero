import React from 'react';
import { EditOutlined } from '@ant-design/icons';
import BaseNode from './BaseNode';

interface NoteNodeProps {
  data: {
    title: string;
    content: string;
    status?: 'pending' | 'in_progress' | 'completed';
    priority?: 'low' | 'medium' | 'high';
  };
}

const NoteNode: React.FC<NoteNodeProps> = ({ data }) => {
  return (
    <BaseNode
      data={data}
      color="#8b5cf6"
      icon={<EditOutlined />}
      className="note-node"
    />
  );
};

export default NoteNode; 