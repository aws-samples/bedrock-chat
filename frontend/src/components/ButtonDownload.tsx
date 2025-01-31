import React, { useCallback } from 'react';
import ButtonIcon from './ButtonIcon';
import { BaseProps } from '../@types/common';
import { PiDownload } from 'react-icons/pi';

interface WindowWithFileSaveAPI {
  showSaveFilePicker?: (options?: {
    suggestedName?: string;
    types?: Array<{
      description: string;
      accept: Record<string, string[]>;
    }>;
  }) => Promise<FileSystemFileHandle>;
}

type Props = BaseProps & {
  text: string;
};

const ButtonDownload: React.FC<Props> = (props) => {
  const getDefaultFileName = () => {
    const now = new Date();
    const date = now.getFullYear() +
      ('0' + (now.getMonth() + 1)).slice(-2) +
      ('0' + now.getDate()).slice(-2);
    
    const time = ('0' + now.getHours()).slice(-2) +
      ('0' + now.getMinutes()).slice(-2) +
      ('0' + now.getSeconds()).slice(-2) +
      ('00' + now.getMilliseconds()).slice(-3);
    
    const timestamp = `${date}_${time}`;
    
    return `code_${timestamp}.txt`;
  };

  const downloadText = useCallback(async (text: string) => {
    const fileName = getDefaultFileName();
    const blob = new Blob([text], { type: 'text/plain' });

    try {
      // Modern browsers - Using File System Access API
      const savePicker = (window as Window & WindowWithFileSaveAPI).showSaveFilePicker;
      if (savePicker) {
        try {
          const handle = await savePicker({
            suggestedName: fileName,
          });
          const writable = await handle.createWritable();
          await writable.write(blob);
          await writable.close();
          return;
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
          // User cancelled the save dialog or other error
          if (err.name !== 'AbortError') {
            console.error('Failed to save file:', err);
          }
          return;
        }
      }

      // Fallback for older browsers
      const downloadLink = document.createElement('a');
      downloadLink.download = fileName;
      downloadLink.href = window.URL.createObjectURL(blob);
      downloadLink.click();
      window.URL.revokeObjectURL(downloadLink.href);

    } catch (error) {
      console.error('Failed to download file:', error);
    }
  }, []);

  return (
    <ButtonIcon
      className={props.className}
      onClick={() => {
        downloadText(props.text);
      }}>
      <PiDownload />
    </ButtonIcon>
  );
};

export default ButtonDownload;
