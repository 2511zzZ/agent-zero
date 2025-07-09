import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, message } from 'antd';
import { ErrorBoundary } from '@/components/Common';
import { ProjectList } from '@/pages/ProjectList';
import ProjectDetail from '@/pages/ProjectDetail/ProjectDetail';
import { getCSRFToken } from '@/services/api';
import './App.css';

// 主题配置
const theme = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
  },
};

const App: React.FC = () => {
  // 应用初始化
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // 获取 CSRF token
        await getCSRFToken();
        console.log('CSRF token initialized successfully');
      } catch (error) {
        console.error('Failed to initialize CSRF token:', error);
        message.error('应用初始化失败，请刷新页面重试');
      }
    };

    initializeApp();
  }, []);

  return (
    <ConfigProvider theme={theme}>
      <ErrorBoundary>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/" element={<Navigate to="/projects" replace />} />
              <Route path="/projects" element={<ProjectList />} />
              <Route path="/project/:id" element={<ProjectDetail />} />
              <Route path="*" element={<div>404 - Page Not Found</div>} />
            </Routes>
          </div>
        </Router>
      </ErrorBoundary>
    </ConfigProvider>
  );
};

export default App;