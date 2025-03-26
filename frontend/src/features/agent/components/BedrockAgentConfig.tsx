import { useTranslation } from 'react-i18next';
import InputText from '../../../components/InputText';
import { BedrockAgentConfig as BedrockAgentConfigType } from '../types';

type Props = {
  config: BedrockAgentConfigType;
  onChange: (config: BedrockAgentConfigType) => void;
};

export const BedrockAgentConfig = ({ config, onChange }: Props) => {
  const { t } = useTranslation();

  return (
    <div className="space-y-4">
      <InputText
        label={t('agent.tools.bedrockAgent.agentId.label')}
        placeholder={t('agent.tools.bedrockAgent.agentId.placeholder')}
        value={config.agentId}
        onChange={(value) => onChange({ ...config, agentId: value })}
      />
      <InputText
        label={t('agent.tools.bedrockAgent.aliasId.label')}
        placeholder={t('agent.tools.bedrockAgent.aliasId.placeholder')}
        value={config.aliasId}
        onChange={(value) => onChange({ ...config, aliasId: value })}
      />
    </div>
  );
};
