import useGlobalConfigApi from './useGlobalConfigApi';

const useGlobalConfig = () => {
  const api = useGlobalConfigApi();

  return {
    getGlobalConfig: api.getGlobalConfig,
  };
};

export default useGlobalConfig;
