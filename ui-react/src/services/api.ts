import axios, { type AxiosResponse } from 'axios';
import type { 
  MessageRequest, 
  MessageResponse, 
  PollRequest, 
  PollResponse,
  Project,
  FlowchartData,
  FlowchartMessage
} from '@/types';

// 创建 axios 实例
const api = axios.create({
  baseURL: import.meta.env.DEV ? '/api' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:50080'),
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加 CSRF token 或其他认证信息
    const token = localStorage.getItem('csrf_token');
    if (token) {
      config.headers['X-CSRF-Token'] = token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    
    // 处理特定错误状态
    if (error.response?.status === 401) {
      // 处理未授权
      window.location.href = '/login';
    } else if (error.response?.status === 403) {
      // 处理 CSRF 错误
      return refreshCSRFToken().then(() => {
        return api.request(error.config);
      });
    }
    
    return Promise.reject(error);
  }
);

// 获取 CSRF Token
export const getCSRFToken = async (): Promise<string> => {
  try {
    const response = await api.get('/csrf_token');
    const token = response.data.token;
    localStorage.setItem('csrf_token', token);
    return token;
  } catch (error) {
    console.error('Failed to get CSRF token:', error);
    throw error;
  }
};

// 刷新 CSRF Token
const refreshCSRFToken = async () => {
  try {
    await getCSRFToken();
  } catch (error) {
    console.error('Failed to refresh CSRF token:', error);
    throw error;
  }
};

// 聊天相关 API（复用现有接口）
export const chatAPI = {
  // 发送消息（异步）
  sendMessage: async (request: MessageRequest): Promise<MessageResponse> => {
    try {
      const response = await api.post('/message_async', request);
      return response.data;
    } catch (error) {
      console.error('Failed to send message:', error);
      throw error;
    }
  },

  // 轮询获取更新
  poll: async (request: PollRequest): Promise<PollResponse> => {
    try {
      const response = await api.post('/poll', request);
      return response.data;
    } catch (error) {
      console.error('Failed to poll:', error);
      throw error;
    }
  },

  // 获取聊天历史
  getChatHistory: async (contextId: string): Promise<any[]> => {
    try {
      const response = await api.post('/history_get', { context: contextId });
      return JSON.parse(response.data.history);
    } catch (error) {
      console.error('Failed to get chat history:', error);
      throw error;
    }
  },

  // 重置聊天
  resetChat: async (contextId: string): Promise<void> => {
    try {
      await api.post('/chat_reset', { context: contextId });
    } catch (error) {
      console.error('Failed to reset chat:', error);
      throw error;
    }
  },

  // 删除聊天
  removeChat: async (contextId: string): Promise<void> => {
    try {
      await api.post('/chat_remove', { context: contextId });
    } catch (error) {
      console.error('Failed to remove chat:', error);
      throw error;
    }
  },
};

// 项目管理 API（新增）
export const projectAPI = {
  // 获取所有项目
  getProjects: async (): Promise<Project[]> => {
      const response = await api.get('/project_list');
      console.log('Project list response:', response.data);
      if (response.data.success) {
        return response.data.projects || [];
      } else {
        console.error('API error:', response.data.error);
        return [];
      }
  },

  // 创建项目
  createProject: async (project: Omit<Project, 'id' | 'createdAt' | 'updatedAt'>): Promise<Project> => {
      const response = await api.post('/project_create', project);
      console.log('Create project response:', response.data);
      if (response.data.success) {
        return response.data.project;
      } else {
        throw new Error(response.data.error || 'Failed to create project');
      }
  },

  // 更新项目
  updateProject: async (id: string, updates: Partial<Project>): Promise<Project> => {
    try {
      const response = await api.post('/project_update', { project_id: id, ...updates });
      console.log('Update project response:', response.data);
      if (response.data.success) {
        return response.data.project;
      } else {
        throw new Error(response.data.error || 'Failed to update project');
      }
    } catch (error) {
      console.error('Failed to update project:', error);
      throw error;
    }
  },

  // 删除项目
  deleteProject: async (id: string): Promise<void> => {
    try {
      const response = await api.post('/project_delete', { project_id: id });
      console.log('Delete project response:', response.data);
      if (!response.data.success) {
        throw new Error(response.data.error || 'Failed to delete project');
      }
    } catch (error) {
      console.error('Failed to delete project:', error);
      throw error;
    }
  },

  // 获取项目详情
  getProject: async (id: string): Promise<Project> => {
    try {
      console.log('Getting project with ID:', id);
      const response = await api.post('/project_get', { project_id: id });
      console.log('Get project response:', response.data);
      if (response.data.success) {
        return response.data.project;
      } else {
        throw new Error(response.data.error || 'Failed to get project');
      }
    } catch (error) {
      console.error('Failed to get project:', error);
      throw error;
    }
  },
};

// 画板管理 API（新增）
export const flowchartAPI = {
  // 获取画板数据
  getFlowchart: async (projectId: string): Promise<FlowchartData> => {
    try {
      const response = await api.get(`/projects/${projectId}/flowchart`);
      return response.data.flowchart;
    } catch (error) {
      console.error('Failed to get flowchart:', error);
      throw error;
    }
  },

  // 更新画板数据
  updateFlowchart: async (projectId: string, flowchartMessage: FlowchartMessage): Promise<FlowchartData> => {
    try {
      const response = await api.post(`/projects/${projectId}/flowchart/update`, flowchartMessage);
      return response.data.flowchart;
    } catch (error) {
      console.error('Failed to update flowchart:', error);
      throw error;
    }
  },

  // 批量更新画板
  batchUpdateFlowchart: async (projectId: string, updates: FlowchartMessage[]): Promise<FlowchartData> => {
    try {
      const response = await api.post(`/projects/${projectId}/flowchart/batch`, { updates });
      return response.data.flowchart;
    } catch (error) {
      console.error('Failed to batch update flowchart:', error);
      throw error;
    }
  },
};

// 系统控制 API（复用现有接口）
export const systemAPI = {
  // 健康检查
  healthCheck: async (): Promise<{ status: string }> => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Failed to check health:', error);
      throw error;
    }
  },

  // 暂停/恢复
  togglePause: async (): Promise<void> => {
    try {
      await api.post('/pause');
    } catch (error) {
      console.error('Failed to toggle pause:', error);
      throw error;
    }
  },

  // 重启
  restart: async (): Promise<void> => {
    try {
      await api.post('/restart');
    } catch (error) {
      console.error('Failed to restart:', error);
      throw error;
    }
  },
};

// 导出默认 API 实例
export default api;