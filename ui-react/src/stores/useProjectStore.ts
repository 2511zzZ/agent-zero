import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { Project, LoadingState } from '@/types';
import { projectAPI } from '@/services/api';

interface ProjectState {
  // 状态
  projects: Project[];
  currentProject: Project | null;
  loading: LoadingState;
  
  // 操作
  fetchProjects: () => Promise<void>;
  createProject: (project: Omit<Project, 'id' | 'createdAt' | 'updatedAt'>) => Promise<Project>;
  updateProject: (id: string, updates: Partial<Project>) => Promise<void>;
  deleteProject: (id: string) => Promise<void>;
  setCurrentProject: (project: Project | null) => void;
  getProject: (id: string) => Promise<Project>;
  
  // 工具方法
  clearError: () => void;
  reset: () => void;
}

const initialState = {
  projects: [],
  currentProject: null,
  loading: {
    isLoading: false,
    error: undefined,
  },
};

export const useProjectStore = create<ProjectState>()(
  devtools(
    (set, _get) => ({
      ...initialState,

      // 获取所有项目
      fetchProjects: async () => {
        set({ loading: { isLoading: true } });
        try {
          const projects = await projectAPI.getProjects();
          set({ 
            projects, 
            loading: { isLoading: false } 
          });
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to fetch projects' 
            } 
          });
        }
      },

      // 创建项目
      createProject: async (projectData) => {
        set({ loading: { isLoading: true } });
        try {
          const newProject = await projectAPI.createProject(projectData);
          set((state) => ({
            projects: [...state.projects, newProject],
            loading: { isLoading: false },
          }));
          return newProject;
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to create project' 
            } 
          });
          throw error;
        }
      },

      // 更新项目
      updateProject: async (id, updates) => {
        set({ loading: { isLoading: true } });
        try {
          const updatedProject = await projectAPI.updateProject(id, updates);
          set((state) => ({
            projects: state.projects.map(p => p.id === id ? updatedProject : p),
            currentProject: state.currentProject?.id === id ? updatedProject : state.currentProject,
            loading: { isLoading: false },
          }));
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to update project' 
            } 
          });
          throw error;
        }
      },

      // 删除项目
      deleteProject: async (id) => {
        set({ loading: { isLoading: true } });
        try {
          await projectAPI.deleteProject(id);
          set((state) => ({
            projects: state.projects.filter(p => p.id !== id),
            currentProject: state.currentProject?.id === id ? null : state.currentProject,
            loading: { isLoading: false },
          }));
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to delete project' 
            } 
          });
          throw error;
        }
      },

      // 设置当前项目
      setCurrentProject: (project) => {
        set({ currentProject: project });
      },

      // 获取特定项目
      getProject: async (id) => {
        set({ loading: { isLoading: true } });
        try {
          const project = await projectAPI.getProject(id);
          set({ 
            currentProject: project,
            loading: { isLoading: false } 
          });
          return project;
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to get project' 
            } 
          });
          throw error;
        }
      },

      // 清除错误
      clearError: () => {
        set((state) => ({
          loading: { ...state.loading, error: undefined }
        }));
      },

      // 重置状态
      reset: () => {
        set(initialState);
      },
    }),
    {
      name: 'project-store',
    }
  )
);