import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { FlowNode, FlowEdge, FlowchartMessage, LoadingState, Viewport } from '@/types';
import { flowchartAPI } from '@/services/api';

interface FlowchartState {
  // 状态
  nodes: FlowNode[];
  edges: FlowEdge[];
  viewport: Viewport;
  version: number;
  loading: LoadingState;
  selectedNodes: string[];
  selectedEdges: string[];
  
  // 操作
  loadFlowchart: (projectId: string) => Promise<void>;
  updateFlowchart: (projectId: string, message: FlowchartMessage) => Promise<void>;
  applyFlowchartUpdate: (message: FlowchartMessage) => void;
  
  // 节点操作
  addNode: (node: FlowNode) => void;
  updateNode: (nodeId: string, updates: Partial<FlowNode>) => void;
  deleteNode: (nodeId: string) => void;
  setSelectedNodes: (nodeIds: string[]) => void;
  
  // 边操作
  addEdge: (edge: FlowEdge) => void;
  updateEdge: (edgeId: string, updates: Partial<FlowEdge>) => void;
  deleteEdge: (edgeId: string) => void;
  setSelectedEdges: (edgeIds: string[]) => void;
  
  // 视窗操作
  setViewport: (viewport: Viewport) => void;
  fitToView: () => void;
  
  // 工具方法
  getNodeById: (nodeId: string) => FlowNode | undefined;
  getEdgeById: (edgeId: string) => FlowEdge | undefined;
  clearSelection: () => void;
  clearError: () => void;
  reset: () => void;
}

const initialState = {
  nodes: [],
  edges: [],
  viewport: { x: 0, y: 0, zoom: 1 },
  version: 0,
  loading: {
    isLoading: false,
    error: undefined,
  },
  selectedNodes: [],
  selectedEdges: [],
};

export const useFlowchartStore = create<FlowchartState>()(
  devtools(
    (set, get) => ({
      ...initialState,

      // 加载画板数据
      loadFlowchart: async (projectId) => {
        set({ loading: { isLoading: true } });
        try {
          const flowchartData = await flowchartAPI.getFlowchart(projectId);
          set({ 
            nodes: flowchartData.nodes || [],
            edges: flowchartData.edges || [],
            viewport: flowchartData.viewport || { x: 0, y: 0, zoom: 1 },
            version: flowchartData.version || 0,
            loading: { isLoading: false } 
          });
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to load flowchart' 
            } 
          });
          throw error;
        }
      },

      // 更新画板数据
      updateFlowchart: async (projectId, message) => {
        set({ loading: { isLoading: true } });
        try {
          const updatedFlowchart = await flowchartAPI.updateFlowchart(projectId, message);
          set({ 
            nodes: updatedFlowchart.nodes || [],
            edges: updatedFlowchart.edges || [],
            viewport: updatedFlowchart.viewport || get().viewport,
            version: updatedFlowchart.version || get().version + 1,
            loading: { isLoading: false } 
          });
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to update flowchart' 
            } 
          });
          throw error;
        }
      },

      // 应用画板更新（来自 Agent 的实时更新）
      applyFlowchartUpdate: (message) => {
        const state = get();
        
        switch (message.action) {
          case 'update_flowchart':
            set({ 
              nodes: message.data.nodes || state.nodes,
              edges: message.data.edges || state.edges,
              viewport: message.data.viewport || state.viewport,
              version: state.version + 1,
            });
            break;
            
          case 'clear_flowchart':
            set({ 
              nodes: [],
              edges: [],
              viewport: { x: 0, y: 0, zoom: 1 },
              version: state.version + 1,
            });
            break;
            
          default:
            console.warn('Unknown flowchart action:', message.action);
        }
      },

      // 添加节点
      addNode: (node) => {
        set((state) => ({
          nodes: [...state.nodes, node],
          version: state.version + 1,
        }));
      },

      // 更新节点
      updateNode: (nodeId, updates) => {
        set((state) => ({
          nodes: state.nodes.map(node => 
            node.id === nodeId ? { ...node, ...updates } : node
          ),
          version: state.version + 1,
        }));
      },

      // 删除节点
      deleteNode: (nodeId) => {
        set((state) => ({
          nodes: state.nodes.filter(node => node.id !== nodeId),
          edges: state.edges.filter(edge => edge.source !== nodeId && edge.target !== nodeId),
          selectedNodes: state.selectedNodes.filter(id => id !== nodeId),
          version: state.version + 1,
        }));
      },

      // 设置选中的节点
      setSelectedNodes: (nodeIds) => {
        set({ selectedNodes: nodeIds });
      },

      // 添加边
      addEdge: (edge) => {
        set((state) => ({
          edges: [...state.edges, edge],
          version: state.version + 1,
        }));
      },

      // 更新边
      updateEdge: (edgeId, updates) => {
        set((state) => ({
          edges: state.edges.map(edge => 
            edge.id === edgeId ? { ...edge, ...updates } : edge
          ),
          version: state.version + 1,
        }));
      },

      // 删除边
      deleteEdge: (edgeId) => {
        set((state) => ({
          edges: state.edges.filter(edge => edge.id !== edgeId),
          selectedEdges: state.selectedEdges.filter(id => id !== edgeId),
          version: state.version + 1,
        }));
      },

      // 设置选中的边
      setSelectedEdges: (edgeIds) => {
        set({ selectedEdges: edgeIds });
      },

      // 设置视窗
      setViewport: (viewport) => {
        set({ viewport });
      },

      // 适应视图
      fitToView: () => {
        // 这里需要根据节点位置计算合适的视窗
        // 实际实现需要考虑节点的边界
        const state = get();
        if (state.nodes.length === 0) return;
        
        const bounds = state.nodes.reduce((acc, node) => ({
          minX: Math.min(acc.minX, node.position.x),
          minY: Math.min(acc.minY, node.position.y),
          maxX: Math.max(acc.maxX, node.position.x + 200), // 假设节点宽度为 200
          maxY: Math.max(acc.maxY, node.position.y + 100), // 假设节点高度为 100
        }), {
          minX: Infinity,
          minY: Infinity,
          maxX: -Infinity,
          maxY: -Infinity,
        });
        
        const width = bounds.maxX - bounds.minX;
        const height = bounds.maxY - bounds.minY;
        const zoom = Math.min(1, Math.min(800 / width, 600 / height)) * 0.8;
        
        set({
          viewport: {
            x: -(bounds.minX + width / 2) * zoom + 400,
            y: -(bounds.minY + height / 2) * zoom + 300,
            zoom,
          },
        });
      },

      // 根据 ID 获取节点
      getNodeById: (nodeId) => {
        return get().nodes.find(node => node.id === nodeId);
      },

      // 根据 ID 获取边
      getEdgeById: (edgeId) => {
        return get().edges.find(edge => edge.id === edgeId);
      },

      // 清除选择
      clearSelection: () => {
        set({ selectedNodes: [], selectedEdges: [] });
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
      name: 'flowchart-store',
    }
  )
);