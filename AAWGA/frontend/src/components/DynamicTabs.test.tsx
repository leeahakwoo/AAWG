import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import DynamicTabs from './DynamicTabs';

describe('DynamicTabs', () => {
  test('초기 탭이 렌더링 된다', () => {
    render(<DynamicTabs />);
    expect(screen.getByText('테스트케이스 명세서')).toBeInTheDocument();
    expect(screen.getByText('요구사항정의서')).toBeInTheDocument();
  });

  test('탭 클릭 시 활성 탭이 변경된다', () => {
    render(<DynamicTabs />);
    const tab1 = screen.getByText('테스트케이스 명세서').closest('.tab')!;
    const tab2 = screen.getByText('요구사항정의서').closest('.tab')!;
    // 초기에는 첫 번째 탭이 active
    expect(tab1).toHaveClass('active');
    fireEvent.click(tab2);
    expect(tab2).toHaveClass('active');
    expect(tab1).not.toHaveClass('active');
  });

  test('＋ 버튼 클릭 시 새 탭이 추가된다', () => {
    render(<DynamicTabs />);
    // aria-label이 "새 탭" 이어야 합니다.
    const addBtn = screen.getByRole('button', { name: /새 탭/i });
    fireEvent.click(addBtn);
    expect(screen.getByText('새 탭')).toBeInTheDocument();
  });

  test('✕ 버튼 클릭 시 해당 탭이 삭제된다', () => {
    render(<DynamicTabs />);
    // 첫 번째 탭의 닫기 버튼: aria-label="닫기 테스트케이스 명세서"
    const closeBtns = screen.getAllByRole('button', { name: /닫기/i });
    expect(closeBtns.length).toBeGreaterThanOrEqual(1);
    // 첫 번째 탭 닫기
    fireEvent.click(closeBtns[0]);
    expect(screen.queryByText('테스트케이스 명세서')).toBeNull();
  });
});
