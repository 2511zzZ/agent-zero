import React, { useEffect, useState } from 'react';
import { 
  Button, 
  Typography, 
  Row, 
  Col, 
  Empty, 
  message,
  Input,
  Select,
  Tag
} from 'antd';
import { 
  PlusOutlined, 
  SearchOutlined, 
  FilterOutlined,
  AppstoreOutlined,
  UnorderedListOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { Layout, Loading, ErrorBoundary } from '@/components/Common';
import { ProjectCard, ProjectCreateModal, ProjectEditModal } from '@/components/Project';
import { useProjectStore } from '@/stores/useProjectStore';
import type { Project } from '@/types';

const { Title, Text } = Typography;
const { Search } = Input;
const { Option } = Select;

const ProjectList: React.FC = () => {
  const navigate = useNavigate();
  const { projects, loading, fetchProjects } = useProjectStore();
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || project.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleCreateProject = () => {
    setCreateModalOpen(true);
  };

  const handleProjectCreated = (project: Project) => {
    message.success('Project created successfully');
    // 自动跳转到新创建的项目
    navigate(`/project/${project.id}`);
  };

  const handleOpenProject = (project: Project) => {
    navigate(`/project/${project.id}`);
  };

  const handleEditProject = (project: Project) => {
    setEditingProject(project);
    setEditModalOpen(true);
  };

  const handleEditSuccess = (_updatedProject: Project) => {
    message.success('Project updated successfully');
    // 可以选择刷新列表或者直接更新本地状态
    fetchProjects();
  };

  const handleEditClose = () => {
    setEditModalOpen(false);
    setEditingProject(null);
  };

  const renderHeader = () => (
    <div className="flex items-center justify-between">
      <div>
        <Title level={2} className="mb-2">Projects</Title>
        <Text type="secondary">
          Manage your Agent Zero projects
        </Text>
      </div>
      <Button 
        type="primary" 
        icon={<PlusOutlined />}
        onClick={handleCreateProject}
      >
        New Project
      </Button>
    </div>
  );

  const renderFilters = () => (
    <div className="mb-6 p-4 bg-gray-50 rounded-lg">
      <Row gutter={[16, 16]} align="middle">
        <Col xs={24} sm={12} md={8}>
          <Search
            placeholder="Search projects..."
            allowClear
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            prefix={<SearchOutlined />}
          />
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Select
            value={statusFilter}
            onChange={setStatusFilter}
            style={{ width: '100%' }}
            prefix={<FilterOutlined />}
          >
            <Option value="all">All Status</Option>
            <Option value="active">Active</Option>
            <Option value="archived">Archived</Option>
          </Select>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <div className="flex items-center space-x-2">
            <Text type="secondary">View:</Text>
            <Button.Group>
              <Button 
                type={viewMode === 'grid' ? 'primary' : 'default'}
                icon={<AppstoreOutlined />}
                onClick={() => setViewMode('grid')}
              />
              <Button 
                type={viewMode === 'list' ? 'primary' : 'default'}
                icon={<UnorderedListOutlined />}
                onClick={() => setViewMode('list')}
              />
            </Button.Group>
          </div>
        </Col>
        <Col xs={24} sm={12} md={4}>
          <div className="text-right">
            <Tag color="blue">{filteredProjects.length} projects</Tag>
          </div>
        </Col>
      </Row>
    </div>
  );

  const renderProjects = () => {
    if (loading.isLoading) {
      return (
        <div className="flex items-center justify-center py-20">
          <Loading size="large" />
        </div>
      );
    }

    if (filteredProjects.length === 0) {
      return (
        <div className="flex items-center justify-center py-20">
          <Empty 
            description={
              searchTerm || statusFilter !== 'all' 
                ? 'No projects match your filters'
                : 'No projects yet'
            }
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            {!searchTerm && statusFilter === 'all' && (
              <Button 
                type="primary" 
                icon={<PlusOutlined />}
                onClick={handleCreateProject}
              >
                Create Your First Project
              </Button>
            )}
          </Empty>
        </div>
      );
    }

    if (viewMode === 'grid') {
      return (
        <Row gutter={[24, 24]}>
          {filteredProjects.map(project => (
            <Col key={project.id} xs={24} sm={12} lg={8} xl={6}>
              <ProjectCard
                project={project}
                onOpen={handleOpenProject}
                onEdit={handleEditProject}
              />
            </Col>
          ))}
        </Row>
      );
    }

    // List view (TODO: 实现列表视图)
    return (
      <div className="space-y-4">
        {filteredProjects.map(project => (
          <ProjectCard
            key={project.id}
            project={project}
            onOpen={handleOpenProject}
            onEdit={handleEditProject}
            className="mb-4"
          />
        ))}
      </div>
    );
  };

  if (loading.error) {
    return (
      <Layout>
        <div className="flex items-center justify-center py-20">
          <Empty 
            description="Failed to load projects"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            <Button onClick={() => fetchProjects()}>
              Try Again
            </Button>
          </Empty>
        </div>
      </Layout>
    );
  }

  return (
    <ErrorBoundary>
      <Layout header={renderHeader()}>
        <div className="max-w-7xl mx-auto p-6">
          {renderFilters()}
          {renderProjects()}
        </div>
        
        <ProjectCreateModal
          open={createModalOpen}
          onClose={() => setCreateModalOpen(false)}
          onSuccess={handleProjectCreated}
        />
        
        <ProjectEditModal
          open={editModalOpen}
          project={editingProject}
          onClose={handleEditClose}
          onSuccess={handleEditSuccess}
        />
      </Layout>
    </ErrorBoundary>
  );
};

export default ProjectList;