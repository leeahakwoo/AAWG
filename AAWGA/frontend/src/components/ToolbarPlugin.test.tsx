// src/components/ToolbarPlugin.test.tsx
/// <reference types="jest" />
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { LexicalComposer } from '@lexical/react/LexicalComposer';
import ToolbarPlugin from './ToolbarPlugin';

// useLexicalComposerContext 훅을 모킹하고 editorMock을 함께 반환합니다.
jest.mock('@lexical/react/LexicalComposerContext', () => {
  const editorMock = { dispatchCommand: jest.fn() };
  return {
    useLexicalComposerContext: () => [editorMock],
    __editorMock: editorMock,  // 런타임에만 사용될 임시 프로퍼티
  };
});

describe('ToolbarPlugin', () => {
  const initialConfig = {
    namespace: 'TestNamespace',
    onError: () => {},
  };

  test('볼드·이탤릭·밑줄·취소선 버튼을 누르면 dispatchCommand가 호출된다', () => {
    const { getByLabelText } = render(
      <LexicalComposer initialConfig={initialConfig}>
        <ToolbarPlugin />
      </LexicalComposer>
    );

    // jest.requireMock을 통해 mock 모듈에서 editorMock을 가져옵니다
    const mockModule = jest.requireMock('@lexical/react/LexicalComposerContext') as any;
    const editorMock = mockModule.__editorMock as { dispatchCommand: jest.Mock };

    fireEvent.click(getByLabelText('볼드'));
    fireEvent.click(getByLabelText('이탤릭'));
    fireEvent.click(getByLabelText('밑줄'));
    fireEvent.click(getByLabelText('취소선'));

    expect(editorMock.dispatchCommand).toHaveBeenCalledTimes(4);
    expect(editorMock.dispatchCommand).toHaveBeenLastCalledWith(
      expect.anything(),
      'strikethrough'
    );
  });
});
