import { useTranslation } from 'react-i18next';
import { useCallback, useState } from 'react';
import { PiEyeLight, PiEyeSlashLight } from 'react-icons/pi';
import InputText from '../../../components/InputText';
import { Slider } from '../../../components/Slider';
import { FirecrawlConfig as FirecrawlConfigType } from '../types';

type Props = {
  config: FirecrawlConfigType;
  onChange: (config: FirecrawlConfigType) => void;
};

export const FirecrawlConfig = ({ config, onChange }: Props) => {
  const { t } = useTranslation();
  const [showPassword, setShowPassword] = useState(false);

  const handleApiKeyChange = useCallback(
    (apiKey: string) => {
      onChange({
        ...config,
        apiKey,
      });
    },
    [config, onChange]
  );

  const handleMaxResultsChange = useCallback(
    (maxResults: number) => {
      onChange({
        ...config,
        maxResults,
      });
    },
    [config, onChange]
  );

  return (
    <div className="space-y-4">
      <div className="flex items-end gap-2">
        <InputText
          className="flex-1"
          label={t('agent.tools.firecrawl.apiKey')}
          type={showPassword ? 'text' : 'password'}
          value={config.apiKey || ''}
          onChange={handleApiKeyChange}
        />
        <button
          type="button"
          className="h-9 w-9 rounded border border-aws-font-color-light/50 p-2 text-sm hover:bg-gray-100 dark:border-aws-font-color-dark/50 dark:hover:bg-gray-800"
          onClick={() => setShowPassword(!showPassword)}
        >
          {showPassword ? <PiEyeLight className="h-5 w-5" /> : <PiEyeSlashLight className="h-5 w-5" />}
        </button>
      </div>
      <Slider
        label={t('agent.tools.firecrawl.maxResults')}
        value={config.maxResults}
        onChange={handleMaxResultsChange}
        range={{
          min: 1,
          max: 50,
          step: 1,
        }}
      />
    </div>
  );
};
