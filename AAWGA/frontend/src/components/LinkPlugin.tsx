import React from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { TOGGLE_LINK_COMMAND } from '@lexical/link';
import { Link as LinkIcon } from 'lucide-react';
import './LinkPlugin.css';

export default function LinkPlugin() {
  const [editor] = useLexicalComposerContext();

  const insertLink = () => {
    const url = window.prompt('연결할 URL을 입력하세요:', 'https://');
    if (url && url.trim().length > 0) {
      editor.dispatchCommand(TOGGLE_LINK_COMMAND, url.trim());
    }
  };

  return (
    <button
      type="button"
      onClick={insertLink}
      aria-label="Insert Link"
      className="link-plugin-button"
    >
      <LinkIcon size={16} />
    </button>
  );
}
