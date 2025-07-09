import React, { useState } from 'react';
import { Modal, Form, Input, Select, message } from 'antd';
import type { Project } from '@/types';
import { useProjectStore } from '@/stores/useProjectStore';

const { TextArea } = Input;
const { Option } = Select;

interface ProjectCreateModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess?: (project: Project) => void;
}

const ProjectCreateModal: React.FC<ProjectCreateModalProps> = ({ 
  open, 
  onClose, 
  onSuccess 
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const { createProject } = useProjectStore();

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const values = await form.validateFields();
      
      const projectData = {
        name: values.name,
        description: values.description,
        status: values.status || 'active',
        flowchart: {
          nodes: [],
          edges: [],
          viewport: { x: 0, y: 0, zoom: 1 },
          version: 0,
        },
        chatHistory: [],
      };

      const newProject = await createProject(projectData);
      
      message.success('Project created successfully');
      form.resetFields();
      onSuccess?.(newProject);
      onClose();
    } catch (error) {
      message.error('Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onClose();
  };

  return (
    <Modal
      title="Create New Project"
      open={open}
      onOk={handleSubmit}
      onCancel={handleCancel}
      confirmLoading={loading}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        requiredMark={false}
        autoComplete="off"
      >
        <Form.Item
          name="name"
          label="Project Name"
          rules={[
            { required: true, message: 'Please enter project name' },
            { max: 100, message: 'Project name cannot exceed 100 characters' },
          ]}
        >
          <Input 
            placeholder="Enter project name"
            autoFocus
          />
        </Form.Item>

        <Form.Item
          name="description"
          label="Description"
          rules={[
            { max: 500, message: 'Description cannot exceed 500 characters' },
          ]}
        >
          <TextArea 
            placeholder="Enter project description (optional)"
            rows={3}
            showCount
            maxLength={500}
          />
        </Form.Item>

        <Form.Item
          name="status"
          label="Status"
          initialValue="active"
        >
          <Select placeholder="Select status">
            <Option value="active">Active</Option>
            <Option value="archived">Archived</Option>
          </Select>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default ProjectCreateModal;