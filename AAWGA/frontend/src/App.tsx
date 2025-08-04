import React from 'react';
import DynamicTabs from './components/DynamicTabs';
import './App.css';

function App() {
  return (
    <div className="app-container h-screen">
      {/* 나중에 헤더/사이드바 컴포넌트 삽입 가능 */}
      <DynamicTabs />
    </div>
  );
}

export default App;
