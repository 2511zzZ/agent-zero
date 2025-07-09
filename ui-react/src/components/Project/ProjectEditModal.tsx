import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Select, message } from 'antd';
import type { Project } from '@/types';
import { useProjectStore } from '@/stores/useProjectStore';

const { TextArea } = Input;
const { Option } = Select;

interface ProjectEditModalProps {
  open: boolean;
  project: Project | null;
  onClose: () => void;
  onSuccess?: (project: Project) => void;
}

const ProjectEditModal: React.FC<ProjectEditModalProps> = ({ 
  open, 
  project,
  onClose, 
  onSuccess 
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const { updateProject } = useProjectStore();

  useEffect(() => {
    if (project && open) {
      form.setFieldsValue({
        name: project.name,
        description: project.description,
        status: project.status,
      });
    }
  }, [project, open, form]);

  const handleSubmit = async () => {
    if (!project) return;

    try {
      setLoading(true);
      const values = await form.validateFields();
      
      await updateProject(project.id, values);
      
      message.success('Project updated successfully');
      onSuccess?.({ ...project, ...values });
      onClose();
    } catch (error) {
      message.error('Failed to update project');
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
      title="Edit Project"
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

export default ProjectEditModal;