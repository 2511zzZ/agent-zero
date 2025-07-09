import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button, Typography, Space, message, Spin } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { Layout, ErrorBoundary } from '@/components/Common';
import { ChatSidebar } from '@/components/Chat';
import { FlowchartCanvas } from '@/components/Flowchart';
import { ProjectEditModal } from '@/components/Project';
import { useProjectStore } from '@/stores/useProjectStore';
import type { Project } from '@/types';

const { Title, Text } = Typography;

const ProjectDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { currentProject, loading, getProject, deleteProject, setCurrentProject } = useProjectStore();
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    if (id) {
      loadProject(id);
    }
  }, [id]);

  const loadProject = async (projectId: string) => {
    try {
      const project = await getProject(projectId);
      setCurrentProject(project);
    } catch (error) {
      message.error('加载项目失败');
      navigate('/');
    }
  };

  const handleGoBack = () => {
    navigate('/');
  };

  const handleEditProject = () => {
    setEditModalOpen(true);
  };

  const handleDeleteProject = async () => {
    if (!currentProject) return;
    
    setIsDeleting(true);
    try {
      await deleteProject(currentProject.id);
      message.success('项目删除成功');
      navigate('/');
    } catch (error) {
      message.error('删除项目失败');
    } finally {
      setIsDeleting(false);
    }
  };

  const handleEditSuccess = (updatedProject: Project) => {
    message.success('项目更新成功');
    setCurrentProject(updatedProject);
  };

  const handleEditClose = () => {
    setEditModalOpen(false);
  };

  if (loading.isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <Spin size="large" />
        </div>
      </Layout>
    );
  }

  if (loading.error || !currentProject) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <Text type="danger">{loading.error || '项目不存在'}</Text>
            <div className="mt-4">
              <Button onClick={handleGoBack}>返回项目列表</Button>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <ErrorBoundary>
      <div className="h-screen flex flex-col bg-gray-50">
        {/* 顶部导航栏 */}
        <div className="flex-shrink-0 bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                type="text"
                icon={<ArrowLeftOutlined />}
                onClick={handleGoBack}
                className="text-gray-600 hover:text-gray-800"
              >
                返回
              </Button>
              
              <div>
                <Title level={3} className="mb-0">
                  {currentProject.name}
                </Title>
                {currentProject.description && (
                  <Text type="secondary" className="text-sm">
                    {currentProject.description}
                  </Text>
                )}
              </div>
            </div>
            
            <Space>
              <Button
                icon={<EditOutlined />}
                onClick={handleEditProject}
              >
                编辑项目
              </Button>
              
              <Button
                danger
                icon={<DeleteOutlined />}
                onClick={handleDeleteProject}
                loading={isDeleting}
              >
                删除项目
              </Button>
            </Space>
          </div>
        </div>

        {/* 主要内容区域 */}
        <div className="flex-1 flex overflow-hidden">
          {/* 左侧：画板区域 */}
          <div className="flex-1 overflow-hidden">
            <FlowchartCanvas 
              projectId={currentProject.id}
              initialData={currentProject.flowchart}
              className="h-full"
            />
          </div>

          {/* 右侧：聊天侧边栏 */}
          <div className="w-96 flex-shrink-0">
            <ChatSidebar 
              projectId={currentProject.id}
              className="h-full"
            />
          </div>
        </div>
      </div>

      {/* 编辑项目弹窗 */}
      {currentProject && (
        <ProjectEditModal
          project={currentProject}
          open={editModalOpen}
          onSuccess={handleEditSuccess}
          onClose={handleEditClose}
        />
      )}
    </ErrorBoundary>
  );
};

export default ProjectDetail; 