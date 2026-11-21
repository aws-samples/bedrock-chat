import { describe, expect, it } from 'vitest';
import { calcTotalFileSizeToSend } from '../AttachmentUtils';

describe('calcTotalFileSizeToSend', () => {
  it('returns 0 when nothing is attached', () => {
    expect(calcTotalFileSizeToSend([], [])).toBe(0);
  });

  it('sums the size of attached images and files', () => {
    expect(
      calcTotalFileSizeToSend(
        ['data:image/png;base64,AAAA', 'data:image/png;base64,BB'],
        [{ content: 'Q0NDQw==' }, { content: 'RA==' }]
      )
    ).toBe(26 + 24 + 8 + 4);
  });

  it('does not count files that were removed or already sent', () => {
    const attachedFiles = [{ content: 'A'.repeat(4 * 1024 * 1024) }];
    expect(calcTotalFileSizeToSend([], attachedFiles)).toBe(4 * 1024 * 1024);

    // After the files are removed or sent, the attached lists are cleared and
    // the total must go back to 0 so that new files can be attached again.
    attachedFiles.splice(0, 1);
    expect(calcTotalFileSizeToSend([], attachedFiles)).toBe(0);
  });
});
