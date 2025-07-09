import React from 'react';
import { Card, Typography, Tag, Button, Dropdown, message } from 'antd';
import { 
  EllipsisOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  FolderOpenOutlined,
  CalendarOutlined 
} from '@ant-design/icons';
import type { Project } from '@/types';
import { useProjectStore } from '@/stores/useProjectStore';

const { Title, Text, Paragraph } = Typography;

interface ProjectCardProps {
  project: Project;
  onEdit?: (project: Project) => void;
  onOpen?: (project: Project) => void;
  className?: string;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ 
  project, 
  onEdit, 
  onOpen, 
  className = '' 
}) => {
  const { deleteProject } = useProjectStore();

  const handleDelete = async () => {
    try {
      await deleteProject(project.id);
      message.success('Project deleted successfully');
    } catch (error) {
      message.error('Failed to delete project');
    }
  };

  const menuItems = [
    {
      key: 'edit',
      label: 'Edit',
      icon: <EditOutlined />,
      onClick: () => onEdit?.(project),
    },
    {
      key: 'delete',
      label: 'Delete',
      icon: <DeleteOutlined />,
      onClick: handleDelete,
      danger: true,
    },
  ];

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <Card
      className={`project-card hover:shadow-lg transition-shadow cursor-pointer ${className}`}
      hoverable
      onClick={() => onOpen?.(project)}
      actions={[
        <Button 
          key="open" 
          type="text" 
          icon={<FolderOpenOutlined />}
          onClick={(e) => {
            e.stopPropagation();
            onOpen?.(project);
          }}
        >
          Open
        </Button>,
        <Dropdown
          key="menu"
          menu={{ items: menuItems }}
          trigger={['click']}
          placement="bottomRight"
        >
          <Button 
            type="text" 
            icon={<EllipsisOutlined />}
            onClick={(e) => e.stopPropagation()}
          />
        </Dropdown>,
      ]}
    >
      <div className="space-y-3">
        <div className="flex items-start justify-between">
          <Title level={4} className="mb-0 flex-1">
            {project.name}
          </Title>
          <Tag color={project.status === 'active' ? 'green' : 'orange'}>
            {project.status}
          </Tag>
        </div>
        
        {project.description && (
          <Paragraph 
            className="text-gray-600 mb-2" 
            ellipsis={{ rows: 2 }}
          >
            {project.description}
          </Paragraph>
        )}
        
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center space-x-1">
            <CalendarOutlined />
            <Text type="secondary">
              Updated {formatDate(project.updatedAt)}
            </Text>
          </div>
          
          <div className="flex items-center space-x-4">
            <Text type="secondary">
              {project.chatHistory?.length || 0} messages
            </Text>
            <Text type="secondary">
              {project.flowchart?.nodes?.length || 0} nodes
            </Text>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default ProjectCard;