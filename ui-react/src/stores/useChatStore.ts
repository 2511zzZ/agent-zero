import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { ChatMessage, ChatContext, LoadingState, MessageRequest, PollRequest } from '@/types';
import { chatAPI } from '@/services/api';

interface ChatState {
  // 状态
  messages: ChatMessage[];
  contexts: ChatContext[];
  currentContext: string | null;
  loading: LoadingState;
  isPolling: boolean;
  pollInterval: number;
  
  // 操作
  sendMessage: (request: MessageRequest) => Promise<void>;
  startPolling: () => void;
  stopPolling: () => void;
  poll: () => Promise<void>;
  loadHistory: (contextId: string) => Promise<void>;
  setCurrentContext: (contextId: string) => void;
  createNewChat: (projectId: string) => string;
  resetChat: (contextId: string) => Promise<void>;
  removeChat: (contextId: string) => Promise<void>;
  
  // 工具方法
  addMessage: (message: ChatMessage) => void;
  updateMessage: (messageId: string, updates: Partial<ChatMessage>) => void;
  clearMessages: () => void;
  clearError: () => void;
  reset: () => void;
}

const initialState = {
  messages: [],
  contexts: [],
  currentContext: null,
  loading: {
    isLoading: false,
    error: undefined,
  },
  isPolling: false,
  pollInterval: 1000, // 1秒轮询间隔
};

export const useChatStore = create<ChatState>()(
  devtools(
    (set, get) => ({
      ...initialState,

      // 发送消息
      sendMessage: async (request) => {
        set({ loading: { isLoading: true } });
        try {
          // 先添加用户消息到本地状态
          const userMessage: ChatMessage = {
            id: Date.now().toString(),
            type: 'user',
            content: request.text,
            timestamp: new Date().toISOString(),
          };
          
          get().addMessage(userMessage);
          
          // 发送到服务器
          const response = await chatAPI.sendMessage(request);
          
          // 添加 Agent 回复消息
          const agentMessage: ChatMessage = {
            id: (Date.now() + 1).toString(),
            type: 'agent',
            content: response.message,
            timestamp: new Date().toISOString(),
          };
          
          get().addMessage(agentMessage);
          
          set({ 
            currentContext: response.context,
            loading: { isLoading: false } 
          });
          
          // 开始轮询获取更新
          get().startPolling();
          
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to send message' 
            } 
          });
          throw error;
        }
      },

      // 开始轮询
      startPolling: () => {
        const state = get();
        if (state.isPolling || !state.currentContext) return;
        
        set({ isPolling: true });
        
        const pollTimer = setInterval(() => {
          get().poll();
        }, state.pollInterval);
        
        // 存储定时器 ID（在实际应用中可能需要更好的管理方式）
        (window as any).pollTimer = pollTimer;
      },

      // 停止轮询
      stopPolling: () => {
        set({ isPolling: false });
        if ((window as any).pollTimer) {
          clearInterval((window as any).pollTimer);
          (window as any).pollTimer = null;
        }
      },

      // 轮询获取更新
      poll: async () => {
        const state = get();
        if (!state.currentContext) return;
        
        try {
          const pollRequest: PollRequest = {
            context: state.currentContext,
            log_from: state.messages.length,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
          };
          
          const response = await chatAPI.poll(pollRequest);
          
          // 处理新的日志/消息
          if (response.logs && response.logs.length > 0) {
            const newMessages: ChatMessage[] = response.logs.map((log: any, index: number) => ({
              id: `${Date.now()}-${index}`,
              type: log.type || 'system',
              content: log.message || log.content,
              timestamp: log.timestamp || new Date().toISOString(),
              metadata: log.metadata,
            }));
            
            set((state) => ({
              messages: [...state.messages, ...newMessages],
            }));
          }
          
          // 处理画板更新
          if (response.flowchartUpdate) {
            // 这里会触发画板更新，需要与 flowchart store 集成
            console.log('Flowchart update received:', response.flowchartUpdate);
          }
          
          // 如果没有更多活动，停止轮询
          if (!response.log_progress_active) {
            get().stopPolling();
          }
          
        } catch (error) {
          console.error('Poll error:', error);
          // 轮询错误不应该中断用户体验，只记录错误
        }
      },

      // 加载历史记录
      loadHistory: async (contextId) => {
        set({ loading: { isLoading: true } });
        try {
          const history = await chatAPI.getChatHistory(contextId);
          const messages: ChatMessage[] = history.map((item: any) => ({
            id: item.id || Date.now().toString(),
            type: item.type || 'system',
            content: item.content || item.message,
            timestamp: item.timestamp || new Date().toISOString(),
            metadata: item.metadata,
          }));
          
          set({ 
            messages,
            currentContext: contextId,
            loading: { isLoading: false } 
          });
        } catch (error) {
          set({ 
            loading: { 
              isLoading: false, 
              error: error instanceof Error ? error.message : 'Failed to load history' 
            } 
          });
          throw error;
        }
      },

      // 设置当前上下文
      setCurrentContext: (contextId) => {
        get().stopPolling();
        set({ currentContext: contextId });
      },

      // 创建新聊天
      createNewChat: (projectId) => {
        const newContextId = `${projectId}_${Date.now()}`;
        set({ 
          currentContext: newContextId,
          messages: [],
        });
        return newContextId;
      },

      // 重置聊天
      resetChat: async (contextId) => {
        try {
          await chatAPI.resetChat(contextId);
          if (get().currentContext === contextId) {
            set({ messages: [] });
          }
        } catch (error) {
          console.error('Failed to reset chat:', error);
          throw error;
        }
      },

      // 删除聊天
      removeChat: async (contextId) => {
        try {
          await chatAPI.removeChat(contextId);
          set((state) => ({
            contexts: state.contexts.filter(ctx => ctx.id !== contextId),
            currentContext: state.currentContext === contextId ? null : state.currentContext,
            messages: state.currentContext === contextId ? [] : state.messages,
          }));
        } catch (error) {
          console.error('Failed to remove chat:', error);
          throw error;
        }
      },

      // 添加消息
      addMessage: (message) => {
        set((state) => ({
          messages: [...state.messages, message],
        }));
      },

      // 更新消息
      updateMessage: (messageId, updates) => {
        set((state) => ({
          messages: state.messages.map(msg => 
            msg.id === messageId ? { ...msg, ...updates } : msg
          ),
        }));
      },

      // 清除消息
      clearMessages: () => {
        set({ messages: [] });
      },

      // 清除错误
      clearError: () => {
        set((state) => ({
          loading: { ...state.loading, error: undefined }
        }));
      },

      // 重置状态
      reset: () => {
        get().stopPolling();
        set(initialState);
      },
    }),
    {
      name: 'chat-store',
    }
  )
);