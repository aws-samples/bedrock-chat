import { create } from 'zustand';
import { Model } from '../@types/conversation';
import { useEffect, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import useLocalStorage from './useLocalStorage';

const MISTRAL_ENABLED: boolean =
  import.meta.env.VITE_APP_ENABLE_MISTRAL === 'true';

const CLAUDE_SUPPORTED_MEDIA_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
];

const useModelState = create<{
  modelId: Model;
  setModelId: (m: Model) => void;
}>((set) => ({
  modelId: 'claude-v3-haiku',
  setModelId: (m) => {
    set({
      modelId: m,
    });
  },
}));

const useModel = () => {
  const { t } = useTranslation();

  const availableModels = useMemo<
    {
      modelId: Model;
      label: string;
      supportMediaType: string[];
      description?: string;
    }[]
  >(() => {
    return !MISTRAL_ENABLED
      ? [
          {
            modelId: 'claude-v3-haiku',
            label: t('model.haiku3.label'),
            description: t('model.haiku3.description'),
            supportMediaType: CLAUDE_SUPPORTED_MEDIA_TYPES,
          },
          {
            modelId: 'claude-v3-sonnet',
            label: t('model.sonnet3.label'),
            description: t('model.sonnet3.description'),
            supportMediaType: CLAUDE_SUPPORTED_MEDIA_TYPES,
          },
          {
            modelId: 'claude-v3.5-sonnet',
            label: t('model.sonnet3-5.label'),
            description: t('model.sonnet3-5.description'),
            supportMediaType: CLAUDE_SUPPORTED_MEDIA_TYPES,
          },
          {
            modelId: 'claude-v3.5-sonnet-v2',
            label: t('model.sonnet3-5-v2.label'),
            description: t('model.sonnet3-5-v2.description'),
            supportMediaType: CLAUDE_SUPPORTED_MEDIA_TYPES,
          },
          {
            modelId: 'claude-v3-opus',
            label: t('model.opus3.label'),
            description: t('model.opus3.description'),
            supportMediaType: CLAUDE_SUPPORTED_MEDIA_TYPES,
          },
        ]
      : [
          {
            modelId: 'mistral-7b-instruct',
            label: t('model.mistral7b.label'),
            supportMediaType: [],
          },
          {
            modelId: 'mixtral-8x7b-instruct',
            label: t('model.mistral8x7b.label'),
            supportMediaType: [],
          },
          {
            modelId: 'mistral-large',
            label: t('model.mistralLarge.label'),
            supportMediaType: [],
          },
        ];
  }, [t]);

  const { modelId, setModelId } = useModelState();
  const [recentUseModelId, setRecentUseModelId] = useLocalStorage(
    'recentUseModelId',
    'claude-v3-haiku'
  );
  useEffect(() => {
    // Restored from LocalStorage
    setModelId(recentUseModelId as Model);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const model = useMemo(() => {
    return availableModels.find((model) => model.modelId === modelId);
  }, [availableModels, modelId]);

  return {
    modelId,
    setModelId: (model: Model) => {
      setRecentUseModelId(model);
      setModelId(model);
    },
    model,
    disabledImageUpload: (model?.supportMediaType.length ?? 0) === 0,
    acceptMediaType:
      model?.supportMediaType.flatMap((mediaType) => {
        const ext = mediaType.split('/')[1];
        return ext === 'jpeg' ? ['.jpg', '.jpeg'] : [`.${ext}`];
      }) ?? [],
    availableModels,
  };
};

export default useModel;
