// 项目相关类型
export interface Project {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
  status: 'active' | 'archived';
  flowchart: FlowchartData;
  chatHistory: ChatMessage[];
}

// React Flow 相关类型
export interface FlowchartData {
  nodes: FlowNode[];
  edges: FlowEdge[];
  viewport: Viewport;
  version: number;
}

export interface FlowNode {
  id: string;
  type: 'plan' | 'milestone' | 'deliverable' | 'note' | 'chat';
  position: { x: number; y: number };
  data: {
    title: string;
    content: string;
    status?: 'pending' | 'in_progress' | 'completed';
    priority?: 'low' | 'medium' | 'high';
    assignee?: string;
    dueDate?: string;
    metadata?: Record<string, any>;
  };
  style?: React.CSSProperties;
  className?: string;
  draggable?: boolean;
  selectable?: boolean;
  connectable?: boolean;
  hidden?: boolean;
}

export interface FlowEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
  type: 'dependency' | 'sequence' | 'reference';
  data: {
    label?: string;
    weight?: number;
    metadata?: Record<string, any>;
  };
  style?: React.CSSProperties;
  className?: string;
  animated?: boolean;
}

export interface Viewport {
  x: number;
  y: number;
  zoom: number;
}

// Agent 消息类型枚举
export type MessageType = 
  | 'user' 
  | 'agent' 
  | 'response' 
  | 'tool' 
  | 'code_exe' 
  | 'browser' 
  | 'warning' 
  | 'rate_limit' 
  | 'error' 
  | 'info' 
  | 'util' 
  | 'hint'
  | 'system';

// 聊天相关类型
export interface ChatMessage {
  id: string;
  type: MessageType;
  content: string;
  heading?: string;
  timestamp: string;
  temp?: boolean;
  kvps?: Record<string, any>;
  role?: 'user' | 'assistant' | 'system';
  metadata?: Record<string, any>;
}

export interface ChatContext {
  id: string;
  messages: ChatMessage[];
  projectId: string;
  createdAt: string;
  updatedAt: string;
}

// Agent 消息格式
export interface FlowchartMessage {
  action: 'update_flowchart' | 'clear_flowchart' | 'get_flowchart';
  data: {
    nodes?: FlowNode[];
    edges?: FlowEdge[];
    viewport?: Viewport;
  };
}

// API 请求/响应类型
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface MessageRequest {
  text: string;
  context: string;
  message_id?: string;
  projectId?: string;
  flowchartContext?: FlowchartData;
}

export interface MessageResponse {
  message?: string;
  context: string;
  flowchartUpdate?: FlowchartMessage;
}

export interface PollRequest {
  context: string;
  log_from?: number;
  timezone?: string;
}

export interface PollResponse {
  context: string;
  contexts: string[];
  tasks: any[];
  logs: any[];
  data?: any[];
  log_guid: string;
  log_version: number;
  log_progress: number;
  log_progress_active: boolean;
  paused: boolean;
  flowchartUpdate?: FlowchartMessage;
}

// 通用工具类型
export interface LoadingState {
  isLoading: boolean;
  error?: string;
}

export interface User {
  id: string;
  name: string;
  email?: string;
  avatar?: string;
}

export interface Settings {
  theme: 'light' | 'dark';
  language: string;
  autoSave: boolean;
  pollInterval: number;
}