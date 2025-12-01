import { visit } from 'unist-util-visit';
import type { Root, Element } from 'hast';

/**
 * Custom rehype plugin that transforms mermaid code blocks into custom elements.
 * The actual rendering is handled by React components via react-markdown's components prop.
 */
const rehypeMermaid = () => {
  return (tree: Root) => {
    visit(tree, 'element', (node: Element, index, parent) => {
      // Look for <pre><code class="language-mermaid">
      if (
        node.tagName === 'pre' &&
        node.children.length === 1 &&
        node.children[0].type === 'element' &&
        node.children[0].tagName === 'code'
      ) {
        const codeElement = node.children[0] as Element;
        const className = codeElement.properties?.className;
        
        if (
          Array.isArray(className) &&
          className.some((c) => String(c).includes('language-mermaid'))
        ) {
          // Extract code text from code element
          const codeText = codeElement.children
            .filter((child): child is { type: 'text'; value: string } => child.type === 'text')
            .map((child) => child.value)
            .join('')
            .replace(/\n$/, '');

          // Replace pre element with custom div
          if (parent && typeof index === 'number') {
            const mermaidNode: Element = {
              type: 'element',
              tagName: 'div',
              properties: {
                'data-mermaid': 'true',
                'data-mermaid-code': codeText,
              },
              children: [],
            };
            (parent.children as Element[])[index] = mermaidNode;
          }
        }
      }
    });
  };
};

export default rehypeMermaid;
