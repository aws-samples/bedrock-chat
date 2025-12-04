import React, { useEffect, useState, useId } from 'react';
import { useTranslation } from 'react-i18next';
import mermaid from 'mermaid';

// Initialize mermaid once
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  suppressErrorRendering: true,
});

type Props = {
  code: string;
};

const MermaidBlock: React.FC<Props> = React.memo(({ code }) => {
  const {t} = useTranslation()
  const [svg, setSvg] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const uniqueId = useId().replace(/:/g, '-');

  useEffect(() => {
    let cancelled = false;

    const render = async () => {
      try {
        // Remove any existing element with this ID to avoid conflicts
        const existingEl = document.getElementById(`mermaid${uniqueId}`);
        if (existingEl) {
          existingEl.remove();
        }
        
        const { svg } = await mermaid.render(`mermaid${uniqueId}`, code);
        if (!cancelled) {
          setSvg(svg);
          setError(null);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : String(e));
          setSvg(null);
        }
      }
    };

    render();

    return () => {
      cancelled = true;
    };
  }, [code, uniqueId]);

  if (error) {
    return (
      <div className="p-3 space-y-1">
        <pre className="p-2 bg-[#1e1e1e] text-xs text-[#d4d4d4] whitespace-pre-wrap break-all">
          {code}
        </pre>
        <div className='text-sm font-bold text-red'>
          
          {t("error.invalidMermaidFormat")}
        </div>
        <div className="p-2 border text-sm rounded text-red/80">
          {error}
        </div>
      </div>
    );
  }

  if (!svg) {
    return (
<pre className="p-2 bg-[#1e1e1e] text-xs text-[#d4d4d4] whitespace-pre-wrap break-all">
                {code}
      </pre>
    );
  }

  return (
    <div
      className="overflow-auto bg-white p-4 rounded"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
});

MermaidBlock.displayName = 'MermaidBlock';

export default MermaidBlock;
