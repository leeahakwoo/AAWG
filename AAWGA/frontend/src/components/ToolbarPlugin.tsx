import React from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import {
  FORMAT_TEXT_COMMAND,
  FORMAT_ELEMENT_COMMAND,
  type ElementFormatType,
} from 'lexical';
import {
  INSERT_UNORDERED_LIST_COMMAND,
  INSERT_ORDERED_LIST_COMMAND,
} from '@lexical/list';
import {
  Bold,
  Italic,
  Underline,
  Strikethrough,
  List as ListIcon,
  ListOrdered,
  Heading1,
  Heading2,
  Link as LinkIcon,
} from 'lucide-react';
import { TOGGLE_LINK_COMMAND } from '@lexical/link';
import './ToolbarPlugin.css';

export default function ToolbarPlugin() {
  const [editor] = useLexicalComposerContext();

  const applyTextFormat = (
    format: 'bold' | 'italic' | 'underline' | 'strikethrough'
  ) => {
    editor.dispatchCommand(FORMAT_TEXT_COMMAND, format);
  };

  const applyBlockFormat = (format: 'h1' | 'h2') => {
    editor.dispatchCommand(
      FORMAT_ELEMENT_COMMAND,
      format as ElementFormatType
    );
  };

  const toggleBulletList = () => {
    editor.dispatchCommand(INSERT_UNORDERED_LIST_COMMAND, undefined);
  };
  const toggleNumberList = () => {
    editor.dispatchCommand(INSERT_ORDERED_LIST_COMMAND, undefined);
  };

  const insertLink = () => {
    const url = window.prompt('URL을 입력하세요:', 'https://');
    if (url && url.trim()) {
      editor.dispatchCommand(TOGGLE_LINK_COMMAND, url.trim());
    }
  };

  return (
    <div className="toolbar-plugin flex gap-2 border-b p-1 bg-white">
      <button onClick={() => applyTextFormat('bold')} aria-label="Bold">
        <Bold size={16} />
      </button>
      <button onClick={() => applyTextFormat('italic')} aria-label="Italic">
        <Italic size={16} />
      </button>
      <button
        onClick={() => applyTextFormat('underline')}
        aria-label="Underline"
      >
        <Underline size={16} />
      </button>
      <button
        onClick={() => applyTextFormat('strikethrough')}
        aria-label="Strikethrough"
      >
        <Strikethrough size={16} />
      </button>

      <button onClick={() => applyBlockFormat('h1')} aria-label="H1">
        <Heading1 size={16} />
      </button>
      <button onClick={() => applyBlockFormat('h2')} aria-label="H2">
        <Heading2 size={16} />
      </button>

      <button onClick={toggleBulletList} aria-label="Bullet List">
        <ListIcon size={16} />
      </button>
      <button onClick={toggleNumberList} aria-label="Numbered List">
        <ListOrdered size={16} />
      </button>

      <button onClick={insertLink} aria-label="Link">
        <LinkIcon size={16} />
      </button>
    </div>
);
}
