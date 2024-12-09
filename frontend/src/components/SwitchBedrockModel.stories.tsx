import SwitchBedrockModel from './SwitchBedrockModel';
import { Model, MODEL_KEYS } from '../@types/conversation';
import { ActiveModels } from '../@types/bot';

export const Ideal = () => (
  <SwitchBedrockModel
    activeModels={
      Object.fromEntries(
        MODEL_KEYS.map((key: Model) => [key, true])
      ) as ActiveModels
    }
  />
);
