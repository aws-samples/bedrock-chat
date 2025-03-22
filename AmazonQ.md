# Bedrock Claude Chat Code Block Fix

This document describes the changes made to fix the issue with code blocks not properly handling line breaks in the Bedrock Claude Chat application.

## Problem

Code blocks in the AI output were not properly handling line breaks, causing code to appear on a single line without proper formatting.

## Solution

The following changes were made to fix the issue:

1. Added global CSS rules in `index.css` to ensure code blocks always wrap properly:
   ```css
   /* コードブロックの改行を強制する */
   .prose pre {
     white-space: pre-wrap !important;
     word-break: break-word !important;
   }
   ```

2. Modified the `SyntaxHighlighter` component in `ChatMessageMarkdown.tsx` to use proper text wrapping settings:
   ```javascript
   customStyle={{
     whiteSpace: 'pre-wrap',
     wordBreak: 'break-word'
   }}
   ```

3. Changed the parent ReactMarkdown component's className from `break-all` to `break-words` for better text wrapping behavior:
   ```javascript
   className={twMerge(className, 'prose dark:prose-invert max-w-full break-words')}
   ```

4. Updated the rehype external links style to use `break-word` instead of `break-all`:
   ```javascript
   const rehypeExternalLinksOptions: Options = {
     target: '_blank',
     properties: { style: 'word-break: break-word;' },
   };
   ```

## Benefits

These changes ensure that:
- Code blocks properly wrap to the next line when they exceed the container width
- Code maintains its formatting and readability
- Long lines break at word boundaries rather than in the middle of words
- Global CSS rules provide a fallback to ensure proper wrapping even if component-level styles are overridden

## Testing

To test these changes, try using the chat with code examples that include long lines. The code should now properly wrap to the next line while maintaining its formatting.
