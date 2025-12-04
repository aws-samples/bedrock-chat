import { useCallback, useEffect, useRef, useState } from 'react';

const useScroll = (conversationId?: string) => {
  const [disabled, setDisabled] = useState(false);
  const isInitialScroll = useRef(true);

  // Reset initial scroll flag when conversationId changes
  useEffect(() => {
    isInitialScroll.current = true;
  }, [conversationId]);

  useEffect(() => {
    const elem = document.getElementById('messages');
    if (!elem) {
      return;
    }
    const listener = () => {
      // Enable auto-scroll when scrolled to the bottom
      if (elem.scrollTop + elem.clientHeight === elem.scrollHeight) {
        setDisabled(false);
      } else {
        setDisabled(true);
      }
    };
    elem.addEventListener('scroll', listener);

    return () => {
      elem.removeEventListener('scroll', listener);
    };
  }, []);

  const scrollToTop = useCallback(() => {
    document.getElementById('messages')?.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  }, []);

  const scrollToBottom = useCallback(() => {
    const elem = document.getElementById('messages');
    if (!elem) {return;}

    const doScroll = () => {
      elem.scrollTo({
        top: elem.scrollHeight,
        behavior: 'instant',
      });
    };

    // Scroll regardless of disabled state on initial scroll
    if (!disabled || isInitialScroll.current) {
      if (isInitialScroll.current) {
        // Use MutationObserver to wait for async rendering (e.g., Mermaid)
        doScroll();
        const observer = new MutationObserver(() => {
          doScroll();
        });
        observer.observe(elem, { childList: true, subtree: true });
        // Stop observing after a certain period
        setTimeout(() => {
          observer.disconnect();
        }, 1000);
        isInitialScroll.current = false;
      } else {
        doScroll();
      }
    }
  }, [disabled]);

  return {
    scrollToTop,
    scrollToBottom,
  };
};

export default useScroll;
