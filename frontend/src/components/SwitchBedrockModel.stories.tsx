import SwitchBedrockModel from './SwitchBedrockModel';
import { Model } from '../@types/conversation';
import { AVAILABLE_MODEL_KEYS } from '../constants/index';
import { ActiveModels } from '../@types/bot';

export const Ideal = () => (
  <SwitchBedrockModel
    activeModels={
      Object.fromEntries(
        AVAILABLE_MODEL_KEYS.map((key: Model) => [key, true])
      ) as ActiveModels
    }
  />
);
