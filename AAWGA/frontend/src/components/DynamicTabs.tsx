import React, { useState } from 'react';
import './DynamicTabs.css';
import LexicalEditor from './LexicalEditor';

interface Tab {
  id: string;
  title: string;
  iconClass: string;
  color: string;
  content: React.ReactNode;
}

export default function DynamicTabs() {
  const [tabs, setTabs] = useState<Tab[]>([
    {
      id: 'test-case',
      title: '테스트케이스 명세서',
      iconClass: 'fas fa-clipboard-list',
      color: '#667eea',
      content: <LexicalEditor />,
    },
    {
      id: 'req-def',
      title: '요구사항정의서',
      iconClass: 'fas fa-file-excel',
      color: '#4caf50',
      content: <LexicalEditor />,
    },
  ]);
  const [activeTabId, setActiveTabId] = useState(tabs[0].id);

  const addTab = () => {
    const newId = `tab-${Date.now()}`;
    setTabs((prev) => [
      ...prev,
      { id: newId, title: '새 탭', iconClass: 'fas fa-plus', color: '#999', content: <LexicalEditor /> },
    ]);
    setActiveTabId(newId);
  };

  const removeTab = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setTabs((prev) => {
      const filtered = prev.filter((t) => t.id !== id);
      if (activeTabId === id && filtered.length > 0) {
        setActiveTabId(filtered[0].id);
      }
      return filtered;
    });
  };

  const switchTab = (id: string) => {
    setActiveTabId(id);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="tab-container">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`tab${tab.id === activeTabId ? ' active' : ''}`}
            onClick={() => switchTab(tab.id)}
          >
            <i className={tab.iconClass} style={{ color: tab.color, marginRight: 4 }} />
            <span className="tab-title">{tab.title}</span>
            <button
              type="button"
              className="tab-close"
              aria-label={`닫기 ${tab.title}`}
              onClick={(e) => removeTab(tab.id, e)}
            >
              ✕
            </button>
          </div>
        ))}
        <button
          type="button"
          className="tab-add"
          aria-label="새 탭"
          onClick={addTab}
        >
          ＋
        </button>
      </div>
      <div className="content-container">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`content-section${tab.id === activeTabId ? '' : ' hidden'}`}
          >
            {tab.content}
          </div>
        ))}
      </div>
    </div>
  );
}
