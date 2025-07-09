import React from 'react';
import { Layout as AntLayout } from 'antd';

const { Header, Content, Sider } = AntLayout;

interface LayoutProps {
  children: React.ReactNode;
  sidebar?: React.ReactNode;
  header?: React.ReactNode;
  className?: string;
}

const Layout: React.FC<LayoutProps> = ({ 
  children, 
  sidebar, 
  header, 
  className = '' 
}) => {
  return (
    <AntLayout className={`layout-container ${className}`}>
      {header && (
        <Header className="bg-white border-b border-gray-200 px-6 h-16 flex items-center">
          {header}
        </Header>
      )}
      <AntLayout className="flex-1">
        {sidebar && (
          <Sider 
            width={320} 
            className="sidebar"
            style={{ backgroundColor: '#fff' }}
          >
            {sidebar}
          </Sider>
        )}
        <Content className="main-content">
          {children}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;