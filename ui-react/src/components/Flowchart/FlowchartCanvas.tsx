import React, { useCallback, useEffect, useRef } from 'react';
import ReactFlow, {
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  MiniMap,
  Background,
  ConnectionMode,
  ReactFlowProvider,
  type Node,
  type Edge,
  type OnConnect,
} from 'reactflow';
import 'reactflow/dist/style.css';

import type { FlowchartData, FlowNode, FlowEdge } from '@/types';
import PlanNode from './nodes/PlanNode';
import MilestoneNode from './nodes/MilestoneNode';
import DeliverableNode from './nodes/DeliverableNode';
import NoteNode from './nodes/NoteNode';

// 自定义节点类型映射
const nodeTypes = {
  plan: PlanNode,
  milestone: MilestoneNode,
  deliverable: DeliverableNode,
  note: NoteNode,
};

interface FlowchartCanvasProps {
  projectId: string;
  initialData?: FlowchartData;
  onDataChange?: (data: FlowchartData) => void;
  className?: string;
}

const FlowchartCanvasInner: React.FC<FlowchartCanvasProps> = ({
  projectId: _projectId,
  initialData,
  onDataChange,
  className = ''
}) => {
  const reactFlowInstance = useRef<any>(null);
  
  // 将 FlowNode 转换为 React Flow 的 Node 格式
  const convertToReactFlowNodes = (flowNodes: FlowNode[]): Node[] => {
    return flowNodes.map(node => ({
      id: node.id,
      type: node.type,
      position: node.position,
      data: node.data,
      style: node.style,
      className: node.className,
      draggable: node.draggable,
      selectable: node.selectable,
      connectable: node.connectable,
      hidden: node.hidden,
    }));
  };

  // 将 FlowEdge 转换为 React Flow 的 Edge 格式
  const convertToReactFlowEdges = (flowEdges: FlowEdge[]): Edge[] => {
    return flowEdges.map(edge => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      sourceHandle: edge.sourceHandle,
      targetHandle: edge.targetHandle,
      type: edge.type === 'dependency' ? 'smoothstep' : 'default',
      label: edge.data.label,
      style: edge.style,
      className: edge.className,
      animated: edge.animated,
      data: edge.data,
    }));
  };

  // 初始化节点和边
  const [nodes, setNodes, onNodesChange] = useNodesState(
    initialData ? convertToReactFlowNodes(initialData.nodes) : []
  );
  const [edges, setEdges, onEdgesChange] = useEdgesState(
    initialData ? convertToReactFlowEdges(initialData.edges) : []
  );

  // 连接节点时的回调
  const onConnect: OnConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // 当节点或边发生变化时，通知父组件
  useEffect(() => {
    if (onDataChange) {
      const flowchartData: FlowchartData = {
        nodes: nodes.map(node => ({
          id: node.id,
          type: node.type as 'plan' | 'milestone' | 'deliverable' | 'note' | 'chat',
          position: node.position,
          data: node.data,
          style: node.style,
          className: node.className,
          draggable: node.draggable,
          selectable: node.selectable,
          connectable: node.connectable,
          hidden: node.hidden,
        })),
        edges: edges.map(edge => ({
          id: edge.id,
          source: edge.source,
          target: edge.target,
          sourceHandle: edge.sourceHandle || undefined,
          targetHandle: edge.targetHandle || undefined,
          type: edge.type === 'smoothstep' ? 'dependency' : 'sequence',
          data: {
            label: edge.label as string,
            weight: 1,
            metadata: edge.data,
          },
          style: edge.style,
          className: edge.className,
          animated: edge.animated,
        })),
        viewport: reactFlowInstance.current?.getViewport() || { x: 0, y: 0, zoom: 1 },
        version: Date.now(),
      };
      
      onDataChange(flowchartData);
    }
  }, [nodes, edges, onDataChange]);

  // 添加新节点的方法
  const addNode = useCallback((type: string, position: { x: number; y: number }) => {
    const newNode: Node = {
      id: `${type}-${Date.now()}`,
      type,
      position,
      data: {
        title: `新${type === 'plan' ? '计划' : type === 'milestone' ? '里程碑' : type === 'deliverable' ? '交付物' : '笔记'}`,
        content: '',
        status: 'pending',
      },
    };
    
    setNodes((nds) => [...nds, newNode]);
  }, [setNodes]);

  // 监听画布双击事件，添加新节点
  const onPaneClick = useCallback((event: React.MouseEvent) => {
    // 检查是否是双击
    if (event.detail === 2 && reactFlowInstance.current) {
      const bounds = (event.target as Element).getBoundingClientRect();
      const position = reactFlowInstance.current.project({
        x: event.clientX - bounds.left,
        y: event.clientY - bounds.top,
      });
      addNode('note', position);
    }
  }, [addNode]);

  return (
    <div className={`w-full h-full ${className}`}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onPaneClick={onPaneClick}
        nodeTypes={nodeTypes}
        connectionMode={ConnectionMode.Loose}
        fitView
        attributionPosition="bottom-left"
        onInit={(rfi) => {
          reactFlowInstance.current = rfi;
        }}
      >
        <Background />
        <Controls />
        <MiniMap 
          nodeColor={(node) => {
            switch (node.type) {
              case 'plan': return '#3b82f6';
              case 'milestone': return '#f59e0b';
              case 'deliverable': return '#10b981';
              case 'note': return '#8b5cf6';
              default: return '#6b7280';
            }
          }}
          nodeStrokeWidth={3}
          zoomable
          pannable
        />
      </ReactFlow>
    </div>
  );
};

const FlowchartCanvas: React.FC<FlowchartCanvasProps> = (props) => {
  return (
    <ReactFlowProvider>
      <FlowchartCanvasInner {...props} />
    </ReactFlowProvider>
  );
};

export default FlowchartCanvas; 