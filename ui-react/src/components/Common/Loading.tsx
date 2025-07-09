import React from 'react';
import { Spin } from 'antd';

interface LoadingProps {
  loading?: boolean;
  children?: React.ReactNode;
  tip?: string;
  size?: 'small' | 'default' | 'large';
  className?: string;
}

const Loading: React.FC<LoadingProps> = ({ 
  loading = true, 
  children, 
  tip = 'Loading...', 
  size = 'default',
  className = ''
}) => {
  if (!loading && !children) return null;
  
  return (
    <Spin 
      spinning={loading} 
      tip={tip} 
      size={size}
      className={className}
    >
      {children}
    </Spin>
  );
};

export default Loading;