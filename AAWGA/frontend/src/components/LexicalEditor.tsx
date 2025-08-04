// src/components/LexicalEditor.tsx

import React, {
  useCallback,
  useMemo,
  Profiler,
  Suspense,
  lazy,
} from 'react';
import { LexicalComposer } from '@lexical/react/LexicalComposer';
import { RichTextPlugin } from '@lexical/react/LexicalRichTextPlugin';
import { ContentEditable } from '@lexical/react/LexicalContentEditable';
import { OnChangePlugin } from '@lexical/react/LexicalOnChangePlugin';
import { $getRoot, EditorState } from 'lexical';
import { TRANSFORMERS, $convertToMarkdownString } from '@lexical/markdown';
import { LexicalErrorBoundary } from '@lexical/react/LexicalErrorBoundary';
import debounce from 'lodash.debounce';
import './LexicalEditor.css';

// 정적 노드 임포트
import { HeadingNode } from '@lexical/rich-text';
import { ListNode, ListItemNode } from '@lexical/list';

// 지연 로딩(코드 스플리팅) 플러그인
const ToolbarPlugin = lazy(() => import('./ToolbarPlugin'));
const HistoryPlugin = lazy(() =>
  import('@lexical/react/LexicalHistoryPlugin').then(mod => ({
    default: mod.HistoryPlugin,
  }))
);
const MarkdownShortcutPlugin = lazy(() =>
  import('@lexical/react/LexicalMarkdownShortcutPlugin').then(mod => ({
    default: mod.MarkdownShortcutPlugin,
  }))
);

interface LexicalEditorProps {
  onChange?: (text: string, md: string) => void;
}

const editorConfig = {
  namespace: 'AAWGAEditor',
  theme: {},
  onError(error: Error) {
    console.error('Lexical Error:', error);
  },
  nodes: [HeadingNode, ListNode, ListItemNode],
};

export default function LexicalEditor({ onChange }: LexicalEditorProps) {
  // 키 입력 시 레이턴시 시작 기록
  const handleKeyDown = () => {
    (window as any).__typingStart = performance.now();
  };

  // React Profiler 콜백
  const onRenderCallback = (
    id: string,
    phase: 'mount' | 'update',
    actualDuration: number
  ) => {
    console.log(
      `[Profiler] ${id} ${phase} took ${actualDuration.toFixed(2)}ms`
    );
  };

  // Markdown 변환 디바운스
  const debouncedMd = useMemo(
    () =>
      debounce((editorState: EditorState) => {
        editorState.read(() => {
          const md = $convertToMarkdownString(TRANSFORMERS);
          console.log('[Markdown]', md);
          onChange?.('', md);
        });
      }, 200),
    [onChange]
  );

  // 에디터 상태 변경 핸들러
  const handleChange = useCallback(
    (editorState: EditorState) => {
      const delta =
        performance.now() - ((window as any).__typingStart || 0);
      if (delta > 0) {
        console.log(`[Typing Latency] ${delta.toFixed(2)}ms`);
      }

      editorState.read(() => {
        const text = $getRoot().getTextContent();
        console.log('[RichText]', text);
        onChange?.(text, '');
      });

      debouncedMd(editorState);
    },
    [debouncedMd, onChange]
  );

  return (
    <Profiler id="LexicalEditor" onRender={onRenderCallback}>
      <LexicalComposer initialConfig={editorConfig}>
        <Suspense fallback={null}>
          <ToolbarPlugin />
        </Suspense>
        <Suspense fallback={null}>
          <HistoryPlugin />
          <MarkdownShortcutPlugin transformers={TRANSFORMERS} />
        </Suspense>
        <div className="editor-wrapper border rounded p-2 min-h-[150px] bg-white">
          <RichTextPlugin
            contentEditable={
              <ContentEditable
                className="editor-input"
                onKeyDown={handleKeyDown}
              />
            }
            placeholder={
              <div className="editor-placeholder">내용을 입력하세요…</div>
            }
            ErrorBoundary={LexicalErrorBoundary}
          />
          <OnChangePlugin onChange={handleChange} />
        </div>
      </LexicalComposer>
    </Profiler>
  );
}
